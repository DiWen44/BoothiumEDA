import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

import utils


"""
Shows a histogram, probability function (pdf) plot and associated data of a numerical variable's distribution

COMMAND WINDOW ARGUMENTS:

var - a numerical variable to get the distribution for. 

outFile - the name of a png file to be created and to save the plot to. In the user's command, this list is denoted by -o or --outfile. 
            Set to 'output.png' file by default.

categoricals - a list of variables in the dataset whose values shall be used  to categorize datapoints of the numerical var.
The distribution data will then be shown for each category, rather than the dataset as a whole. Denoted in user command by -c or --categoricals.
If no categoricals are provided, no categorization will take place and summary statistics will be calculated for the whole dataset holistically. By default the categoricals list will be empty.

FUNCTION PARAMETERS:
data - the input dataframe
args - array of command window argument strings obtained by command interpreter module
"""
def showDistInfo(data, args):

    # Deriving argument values from args array using argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('var'),
    parser.add_argument('-o', '--outfile',
                        nargs='?',
                        default='output.png')
    parser.add_argument('-c', '--categoricals',
                        nargs='*',
                        default=[]),
    parsedArgs = parser.parse_args(args)

    # Check if requested numerical var is valid
    if utils.checkNumericalVarsRequested(data, [parsedArgs.var]) == -1:
        return 
    
    # Check if specified output file is a png
    if  utils.checkValidPng(parsedArgs.outfile) == -1:
        return 
    
    if parsedArgs.categoricals == []:
        plot = __plotDist(data, parsedArgs.var)
    else:
        # Check if categorical vars requested are present in data
        if utils.checkValidCategoricals(data, parsedArgs.categoricals) == -1:
            return
        plot = __plotDistByCategoricals(data, parsedArgs.var, parsedArgs.categoricals)

    # Save plot to png file
    plot.figure.savefig(parsedArgs.outfile)

    # Display saved image
    img = Image.open(parsedArgs.outfile)
    img.show()


"""
Returns a seaborn figure graph showing the probability curve (pdf) and a histogram of a provided pd series.

PARAMETERS:
data - The pandas dataframe holding the data
var - numerical var to get distribution for
"""
def __plotDist(data, var):
    plot = sns.displot(data=data, kde=True, color='r', x=var, bins='sqrt')
    plot.set_titles(f"DISTRIBUTION OF {var}")
    return plot


"""
Returns a seaborn figure containing a series of plots, each plot showing the probability curve (pdf) 
and histogram of each category in a provided pd series.

PARAMETERS:
data - The pandas dataframe holding the data
var - numerical var to get distribution for
categoricals - categorical variable(s) to categorize values of var along
"""
def __plotDistByCategoricals(data, var, categoricals):
    cutData = data[categoricals+[var]] # Trim data to get only necessary columns i.e. those for the categoricals and the var, so as to reduce processing time.

    if len(categoricals) > 1: # If more than 1 category requested
        plotData = cutData.set_index(categoricals) # Make index a multiindex of the categoricals
        plotData.index = ['_'.join(row) for row in plotData.index.values] # Fuses plotData's multiindex of categoricals into a single index
        plot = sns.displot(data=plotData, x=var, kde=True, bins='sqrt', col=plotData.index.values, col_wrap=3)
    else:
        plot = sns.displot(data=cutData, x=var, kde=True, bins='sqrt', col=categoricals[0], col_wrap=3)
    
    plot.figure.subplots_adjust(top=0.9)
    plot.figure.suptitle(f"DISTRIBUTION OF {var} BY {categoricals}")
    return plot


