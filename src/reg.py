import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
from PIL import Image
from scipy import stats

import utils


"""
For an explanatory var and a response var provided by the user, outputs:
- a table including sample estimates and confidence intervals of the linear regression intercept and slope parameters
for the regression model of those two variables
- a seaborn plot including a scatterplot and the fitted regression line
- An ANOVA table

COMMAND WINDOW ARGUMENTS:
x - explanatory variable
y - response variable
lvl - level of confidence (e.g. 0.99 for a 99% CI) for the confidence intervals of regression parameters 
(alpha and beta). Default is 0.95
outFile - the name of a png file to be created (if it does not exist already) and to save the plot to. 
            In the user's command, this is denoted by -o or --outfile. 
            Set to 'output.png' file by default.

FUNCTION PARAMETERS:
data - the input dataframe
args - array of command window argument strings obtained by command interpreter module
"""
def analyze(data, args):

    # Deriving argument values from args array using argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('x', choices=list(data.select_dtypes(include='number').columns))  # Explanatory var
    parser.add_argument('y', choices=list(data.select_dtypes(include='number').columns))  # Response var
    parser.add_argument('lvl',
                        nargs='?',
                        default=0.95,
                        type=float)
    parser.add_argument('-o', '--outfile',
                        nargs='?',
                        default='output.png')
    parsed_args = parser.parse_args(args)

    # Check if specified output file is a png
    if utils.checkValidPng(parsed_args.outfile) == -1:
        return

    parameter_stats = __get_model_param_stats(data, parsed_args.lvl, parsed_args.x, parsed_args.y)
    print(parameter_stats)


"""
Return a dataframe of statistics for the slope(beta) and intercept(alpha) linear regression parameters
For each of these 2 parameters, the dataframe will show:
 - The sample estimates/observed value
 - The lower & upper bound of a confidence interval for the population value of that parameter
 
PARAMETERS:
data - the input dataframe
exp_var - name of explanatory variable (x)
resp_var - name of response variable (y)
cl - level of confidence for confidence interval (e.g. 0.99 for a 99% CI).
"""
def __get_model_param_stats(data, exp_var, resp_var, cl):
    x = data[exp_var]
    y = data[resp_var]
    n = len(data[[exp_var, resp_var]].dropna())  # No. of datapoints where neither exp_var nor resp_var values are missing

    ahat, bhat = np.polyfit(x, y, 1)  # Sample estimates of alpha and beta

    y_pred = ahat + (bhat*x)
    residuals = np.subtract(y, y_pred)
    rss = np.sum(np.square(residuals))  # Residual sum of squares / sum of squared errors
    estimated_error_variance = rss/n-2

    sxx = __sum_of_squares(x)

    # Standard errors of alpha & beta estimates
    se_beta = np.sqrt(estimated_error_variance/sxx)
    se_alpha = np.sqrt(estimated_error_variance * (1/n + (np.mean(x)**2/sxx)))

    t_value = stats.t.ppf(1 - cl / 2, df=n-2)
    alpha_margin_of_err = t_value * se_alpha
    beta_margin_of_err = t_value * se_beta

    ci_alpha = (ahat-alpha_margin_of_err, ahat+alpha_margin_of_err)
    ci_beta = (bhat-beta_margin_of_err, bhat+beta_margin_of_err)

    output = {'estimate': [ahat, bhat],
              f"CI({cl*100}%) lower": [ci_alpha[0], ci_beta[0]],
              f"CI({cl*100}%) upper": [ci_alpha[1], ci_beta[1]]
              }
    return pd.DataFrame(data=output, index=['intercept', 'slope'])


# Calculates the sum of squares of a given series/array
def __sum_of_squares(series):
    mean = np.mean(series)
    squares = series - mean
    return np.sum(squares)
