import helpers as hlp 
import argparse
import os
import json 
from multiprocessing import Pool


parser = argparse.ArgumentParser()
parser.add_argument('--path', metavar='-p',
                    help='Path of .csv files')

parser.add_argument("--cores", metavar="-c",
                    help="number of cores to be used")

parser.add_argument('--Log', metavar='-L',
                    help='If logarithm of total degree has to be used for fitting the distrubtion')

parser.add_argument('--pdf', metavar='-P',
                    help='probability density function: one of those in scipy.stats')

parser.add_argument('--out', metavar='-o',
                    help='path to output file')

args = parser.parse_args()

cores = args.cores
distr = args.pdf
path = args.path
out_path = args.out 
logarithm_degree = args.Log

total_cores = os.cpu_count()

if cores>total_cores:
    print(f"Total number of present cores {total_cores} is less than {cores}")
    exit()

if logarithm_degree == None:
    logarithm_degree = True
elif logarithm_degree in ["y","Y", "yes", "Yes"]:
    logarithm_degree = True
elif logarithm_degree in ["n", "N", "no", "No"]:
    logarithm_degree = False
else:
    print("Not a valid option for Log")
    exit()

if distr == None:
    distr = "powerlognorm"

if distr not in hlp.DISTRIBUTIONS:
    print("Not a valid distribution")
    exit()

if path == None: 
    print("path is an obligatory parameter")
    exit()


if out_path == None:
    out_path = os.path.join(path, "output")


files = [x for x in os.listdir(path) if x.endswith(".csv")]

parameters = dict()
#Crear carpeta de salida:
try:
    os.makedirs(out_path, exist_ok= True)
    print(f"Directory {out_path} created successfully")
except OSError as error:
    print(f"Directory {out_path} can not be created")
    exit()

 if logarithm_degree:
     output_file_path = os.path.join(out_path, distr+"_parameters_Log_total_degree.json")
 else:
     output_file_path = os.path.join(out_path, distr+"_parameters_total_degree.json")

list_of_file_paths = [os.path.join(path, x) for x in files]
work_data = tuple([[x, logarithm_degree, distr] for x in list_of_file_paths])


def obtain_parameter_dictionary(list_args):
    """Funtion to obtain and write the parameters in 
    output file of one of the inputs .csv.
    """
    data = hlp.obtain_data(list_args[0], list_args[1])
    key = list_args[0].split("/")[-1].split(".")[0]
    global parameters
    parameters[key] = hlp.fitter(data, list_args[2])


def pool_handler():
    p = Pool(cores)
    p.map(obtain_parameter_dictionary, work_data)

pool_handler()
# for csv_file in files:
#     file_path = os.path.join(path, csv_file)
#     data = hlp.obtain_data(file_path,logarithm_degree)
#     key = csv_file.split(".")[0]
#     parameters[key] = hlp.fitter(data, distr)

with open(output_file_path, "w") as outfile:
    json.dump(parameters, outfile)

    
print(f"The parameters have been obtained successfully.")
