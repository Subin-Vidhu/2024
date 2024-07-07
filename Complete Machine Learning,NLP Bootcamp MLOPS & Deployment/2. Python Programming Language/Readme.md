### Python Programming Language

- Create a new env

    - `conda create -p myenv python==3.12` # -p is the path

- Activate the environment
    
    - `conda activate myenv`

- Install ipykernel package

    - `pip install ipykernel` # This package is required to run the jupyter notebook in the new environment.


    - Use  `shift + enter` to run the code in the jupyter notebook.

- Different ways of Creating Virtual Environment

    - `python -m venv myenv`

        - To activate:
                
                - `myenv\Scripts\activate`
        
        - To check python version:
                
                - `python --version`

        - To deactivate:
                
                - `deactivate`
        
    