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

bins - how many intervals to divide data into for histogram - if none is provided, a suitable number will be calculated based on the data
        This is a non-positional arg with flag -b or --bins 

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
    parser.add_argument('-b', '--bins',
                    nargs='?',
                    type=int,
                    default=None)
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
    if  __checkValidPng(parsedArgs.outfile) == -1:
        return 
    
    if parsedArgs.categoricals == []:
        plot = __plotDist(data, parsedArgs.var, parsedArgs.bins)
    else:
        # Check if categorical vars requested are present in data
        if utils.checkValidCategoricals(data, parsedArgs.categoricals) == -1:
            return
        plot = __plotDistByCategoricals(data, parsedArgs.var, parsedArgs.categoricals, parsedArgs.bins)

    # Save plot to png file
    plot.figure.savefig(parsedArgs.outfile)

    # Display saved image
    img = Image.open(parsedArgs.outfile)
    img.show()


"""
Returns a plotted graph showing the probability curve (pdf) and a histogram of a provided pd series.

PARAMETERS:
data - The pandas dataframe holding the data
var - numerical var to get distribution for
bins - number of intervals to divide values into for the histogram
"""
def __plotDist(data, var, bins):
    # Calculate suitable no. of bins if none is provided by user
    if bins is None:
        bins = __calcBins(data[var])

    plot = sns.displot(data=data, kde=True, x=var, bins=bins)
    plot.set_titles(f"Distribution of {var}")
    return plot


"""
Returns a plotted graph showing the probability curves (pdf) and a histograms of categories in a provided pd series.

PARAMETERS:
data - The pandas dataframe holding the data
var - numerical var to get distribution for
categoricals - categorical variable(s) to categorize values of var along
bins - number of intervals to divide values into for the histogram
"""
def __plotDistByCategoricals(data, var, categoricals, bins):
    cutData = data[categoricals+var] # Trim data to get only necessary columns i.e. those for the categoricals and the var, so as to reduce processing time.

    if len(categoricals) > 1: # If more than 1 category requested
        plotData = cutData.set_index(categoricals) # Make index a multiindex of the categoricals
        plotData.index = ['_'.join(row) for row in plotData.index.values] # Fuses plotData's multiindex of categoricals into a single index

        plot = sns.displot(data=plotData, kde=True, bins=bins, x=var, hue=plotData.index)

    else:
        plot = sns.displot(data=cutData, kde=True, bins=bins, x=var, hue=categoricals[0])
    
    plot.set_titles(f"Distribution of {var} by {categoricals}")
    return plot


# Used to check if user-requested output file is valid
# Given the filename, checks if a provided png file is actually a png file.
# Returns 0 if valid, otherwise prints an error message and returns -1
def __checkValidPng(filename):
    if filename[-4:] != '.png':
        print("ERROR: output file must be a .png file")
        return -1 
    return 0


# Calculates a suitable number of bins/intervals for a series/column's distribution histogram, using the Freedman–Diaconis rule
def __calcBins(series):
    # Get interquartile range
    quartiles = series.quantile([0.25,0.75])
    IQR = quartiles[0.75] - quartiles[0.25]

    n = series.dropna().size
    min = series.min()
    max = series.max()
    width = 2*IQR/np.cbrt(n) # Freedman–Diaconis rule
    numBins = np.ceil((max-min)/width)
    return int(numBins)


"""
Given a numerical variable and a categorical variable name,
calculates a suitable number of bins/intervals for each category's distribution histogram of that numerical variable.
Returns a dictionary that maps each category name to a suitable no. of bins for that category.
NOTE: THIS FUNCTION CAN ONLY WORK FOR A SINGLE CATEGORICAL VARIABLE (i.e. ONLY 1 LEVEL OF CATEGORIZATION).

PARAMETERS:
data - the input dataframe
var - the numerical variable
categorical - the categorical variable along which var datapoints are being categorized
"""
def __calcBinsForCategories(data, var, categorical):
    bins = {}
    categories = pd.unique(data[categorical])
    for cat in categories:
        catVars = data[data[categorical] == cat][var]
        bins[cat] = __calcBins(catVars)   

    return bins