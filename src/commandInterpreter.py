import sys

import summaryStats
import confidenceIntervals

# When provided a command string, interprets that command based on first token (the "opcode"). 
# Also takes the user's input data as a pd dataframe called "data".
def interpret(command, data):
    command = command.split()
    opcode = command[0]
    args = command[1:]

    match opcode:

        case 'exit':
            sys.exit(0)
        
        case 'help':
            print("help placeholder")
        
        # Summary statistics table
        case 'summary':
            summaryStats.getStats(data, args)

        #confidence intervals
        case 'ci':
            confidenceIntervals.getCI(data, args)

        case _:
            print("ERROR: Invalid command")
    
