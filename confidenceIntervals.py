import argparse
from functools import reduce
from math import sqrt

import pandas as pd
import numpy as np
from scipy import stats

import utils


"""
Prints a table of confidence intervals (CI) for population means based on passed command arguments

COMMAND WINDOW ARGUMENTS:

lvl - level of confidence (e.g. 0.99 for a 99% CI). Default is 0.95

vars - a list of numerical variables to get CIs of population means for. In the user's command, this list is denoted by -v or --vars. 
By default, this will be all numerical variables in the dataset.

categoricals - a list of variables in the dataset whose values shall be used as categories to sort data into. 
CIs  will then be calculated for the means of the numerical variables of each category, rather than the dataset as a whole. Denoted in user command by -c or --categoricals.
If no categoricals are provided, no categorization will take place and confidence intervals will be calculated for the whole dataset holistically. By default the categoricals list will be empty.

FUNCTION PARAMETERS:
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
    parser.add_argument('-c', '--categoricals',
                        nargs='*',
                        default=[])
    parsedArgs = parser.parse_args(args)

    # Check if requested numerical vars are valid
    check = utils.checkNumericalVarsRequested(data, parsedArgs.vars)
    if check == -1:
        return 

    varsDict = {}
    for var in parsedArgs.vars:
        varsDict[var] = __getMeanInt

    if parsedArgs.categoricals == []:
        table = data.agg(varsDict)
    else:
        # Check if categorical vars requested are present in data
        if not set(parsedArgs.categoricals).issubset(data.columns):
            print("ERROR: Specified categorical variable(s) not present in data")
            return
        table = data.groupby(parsedArgs.categoricals).agg(varsDict)
    
    print(table)


# Provided a pandas series/column, returns a confidence interval for the population mean of the variable represented by the series/column
# The interval is returned as a single item list containing a tuple that itself contains the lower and upper bounds (in that order) of the interval
# Wrapping the tuple in a list means that pandas will place the interval into a single column of the table, rather than splitting that column into 2 subcolumns
def __getMeanInt(series):

    interval = stats.t.interval(alpha=0.95, loc=series.mean(), df=series.dropna().size-1, scale=stats.sem(series))
    return [interval] # Return as a 1 item list, containing the interval as a tuple. This means that pandas will place the interval into a single column of the resulting dataframe
