import sys
import commandParser

import pandas as pd

# Command-line arg is name of input CSV file
try:
    filename = sys.argv[1]
except IndexError: # If no file was provided
    print("ERROR: No input CSV file provided")
    sys.exit()

# If provided file isn't a CSV file
if filename[-4:] != '.csv':
    print("ERROR: Input file must be a CSV file")
    sys.exit()

try:
    data = pd.read_csv(filename) # Load file into pd dataframe
except FileNotFoundError:
    print("ERROR: File does not exist")
    sys.exit()

print("-"*40 + "\n")

print("EDA TOOL: \n")
print("Type HELP command for information \n\n")

# Command loop
while True:
    command = str(input("> "))
    print("\n")
    commandParser.parse(command, data)



