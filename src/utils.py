import pandas as pd


"""
Checks if a provided CSV file is:
- Existent
- Actually a CSV file

If so, loads the CSV file into a pd dataframe that is then returned. 
If CSV file isn't valid, prints an appropriate error msg then returns an empty dataframe
"""
def checkAndLoadCSVFile(filename):
    
    # If provided file isn't a CSV file
    if filename[-4:] != '.csv':
        print("ERROR: Input file must be a CSV file")
        return pd.DataFrame() # Empty df

    try:
        data = pd.read_csv(filename) # Load file into pd dataframe
        return data
    except FileNotFoundError:
        print("ERROR: File does not exist")
        return pd.DataFrame()


"""
Checks that numerical vars for which data have been requested
- exist in the data
- are actually numerical

Returns 0 if these are true, otherwise prints an appropriate error msg and returns -1
"""
def checkNumericalVarsRequested(data, vars):
    # Check if requested vars are all present in data
    if not set(vars).issubset(data.columns):
        print("ERROR: Specified variable(s) not present in data")
        return -1
    
    # Check if requested vars are numerical by iterating through columns of requested vars
    for i in data[vars]:
        if not pd.api.types.is_numeric_dtype(data[i]):
            print(f"ERROR: Type {i} is not numeric")
            return -1
    
    return 0
        