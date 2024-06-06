import sys

import summaryStats
import confidenceIntervals
import dist
import reg
import tests

# When provided a command string, interprets that command based on first token (the "opcode"). 
# Also takes the user's input data as a pd dataframe called "data".
def interpret(command, data):
    command = command.split()
    opcode = command[0]

    match opcode:

        case 'exit':
            sys.exit(0)
        
        case 'help':
            print("help placeholder")
        
        # Summary statistics table
        case 'summary':
            args = command[1:]
            summaryStats.get_stats(data, args)

        # Confidence intervals
        case 'ci':
            args = command[1:]
            confidenceIntervals.get_cis(data, args)

        # Numerical var distribution
        case 'dist':
            kind = command[1]
            args = command[2:]
            if kind == 'univ' or kind == 'U':
                dist.show_dist(data, args)
            elif kind == 'biv' or kind == 'B':
                dist.show_biv_dist(data, args)
            else:
                print("ERROR: Invalid command")


        # Simple linear regression & ANOVA
        case 'reg':
            args = command[1:]
            reg.analyze(data, args)

        # Hypothesis testing
        case 'test':
            kind = command[1]
            args = command[2:]
            match kind:
                case '1samp':
                    tests.one_sample_ttest(data, args)
                case '2samp_cat':
                    tests.two_sample_ttest_by_cat(data, args)
                case '2samp_col':
                    tests.two_sample_ttest_by_col(data, args)
                case 'paired':
                    tests.paired_ttest(data, args)
                case _:
                    print("ERROR: Invalid command")

        case _:
            print("ERROR: Invalid command")
    
