import argparse

def main():
    parser = argparse.ArgumentParser(description='Print a greeting message')
    parser.add_argument('name', type=str, help='Your name')
    args = parser.parse_args()
    print(f'Hello, {args.name}!')

if __name__ == '__main__':
    main()


# To run: (test_venv) D:\2024> python d:\2024\Personal\CLI\argparse_test.py subin