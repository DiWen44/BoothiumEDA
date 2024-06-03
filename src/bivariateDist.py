import argparse
import seaborn as sns
from PIL import Image

import utils


def show_dist(data, args):
    """ Shows a plot of the joint/bivariate distribution of 2 numerical variables.
    If categoricals are provided, then categorizes the datapoints and shows multiple of these distribution plots.

    COMMAND WINDOW ARGUMENTS:

        v1, v2 - numerical variables to get the joint distribution for.

        type - type of plot to generate, 'gaussian' or 'heatmap'.

        outFile - the name of a png file to be created (if it does not exist already) and to save the plot to.
                    In the user's command, this is denoted by -o or --outfile.
                    Set to 'output.png' file by default.

        categoricals - a list of variables in the dataset whose values shall be used  to categorize datapoints.
        The distribution plots will then be shown for each category, rather than the dataset as a whole. Denoted in user command by -c or --categoricals.
        If no categoricals are provided, no categorization will take place and the distribution will be shown for the dataset holistically.
        By default, the categoricals list will be empty.

    FUNCTION PARAMETERS:
        data - the input dataframe
        args - array of command window argument strings obtained by command interpreter module
    """

    # Deriving argument values from args array using argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('v1', choices=utils.get_numericals(data))
    parser.add_argument('v2', choices=utils.get_numericals(data))
    parser.add_argument('type', 
                        nargs='?', 
                        choices=('heatmap', 'gaussian'), 
                        default='heatmap')
    parser.add_argument('-o', '--outfile',
                        nargs='?',
                        default='output.png')
    parser.add_argument('-c', '--categoricals',
                        nargs='*',
                        default=[],
                        choices=data.columns.values)
    parsed_args = parser.parse_args(args)
    
    # Check if specified output file is a png
    if utils.check_valid_png(parsed_args.outfile) == -1:
        return 
    
    if parsed_args.categoricals == []:
        plot = __plot_dist(data, parsed_args.v1, parsed_args.v2, parsed_args.type)
    else:
        plot = __plot_dist_by_categoricals(data, parsed_args.v1, parsed_args.v2, parsed_args.type, parsed_args.categoricals)

    # Save plot to png file
    plot.figure.savefig(parsed_args.outfile)

    # Display saved image
    img = Image.open(parsed_args.outfile)
    img.show()


def __plot_dist(data, v1, v2, plot_type):
    """ Returns a seaborn FacetGrid with a single plot of a bivariate distribution of 2 numerical vars.

    PARAMETERS:
        data - The pandas dataframe holding the data
        v1, v2 - numerical vars to get bivariate distribution for
        plot_type - type of plot to generate, 'gaussian' or 'heatmap'.
    """
    kind = 'kde' if (plot_type == 'gaussian') else 'hist'  # Determine "kind" parameter for displot
    plot = sns.displot(data=data, x=v1, y=v2, kind=kind)
    plot.set_titles(f"DISTRIBUTION OF {v1}, {v2}")
    return plot


def __plot_dist_by_categoricals(data, v1, v2, plot_type, categoricals):
    """ Returns a seaborn FacetGrid containing a series of plots of bivariate distributions, with each plot corresponding to a category.

    PARAMETERS:
        data - The pandas dataframe holding the data
        v1, v2 - numerical vars to get bivariate distribution for
        plot_type - type of plot to generate, 'gaussian' or 'heatmap'
        categoricals - categorical variable(s) to categorize values of var along
    """

    kind = 'kde' if (plot_type == 'gaussian') else 'hist'

    if len(categoricals) > 1:  # If more than 1 category requested
        plot_data = data.set_index(categoricals)  # Make index of plot data a multiindex of the categoricals
        # Since inplace=True is not passed to set_index(), this does not change the index of the original data df.

        plot_data.index = ['_'.join(row) for row in plot_data.index.values]  # Fuses plot_data's multiindex of categoricals into a single index
        plot = sns.displot(data=data, x=v1, y=v2, kind=kind, col=plot_data.index.values, col_wrap=3)
    else:
        plot = sns.displot(data=data, x=v1, y=v2, kind=kind, col=categoricals[0], col_wrap=3)
    
    plot.figure.subplots_adjust(top=0.9)
    plot.figure.suptitle(f"DISTRIBUTION OF {v1}, {v2} BY {categoricals}")
    return plot
