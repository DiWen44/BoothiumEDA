import pandas as pd


"""
Checks if a provided CSV file is:
- Existent
- Actually a CSV file

If so, loads the CSV file into a pd dataframe that is then returned. 
If CSV file isn't valid, prints an appropriate error msg then returns an empty dataframe.

PARAMETERS:
filename - name of requested csv file
"""
def checkAndLoadCSVFile(filename):
    
    # If provided file isn't a CSV file
    if filename[-4:] != '.csv':
        print("ERROR: Input file must be a CSV file")
        return pd.DataFrame() # Empty df

    try:
        data = pd.read_csv(filename) # Load file into pd dataframe
    except FileNotFoundError:
        print("ERROR: File does not exist")
        return pd.DataFrame()

    return data


"""
Checks that numerical vars for which data have been requested
- exist in the data
- are actually numerical

Returns 0 if these are true, otherwise prints error msg and returns -1.

PARAMETERS:
data - the input dataframe
vars - array of strings for the numerical variables
"""
def checkNumericalVarsRequested(data, vars):
    # Check if requested vars are all present in data
    if not set(vars).issubset(data.columns):
        print("ERROR: Specified variable(s) not present in data")
        return -1
    
    # Check if requested vars are numerical by iterating through columns of requested vars
    for i in data[vars]:
        if not pd.api.types.is_numeric_dtype(data[i]):
            print(f"ERROR: Variable {i} is not numeric")
            return -1
    
    return 0
        

"""
Checks if requested categorical vars are present in the data.
Returns 0 if valid, otherwise prints error msg and returns -1.

PARAMETERS:
data - the input dataframe
categoricals - array of strings for the categorical variables
"""
def checkValidCategoricals(data, categoricals):
    if not set(categoricals).issubset(data.columns):
        print("ERROR: Specified categorical variable(s) not present in data")
        return -1
    return 0