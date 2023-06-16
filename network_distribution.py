import helpers as hlp 
import argparse
import os
import json 

parser = argparse.ArgumentParser()
parser.add_argument('--path', metavar='-p',
                    help='Path of .csv files')

parser.add_argument('--Log', metavar='-L',
                    help='If logarithm of total degree has to be used for fitting the distrubtion')

parser.add_argument('--pdf', metavar='-P',
                    help='probability density function: one of those in scipy.stats')

parser.add_argument('--out', metavar='-o',
                    help='path to output file')

args = parser.parse_args()

distr = args.pdf
path = args.path
out_path = args.out 
logarithm_degree = args.Log

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

for csv_file in files:
    file_path = os.path.join(path, csv_file)
    data = hlp.obtain_data(file_path,logarithm_degree)
    key = csv_file.split(".")[0]
    parameters[key] = hlp.fitter(data, distr)

with open(output_file_path, "w") as outfile:
    json.dump(parameters, outfile)

    
print(f"The parameters have been obtained successfully.")

