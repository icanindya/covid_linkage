import csv
import helper
import os
import pandas as pd

FL_EXT_PATH = r'E:\Data\Covid\fl_voters_053020_ext'
LINKAGE_DSB = r'E:\Data\Covid\voterside_053020.csv'

field_names = ['voter_serial', 'fname', 'mname', 'lname', 'gender',
              'dob', 'race', 'add1', 'add2', 'city', 'zip',
              'county', 'party', 'phone', 'email']

df_list = []

for filenname in os.listdir(FL_EXT_PATH):
    csv_path = os.path.join(FL_EXT_PATH, filenname)
    df_list.append(pd.read_csv(csv_path, sep='\t', names=field_names))

df = pd.concat(df_list)

df.to_csv(LINKAGE_DSB, index=False)

print(len(df))




