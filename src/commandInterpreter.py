import sys

import summaryStats
import confidenceIntervals
import dist
import reg
import tests


def interpret(command, data):
    """ When provided a command string, interprets that command and calls an appropriate function.

        As their first token, commands have an opcode, specifying the statistical method to use (e.g. dist, summary, reg).

        For most methods, all the following tokens are method-pertinent arguments to be passed to the analysis function
        (e.g. confidence level for confidenceIntervals, x and y variables for reg.)
        This is with the exception of the dist and tests modules, for whom the second token is a "kind" specifier that
        indicates (for dist) whether to compute a univariate or bivariate distribution or (for tests) which type of
        t-test to use. All the following tokens are then method-pertinent arguments.

        PARAMETERS:
            command - string representing the command inputted by the user
            data - the input dataframe
    """
    command = command.split()
    opcode = command[0]

    match opcode:

        case 'exit':
            sys.exit(0)
        
        case 'help':
            method = command[1]
            match method:
                case 'summary':
                    summaryStats.print_help()
                case 'ci':
                    confidenceIntervals.print_help()
                case 'dist':
                    dist.print_help()
                case 'reg':
                    reg.print_help()
                case 'test':
                    tests.print_help()
                case _:
                    print(f"ERROR: {method} is not a valid function")
        
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
            if kind == 'univ' or kind == 'u':
                dist.show_dist(data, args)
            elif kind == 'biv' or kind == 'b':
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
