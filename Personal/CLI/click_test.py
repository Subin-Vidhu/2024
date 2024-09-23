import click

@click.command()
@click.argument('name', type=str)
def greet(name):
    """Print a greeting message"""
    click.echo(f'Hello, {name}!')

if __name__ == '__main__':
    greet()


# To run: (test_venv) D:\2024> python d:\2024\Personal\CLI\click_test.py subin
# Output: Hello, subin!

# To find args: (test_venv) D:\2024> python d:\2024\Personal\CLI\click_test.py --help