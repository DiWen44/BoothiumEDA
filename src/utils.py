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
def check_and_load_csv_file(filename):
    
    # If provided file isn't a CSV file
    if filename[-4:] != '.csv':
        print("ERROR: Input file must be a CSV file")
        return pd.DataFrame()  # Empty df

    try:
        data = pd.read_csv(filename)  # Load file into pd dataframe
    except FileNotFoundError:
        print("ERROR: File does not exist")
        return pd.DataFrame()

    return data


# For the provided dataframe "data", returns a list of column names that correspond to numerical columns
def get_numericals(data):
    return list(data.select_dtypes(include='number').columns)


"""
Used to check if user-requested output image file for generated plots is valid
Given the filename, checks if a provided png file is actually a png file.
Returns 0 if file is valid, otherwise prints an error message and returns -1.

NOTE: THIS ONLY CHECKS IF THE FILENAME IS A .png. It does not check that the file exists, as it does not need to 
(if it doesn't exist it will be created by matplotlib when the plots are saved to it)
"""
def check_valid_png(filename):
    if filename[-4:] != '.png':
        print("ERROR: output file must be a .png file")
        return -1 
    return 0
