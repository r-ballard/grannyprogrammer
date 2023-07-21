import os
import string
import pandas as pd

def find_next_available_name(starting_letter, starting_second_character, used_names):
    for first_char in string.ascii_uppercase:
        if first_char < starting_letter:
            continue
        for second_char in string.ascii_uppercase + string.digits:
            if (first_char, second_char) not in used_names:
                return first_char, second_char

def rename_files_in_directory(directory, starting_letter, starting_second_character):
    # Ensure the starting_letter is in uppercase
    starting_letter = starting_letter.upper()

    # Ensure the starting_second_character is in uppercase
    starting_second_character = starting_second_character.upper()

    # Calculate the starting sequence value
    starting_sequence_value = (ord(starting_letter) - ord('A')) * 36 + int(starting_second_character, 36)

    # Initialize the list to store old and new file names
    file_data = []

    # Set to store the used names
    used_names = set()

    # Iterate over the files in the directory
    for filename in os.listdir(directory):
        old_name = filename
        name, ext = os.path.splitext(filename)
        if len(name) == 2 and name[0].isalpha() and name[1].isalnum():
            first_char, second_char = name[0].upper(), name[1].upper()
            if first_char in string.ascii_uppercase and second_char in string.ascii_uppercase + string.digits:
                # Skip renaming if the file already follows the convention
                used_names.add((first_char, second_char))
                continue

        # Get the next available name
        first_char, second_char = find_next_available_name(starting_letter, starting_second_character, used_names)

        new_name = f"{first_char}{second_char}"

        # Append the old and new names to the list
        file_data.append({'Old Name': old_name, 'New Name': new_name})

        # Update the used names set
        used_names.add((first_char, second_char))

        # Rename the file
        os.rename(os.path.join(directory, old_name), os.path.join(directory, f"{first_char}{second_char}.wav"))

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(file_data)

    return df

if __name__ == "__main__":
    # Replace 'your_directory_path' with the actual path of the directory
    directory_path = 'your_directory_path'
    if not os.path.isdir(directory_path):
        print(f"Error: '{directory_path}' is not a valid directory.")
    else:
        starting_letter = input("Enter the starting letter (A-Z): ")
        starting_second_character = input("Enter the starting second character (A-Z or 0-9): ")
        if not starting_letter.isalpha() or len(starting_letter) != 1 or not starting_letter.isupper():
            print("Error: Please enter a single uppercase letter (A-Z) for the starting letter.")
        elif not (starting_second_character.isalpha() and starting_second_character.isupper()) and not starting_second_character.isdigit():
            print("Error: Please enter a single uppercase letter (A-Z) or digit (0-9) for the starting second character.")
        else:
            result_df = rename_files_in_directory(directory_path, starting_letter, starting_second_character)
            print(result_df)
            # If you want to save the dataframe to a CSV file, you can use:
            # result_df.to_csv('renaming_log.csv', index=False)
