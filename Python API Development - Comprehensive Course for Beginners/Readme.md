### Python API Development - Comprehensive Course for Beginners

- Reference: [Video](https://youtu.be/0sOvCWFmrtA?si=-05wLEo8dSuYzQfz)

- To run on Windows:

    - Install:
    
        - `python -m venv test_venv` # Create a virtual environment if not already created
        
        - `test_venv\Scripts\activate` # Activate the virtual environment
        
        - `pip install "fastapi[standard]"` # Refer to [FastAPI](https://fastapi.tiangolo.com/tutorial/#run-the-code:~:text=checks%2C%20autocompletion%2C%20etc.-,Install%20FastAPI,-%C2%B6) for more details

    - Run:

        - `(test_venv) D:\2024>fastapi dev "d:\2024\Python API Development - Comprehensive Course for Beginners\fastapi_main.py"`

        - `(test_venv) D:\2024>fastapi dev "d:\2024\Python API Development - Comprehensive Course for Beginners\fastapi_main.py" --reload` # To reload the server on changes, mostly for development

    - Test:
    
            - `http://localhost:8000/docs` # Swagger UI
            - `http://localhost:8000/redoc` # ReDoc UI