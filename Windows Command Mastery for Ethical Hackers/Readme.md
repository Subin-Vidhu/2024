 - cmd : Command Prompt
 - color help : change the color of the text
   ```
    Microsoft Windows [Version 10.0.19045.3930]
    (c) Microsoft Corporation. All rights reserved.

    C:\Users\Subin-PC>color help
    Sets the default console foreground and background colors.

    COLOR [attr]

    attr        Specifies color attribute of console output

    Color attributes are specified by TWO hex digits -- the first
    corresponds to the background; the second the foreground.  Each digit
    can be any of the following values:

        0 = Black       8 = Gray
        1 = Blue        9 = Light Blue
        2 = Green       A = Light Green
        3 = Aqua        B = Light Aqua
        4 = Red         C = Light Red
        5 = Purple      D = Light Purple
        6 = Yellow      E = Light Yellow
        7 = White       F = Bright White

    If no argument is given, this command restores the color to what it was
    when CMD.EXE started.  This value either comes from the current console
    window, the /T command line switch or from the DefaultColor registry
    value.

    The COLOR command sets ERRORLEVEL to 1 if an attempt is made to execute
    the COLOR command with a foreground and background color that are the
    same.

    Example: "COLOR fc" produces light red on bright white

    C:\Users\Subin-PC>color 1
   ```

 - prompt : allows you to customize the appearence of cmd prompt window.

   ```
    C:\Users\Subin-PC>help prompt
    Changes the cmd.exe command prompt.

    PROMPT [text]

    text    Specifies a new command prompt.

    Prompt can be made up of normal characters and the following special codes:

    $A   & (Ampersand)
    $B   | (pipe)
    $C   ( (Left parenthesis)
    $D   Current date
    $E   Escape code (ASCII code 27)
    $F   ) (Right parenthesis)
    $G   > (greater-than sign)
    $H   Backspace (erases previous character)
    $L   < (less-than sign)
    $N   Current drive
    $P   Current drive and path
    $Q   = (equal sign)
    $S     (space)
    $T   Current time
    $V   Windows version number
    $_   Carriage return and linefeed
    $$   $ (dollar sign)

    If Command Extensions are enabled the PROMPT command supports
    the following additional formatting characters:

    $+   zero or more plus sign (+) characters depending upon the
        depth of the PUSHD directory stack, one character for each
        level pushed.

    $M   Displays the remote name associated with the current drive
        letter or the empty string if current drive is not a network
        drive.
   ```

 - help : help page
    ```
    C:\Users\Subin-PC>help
    For more information on a specific command, type HELP command-name
    ASSOC          Displays or modifies file extension associations.
    ATTRIB         Displays or changes file attributes.
    BREAK          Sets or clears extended CTRL+C checking.
    BCDEDIT        Sets properties in boot database to control boot loading.
    CACLS          Displays or modifies access control lists (ACLs) of files.
    CALL           Calls one batch program from another.
    CD             Displays the name of or changes the current directory.
    CHCP           Displays or sets the active code page number.
    CHDIR          Displays the name of or changes the current directory.
    CHKDSK         Checks a disk and displays a status report.
    CHKNTFS        Displays or modifies the checking of disk at boot time.
    CLS            Clears the screen.
    CMD            Starts a new instance of the Windows command interpreter.
    COLOR          Sets the default console foreground and background colors.
    COMP           Compares the contents of two files or sets of files.
    COMPACT        Displays or alters the compression of files on NTFS partitions.
    CONVERT        Converts FAT volumes to NTFS.  You cannot convert the
                current drive.
    COPY           Copies one or more files to another location.
    DATE           Displays or sets the date.
    DEL            Deletes one or more files.
    DIR            Displays a list of files and subdirectories in a directory.
    DISKPART       Displays or configures Disk Partition properties.
    DOSKEY         Edits command lines, recalls Windows commands, and
                creates macros.
    DRIVERQUERY    Displays current device driver status and properties.
    ECHO           Displays messages, or turns command echoing on or off.
    ENDLOCAL       Ends localization of environment changes in a batch file.
    ERASE          Deletes one or more files.
    EXIT           Quits the CMD.EXE program (command interpreter).
    FC             Compares two files or sets of files, and displays the
                differences between them.
    FIND           Searches for a text string in a file or files.
    FINDSTR        Searches for strings in files.
    FOR            Runs a specified command for each file in a set of files.
    FORMAT         Formats a disk for use with Windows.
    FSUTIL         Displays or configures the file system properties.
    FTYPE          Displays or modifies file types used in file extension
                associations.
    GOTO           Directs the Windows command interpreter to a labeled line in
                a batch program.
    GPRESULT       Displays Group Policy information for machine or user.
    GRAFTABL       Enables Windows to display an extended character set in
                graphics mode.
    HELP           Provides Help information for Windows commands.
    ICACLS         Display, modify, backup, or restore ACLs for files and
                directories.
    IF             Performs conditional processing in batch programs.
    LABEL          Creates, changes, or deletes the volume label of a disk.
    MD             Creates a directory.
    MKDIR          Creates a directory.
    MKLINK         Creates Symbolic Links and Hard Links
    MODE           Configures a system device.
    MORE           Displays output one screen at a time.
    MOVE           Moves one or more files from one directory to another
                directory.
    OPENFILES      Displays files opened by remote users for a file share.
    PATH           Displays or sets a search path for executable files.
    PAUSE          Suspends processing of a batch file and displays a message.
    POPD           Restores the previous value of the current directory saved by
                PUSHD.
    PRINT          Prints a text file.
    PROMPT         Changes the Windows command prompt.
    PUSHD          Saves the current directory then changes it.
    RD             Removes a directory.
    RECOVER        Recovers readable information from a bad or defective disk.
    REM            Records comments (remarks) in batch files or CONFIG.SYS.
    REN            Renames a file or files.
    RENAME         Renames a file or files.
    REPLACE        Replaces files.
    RMDIR          Removes a directory.
    ROBOCOPY       Advanced utility to copy files and directory trees
    SET            Displays, sets, or removes Windows environment variables.
    SETLOCAL       Begins localization of environment changes in a batch file.
    SC             Displays or configures services (background processes).
    SCHTASKS       Schedules commands and programs to run on a computer.
    SHIFT          Shifts the position of replaceable parameters in batch files.
    SHUTDOWN       Allows proper local or remote shutdown of machine.
    SORT           Sorts input.
    START          Starts a separate window to run a specified program or command.
    SUBST          Associates a path with a drive letter.
    SYSTEMINFO     Displays machine specific properties and configuration.
    TASKLIST       Displays all currently running tasks including services.
    TASKKILL       Kill or stop a running process or application.
    TIME           Displays or sets the system time.
    TITLE          Sets the window title for a CMD.EXE session.
    TREE           Graphically displays the directory structure of a drive or
                path.
    TYPE           Displays the contents of a text file.
    VER            Displays the Windows version.
    VERIFY         Tells Windows whether to verify that your files are written
                correctly to a disk.
    VOL            Displays a disk volume label and serial number.
    XCOPY          Copies files and directory trees.
    WMIC           Displays WMI information inside interactive command shell.

    For more information on tools see the command-line reference in the online help.

    C:\Users\Subin-PC>help cd
    Displays the name of or changes the current directory.

    CHDIR [/D] [drive:][path]
    CHDIR [..]
    CD [/D] [drive:][path]
    CD [..]

    ..   Specifies that you want to change to the parent directory.

    Type CD drive: to display the current directory in the specified drive.
    Type CD without parameters to display the current drive and directory.

    Use the /D switch to change current drive in addition to changing current
    directory for a drive.

    If Command Extensions are enabled CHDIR changes as follows:

    The current directory string is converted to use the same case as
    the on disk names.  So CD C:\TEMP would actually set the current
    directory to C:\Temp if that is the case on disk.

    CHDIR command does not treat spaces as delimiters, so it is possible to
    CD into a subdirectory name that contains a space without surrounding
    the name with quotes.  For example:

        cd \winnt\profiles\username\programs\start menu

    is the same as:

        cd "\winnt\profiles\username\programs\start menu"

    which is what you would have to type if extensions were disabled.
    ```

 - cls : clear the screen

 - start : to start a new cmd prompt

 - exit : to exit the terminal

 - dir : for listing files and folders

 - cd : change directory

 - cd.. : to move back to the previous dir

 - echo : to right text to a file

   ```
    C:\Users\Subin-PC>echo "testing" >> new.txt

    C:\Users\Subin-PC>type new.txt
    "testing"
   ```

 - mkdir : to create directories

 - rename : to rename a file

 - xcopy : to copy the content of one folder to another

 - rmdir : to remove empty directories

 - rmdir /s /q dir_name : to remove non-empty directories

 - del : to delete a file

 - ipconfig : information about the network configuration

 - ping destination : checks for the connectivity and measures the round trip time

 - nslookup domain_name : to check the ip address

 - tracert domain_name : shows you the ip addresses of routers along the way

 - netstat : display active network connection, listening ports and other network related information.

 - date and time : to change and set date and time.

 - attrib +h +s Hidden_Test : to hide a folder

 - attrib -h -s Hidden_Test : to unhide a folder

 - shutdown /s /f /t 0 : shortcut to shutdown the system, the last input is the delay

 - netsh wlan show profiles : displays all the wireless networks

 - netsh wlan show profile "name" key=clear : to get the details

 - hostname : display the hostname of the current computer

 - netsh advfirewall set all state off/on : to turn off/on firewall

 - wmic cpu : details of cpu

 - tasklist : to display the processess that are running on your system.
 
 - taskkill /pid pid_no : kills the task

 - driverquery : list the information of all installed drivers

 - winver : displays the version of windows installed

 - net user : to list all the users

 - systeminfo : system details

 - notepad : to open notepad
 
 - calc : to open calculator
