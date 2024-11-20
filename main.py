import PyMacro
from plyer import filechooser

file_path = filechooser.open_file(filters=["*.pymacro", "*.txt"])

if not file_path:
    exit("No file selected. Exiting...")

try:
    with open(file_path[0], "r") as file:
        script_content = file.read()
        PyMacro.macro(script_content)
except Exception as e:
    print(f"Error while running the macro: {e}")