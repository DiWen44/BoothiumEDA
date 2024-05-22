import sys
import argparse
import pandas

import summaryStats

# When provided a command string, parses that command. Also takes a pd dataframe as "data"
def parse(command, data):
    command = command.split()
    opcode = command[0]
    args = command[1:]

    if opcode == "exit":
        sys.exit(0)
    
    elif opcode == "help":
        print("help placeholder")
    
    # Summary statistics table
    elif opcode == "summary":
        summaryStats.summaryStats(data, args)
    
