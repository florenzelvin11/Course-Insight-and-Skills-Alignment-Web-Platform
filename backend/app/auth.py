import re


def is_valid_email(email):
    # Define a regex pattern to match the desired format
    pattern1 = r"^z\d{7}@ad\.unsw\.edu\.au$"
    pattern2 = r"^.+@student\.unsw\.edu\.au$"
    pattern3 = r"^.+@unsw\.edu\.au$"

    # Use re.match to check if the email matches the pattern
    if (
        re.match(pattern1, email)
        or re.match(pattern2, email)
        or re.match(pattern3, email)
    ):
        return True
    else:
        return False


def has_consecutive_numbers(input_str):
    count = 1
    for i in range(1, len(input_str)):
        if ord(input_str[i]) == ord(input_str[i - 1]) + 1:
            count += 1
            if count >= 3:
                return True
        else:
            count = 1
    return False


def is_strong_password(password):
    # Check if the password meets the following criteria:
    # 1. Minimum length (e.g., 8 characters)
    # 2. Contains at least one uppercase letter
    # 3. Contains at least one lowercase letter
    # 4. Contains at least one digit
    # 5. Contains at least one special character (e.g., !@#$%^&*)
    # 6. Does not have three consecutive numbers

    if len(password) < 8:
        return False

    if not re.search(r"[A-Z]", password):
        return False

    if not re.search(r"[a-z]", password):
        return False

    if not re.search(r"[0-9]", password):
        return False

    if not re.search(r"[!@#$%^&*]", password):
        return False

    if has_consecutive_numbers(password):
        return False

    return True


def is_valid_zID(input_string):
    # Check if the input string is exactly 7 characters long
    if len(input_string) != 7:
        return False

    # Check if all characters in the input string are digits
    if not input_string.isdigit():
        return False

    # If both conditions are met, the input is valid
    return True
