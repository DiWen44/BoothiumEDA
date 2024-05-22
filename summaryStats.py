import argparse
import pandas as pd

"""Prints table of summary stats based on passed command arguments

PARAMETERS:
data - the input dataframe
args - array of command window arguments
"""
def summaryStats(data, args):

    # Getting arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-v','--vars', 
                        nargs='*', 
                        default=list(data.columns.values),
                        help="The variables to analyze")
    parser.add_argument('-s', '--stats',
                        nargs='*',
                        default=['MEAN', 'MEDIAN', 'VAR', 'RANGE'],
                        help="Summary statistics to find")
    parser.add_argument('-c', '--categoricals',
                        nargs='*',
                        default=[],
                        help="Categorical variables along which to seperate data")
    parsedArgs = parser.parse_args(args)

    table = tabulate(data, args.vars, args.stats, args.categoricals)
    print(table)



"""
Find summary statistics for provided numerical variables and tabulates them in a dataframe 
If no categorical variables (to calculate summary statistics for variables of individuals belonging to specific categories) are provided then the 
returned dataframe will have the variables as indices and the summary statistics (e.g mean, mode, variance) as columns.

If categorical variables are provided, then a multiindex of the categorical variables and the numerical variables is used, 
with 1 level of the multiindex for each categorical variables, plus 1 level for the numerical variables. The summary statistics will still be the columns here. 
The number of levels of this multiindex depends on the number of categorical variables provided. For n categorical variables, the multiindex will have n+1 levels (categorical variables + one for the numerical variables)

PARAMETERS:
data- the input dataframe
vars - array of numerical variables to find summary statistics for
stats - array of summary statistics (e.g. mean, variance, mode) to find. 
categoricals - categorical variables in the data to divide entries into categories along, so as to be able to find summary statistics for each category

Vars, stats and categoricals are extracted from command arguments in the summmaryStats function that calls this function.
"""
def tabulate(data, vars, stats, categoricals):
        
        # If no categoricals, then can use single-level index
        if categoricals == []:

            table = pd.DataFrame(index=vars) # Results table - index is numerical variables, columns are summary statistics

            for stat in stats:
                if stat == 'MEAN':
                    means = data.mean(axis=0)[vars] # Pandas series of means for each variable. Use [vars] to only get statistics for requested variables.
                    means.rename('mean') # Rename series so that when joined to dataframe, column has that name
                    table.join(means)

                elif stat == 'MEDIAN':
                    medians = data.median(axis=0)[vars]
                    medians.rename('median')
                    table.join(medians)

                elif stat == 'MIN': 
                    mins = data.min()[vars]
                    mins.rename('min')
                    table.join(mins)

                elif stat == 'MAX': 
                    maxs = data.max()[vars]
                    maxs.rename('max')
                    table.join(maxs)

                elif stat == 'RANGE':
                    ranges = data.max()[vars].sub(data.min()[vars])
                    ranges.rename('range')
                    table.join(ranges)

                elif stat == 'VAR': # Variance
                    variances = data.var(axis=0)[vars] 
                    variances.rename('variance')
                    table.join(variances)

                elif stat == 'STD': # Standard deviation
                    stds = data.std(axis=0)[vars] 
                    stds.rename('STD')
                    table.join(stds)

                elif stat == 'MODE':
                    modes = data.mode(axis=0)[vars] 
                    modes.rename('mode')
                    table.join('mode')

                else:
                    print(f"ERROR: {stat} IS NOT A VALID SUMMARY STATISTIC")
                    return -1
        

        # If categoricals provided, need to use a multiindex
        else:

            indices = [] # multidimensional array from which to create multiindex
            for i in categoricals:
                categories = data[i].unique # Each unique value of categorical variable represents a category
                indices.append(categories)
            indices.append(vars) # Final level of multiindex is for numerical variables

            labels = categoricals.append("numericals") # Labels for each level of the multiindex (names of each categorical variable, plus "numeric" for the numerical variables)
            index = pd.MultiIndex.from_product(indices, names=labels)
            table = pd.DataFrame(index=index)

            
        return table
            

                
