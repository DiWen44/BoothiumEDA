import sys


# Command-line arg is name of input CSV file
try:
    filename = sys.argv[1]
except IndexError: # If no file was provided
    print("ERROR: No input CSV file provided")
    sys.exit()

try:
    file = open(filename, "r")
except FileExistsError:
    print("ERROR: File does not exist")
    sys.exit()

if filename[-3:] != '.csv': # If provided file isn't a CSV file
    print("ERROR: Input file must be a CSV file")
    sys.exit()

print("-"*40 + "\n")

print("EDA TOOL: \n")
print("Type HELP command for information \n\n")

# Command loop
while True:
    command = str(input("> ")).split()
    print("\n")
    

