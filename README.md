# pycalc
A basic calculator which can parse and evaluate textual input. Expressions are entered through the command-line and the evaluated value is displayed.

This program was created as part of a programming task for a job application. I completed this part of the task in roughly 2 hours.

## Features
* Supports four basic operations: `"+", "-", "*", "/"`
* Numbers can be integers or decimal.
* Parentheses can be used to alter operator precedence (default is according to BODMAS).
* Can sketch an equation using matplotlib if input begins with `"y ="` and is followed by an expression containing `"x"` (case-sensitive).

## Local setup instructions
The `main.py` script can be executed as long as Python 3 is installed. 

If you want to sketch equations with `sketch.py` follow the instructions below.

1. Ensure Python 3 is installed.
2. `python3 -m venv venv` to create a virtual environemnt.
3. `venv/Scripts/activate` to activate virtual environment.
4. `pip install -r requirements.txt` to install required packages (matplotlib).
5. `python src/sketch.py` to execute the script.
