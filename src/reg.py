import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
from scipy import stats

import utils


def analyze(data, args):
    """ For an explanatory var and a response var provided by the user, outputs:
        - A table including sample estimates and confidence intervals of the linear regression intercept and slope parameters
            for the regression fit of those two variables
        - A seaborn plot including a scatterplot and the fitted regression line
        - An ANOVA table

    COMMAND WINDOW ARGUMENTS:
        x - explanatory variable
        y - response variable
        cl - level of confidence (e.g. 0.99 for a 99% CI) for the confidence intervals of regression parameters and to
                be used for the prediction interval shown on the regression plot
                (alpha and beta). Default is 0.95
        outFile - the name of a png file to be created (if it does not exist already) and to save the plot to.
                    In the user's command, this is denoted by -o or --outfile.
                    Set to 'output.png' file by default.

    FUNCTION PARAMETERS:
        data - the input dataframe
        args - array of command window argument strings obtained by command interpreter module
    """

    # Deriving argument values from args array using argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('x', choices=utils.get_numericals(data))  # Explanatory var
    parser.add_argument('y', choices=utils.get_numericals(data))  # Response var
    parser.add_argument('cl',
                        nargs='?',
                        default=0.95,
                        type=float)
    parser.add_argument('-o', '--outfile',
                        nargs='?',
                        default='output.png')
    parsed_args = parser.parse_args(args)

    # Check if specified output file is a png
    if utils.check_valid_png(parsed_args.outfile) == -1:
        return

    parameter_stats = __get_model_param_stats(data, parsed_args.x, parsed_args.y, parsed_args.cl)
    print("PARAMETERS:")
    print(parameter_stats)
    print("\n")

    # Create and show regression plot
    fig = plt.figure()
    plot = sns.regplot(data=data, x=parsed_args.x, y=parsed_args.y, ci=parsed_args.cl*100)
    plot.set_title(f"REGRESSION: {parsed_args.y} AGAINST {parsed_args.x}")
    fig.add_axes(plot)
    fig.savefig(parsed_args.outfile)
    img = Image.open(parsed_args.outfile)
    img.show()

    # ANOVA
    print("ANOVA:")
    anova_table = __anova(data, parsed_args.x, parsed_args.y)
    print(anova_table)

    print("\n")


def __get_model_param_stats(data, exp_var, resp_var, cl):
    """ Return a dataframe of statistics for the slope(beta) and intercept(alpha) linear regression parameters

    For each of these 2 parameters, the dataframe will show:
        - The sample estimates/observed value
        - The lower & upper bound of a confidence interval for the population value of that parameter

    PARAMETERS:
        data - the input dataframe
        exp_var - name of explanatory variable (x)
        resp_var - name of response variable (y)
        cl - level of confidence for confidence interval (e.g. 0.99 for a 99% CI).
    """
    x = data[exp_var]
    y = data[resp_var]
    n = len(data[[exp_var, resp_var]].dropna())  # No. of datapoints where neither exp_var nor resp_var values are missing

    bhat, ahat = np.polyfit(x, y, 1)  # Sample estimates of alpha and beta

    y_pred = ahat + (bhat*x)
    residuals = np.subtract(y, y_pred)
    rss = np.sum(np.square(residuals))  # Residual sum of squares / sum of squared errors
    estimated_error_variance = rss/n-2  # Estimated variance of errors

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
 

def __sum_of_squares(series):
    """Calculates the corrected sum of squares of a given series/array"""
    mean = np.mean(series)
    squares = np.square(series - mean)
    return np.sum(squares)


def __sum_of_prods(s1, s2):
    """Calculates the corrected sum of products of 2 given series/arrays"""
    m1 = np.mean(s1)
    m2 = np.mean(s2)
    products = np.multiply(s1-m1, s2-m2)
    return np.sum(products)


def __anova(data, exp_var, resp_var):
    """
    Prints an ANOVA table for the given data

    This table will show:
        - degrees of freedom (total, regression, residual)
        - sum of squares (total, regression, residual)
        - mean sum of squares (total, regression, residual)
        - FR test statistic and resulting p-value of F-test with that statistic

    PARAMETERS:
        data - the input dataframe
        exp_var - name of explanatory variable (x)
        resp_var - name of response variable (y)
    """
    y = data[resp_var]
    x = data[exp_var]
    n = len(data[[exp_var, resp_var]].dropna())  # No. of datapoints where neither exp_var nor resp_var values are missing

    tss = __sum_of_squares(y)  # TSS = SYY
    regss = __sum_of_prods(x, y)**2 / __sum_of_squares(x)  # Regression SS
    rss = tss - regss  # Residual SS / SSE

    tms = tss / n-1
    regms = regss
    rms = rss/n-2

    fr = regms/rms
    p = stats.f.sf(fr, 1, n-2)

    output = {'df': [1, n-2, n-1],
              'SS': [regss, rss, tss],
              'MS': [regms, rms, tms],
              'FR': [fr],
              'p': [p]}
    return pd.DataFrame(data=output, index=['regression', 'residual', 'total'])
