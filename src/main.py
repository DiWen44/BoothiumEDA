import sys

import commandInterpreter
import utils


# Command-line arg is name of input CSV file
try:
    filename = sys.argv[1]
except IndexError:  # If no file was provided
    print("ERROR: No input CSV file provided")
    sys.exit()

data = utils.check_and_load_csv_file(filename)
if data.empty:
    sys.exit()

print("-"*40 + "\n")

print("BOOTHIUMEDA: \n")
print("Type HELP command for information \n\n")

# Command loop
while True:
    command = str(input("> "))
    print("\n")
    commandInterpreter.interpret(command, data)



