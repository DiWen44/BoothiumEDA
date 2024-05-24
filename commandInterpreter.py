import sys
import argparse
import pandas

import summaryStats
import confidenceIntervals

# When provided a command string, interprets that command based on first token (the "opcode"). 
# Also takes the data as a pd dataframe called "data".
def interpret(command, data):
    command = command.split()
    opcode = command[0]
    args = command[1:]

    if opcode == "exit":
        sys.exit(0)
    
    elif opcode == "help":
        print("help placeholder")
    
    # Summary statistics table
    elif opcode == "summary":
        summaryStats.getStats(data, args)

    #confidence intervals
    elif opcode == "ci":
        confidenceIntervals.getCI(data, args)
    
