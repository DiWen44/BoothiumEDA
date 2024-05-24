import argparse
from functools import reduce
from math import sqrt

import pandas as pd
import numpy as np
from scipy import stats


"""
Prints a table of confidence intervals based on passed command arguments

COMMAND WINDOW ARGUMENTS:

lvl - level of confidence (e.g. 0.99 for a 99% CI). Default is 0.95

vars - a list of numerical variables to get confidence intervals for. In the user's command, this list is denoted by -v or --vars. 
By default, this will be all numerical variables in the dataset.

popParams - a list of the population parameters to find confidence intervals for. Denoted in user command by -p. 
By default intervals for population mean and variance will be found. Possible population parameters to use: ['mean', 'std', 'var', 'prop']

categoricals - a list of variables in the dataset whose values shall be used as categories to sort data into. 
Confidence intervals  will then be calculated for the population parameters of the numerical variables of each category, rather than the dataset as a whole. Denoted in user command by -c or --categoricals.
If no categoricals are provided, no categorization will take place and confidence intervals will be calculated for the whole dataset holistically. By default the categoricals list will be empty.

PARAMETERS:
data - the input dataframe
args - array of command window argument strings obtained by command interpreter module
"""
def getCI(data, args):

    # Deriving argument values from args string using argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('lvl', 
                        nargs='?',
                        default=0.95)
    parser.add_argument('-v','--vars', 
                        nargs='*', 
                        default=list(data.select_dtypes(include='number').columns)) # Default value is all numerical variables in the dataset, so the names of the numerical columns in the dataframe
    parser.add_argument('-p', '--params',
                        nargs='*', 
                        default=['mean','std', 'var'])
    parser.add_argument('-c', '--categoricals',
                        nargs='*',
                        default=[])
    parsedArgs = parser.parse_args(args)

    # Check if requested vars are all present in data
    if not set(parsedArgs.vars).issubset(data.columns):
        print("ERROR: Specified variable(s) not present in data")
        return
    
    # Check if requested vars are numerical by iterating through columns of requested vars
    for i in data[parsedArgs.vars]:
        if not pd.api.types.is_numeric_dtype(data[i]):
            print(f"ERROR: Type {i} is not numeric")
            return

    operations = []
    for i in parsedArgs.params:
        match i:
            case 'mean':
                operations.append(__getMeanInt)
            case 'var':
                operations.append(__getVarInt)
            case 'std':
                operations.append(__getStdInt)
            case _:
                print(f"ERROR: {i} is not a valid population parameter")
                return

    if parsedArgs.categoricals == []:
        table = data[parsedArgs.vars].agg(operations)
    else:
        # Check if categorical vars requested are present in data
        if not set(parsedArgs.categoricals).issubset(data.columns):
            print("ERROR: Specified categorical variable(s) not present in data")
            return
        table = (data.groupby(parsedArgs.categoricals))[parsedArgs.vars].agg(operations)


# Provided a pandas series/column, returns a confidence interval for the population mean of the variable represented by the series/column
def __getMeanInt(series):
    interval = stats.t.interval(alpha=0.95, loc=series.mean(), df=series.dropna().size-1, scale=stats.sem(series))
    return [interval] # Return as a 1 item list, containing the interval as a tuple. This means that pandas will place the interval into a single column of the resulting dataframe


# Provided a pandas series/column, returns a confidence interval for the population variance of the variable represented by the series/column
def __getVarInt(series):
    interval = stats.chi2.interval(alpha=0.95, loc=0, df=series.dropna().size-1)
    return [interval] # Return as a 1 item list, containing the interval as a tuple. This means that pandas will place the interval into a single column of the resulting dataframe


# Provided a pandas series/column, returns a confidence interval for the population standard dev. of the variable represented by the series/column
def __getStdInt(series):
    varInt = __getVarInt(series)
    root = lambda x: sqrt(x)
    return reduce(root, varInt[0]) # Interval bounds for std are the square root of those of variance

