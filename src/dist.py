import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

import utils


"""
Shows a histogram, probability function (pdf) plot and associated data of a numerical variable's distribution

COMMAND WINDOW ARGUMENTS:

var - a numerical variable to get the distribution for. 

bins - how many intervals to divide data into for histogram - default is 10

outFile - the name of a png file to be created and to save the plot to. 
            Set to 'output.png' file by default.

categoricals - a list of variables in the dataset whose values shall be used as categories to group datapoints of the numerical var into. 
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
    parser.add_argument('bins',
                    nargs='?',
                    type=int,
                    default=10)
    parser.add_argument('-o', '--outFile',
                        nargs='?',
                        default='output.png')
    parser.add_argument('-c', '--categoricals',
                        nargs='*',
                        default=[]),
    parsedArgs = parser.parse_args(args)

    # Check if requested numerical var is valid
    checkVar = utils.checkNumericalVarsRequested(data, [parsedArgs.var])
    if checkVar == -1:
        return 
    
    # Check if specified output file is a png
    checkFile = __checkValidPng(parsedArgs.outFile)
    if checkFile == -1:
        return 

    if parsedArgs.categoricals == []:
        plot = __plotDist(data, parsedArgs.var, parsedArgs.bins)
    else:
        # Check if categorical vars requested are present in data
        if utils.checkValidCategoricals(data, parsedArgs.categoricals) == -1:
            return
        plot = __plotDistByCategoricals(data, parsedArgs.var, parsedArgs.categoricals, parsedArgs.bins)

    # Save plot to png file
    plot.figure.savefig(parsedArgs.outFile)

    # Display saved image
    img = Image.open(parsedArgs.outFile)
    img.show()


"""
Returns a plotted graph showing the probability curghghghnhyuigbtyuve (pdf) and a histogram of a provided pd series.

PARAMETERS:
data - The pandas dataframe holding the data
var - numerical var to get distribution for
bins - number of intervals to divide values into for the histogram
"""
def __plotDist(data, var, bins):
    plot = sns.displot(data=data, kde=True, x=var, bins=bins)
    plot.set_titles(f"Distribution of {var}")
    return plot


"""
Returns a plotted graph showing the probability curves (pdf) and a histograms of categories in a provided pd series.

PARAMETERS:
data - The pandas dataframe holding the data
var - numerical var to get distribution for
categoricals - categorical variable(s) to seperate values of var along
bins - number of intervals to divide values into for the histogram
"""
def __plotDistByCategoricals(data, var, categoricals, bins):
    cutData = data[categoricals+var] # Get only the necessary columns i.e. those for the categoricals and the var, so as to reduce processing time

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
