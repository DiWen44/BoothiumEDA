import argparse
import numpy as np
from scipy import stats

import utils


def get_cis(data, args):
    """ Prints a table of confidence intervals (CI) for population means based on passed command arguments

    COMMAND WINDOW ARGUMENTS:

        lvl - level of confidence (e.g. 0.99 for a 99% CI). Default is 0.95

        vars - a list of numerical variables to get CIs of population means for. In the user's command, this list is denoted by -v or --vars.
        By default, this will be all numerical variables in the dataset.

        categoricals - a list of variables in the dataset whose values shall be used as categories to sort data into.
        CIs  will then be calculated for the means of the numerical variables of each category, rather than the dataset as a whole.
        Denoted in user command by -c or --categoricals.
        If no categoricals are provided, no categorization will take place and confidence intervals will be calculated for the whole dataset holistically.
        By default, the categoricals list will be empty.

    FUNCTION PARAMETERS:
        data - the input dataframe
        args - array of command window argument strings obtained by command interpreter module
    """

    # Deriving argument values from args array using argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('lvl',
                        nargs='?',
                        default=0.95,
                        type=float)
    parser.add_argument('-v', '--vars',
                        nargs='*',
                        default=utils.get_numericals(data),
                        choices=utils.get_numericals(data))
    parser.add_argument('-c', '--categoricals',
                        nargs='*',
                        default=[],
                        choices=data.columns.values)
    parsed_args = parser.parse_args(args)
    
    # Check if provided confidence level is valid
    if parsed_args.lvl >= 1 or parsed_args.lvl <= 0:
        print("ERROR: Confidence level must be a float between 0 and 1")
        return

    # NESTED FUNCTION FOR USE AS AN AGGREGATION FUNCTION IN .agg()
    # Provided a pandas series/column, returns a confidence interval for the population mean of the variable represented by the series/column
    # The interval is returned as a single item list containing a tuple that itself contains the lower and upper bounds (in that order) of the interval
    # Wrapping the interval tuple in a list means that pandas will place the interval into a single column of the df, rather than splitting that column into 2 subcolumns
    def __get_mean_interval(series):
        n = series.dropna().size 
        xbar = series.mean()  # Sample mean
        s = series.std()  # Sample std
        cl = parsed_args.lvl  # Confidence level
        t_value = stats.t.ppf(1 - cl/2, df=n-1)
        margin_of_err = t_value * (s / np.sqrt(n))
        interval = (xbar-margin_of_err, xbar+margin_of_err)
        return [interval]

    # Dictionary to map requested vars to __get_mean_interval() function, for use in .agg()
    vars_dict = {}
    for var in parsed_args.vars:
        vars_dict[var] = __get_mean_interval

    if parsed_args.categoricals == []:
        table = data.agg(vars_dict)
    else:
        table = data.groupby(parsed_args.categoricals).agg(vars_dict)
    
    print(table)


def print_help():
    """Prints a help message for this module"""
    print("usage: ci [lvl] [-v/--vars] [-c/--categoricals]")
    print("\tlvl                   Level of confidence for intervals (e.g. 0.99 for a 99% CI). Default is 0.95")
    print("\t-v/--vars             List of numerical variables to get summary statistics for (default: all numerical vars in data)")
    print("\t-c/--categoricals     List of categorical variables to categorize datapoints on (empty by default). No categorization if none provided")
    print("\n")
