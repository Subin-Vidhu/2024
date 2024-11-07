# Used commands

    - pwd: print working directory
    - ls: list files in the directory
    - cd: change directory
    - cp seasonal/spring.csv seasonal/summer.csv backup: copy files
    - mv seasonal/spring.csv seasonal/summer.csv backup: move files
    - rm: remove files
    - mkdir: create a directory
    - rmdir: remove a directory
    - touch: create an empty file
    - nano: edit a file
    - cat: print file contents
    - head: print first few lines of a file
    - head -n 5 seasonal/summer.csv: print first 5 lines of a file
    - tail: print last few lines of a file
    - less: scroll through a file
    - :q: quit less
    - :n: next file in less
    - wc: count lines, words, and characters in a file
    - *: wildcard for matching filenames
    - ?: wildcard for matching single characters
    - [aeiou]: wildcard for matching any character inside the brackets
    - [0-9]: wildcard for matching any character inside the range
    - less seasonal/spring.csv seasonal/summer.csv | cat : view multiple files
    - grep: search for patterns in files    
    - ls -R -F /home/repl: list all files in the directory and subdirectories
    - man tail | cat: view the manual page for a command
    - tail -n +7 seasonal/spring.csv: print all lines starting from the 7th line
    - cut -f 2-5,8 -d , values.csv: extract columns 2-5 and 8 from a CSV file
    - history: view the history of commands
    `grep` can search for patterns as well; we will explore those in the next course. What's more important right now is some of grep's more common flags:

        -c: print a count of matching lines rather than the lines themselves
        -h: do not print the names of files when searching multiple files
        -i: ignore case (e.g., treat "Regression" and "regression" as matches)
        -l: print the names of files that contain matches, not the matches
        -n: print line numbers for matching lines
        -v: invert the match, i.e., only show lines that don't match

    - tail -n 5 seasonal/winter.csv > last.csv: get the last 5 lines of a file and save them to a new file
    - cut -d , -f 2 seasonal/summer.csv | grep -v Tooth: extract the second column from a CSV file and remove any lines that contain the word "Tooth"
    - head -n 3 seasonal/s* # ...or seasonal/s*.csv, or even s*/s*.csv: print the first 3 lines of all files in the seasonal directory that start with "s"
    - tail -n 1 seasonal/s* # ...or seasonal/s*.csv, or even s*/s*.csv: print the last line of all files in the seasonal directory that start with "s"
    