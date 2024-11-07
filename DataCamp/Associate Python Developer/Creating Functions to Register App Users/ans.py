from python_functions import validate_name, validate_email, validate_password, top_level_domains

# 1. Function to validate user input from sign-up form
def validate_user(name, email, password):
    """Validate the user name, email and password.

    Args:
        name (string): Name that we're attempting to validate.
        email (string): Email address that we're attempting to validate.
        password (string): Password that we're attempting to validate.

    Returns:
        Boolean: Will return True if all validation checks pass

    Raises ValueError if validation fails.
    """

    # Check if name is not valid, if not raise value error.
    if validate_name(name) == False:
        raise ValueError("Please make sure your name is greater than 2 characters!")

    # Check if email is not valid, if not raise value error.
    if validate_email(email) == False:
        raise ValueError("Your email address is in the incorrect format, please enter a valid email.")

    # Check if password is not valid, if not raise value error.
    if validate_password(password) == False:
        raise ValueError("Your password is too weak, ensure that your password is greater than 8 characters, contains a capital letter and a number.")

    # If none of the if not statements are triggered, return True
    return True

# 2. Function to register validated user if all checks have passed
def register_user(name, email, password):
    """Attempt to register the user if they pass validation.

    Args:
        name (string): Name of the user
        email (string): Email address of the user
        password (string): Password of the user

    Returns:
        Dict: Return a dictionary with the user details

    Raises ValueError on missing arguments.
    """

    # Check if user input is valid by calling the validate user function
    if validate_user(name, email, password):
        # Create user object with details
        user = {
            "name": name,
            "email": email,
            "password": password
        }

        # Return user object
        return user

    # If validation fails, return False
    return False