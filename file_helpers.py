"""
Basic reusable scripts for file processing

email: kshankar@crimson.ua.edu
lab url: https://acmelab.ua.edu/
"""

import os

def create_folder(folder_path):
    """
    Create a folder if it does not exist.

    Args:
        folder_path (str): Path to the folder to be created.

    Returns:
        str: The path to the created folder.
    """
    # Check if the folder already exists
    if not os.path.exists(folder_path):
        # Create the folder recursively if it doesn't exist
        os.makedirs(folder_path)

    return folder_path


def save_dict_to_json(dict_data, json_file_path, indent=4):
    """
    Save any dictionary to a JSON file.

    Args:
        dict_data (dict): Dictionary containing yield stress values.
        json_file_path (str): Path to the JSON file.
        indent (int, optional): Number of spaces used for indentation (default is 4).
    """
    with open(json_file_path, 'w') as json_file:
        json.dump(dict_data, json_file, indent=indent)


def read_file_contents(file_path, col=0):
    """
    Read the contents of a file and process based on the number of lines and values.

    Args:
        file_path (str): Path to the file.
        col (int, optional): Index of the column to return (default: 0).

    Returns:
        float or list or None: If the file has one line with one value, return the value as a float.
                               If the file has one line with multiple values, return the values as a list of floats.
                               If the file has more than one line, return None.
                               If the specified column index does not exist, return None.
                               If col is specified, return the value at the specified column index.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Check if there is more than one line in the file
    if len(lines) > 1:
        return None

    # If there is only one line, split it by space
    values = lines[0].strip().split()

    # If there is only one value, return it as a float
    if len(values) == 1:
        return float(values[0])
    # If there are multiple values, return them as a list of floats
    else:
        float_values = [float(value) for value in values]
        # If col is specified and the index exists, return the value at that index
        if col < len(float_values):
            return float_values[col]
        else:
            return None            
