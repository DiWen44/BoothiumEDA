import argparse
import pandas as pd


"""
Prints table of summary stats based on passed command arguments

PARAMETERS:
data - the input dataframe
args - array of command window arguments
"""
def summaryStats(data, args):

    # Getting arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-v','--vars', 
                        nargs='*', 
                        default=list(data.select_dtypes(include='number').columns) , # Default value is all numerical variables in the dataset, so the names of the numerical columns in the dataframe
                        help="The variables to analyze")
    parser.add_argument('-s', '--stats',
                        nargs='*', 
                        default=['mean', 'median', 'var'],
                        help="Summary statistics to find")
    parser.add_argument('-c', '--categoricals',
                        nargs='*',
                        default=[],
                        help="Categorical variables along which to seperate data")
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
        
    # Check if requested summary stats are valid
    validStats = ['mean', 'median', 'mode', 'count', 'sum', 'std', 'var', 'min', 'max']
    for i in parsedArgs.stats:
        if i not in validStats:
            print(f"ERROR: {i} is not a valid summary statistic")
            return

    if parsedArgs.categoricals == []:
        table = tabulate(data, parsedArgs.vars, parsedArgs.stats)  
    else:
        # Check if categorical vars requested are present in data
        if not set(parsedArgs.categoricals).issubset(data.columns):
            print("ERROR: Specified categorical variable(s) not present in data")
            return
        table = tabulateByCategoricals(data, parsedArgs.vars, parsedArgs.stats, parsedArgs.categoricals)

    print(table)


"""
Find summary statistics for provided numerical variables and tabulates them in a dataframe 
This dataframe will have the numerical variables as columns and their corresponding summary statistics (e.g mean, mode, variance) as indices.
Returns the new tabulated summary stats as a dataframe.

PARAMETERS:
data- the input dataframe
vars - array of numerical variables to find summary statistics for
stats - array of summary statistics (e.g. mean, variance, mode) to find. 

TO GROUP SUMMARY STATISTICS FOR NUMERICAL VARIABLES BY CATEGORIES SPECIFIED BY CATEGORICAL VARIABLES IN THE DATA, USE tabulateByCategoricals()
"""
def tabulate(data, vars, stats):
    table = data[vars].agg(stats)
    return table
            
                
"""
Divides provided numerical variables into categories based on provided categorical variables, finds summary statistics for the numerical vars,
and tabulates them in a dataframe.
Returns the new tabulated summary stats as a dataframe

For the index of the returned dataframe, a multiindex of the categorical variables and the numerical variables is used, 
with 1 level of the multiindex for each categorical variables, plus 1 level for the numerical variables. The summary statistics will be the columns here. 
The number of levels of this multiindex depends on the number of categorical variables provided. For n categorical variables, the multiindex will have n+1 levels (categorical variables + one for the numerical variables)

PARAMETERS:
data- the input dataframe
vars - array of numerical variables to find summary statistics for
stats - array of summary statistics (e.g. mean, variance, mode) to find. 
categoricals - categorical variables in the data to divide entries into categories along, so as to be able to find summary statistics for each category.
"""
def tabulateByCategoricals(data, vars, stats, categoricals):
    table = (data.groupby(categoricals))[vars].agg(stats)
    return table