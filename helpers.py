import numpy as np
import scipy as sci
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fitter import Fitter
from scipy.stats import *

DISTRIBUTIONS = ["powerlognorm", "beta", "gamma","chi2"]

def fitter(data, distrib="powerlognorm"):
    ''' This function returns a tuple with the parameters of the distrib
    that best fits the data. 
    '''

    fi = Fitter(data, distributions=[distrib])
    
    fi.fit()
    return fi.fitted_param[distrib]

def obtain_data(csv_file, log_degree = True):
    """ This function returns a series with the total degree of the
    agebs in the csv files.
    """
    
    df = pd.read_csv(csv_file)

    df_exgrados = df["source"].value_counts().to_frame(name="ex_grade")
    df_exgrados.reset_index(inplace=True)
    df_exgrados.rename(columns={"index": "agebs_ids"},inplace=True)

    df_ingrados = df["target"].value_counts().to_frame(name="in_grade")
    df_ingrados.reset_index(inplace=True)
    df_ingrados.rename(columns={"index": "agebs_ids"},inplace=True)

    df_grados = df_ingrados.merge(df_exgrados, on="agebs_ids", how="left")
    df_grados.fillna(0,inplace=True)
    df_grados["ex_grade"] = df_grados["ex_grade"].astype("int32")
    df_grados["total_degree"] = df_grados.sum(axis=1)

    df_grados["Log(total_degree)"] = np.log(df_grados["total_degree"])

    if log_degree == True:
        return df_grados["Log(total_degree)"]
    else:
        return df_grados["total_degree"]

