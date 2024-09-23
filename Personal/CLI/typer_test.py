import typer

app = typer.Typer()

@app.command()
def greet(name: str):
    """Print a greeting message"""
    print(f'Hello, {name}!')

if __name__ == '__main__':
    app()


# To run: (test_venv) D:\2024> python d:\2024\Personal\CLI\typer_test.py subin
# Output: Hello, subin!

# To find args: (test_venv) D:\2024> python d:\2024\Personal\CLI\typer_test.py --help