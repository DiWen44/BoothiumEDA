import sys
import pandas as pd

import commandInterpreter
import utils


# Command-line arg is name of input CSV file
try:
    filename = sys.argv[1]
except IndexError: # If no file was provided
    print("ERROR: No input CSV file provided")
    sys.exit()

data = utils.checkAndLoadCSVFile(filename)
if data.empty:
    sys.exit()

print("-"*40 + "\n")

print("EDA TOOL: \n")
print("Type HELP command for information \n\n")

# Command loop
while True:
    command = str(input("> "))
    print("\n")
    commandInterpreter.interpret(command, data)



