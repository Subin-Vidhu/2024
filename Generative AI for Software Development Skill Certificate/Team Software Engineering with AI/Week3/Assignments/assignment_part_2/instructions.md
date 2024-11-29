# Assignment Part 2: Resolving Dependency Conflicts

**Please open this file as follows: Right click on `instructions.md` (in the left panel) -> `Open with` -> `Markdown preview`. This will ensure a better reading experience.**

## Overview

This assignment requires you to use terminal commands to debug and resolve script execution and library dependency conflicts, focusing on managing employee schedules with Python scripts. Follow these instructions carefully to complete the assignment successfully.

## Getting Started

1. **Preview Instructions**: For an enhanced reading experience, right-click on this file (`instructions.md’) and select Open With -> Markdown Preview.

2. **Environment Activation**: Activate the `assignment` environment before starting any script executions or library installations by running `conda activate assignment` in the terminal.

3. **Assignment Workspace**: Your workspace for this assignment is the `assignment_part_2` folder, where you will execute scripts and manage library dependencies.

4. **Backup Data**: The `backup_data` folder inside `assignment_part_2` contains copies of all scripts. Use these backups if you need to revert any changes made to the scripts in the main folder.

5. **Requirements File**: The `requirements.txt` file, which you need to edit and submit, lists all necessary libraries. If library dependencies are mistakenly altered, restore the initial setup by retrieving the original `requirements.txt` from the `backup_data` folder and running `pip install -r requirements.txt`.

## Leveraging LLM Assistance

If you encounter dependency issues or need clarification on how the scripts work and interact with each other, do not hesitate to use a Large Language Model (LLM) like ChatGPT. This tool can provide explanations, debug assistance, and guidance on resolving dependency conflicts effectively.

## Understanding the Scripts

### Script Descriptions:

- **df_converter.py**: This script takes a `.json` file containing employee schedules and converts it into a Pandas DataFrame. It then enriches this DataFrame with statistics before saving the output. 

- **internal_stats.py**: Extract the working schedules for each employee from a Pandas DataFrame.

- **gen_employee_schedule.py**: Integrates the functionalities of the above scripts into a single workflow. It aims to convert the `.json` schedule file into a DataFrame, enrich it with statistics, and extract detailed schedules for each employee. However, this script is currently not running due to issues that need to be resolved. It outputs a `.csv`file with the employee data parsed from the `.json` file, adding some statistics. It also outputs a `.json` file called `schedule.json` with the employee schedule.

## Assignment Task

### Task Instructions

1. **Attempt Script Execution**: In the `assignment_part_2` folder, try running `python gen_employee_schedule.py`. Identify why the script fails to execute and fix the issue to generate outputs identical to `data_example.csv` and `schedule_example.json`.

2. **Library Installation and Dependency Management**: Install additional libraries or specific versions with `pip install library==version` as needed to resolve dependency conflicts. Remember to update the `requirements.txt` file accordingly.

3. **YOU MAY ONLY CHANGE PANDAS AND/OR NUMPY LIBRARY, ANY OTHER CHANGE MAY CAUSE A ZERO SCORE.**

## Working on Your Solution

- **Code Modification**: Avoid altering code sections explicitly marked as immutable. Use the `backup_data` folder to start over if necessary.
- **Execute Your Solution**: Run your corrected script with `python gen_employee_schedule.py`.
- **Update Requirements**: After successful script execution, update the `requirements.txt` with the libraries used by running `pip freeze > requirements.txt`.

## Graded Files

- The scripts within the `assignment_part_2` folder (`df_converter.py`, `internal_stats.py`, and `gen_employee_schedule.py`).
- The `requirements.txt` file listing all libraries used.


## How to submit your solution

To submit your solution, in the folder for this part (assignment_part_2) run the following command in the terminal `bash submit_solution.sh`. It will generate a file called `submission.tar.gz`. Then click "submit assignment" on the top right corner.

## Terminal Commands Recap

- Activate the environment: `conda activate assignment`
- Install or manage libraries: `pip install library==version`
- Navigate directories: `cd folder`
- List directory contents: `ls`
- Execute script: `python script_name.py`

By following these instructions and leveraging LLM assistance as needed, you will be able to debug the script and manage library dependencies effectively, ensuring the production of the required outputs.