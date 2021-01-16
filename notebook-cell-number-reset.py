#!/usr/bin/env python3

"""
notebook-cell-number-reset.py

Takes a series of Python notebook file paths as command line arguments and
  resets the numbering for their code cells.
  
In the command line, type
  "python3 notebook-cell-number-reset.py filepath1 filepath2" ...
"""

__author__ = "Bofan Chen"

# Takes command line arguments and exception types.
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
        # Atomic opening of the file.
        with open(path, mode = "r+", encoding = "utf8") as file:
            data = json.loads(file.read())
            counter = 1
            for cell in data["cells"]:
                # Only code cells are labelled.
                if cell["cell_type"] == "code":
                    cell["execution_count"] = counter
                    # Change the labels for the relevant output blocks, as well.
                    for output in cell["outputs"]:
                        if "execution_count" in output:
                            output["execution_count"] = counter
                    counter += 1
            # Go to the beginning of the file.
            file.seek(0)
            # Remove all existing content in the file.
            # This way, if the new file content is shorter than the previous, 
            #   there won't be any old text left over at the end.
            file.truncate()
            json.dump(data, file, indent = 4)
    except Exception as e:
        print(e.__class__ + " encountered when dealing with the file at [" \
          + path + "].")

def main():
    """
    DESCRIPTION
        Goes over each file in a series.
    
    PARAMETERS
        ~ "files" > A list of file paths.
    
    RETURNS
        NONE
    """
    # The first index will contain the file name.
    # The rest will be the command line arguments,
    #   which are expected to be file paths.
    for path in sys.argv[1:]:
        if path[-6:] != ".ipynb":
            print("File at [" + path + "] is not a Python notebook file.")
        else:
            reset_code_cell_numbers(path)

if __name__ == "__main__":
    main()
