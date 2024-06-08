# BoothiumEDA

BoothiumEDA is a command-line tool for simple EDA.

## Requirements

Python 3.11 or above, and the following python libraries:
- pandas
- numpy
- scipy
- matplotlib
- seaborn

## Usage

### Getting Started

First, download the code from this repository.

To open the command loop for this tool, type the following into the shell:
`python [PATH OF BOOTHIUMEDA FOLDER]/src/main.py [PATH OF FILE TO OPEN]`
 
Note that the path of the file to open must be the absolute path (i.e path relative to the root directory), rather than a relative path.


### Summary Statistics
`summary [-v/--vars] [-s/--stats] [-c/--categoricals]`
- `-v/--vars`             List of numerical variables to get summary statistics for (default: all numerical vars in data).
- `-s/--stats`            List of summary stats to get (default: mean, median, variance).
- `c/--categoricals`      List of categorical variables to categorize datapoints on (default: None). No categorization if none provided.


### Confidence Intervals
`ci [lvl] [-v/--vars] [-c/--categoricals]`
- `lvl`                   Level of confidence for intervals (e.g. 0.99 for a 99% CI). Default is 0.95.
- `-v/--vars`             List of numerical variables to get summary statistics for (default: all numerical vars in data).
- `-c/--categoricals`     List of categorical variables to categorize datapoints on (empty by default). No categorization if none provided.


### Distribution

#### Univariate Distribution
`dist [U/univ] [var] [-o/--outfile] [-c/--categoricals]`
- `var`                   Numerical variable to show dist for
- `-o/--outfile`          Name of .png file to save outputted plot image to, if so desired
- `-c/--categoricals`     List of categorical variables to categorize datapoints on (default: None). No categorization if none provided

#### Bivariate Distribution
`dist [B/biv] [v1] [v2] [plot_type] [-o/--outfile] [-c/--categoricals]`
- `v1, v2`                Numerical variables to show dist for
- `plot_type`             Type of plot to generate, 'gaussian' or 'heatmap' (default: 'heatmap')
- `-o/--outfile`          Name of .png file to save outputted plot image to, if so desired
- `-c/--categoricals`     List of categorical variables to categorize datapoints on (default: None). No categorization if none provided


### Simple Linear Regression
`reg [x] [y] [cl] [-o/--outfile]")`
- `x`               Explanatory variable.
- `y`               Response variable.
- `cl`              Level of confidence for intervals (e.g. 0.99 for a 99% CI). Default is 0.95.
- `-o/--outfile`    Name of .png file to save outputted plot image to, if so desired.


### Hypothesis Testing

#### 1-sample T-Test
`test 1samp [var] [h0] [alternative]`
- `var`                   Numerical variable to test")
- `h0`                    Value of population mean according to null hypothesis")
- `alternative`           'less', 'greater', or 'two-sided' (defaults to 'two-sided')")

#### Difference of means T-Test for 2 (independent) categories
`test 2samp_cat [var] [categorical] [c1] [c2] [alternative]`
- `var`                    Numerical variable to test")
- `categorical`            Categorical variable")
- `c1,c2`                  Categories of categorical variable to test diff. of means between")
- `alternative`            'less', 'greater', or 'two-sided' (defaults to 'two-sided')")

#### Difference of means T-Test for 2 (independent) columns/variables
`test paired [col1] [col2] [alternative]`
- `col1,col2`               PAIRED/RELATED Numerical columns/variables to test
- `alternative`            'less', 'greater', or 'two-sided' (defaults to 'two-sided')

#### Paired/Related difference of means T-Test
`test paired [col1] [col2] [alternative]`
- `col1,col2`               PAIRED/RELATED Numerical columns/variables to test
- `alternative`            'less', 'greater', or 'two-sided' (defaults to 'two-sided')