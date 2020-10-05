import pandas as pd
import random
from data import county_dict

COVID_FILE = r"E:\Data\Covid\Florida_COVID19_Case_Line_Data_081020.csv"

patient_df = pd.read_csv(COVID_FILE, header=0)

patient_df['race'] = patient_df['county'].apply(lambda x: random.choices([1,2,3,4,5], racial_weights[county_dict[x]], 1)[0])
