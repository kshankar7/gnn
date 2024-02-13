"""
Basic reusable scripts for fepx processing

email: kshankar@crimson.ua.edu
lab url: https://acmelab.ua.edu/
"""

import os

def get_sim_fdr(sim_fdr):
    """
    Get the simulation folder.

    Args:
        sim_fdr (str): Path to the simulation folder.

    Returns:
        str: Path to the simulation folder (conforms to both fepx1.3 and fepx2.0).
    """
    return os.path.join(sim_fdr, 'simulation.sim') if os.path.exists(os.path.join(sim_fdr, 'simulation.sim')) else sim_fdr


def get_input_filepath(sim_fdr, input_type='config'):
    """
    Generate the filepath for a specific input file type within a simulation folder.

    Parameters:
    - sim_folder (str): Path to the simulation folder.
    - input_type (str, optional): Type of input file (default is 'config').

    Returns:
    - str: Filepath for the specified input file type.
    """
    sim_fdr = get_sim_fdr(sim_fdr)
    
    # Dictionary mapping input types to their corresponding filenames
    valid_input_types = {'config': 'simulation.cfg',
                         'mesh': 'simulation.mesh',
                         'tess': 'simulation.tess',
                         'opt': 'simulation.opt'}

    # Convert input_type to lowercase for case-insensitive comparison
    input_type = input_type.lower()

    # Check if input_type is valid
    if input_type not in valid_input_types:
        raise ValueError(f"Invalid input type. Supported types: {', '.join(valid_input_types)}")

    # Construct the filepath using os.path.join()
    input_filepath = os.path.join(sim_fdr, 'inputs', valid_input_types[input_type])

    # Check if the file exists
    if os.path.exists(input_filepath):
        return input_filepath
    else:
        return None


def get_result_filepath(sim_fdr, result='stress_eq', entity='elts', steps=0):
    """
    Get file path(s) for simulation result(s).

    This function constructs file path(s) for simulation result(s) based on the provided parameters.

    Args:
        sim_fdr (str): Path to the simulation folder.
        result (str, optional): Type of result (default: 'stress_eq').
        entity (str, optional): Entity type ('elts', 'elsets', or 'mesh') (default: 'elts').
        steps (int or list of ints, optional): Step(s) of the simulation (default: 0).

    Returns:
        str or list of str: File path(s) for the simulation result(s).
    """
    sim_fdr = get_sim_fdr(sim_fdr)
    
    # Check if entity is valid
    if entity not in ['elts', 'elsets', 'mesh']:
        raise ValueError("Invalid entity type. Entity must be one of: 'elts', 'elsets', 'mesh'")

    # Construct path to the result folder
    res_fdr = os.path.join(sim_fdr, 'results', entity, result)
    
    # If steps is an integer, convert it to a list of steps
    if isinstance(steps, int):
        steps = [steps] if steps != 0 else _get_number_of_steps(sim_fdr, include_zero=True)
    
    # Construct file paths for each step
    res_fp = [os.path.join(res_fdr, f'{result}.step{step}') for step in steps]
    
    # Return single file path if only one result, otherwise return list of file paths
    return res_fp[0] if len(res_fp) == 1 else res_fp    


def sort_sim_steps(step_files):
    """
    Sort a list of step files considering the numbers at the end.

    Args:
        step_files (list): List of step files to be sorted.

    Returns:
        list: Sorted list of step files.
    """
    # Define a key function to extract the numerical part at the end of a step file
    def key_func(step_file):
        num_part = re.findall(r'\d+$', step_file)
        return int(num_part[0]) if num_part else step_file

    # Sort the list using the custom key function
    return sorted(step_files, key=key_func)        


def get_number_of_steps(sim_fdr, include_zero=False):
    """
    Get the list of printed steps from the simulation folder.

    This function reads the '.sim' file in the provided simulation folder
    to extract the list of printed steps. Optionally, it can include step zero.

    Args:
        sim_fdr (str): Path to the simulation folder.
        include_zero (bool, optional): Whether to include step zero (default: False).

    Returns:
        list: List of printed steps from the simulation, or [0] if '.sim' file does not exist.
    """
    sim_fdr = get_sim_fdr(sim_fdr)
    
    # Path to the '.sim' file
    dot_sim = os.path.join(sim_fdr, '.sim')

    # Check if '.sim' file exists
    if not os.path.exists(dot_sim):
        return [0]

    # Read the '.sim' file
    with open(dot_sim, 'r') as fp:
        data = fp.readlines()
    
    # Determine the starting step
    start = 0 if include_zero else 1
    
    # Extract the total steps
    total_steps = []
    for i, line in enumerate(data):
        if 'step' in line:
            total_steps = list(range(start, int(data[i+1].split()[-1]) + 1))
    
    # Extract skipped steps
    skipped_steps = []
    if total_steps:
        for i, line in enumerate(data):
            if 'printed' in line:
                skipped_steps = data[i+2].split()
    
    # Remove empty strings and convert to integers
    new_skipped_steps = [int(_s) for _s in skipped_steps if _s.strip()]
    
    # Filter printed steps
    printed_steps = [step for step in total_steps if step not in new_skipped_steps]
    
    return printed_steps
