import argparse
from scipy import stats
import pandas as pd

import utils


def one_sample_ttest(data, args):
    """ Performs a t-test for the population mean of a provided numerical var

    Outputs a pandas series containing:
        - T-Test statistic
        - p-value from test
        - degrees of freedom for the t-distribution.

    COMMAND WINDOW ARGUMENTS:
        var - name of numerical variable to test
        h0 - Expected value of population mean in null hypothesis
        alternative - less than, greater than or 2-sided (defaults to 2-sided)

    FUNCTION PARAMETERS:
        data - the input dataframe
        args - array of command window argument strings obtained by command interpreter module
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('var', choices=utils.get_numericals(data))
    parser.add_argument('h0', type=float)
    parser.add_argument('-a', '--alternative',
                        nargs='?',
                        choices=['less', 'greater', 'two-sided'],
                        default='two-sided')
    parsed_args = parser.parse_args(args)

    res = stats.ttest_1samp(data[parsed_args.var], parsed_args.h0, alternative=parsed_args.alternative)
    __print_result(res)


def two_sample_ttest_by_cat(data, args):
    """ Performs a t-test for the difference in population means of a numerical variable between 2 independent categories
    i.e. Tests the null hypothesis that these 2 categories have the same population means.

    Outputs a pandas series containing:
        - T-Test statistic
        - p-value from test
        - degrees of freedom for the t-distribution.

    COMMAND WINDOW ARGUMENTS:
        var - name of numerical variable to test
        categorical - categorical variable to categorize datapoints into
        c1, c2 - categories (possible values of categorical) to test diff of means between
        alternative - less than, greater than or 2-sided (defaults to 2-sided)

    FUNCTION PARAMETERS:
        data - the input dataframe
        args - array of command window argument strings obtained by command interpreter module
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('var', choices=utils.get_numericals(data))
    parser.add_argument('categorical', choices=data.columns.values)
    parser.add_argument('c1')
    parser.add_argument('c2')
    parser.add_argument('-a', '--alternative',
                        nargs='?',
                        choices=['less', 'greater', 'two-sided'],
                        default='two-sided')
    parsed_args = parser.parse_args(args)

    # Check if provided categories are valid
    possible_categories = data[parsed_args.categorical].unique()
    if parsed_args.c1 not in possible_categories:
        msg = f"invalid choice: {parsed_args.c1} (choose from {possible_categories})"
        action = argparse.Action('c1', 'c1', choices=possible_categories)
        raise argparse.ArgumentError(action, msg)
    elif parsed_args.c2 not in possible_categories:
        msg = f"invalid choice: {parsed_args.c2} (choose from {possible_categories})"
        action = argparse.Action('c1', 'c1', choices=possible_categories)
        raise argparse.ArgumentError(action, msg)

    s1 = data[data[parsed_args.categorical] == parsed_args.c1][parsed_args.var]
    s2 = data[data[parsed_args.categorical] == parsed_args.c2][parsed_args.var]

    # Test for equality of variance first to determine what kind of test scipy will use for diff of means
    eqvar = __equality_of_variances(s1, s2)
    res = stats.ttest_ind(s1, s2, alternative=parsed_args.alternative, equal_var=eqvar)
    __print_result(res)


def two_sample_ttest_by_col(data, args):
    """ Performs a t-test for the difference in population means between 2 (numerical) independent columns of the data

     Outputs a pandas series containing:
        - T-Test statistic
        - p-value from test
        - degrees of freedom for the t-distribution.

    COMMAND WINDOW ARGUMENTS:
        col1, col2 - Name of columns to test
        alternative - less than, greater than or 2-sided (defaults to 2-sided)

    FUNCTION PARAMETERS:
        data - the input dataframe
        args - array of command window argument strings obtained by command interpreter module
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('col1', choices=utils.get_numericals(data))
    parser.add_argument('col2', choices=utils.get_numericals(data))
    parser.add_argument('-a', '--alternative',
                        nargs='?',
                        choices=['less', 'greater', 'two-sided'],
                        default='two-sided')
    parsed_args = parser.parse_args(args)

    s1 = data[parsed_args.col1]
    s2 = data[parsed_args.col2]
    # Test for equality of variance first to determine what kind of test scipy will use for diff of means
    eqvar = __equality_of_variances(s1, s2)
    res = stats.ttest_ind(s1, s2, alternative=parsed_args.alternative, equal_var=eqvar)
    __print_result(res)


def paired_ttest(data, args):
    """ Performs a t-test for the difference in population means between 2 (numerical) paired/related columns

     Outputs a pandas series containing:
        - T-Test statistic
        - p-value from test
        - degrees of freedom for the t-distribution.

    COMMAND WINDOW ARGUMENTS:
        col1, col2 - Name of columns to test
        alternative - less than, greater than or 2-sided (defaults to 2-sided)

    FUNCTION PARAMETERS:
        data - the input dataframe
        args - array of command window argument strings obtained by command interpreter module
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('col1', choices=utils.get_numericals(data))
    parser.add_argument('col2', choices=utils.get_numericals(data))
    parser.add_argument('-a', '--alternative',
                        nargs='?',
                        choices=['less', 'greater', 'two-sided'],
                        default='two-sided')
    parsed_args = parser.parse_args(args)

    s1 = data[parsed_args.col1]
    s2 = data[parsed_args.col2]
    res = stats.ttest_rel(s1, s2, alternative=parsed_args.alternative)
    __print_result(res)


def __equality_of_variances(s1, s2):
    """ Tests equality of variances between 2 series at 10% significance level using Levene's test

    Returns True if variances can be assumed to be equal, otherwise returns false
    
    PARAMETERS:
        s1, s2 - Pandas series to test
    """
    res = stats.levene(s1, s2)
    p = res[0]
    # Use 10% significance level
    if p < 0.1:
        return False
    else:
        return True


def __print_result(res):
    """ When provided a TtestResult object (generated from a stats ttest), tabulates it into a dataframe then prints """
    output = pd.Series(data=[res.statistic, res.pvalue, res.df], index=['T', 'p', 'df'])
    print(output)
