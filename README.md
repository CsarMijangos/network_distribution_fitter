<center><h1> network_distribution_fitter </h1> </center>

This python program fits a distribution provided by the user to 
the total degree or (Log(total_degree)) of the nodes of a network in order
to obtain the distribution's parameters that best fit the data.
The program uses fitter to obtain the best fit. 

**Input:** The path to the .csv files with the information of source, target and weight of the edges of the network.
| **source** | **target** | **w** |
|------------|------------|-------|
| $node_i$   | $node_j$   |$w_{ij}$|


**Output:** A directory with .json file. The keys of this json file are the names of the .csv files of the input and
the value of each key is a tuple with the parameters of the distribution with the best fit for the data. 

The command to run:

**python network_distribution.py --path <path_to_the_directory_with_the_csv_files>**

The complete list of flags that we can pass are:
- --path : [Obligatory argument] The path to the input .csv files
- --Log : [Optional argument] If y is passed, then the data to fit will be Log(total_degree). If the argument is n, then
total_degree is passed to the fitter. Default is y.
- --pdf : [Optional argument] The probability density funtion in scipy format that will be used to fit the data. Default is:
powerlognorm.
- --out :  [Optional argument] The path to the directory for the output directory. Default is the same as --path.


The list of distributions available to the moment is: ["powerlognorm", "beta", "gamma","chi2", "weibull_min"] but this can be extended easily
to the complete list of distributions available in scipy.stats.
