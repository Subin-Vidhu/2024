PostgreSQL Setup Instructions
==========================

1. Extract the contents of this zip file to a folder of your choice.

2. Make sure you have the following structure:
   YourFolder/
   ├── postgres_files/
   │   └── bin/
   │       ├── pg_ctl.exe
   │       ├── postgres.exe
   │       └── [other PostgreSQL files]
   ├── start_postgres.bat
   └── [other files]

3. Double-click "start_postgres.bat" to run the setup.

4. If this is a new installation:
   - The default password will be: password
   - The program will create all necessary databases

5. If you have an existing PostgreSQL installation:
   - You will be prompted for your existing password
   - The password will be hidden while typing

6. To stop the server:
   - Press Ctrl+C in the terminal window
   - Press Y when asked "Terminate batch job (Y/N)?"

Notes:
- The program needs port 8060 to be available
- Data will be stored in the "postgres_data" folder
- Do not close the window while the server is running 