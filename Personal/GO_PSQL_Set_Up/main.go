package main

import (
	"archive/zip"
	"database/sql"
	"fmt"
	"io"
	"net"
	"net/http"
	"os"
	"os/exec"
	"os/signal"
	"path/filepath"
	"strings"
	"syscall"
	"time"

	_ "github.com/lib/pq"
)

const (
	pgVersion   = "15.5"
	pgBinaryURL = "https://get.enterprisedb.com/postgresql/postgresql-15.5-1-windows-x64-binaries.zip"
	pgBinaryDir = "./postgres_files"
	pgDataDir   = "./postgres_data"
	pgPort      = "8060"
	pgUser      = "postgres"
	pgDatabase  = "RadiumTest"
)

// Global variables
var pgPassword = "password"

// PostgreSQL represents a PostgreSQL instance
type PostgreSQL struct {
	binPath string
	dataDir string
	port    string
}

// NewPostgreSQL creates a new PostgreSQL instance
func NewPostgreSQL() *PostgreSQL {
	return &PostgreSQL{
		binPath: filepath.Join(pgBinaryDir, "bin"),
		dataDir: pgDataDir,
		port:    pgPort,
	}
}

// Initialize checks and sets up PostgreSQL
func (pg *PostgreSQL) Initialize() error {
	fmt.Println("\nStarting setup process...")

	// Check if binaries exist
	if !pg.checkBinaries() {
		fmt.Println("Required files not found.")
		fmt.Printf("Looking in: %s\n", pg.binPath)
		fmt.Println("\nPlease ensure required files are in the correct location:")
		fmt.Printf("%s/\n", pgBinaryDir)
		fmt.Println("  └── bin/")
		fmt.Println("      ├── pg_ctl.exe")
		fmt.Println("      └── postgres.exe")
		return fmt.Errorf("required files not found in %s", pg.binPath)
	}
	fmt.Println("✓ Found required files")

	// Check if data directory exists and is valid
	if !pg.checkDataDir() {
		fmt.Printf("Initializing new database in: %s\n", pg.dataDir)
		// Create data directory if it doesn't exist
		if err := os.MkdirAll(pg.dataDir, 0755); err != nil {
			return fmt.Errorf("failed to create data directory: %w", err)
		}
		if err := pg.initDB(); err != nil {
			return fmt.Errorf("initialization failed: %w", err)
		}
		fmt.Println("✓ Database initialization complete")
	} else {
		fmt.Println("✓ Using existing database directory")
	}

	return nil
}

// checkBinaries verifies if PostgreSQL binaries exist
func (pg *PostgreSQL) checkBinaries() bool {
	pgCtlPath := filepath.Join(pg.binPath, "pg_ctl.exe")
	_, err := os.Stat(pgCtlPath)
	return err == nil
}

// downloadBinaries downloads and extracts PostgreSQL binaries
func (pg *PostgreSQL) downloadBinaries() error {
	// Create temporary file for zip
	zipPath := "postgresql.zip"
	fmt.Printf("Downloading PostgreSQL %s binaries...\n", pgVersion)

	// Download file
	resp, err := http.Get(pgBinaryURL)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	out, err := os.Create(zipPath)
	if err != nil {
		return err
	}
	defer out.Close()

	_, err = io.Copy(out, resp.Body)
	if err != nil {
		return err
	}

	// Extract zip file
	fmt.Println("Extracting binaries...")
	err = pg.unzip(zipPath, ".")
	if err != nil {
		return err
	}

	// Clean up
	os.Remove(zipPath)
	return nil
}

// unzip extracts a zip file
func (pg *PostgreSQL) unzip(src, dest string) error {
	r, err := zip.OpenReader(src)
	if err != nil {
		return err
	}
	defer r.Close()

	for _, f := range r.File {
		fpath := filepath.Join(dest, f.Name)

		if f.FileInfo().IsDir() {
			os.MkdirAll(fpath, os.ModePerm)
			continue
		}

		if err = os.MkdirAll(filepath.Dir(fpath), os.ModePerm); err != nil {
			return err
		}

		outFile, err := os.OpenFile(fpath, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, f.Mode())
		if err != nil {
			return err
		}

		rc, err := f.Open()
		if err != nil {
			outFile.Close()
			return err
		}

		_, err = io.Copy(outFile, rc)
		outFile.Close()
		rc.Close()
		if err != nil {
			return err
		}
	}
	return nil
}

// checkDataDir verifies if data directory exists and is a valid PostgreSQL data directory
func (pg *PostgreSQL) checkDataDir() bool {
	// First check if directory exists
	_, err := os.Stat(pg.dataDir)
	if err != nil {
		return false
	}

	// Check if it's a valid PostgreSQL data directory by looking for PG_VERSION file
	_, err = os.Stat(filepath.Join(pg.dataDir, "PG_VERSION"))
	return err == nil
}

// initDB initializes the PostgreSQL data directory
func (pg *PostgreSQL) initDB() error {
	fmt.Println("Creating temporary password file...")
	// Create a temporary password file
	pwFile := filepath.Join(os.TempDir(), "pgpass.txt")
	err := os.WriteFile(pwFile, []byte(pgPassword), 0600)
	if err != nil {
		return fmt.Errorf("failed to create password file: %w", err)
	}
	defer os.Remove(pwFile) // Clean up the password file when done

	fmt.Println("Running initdb command...")
	initdbPath := filepath.Join(pg.binPath, "initdb.exe")
	cmd := exec.Command(initdbPath,
		"-D", pg.dataDir,
		"--username="+pgUser,
		"--auth=md5",
		"--pwfile="+pwFile,
		"--encoding=UTF8",
		"--locale=C",
	)

	// Capture both stdout and stderr
	output, err := cmd.CombinedOutput()
	if err != nil {
		// Print the full output for debugging
		fmt.Println("\nInitialization output:")
		fmt.Println(string(output))
		return fmt.Errorf("initdb failed: %w", err)
	}
	fmt.Println("✓ Database files created")

	fmt.Println("Configuring authentication...")
	// Create/update pg_hba.conf for MD5 authentication
	hbaPath := filepath.Join(pg.dataDir, "pg_hba.conf")
	hbaContent := `# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   all             all                                     md5
host    all             all             127.0.0.1/32            md5
host    all             all             ::1/128                 md5`

	err = os.WriteFile(hbaPath, []byte(hbaContent), 0600)
	if err != nil {
		return fmt.Errorf("failed to update pg_hba.conf: %w", err)
	}
	fmt.Println("✓ Authentication configured")

	return nil
}

// Start starts the PostgreSQL server
func (pg *PostgreSQL) Start() error {
	fmt.Println("\nStarting PostgreSQL server...")
	ctlExe := filepath.Join(pg.binPath, "pg_ctl.exe")
	logFile := filepath.Join(pg.dataDir, "log.txt")

	// Ensure port is explicitly set in postgres configuration
	configPath := filepath.Join(pg.dataDir, "postgresql.conf")
	configContent := fmt.Sprintf("port = %s\nlisten_addresses = '*'", pg.port)
	err := os.WriteFile(configPath, []byte(configContent), 0600)
	if err != nil {
		return fmt.Errorf("failed to update postgresql.conf: %w", err)
	}

	cmd := exec.Command(ctlExe,
		"-D", pg.dataDir,
		"-l", logFile,
		"-o", fmt.Sprintf(`"-p %s"`, pg.port),
		"-w", // Wait for startup to complete
		"start",
	)

	output, err := cmd.CombinedOutput()
	if err != nil {
		// If there's an error, try to read the log file
		logContent, readErr := os.ReadFile(logFile)
		if readErr == nil {
			fmt.Println("\nServer log:")
			fmt.Println(string(logContent))
		}
		return fmt.Errorf("start failed: %w\n%s", err, output)
	}

	// Verify server is running by attempting a connection
	for i := 0; i < 3; i++ {
		conn, err := net.DialTimeout("tcp", fmt.Sprintf("localhost:%s", pg.port), time.Second)
		if err == nil {
			conn.Close()
			fmt.Println("✓ Server is running and accepting connections")
			return nil
		}
		time.Sleep(time.Second)
	}

	// Try to connect to the database to ensure it's really ready
	db, err := sql.Open("postgres", pg.getDefaultConnString())
	if err == nil {
		defer db.Close()
		if err = db.Ping(); err == nil {
			fmt.Println("✓ Database connection verified")
			return nil
		}
	}

	return fmt.Errorf("server started but not responding to connections")
}

// Stop stops the PostgreSQL server
func (pg *PostgreSQL) Stop() error {
	ctlExe := filepath.Join(pg.binPath, "pg_ctl.exe")
	cmd := exec.Command(ctlExe,
		"-D", pg.dataDir,
		"stop",
	)
	output, err := cmd.CombinedOutput()
	if err != nil {
		return fmt.Errorf("stop failed: %w\n%s", err, output)
	}
	return nil
}

// IsRunning checks if PostgreSQL is running and returns (bool, bool, error)
// First bool: Is PostgreSQL running?
// Second bool: Is it a password authentication error?
func (pg *PostgreSQL) IsRunning() (bool, bool, error) {
	fmt.Printf("Checking port %s...\n", pg.port)

	// Check if our specific port is in use
	conn, err := net.DialTimeout("tcp", fmt.Sprintf("localhost:%s", pg.port), time.Second)
	if err == nil {
		conn.Close()
		fmt.Printf("Port %s is in use\n", pg.port)
	} else {
		fmt.Printf("Port %s is not in use\n", pg.port)
		return false, false, nil
	}

	// Try database connection to postgres database
	db, err := sql.Open("postgres", pg.getDefaultConnString())
	if err != nil {
		return false, false, err
	}
	defer db.Close()

	err = db.Ping()
	if err != nil {
		// Check if it's an authentication error
		if strings.Contains(err.Error(), "password authentication failed") {
			return true, true, nil
		}
		return false, false, err
	}

	fmt.Printf("Successfully connected to PostgreSQL on port %s\n", pg.port)
	return true, false, nil
}

// getConnString returns the PostgreSQL connection string
func (pg *PostgreSQL) getConnString() string {
	return fmt.Sprintf("host=localhost port=%s user=%s password=%s dbname=%s sslmode=disable",
		pg.port, pgUser, pgPassword, strings.ToLower(pgDatabase))
}

// getDefaultConnString returns connection string for postgres database
func (pg *PostgreSQL) getDefaultConnString() string {
	return fmt.Sprintf("host=localhost port=%s user=%s password=%s dbname=postgres sslmode=disable",
		pg.port, pgUser, pgPassword)
}

// CreateTestTable creates the database schema and tables
func (pg *PostgreSQL) CreateTestTable() error {
	fmt.Println("\n=== Starting Database Setup ===")
	fmt.Printf("1. Initial connection string: %s\n", pg.getDefaultConnString())

	// First, connect to default 'postgres' database
	fmt.Println("2. Attempting to connect to default postgres database...")
	db, err := sql.Open("postgres", pg.getDefaultConnString())
	if err != nil {
		return fmt.Errorf("❌ failed to connect to postgres database: %w", err)
	}
	defer db.Close()

	// Test the connection
	fmt.Println("3. Testing connection with Ping...")
	err = db.Ping()
	if err != nil {
		return fmt.Errorf("❌ failed to ping postgres database: %w", err)
	}
	fmt.Println("✓ Successfully connected to PostgreSQL")

	// Convert database name to lowercase for consistency
	dbName := strings.ToLower(pgDatabase)

	// Drop database if exists
	fmt.Printf("4. Attempting to drop database '%s' if it exists...\n", dbName)
	_, err = db.Exec(fmt.Sprintf("DROP DATABASE IF EXISTS %s", dbName))
	if err != nil {
		fmt.Printf("⚠️ Warning: Could not drop database: %v\n", err)
	} else {
		fmt.Printf("✓ Successfully dropped existing database '%s'\n", dbName)
	}

	// Create the database
	fmt.Printf("5. Creating new database '%s'...\n", dbName)
	_, err = db.Exec(fmt.Sprintf("CREATE DATABASE %s WITH OWNER = %s ENCODING = 'UTF8'", dbName, pgUser))
	if err != nil {
		return fmt.Errorf("❌ failed to create database: %w", err)
	}
	fmt.Printf("✓ Database '%s' created successfully\n", dbName)

	// Close connection to postgres database and wait
	db.Close()
	fmt.Println("6. Waiting for database to be ready (5 seconds)...")
	time.Sleep(5 * time.Second)

	// Connect to the new database
	fmt.Printf("7. Connecting to new '%s' database...\n", dbName)
	fmt.Printf("Connection string: %s\n", pg.getConnString())
	newDb, err := sql.Open("postgres", pg.getConnString())
	if err != nil {
		return fmt.Errorf("❌ failed to connect to %s database: %w", dbName, err)
	}
	defer newDb.Close()

	// Test connection to new database
	fmt.Println("8. Testing connection to new database...")
	err = newDb.Ping()
	if err != nil {
		return fmt.Errorf("❌ failed to ping new database: %w", err)
	}
	fmt.Printf("✓ Successfully connected to '%s' database\n", dbName)

	// Create extensions
	fmt.Println("9. Creating required extensions...")
	_, err = newDb.Exec("CREATE EXTENSION IF NOT EXISTS citext")
	if err != nil {
		return fmt.Errorf("❌ failed to create citext extension: %w", err)
	}
	fmt.Println("✓ Extensions created successfully")

	// Create schema
	fmt.Println("10. Creating RadiumTest schema...")
	_, err = newDb.Exec("CREATE SCHEMA IF NOT EXISTS RadiumTest")
	if err != nil {
		return fmt.Errorf("❌ failed to create schema: %w", err)
	}
	fmt.Println("✓ Schema created successfully")

	// Create PACS table
	fmt.Println("11. Creating PACS table...")
	_, err = newDb.Exec(`
		CREATE TABLE IF NOT EXISTS RadiumTest.pacs (
			ixStudy SERIAL PRIMARY KEY,
			StudyInstanceUID VARCHAR(64) UNIQUE,
			PatientID VARCHAR(32),
			PatientName VARCHAR(128),
			PatientBirthDate VARCHAR(32),
			PatientAge VARCHAR(8),
			PatientSex VARCHAR(2),
			StudyDate VARCHAR(32),
			StudyTime VARCHAR(32),
			AccessionNumber VARCHAR(64),
			StudyDescription VARCHAR(128),
			ReferringPhysicianName VARCHAR(128),
			PerformingPhysicianName VARCHAR(128),
			InstitutionName VARCHAR(128),
			StationName VARCHAR(128),
			Modality VARCHAR(2),
			NumberOfStudyRelatedSeries SMALLINT,
			NumberOfStudyRelatedInstances SMALLINT,
			DeviceSerialNumber VARCHAR(128),
			Manufacturer VARCHAR(128),
			ManufacturerModelName VARCHAR(128),
			SourceAETitle VARCHAR(128),
			DIR_path VARCHAR(256),
			StartedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
			FinishedAt TIMESTAMP,
			ModifiedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
			StudyStatus SMALLINT DEFAULT 1
		)
	`)
	if err != nil {
		return fmt.Errorf("❌ failed to create PACS table: %w", err)
	}
	fmt.Println("✓ PACS table created successfully")

	// Create indexes
	fmt.Println("12. Creating indexes...")
	indexes := []struct {
		name string
		sql  string
	}{
		{"idx_study_instance_uid", "CREATE INDEX IF NOT EXISTS idx_study_instance_uid ON RadiumTest.pacs(StudyInstanceUID)"},
		{"idx_patient_id", "CREATE INDEX IF NOT EXISTS idx_patient_id ON RadiumTest.pacs(PatientID)"},
		{"idx_patient_name", "CREATE INDEX IF NOT EXISTS idx_patient_name ON RadiumTest.pacs(PatientName)"},
		{"idx_study_date", "CREATE INDEX IF NOT EXISTS idx_study_date ON RadiumTest.pacs(StudyDate)"},
		{"idx_modality", "CREATE INDEX IF NOT EXISTS idx_modality ON RadiumTest.pacs(Modality)"},
	}

	for _, idx := range indexes {
		fmt.Printf("Creating index %s...\n", idx.name)
		_, err = newDb.Exec(idx.sql)
		if err != nil {
			return fmt.Errorf("❌ failed to create index %s: %w", idx.name, err)
		}
	}
	fmt.Println("✓ All indexes created successfully")

	// Insert sample data
	fmt.Println("13. Adding sample data...")
	_, err = newDb.Exec(`
		INSERT INTO RadiumTest.pacs (
			StudyInstanceUID, PatientID, PatientName, PatientBirthDate,
			PatientAge, PatientSex, StudyDate, StudyTime, Modality,
			StudyDescription, InstitutionName, StudyStatus,
			NumberOfStudyRelatedSeries, NumberOfStudyRelatedInstances,
			ReferringPhysicianName, PerformingPhysicianName
		) VALUES 
		(
			'1.2.3.4.5.1', 'PAT001', 'John Doe', '19800101',
			'43', 'M', '20231201', '093000', 'CT',
			'Chest CT', 'General Hospital', 1,
			2, 124,
			'Dr. Smith', 'Dr. Johnson'
		)
		ON CONFLICT (StudyInstanceUID) DO NOTHING
	`)
	if err != nil {
		return fmt.Errorf("❌ failed to insert sample data: %w", err)
	}
	fmt.Println("✓ Sample data added successfully")

	// Verify data
	fmt.Println("14. Verifying data...")
	var count int
	err = newDb.QueryRow("SELECT COUNT(*) FROM RadiumTest.pacs").Scan(&count)
	if err != nil {
		return fmt.Errorf("❌ failed to verify data: %w", err)
	}
	fmt.Printf("✓ Verified %d records in database\n", count)

	fmt.Println("\n=== Database Setup Complete ===")
	return nil
}

// SetPassword updates the password for the PostgreSQL connection
func (pg *PostgreSQL) SetPassword(password string) {
	pgPassword = password
}

// readPassword reads a password from stdin
func readPassword() string {
	var password string
	fmt.Print("Enter password for user 'postgres': ")
	fmt.Scanln(&password)
	return password
}

// tryDefaultPassword attempts to connect with the default password
func (pg *PostgreSQL) tryDefaultPassword() (bool, error) {
	pg.SetPassword("password") // Try default password first
	_, needsPassword, err := pg.IsRunning()
	if err != nil {
		return false, err
	}
	return !needsPassword, nil
}

func main() {
	fmt.Println("\nPostgreSQL Setup")
	fmt.Println("================")
	fmt.Printf("Version: %s\n", pgVersion)
	fmt.Printf("Port: %s\n", pgPort)
	fmt.Println("================\n")

	pg := NewPostgreSQL()

	// Check if our PostgreSQL instance is already running on port 8060
	fmt.Printf("Checking if PostgreSQL is already running on port %s...\n", pgPort)
	serverRunning, needsPassword, err := pg.IsRunning()
	if err != nil {
		fmt.Printf("Error checking PostgreSQL: %v\n", err)
		fmt.Println("\nPress Enter to exit...")
		fmt.Scanln()
		return
	}

	if serverRunning {
		fmt.Printf("\nExisting PostgreSQL instance found on port %s!\n", pgPort)

		// First try with default password
		fmt.Println("Attempting to connect with default password...")
		success, err := pg.tryDefaultPassword()
		if err != nil {
			fmt.Printf("Error during connection attempt: %v\n", err)
			fmt.Println("\nPress Enter to exit...")
			fmt.Scanln()
			return
		}

		// If default password failed, prompt for password
		if !success {
			fmt.Println("Default password failed. Please enter your password:")
			password := readPassword()
			pg.SetPassword(password)

			// Try connection again
			_, needsPassword, err = pg.IsRunning()
			if err != nil || needsPassword {
				fmt.Println("\n❌ Connection failed: Invalid password or access denied")
				fmt.Println("\nPress Enter to exit...")
				fmt.Scanln()
				return
			}
		}
		fmt.Printf("\n✓ Successfully connected to existing PostgreSQL instance on port %s\n", pgPort)
	} else {
		fmt.Printf("No PostgreSQL instance found on port %s.\n", pgPort)
		fmt.Println("Starting new PostgreSQL instance...")
		// Initialize and start PostgreSQL
		if err := pg.Initialize(); err != nil {
			fmt.Printf("Failed to initialize PostgreSQL: %v\n", err)
			fmt.Println("\nPress Enter to exit...")
			fmt.Scanln()
			return
		}

		if err := pg.Start(); err != nil {
			fmt.Printf("Failed to start PostgreSQL: %v\n", err)
			fmt.Printf("Please check if port %s is available\n", pg.port)
			fmt.Println("\nPress Enter to exit...")
			fmt.Scanln()
			return
		}
		fmt.Printf("✓ PostgreSQL started successfully on port %s\n", pgPort)

		fmt.Println("Waiting for server to be ready...")
		time.Sleep(5 * time.Second)
	}

	// Try database setup once
	fmt.Println("\nAttempting database setup...")
	err = pg.CreateTestTable()
	if err != nil {
		if strings.Contains(err.Error(), "database \"radiumtest\" already exists") ||
			strings.Contains(err.Error(), "being accessed by other users") {
			fmt.Println("✓ Database already exists and is in use")
		} else {
			fmt.Printf("\nError: Failed to setup database: %v\n", err)
			fmt.Println("\nPress Enter to exit...")
			fmt.Scanln()
			return
		}
	}

	fmt.Println("\n✓ Setup completed successfully!")
	fmt.Println("\nConnection Details:")
	fmt.Println("------------------")
	fmt.Printf("Host: localhost\n")
	fmt.Printf("Port: %s\n", pgPort)
	fmt.Printf("Database: %s\n", pgDatabase)
	fmt.Printf("Schema: RadiumTest\n")
	fmt.Printf("Table: pacs\n")
	fmt.Println("\nPress Ctrl+C to stop the server...")

	// Keep the program running
	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt, syscall.SIGTERM)
	<-c

	// Cleanup on exit
	if !serverRunning {
		fmt.Println("\nStopping PostgreSQL...")
		if err := pg.Stop(); err != nil {
			fmt.Printf("Error stopping PostgreSQL: %v\n", err)
		} else {
			fmt.Println("✓ PostgreSQL stopped successfully")
		}
	}

	fmt.Println("\nPress Enter to exit...")
	fmt.Scanln()
}
