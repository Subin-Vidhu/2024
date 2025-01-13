@echo off
echo Starting PostgreSQL Setup...
echo.

REM Check if postgres_files directory exists
if not exist "postgres_files\bin\pg_ctl.exe" (
    echo Error: Required files not found!
    echo Please ensure PostgreSQL files are in the correct location:
    echo   postgres_files\bin\pg_ctl.exe
    echo   postgres_files\bin\postgres.exe
    echo.
    pause
    exit /b 1
)

REM Run the setup program
go run main.go

REM If the program exits with an error
if errorlevel 1 (
    echo.
    echo Setup encountered an error.
    pause
    exit /b 1
)

exit /b 0 