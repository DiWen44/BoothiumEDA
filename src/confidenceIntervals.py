import argparse
from functools import reduce

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
                        default=0.95,
                        type=float)
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
    
    # Check if provided confidence level is valid
    if parsedArgs.lvl >= 1 or parsedArgs.lvl <= 0:
        print("ERROR: Confidence level must be a float between 0 and 1")
        return


    # NESTED FUNCTION FOR USE AS AN AGGREGATION FUNCTION IN .agg()
    # Provided a pandas series/column, returns a confidence interval for the population mean of the variable represented by the series/column
    # The interval is returned as a single item list containing a tuple that itself contains the lower and upper bounds (in that order) of the interval
    # Wrapping the tuple in a list means that pandas will place the interval into a single column of the table, rather than splitting that column into 2 subcolumns
    def getMeanInt(series):
        n = series.dropna().size 
        xbar = series.mean() # Sample mean
        s = series.std() # Sample std
        cl = parsedArgs.lvl > 1 or parsedArgs.lvl < 0 # Confidence level
        t_value = stats.t.ppf(1 - cl/2, df=n-1)
        marginOfErr = t_value * (s / np.sqrt(n))
        interval = (xbar-marginOfErr, xbar+marginOfErr)
        return [interval] # Return as a 1 item list, containing the interval as a tuple. This means that pandas will place the interval into a single column of the resulting dataframe
    

    # Dictionary to map requested vars to getMeanInt() function, for use in .agg()
    varsDict = {}
    for var in parsedArgs.vars:
        varsDict[var] = getMeanInt

    if parsedArgs.categoricals == []:
        table = data.agg(varsDict)
    else:
        # Check if categorical vars requested are present in data
        if not set(parsedArgs.categoricals).issubset(data.columns):
            print("ERROR: Specified categorical variable(s) not present in data")
            return
        table = data.groupby(parsedArgs.categoricals).agg(varsDict)
    
    print(table)
