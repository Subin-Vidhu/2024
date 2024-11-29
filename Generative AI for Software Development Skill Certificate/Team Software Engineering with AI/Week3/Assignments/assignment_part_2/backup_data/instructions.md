# Instructions

You may click with the right button in this file (`instrutions.md`) and go under Open With -> Markdown preview to have a better layout of these instructions.

Read it carefully to understand how the assignment works.

## Story
You work as a Software Developer in a company where they have employees that work in shifts. They have a very old system and they store their employee working schedule within a `.json` file. Once, a previous Software Developer built a script to convert this json file into a Pandas DataFrame. Now your boss wants to use a new script to extract the employees schedule given a their working schedule. 

The files given to you are: 

- df_converter.py. The library containing the function to parse the .json file and generate a new dataframe with some statistics and save it in a file.
- internal_stats.py. The library your boss provided to you, containing the script you must use to extract the working schedule of each employee.

You then built a third script joining these two scripts together, called `gen_employee_schedule.py`. However, for some reason, the script does not run. You may try it by opening a terminal (click on the blue + button in the top left corner and open a terminal) and typing `python gen_employee_schedule.py`. 

Your job is to find what is going on and fix the issue, so the script runs and generates files identical to `data_example.csv` and `schedule_example.json`.

## Further instructions

Some **terminal commands** that may be useful

- Please ensure that you are in the `assignment` environmnent. Run `conda activate assignment` before running any script or installing any library.
- You may need `pip install` to install libraries. Don't forget to specify the version of the libraries that you want to install! You can do so by `pip install library==1.4.7´ where library is the intended library and 1.4.7 is the desired version of it.
- Remember to check if you are in the correct folder before running the script. If not, you can navigate through folders by typing `cd folder` where folder is the desired folder.
- To show all files in the directory you are, you may run `ls`.

If you are comfortable with, you may open a Jupyter notebook. **Just remember to open the one called "Python 3.6 (assignment part 1 and 2)"**. But the final solutions must be within the scripts and must run as `python gen_employee_solution.py`. 

## How to work on your solution

There is a folder called `solution_folder` in the directory. All files there have a `_solution` suffix. These will be the graded files. Please do NOT modify the code where it is explicitly said so. The reason for this folder is that you don't lose the original files if anything goes wrong. To run your solution script you may run `python gen_employee_schedule_solution.py`

You may edit one or every script in the solution folder. There are several possible solutions that involves editing one, two or even every script. What matters is to provide the files exactly how it is supposed to be. The `data_example.csv` and the `schedule_example.json` have the intended output for the example in `info_example.json`.

There is a file called `requirements_solution.txt`. After you finish your task and the script runs properly, you **must** add the libraries you are using in this file. You can do so by running `pip freeze > requirements_solution.txt`. Remember to work in the desired folder the files are placed. 


