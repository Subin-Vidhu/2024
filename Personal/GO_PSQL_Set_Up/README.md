# PostgreSQL Binary Setup

A Go application that manages a portable PostgreSQL instance without requiring administrative privileges. This application uses PostgreSQL binaries instead of a system-wide installation.

## Features

- Downloads and manages PostgreSQL binaries locally
- No administrative privileges required
- Automatic database initialization and management
- Self-contained and portable
- Detects existing PostgreSQL installations
- PACS-like database schema with optimized indexes

## Code Structure

### Core Components

1. **PostgreSQL Struct**
   ```go
   type PostgreSQL struct {
       binPath string  // Path to PostgreSQL binaries
       dataDir string  // Path to data directory
       port    string  // Port number
   }
   ```

2. **Configuration Constants**
   ```go
   const (
       pgVersion   = "15.5"
       pgBinaryURL = "..."
       pgBinaryDir = "./pgsql"
       pgDataDir   = "./data/pgdata"
       pgPort      = "8060"
       pgUser      = "postgres"
       pgDatabase  = "RadiumTest"
   )
   ```

### Key Functions

1. **Initialization & Setup**
   - `Initialize()`: Prepares PostgreSQL environment
   - `checkBinaries()`: Verifies binary existence
   - `downloadBinaries()`: Downloads PostgreSQL binaries
   - `initDB()`: Initializes data directory

2. **Server Management**
   - `Start()`: Starts PostgreSQL server
   - `Stop()`: Stops PostgreSQL server
   - `IsRunning()`: Checks server status

3. **Database Operations**
   - `CreateTestTable()`: Sets up database schema and tables
   - `getConnString()`: Generates connection strings
   - `SetPassword()`: Updates PostgreSQL password

## Database Schema

### RadiumTest Schema
```sql
CREATE SCHEMA IF NOT EXISTS RadiumTest;

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
);
```

### Optimized Indexes
```sql
CREATE INDEX idx_study_instance_uid ON RadiumTest.pacs(StudyInstanceUID);
CREATE INDEX idx_patient_id ON RadiumTest.pacs(PatientID);
CREATE INDEX idx_patient_name ON RadiumTest.pacs(PatientName);
CREATE INDEX idx_study_date ON RadiumTest.pacs(StudyDate);
CREATE INDEX idx_modality ON RadiumTest.pacs(Modality);
```

## Program Flow

1. **Startup Process**
   - Checks for existing PostgreSQL installation
   - Verifies port availability (8060)
   - Detects running PostgreSQL processes
   - Handles authentication if needed

2. **Installation Flow**
   - Downloads PostgreSQL binaries if not present (~150MB)
   - Extracts to local directory
   - Initializes data directory with MD5 authentication
   - Configures pg_hba.conf for secure connections

3. **Database Setup**
   - Creates RadiumTest database if not exists
   - Creates RadiumTest schema
   - Sets up PACS table with indexes
   - Adds sample medical records

4. **Error Handling**
   - Connection retry logic
   - Authentication error detection
   - Case-sensitive naming handling
   - Graceful cleanup on exit

## Requirements

- Go 1.16 or higher
- Windows operating system
- Internet connection (for first-time binary download)
- ~200MB free disk space

## Usage

1. Build the application:
   ```bash
   go mod init postgres-setup
   go mod tidy
   go build -o postgres-setup.exe
   ```

2. Run the executable:
   ```bash
   ./postgres-setup.exe
   ```

## Security Features

- MD5 password authentication
- Secure connection configuration
- No administrative privileges required
- Proper password handling

## Performance Optimizations

- Optimized work memory (256MB)
- Strategic index placement
- Connection pooling
- Retry mechanisms with backoff

## Notes

- The application manages PostgreSQL as a regular process
- All data is stored locally in the application directory
- Suitable for development environments
- Preserves existing PostgreSQL installations
- Safe to run multiple times (idempotent)

## Troubleshooting

1. Connection Issues:
   - Check if port 8060 is available
   - Verify PostgreSQL processes
   - Check authentication credentials

2. Database Creation:
   - Case sensitivity in database names
   - Schema ownership and permissions
   - Connection retry timing

3. Sample Data:
   - Unique constraint violations
   - Default timestamp handling
   - Status field defaults 