//Random Password Generator
import random
import string


def get_user_preferences():
    length = int(input("Enter the desired password length: "))
    print("Select character types to include in the password:")
    print("1. Letters (a-z, A-Z)")
    print("2. Digits (0-9)")
    print("3. Symbols (!@#$%^&*)")
    char_types = input("Enter the numbers corresponding to your choices (e.g., 123 for all types): ")
    return length, char_types


def generate_password(length, char_types):
    char_set = ""
    if '1' in char_types:
        char_set += string.ascii_letters
    if '2' in char_types:
        char_set += string.digits
    if '3' in char_types:
        char_set += string.punctuation

    if not char_set:
        raise ValueError("No character types selected")

    return ''.join(random.choice(char_set) for _ in range(length))


def main():
    try:
        length, char_types = get_user_preferences()
        password = generate_password(length, char_types)
        print(f"Generated password: {password}")
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
