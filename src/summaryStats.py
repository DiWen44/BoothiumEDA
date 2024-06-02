import argparse
import pandas as pd

import utils


"""
Prints table of summary stats based on passed command arguments

COMMAND WINDOW ARGUMENTS:

vars - a list of numerical variables to get statistics for. In the user's command, this list is denoted by -v or --vars. 
By default, this will be all numerical variables in the dataset.

stats - a list of the summary statistics to find. Denoted in user command by -s or --stats. By default mean, median and variance will be found.
Possible statistics that can be calculated: ['mean', 'median', 'mode', 'count', 'sum', 'std', 'var', 'min', 'max'].

categoricals - a list of variables in the dataset whose values shall be used as categories to sort data into. 
Requested sample statistics will then be calculated for the numerical variables of each category, rather than the dataset as a whole. Denoted in user command by -c or --categoricals.
If no categoricals are provided, no categorization will take place and summary statistics will be calculated for the whole dataset holistically. By default the categoricals list will be empty.


FUNCTION PARAMETERS:
data - the input dataframe
args - array of command window argument strings obtained by command interpreter module
"""
def get_stats(data, args):

    # Deriving argument values from args array using argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-v','--vars', 
                        nargs='*', 
                        default=utils.get_numericals(data),
                        choices=utils.get_numericals(data))
    parser.add_argument('-s', '--stats',
                        nargs='*', 
                        default=['mean', 'median', 'var'],
                        choices=['mean', 'median', 'mode', 'count', 'sum', 'std', 'var', 'min', 'max'])
    parser.add_argument('-c', '--categoricals',
                        nargs='*',
                        default=[],
                        choices=data.columns.values)
    parsed_args = parser.parse_args(args)

    if parsed_args.categoricals == []:
        table = __tabulate(data, parsed_args.vars, parsed_args.stats)
    else:
        table = __tabulate_by_categoricals(data, parsed_args.vars, parsed_args.stats, parsed_args.categoricals)

    print(table)


"""
ONLY FOR USE WITHIN THE SUMMARYSTATS MODULE

Find summary statistics for provided numerical variables and tabulates them in a dataframe 
This dataframe will have the numerical variables as columns and their corresponding summary statistics (e.g mean, mode, variance) will form the row index.
Returns the new tabulated summary stats as a dataframe. 

PARAMETERS:
data- the input dataframe
vars - array of numerical variables to find summary statistics for
stats - array of summary statistics (e.g. mean, variance, mode) to find. 

TO GROUP SUMMARY STATISTICS FOR NUMERICAL VARIABLES BY CATEGORIES SPECIFIED BY CATEGORICAL VARIABLES IN THE DATA, USE tabulateByCategoricals()
"""
def __tabulate(data, vars, stats):

    # Dictionary to map requested vars to array of requested stats, for use in .agg()
    vars_dict = {}
    for var in vars:
        vars_dict[var] = stats

    table = data.agg(vars_dict)
    return table
            
                
"""
ONLY FOR USE WITHIN THE SUMMARYSTATS MODULE

Divides provided numerical variables into categories based on provided categorical variables, finds summary statistics for the numerical vars,
and tabulates them in a dataframe.
Returns the new tabulated summary stats as a dataframe

The columns of the returned dataframe will be a 2-level multiindex, the upper level being the numerical variables and the lower level 
being the requested summary statistics.
The rows of the dataframe will pertain to the categoricals provided. If one categorical variable is provided, then it will be a simple index of the categoricals.
If more than one is provided, the row index will be a multiindex of the categorical variable (each level pertains to one of the requested categoricals).
So, for n categoricals, an n-level multiindex will be used for the rows

PARAMETERS:
data- the input dataframe
vars - array of numerical variables to find summary statistics for
stats - array of summary statistics (e.g. mean, variance, mode) to find. 
categoricals - categorical variables in the data to divide entries into categories along, so as to be able to find summary statistics for each category.
"""
def __tabulate_by_categoricals(data, vars, stats, categoricals):

    # Dictionary to map requested vars to array of requested stats, for use in .agg()
    vars_dict = {}
    for var in vars:
        vars_dict[var] = stats

    table = (data.groupby(categoricals)).agg(vars_dict)
    return table
