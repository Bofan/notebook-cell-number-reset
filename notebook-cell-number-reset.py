#!/usr/bin/env python3

"""
notebook-cell-number-reset.py

Takes a series of Python notebook file paths as command line arguments and
  resets the numbering for their code cells.
"""

__author__ = "Bofan Chen"

# Takes command line arguments.
import sys
# Handles JSON files.
import json

def reset_code_cell_numbers(path):
    """
    DESCRIPTION
        Overwrites the .ipynb file at a given path with reset code cell numbers.

    PARAMETERS
        ~ "path" > A file path to an .ipynb notebook.

    RETURNS
        NONE
    """
    try:
        with open(path, mode = "r+", encoding = "utf8") as file:
            data = json.loads(file.read())
            counter = 1
            for cell in data["cells"]:
                # Only code cells are labelled.
                if cell["cell_type"] == "code":
                    cell["execution_count"] = counter
                    # Change the labels for the output blocks, as well.
                    for output in cell["outputs"]:
                        if "execution_count" in output:
                            output["execution_count"] = counter
                    counter += 1
            # Go to the beginning of the file.
            file.seek(0)
            # Remove all existing contect in the file.
            file.truncate()
            json.dump(data, file, indent = 4)
    except:
        print("Error encountered when dealing with the file at [" + path + "].")

def main(files):
    """
    DESCRIPTION
        Goes over each file in a series.
    
    PARAMETERS
        ~ "files" > A list of file paths.
    
    RETURNS
        NONE
    """
    for path in files:
        if path[-6:] != ".ipynb":
            print("File at [" + path + "] is not a Python notebook file.")
        else:
            reset_code_cell_numbers(path)

if __name__ == "__main__":
    # The first index will contain the file name.
    # The rest will be the command line arguments,
    #   which are expected to be file paths.
    files = sys.argv[1:]
    # Pass on the list of file paths to the main function.
    main(files)