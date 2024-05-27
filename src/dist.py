import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import utils


"""
Shows a histogram, probability function (pdf) plot and associated data of a numerical variable's distribution

COMMAND WINDOW ARGUMENTS:

var - a numerical variable to get the distribution for. 

categoricals - a list of variables in the dataset whose values shall be used as categories to group datapoints of the numerical var into. 
The distribution data will then be shown for each category, rather than the dataset as a whole. Denoted in user command by -c or --categoricals.
If no categoricals are provided, no categorization will take place and summary statistics will be calculated for the whole dataset holistically. By default the categoricals list will be empty.
"""
def showDistInfo(data, args):

    # Deriving argument values from args array using argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('var', nargs=1) 
    parser.add_argument('-c', '--categoricals',
                        nargs='*',
                        default=[])
    parsedArgs = parser.parse_args(args)


    # Check if requested numerical var is valid
    check = 0 # utils.checkNumericalVarsRequested(data, [parsedArgs.var])
    if check == -1:
        return 
    
    if parsedArgs.categoricals == []:
        values = data[parsedArgs.var]
        __plotDist(values)
    else:
        # Check if categorical vars requested are present in data
        if not set(parsedArgs.categoricals).issubset(data.columns):
            print("ERROR: Specified categorical variable(s) not present in data")
            return


# Given an array of values, plots a graph showing their probability curve (pdf) and a histogram
def __plotDist(values):
    