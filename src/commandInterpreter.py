import sys

import summaryStats
import confidenceIntervals
import dist
import reg


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
            summaryStats.get_stats(data, args)

        # Confidence intervals
        case 'ci':
            confidenceIntervals.get_cis(data, args)

        # Numerical var distribution
        case 'dist':
            dist.show_dist(data, args)

        # Bivariate (2 numerical var) distribution
        case 'bivdist':
            dist.show_biv_dist(data, args)

        # Simple linear regression & ANOVA
        case 'reg':
            reg.analyze(data, args)

        case _:
            print("ERROR: Invalid command")
    
