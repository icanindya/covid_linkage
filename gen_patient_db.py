import random
from county_race_stat import racial_weights
from data import county_dict
import pandas as pd

COVID_FILE = r"E:\Data\Covid\Florida_COVID19_Case_Line_Data_120720.csv"
COVID_FILE_RACE = r"E:\Data\Covid\patient_with_race_120720.csv"

df_patient = pd.read_csv(COVID_FILE, header=0, usecols=['ObjectId', 'County', 'Age', 'Gender',
                                                        'EventDate', 'Jurisdiction', 'Hospitalized'])
df_patient.rename(columns={'ObjectId': 'patient_serial',
                           'County': 'county',
                           'Age': 'age',
                           'Gender': 'gender',
                           'EventDate': 'event_date',
                           'Jurisdiction': 'jurisdiction',
                           'Hospitalized': 'hospitalized'}, inplace=True)
print('Num. of patients: {}'.format(len(df_patient)))

df_patient.dropna(inplace=True)

df_patient['age'] = df_patient['age'].apply(int)
df_patient = df_patient.loc[(df_patient['county'] != 'Unknown') &
                            (df_patient['age'] >= 0) &
                            (df_patient['gender'] != 'Unknown') &
                            (df_patient['jurisdiction'] == 'FL resident')]

df_patient['event_date'] = df_patient['event_date'].apply(lambda x: x[:10])
df_patient['county'] = df_patient['county'].apply(lambda x: county_dict[x])
df_patient['gender'] = df_patient['gender'].apply(lambda x: x[0])
df_patient['race'] = df_patient['county'].apply(lambda x: random.choices([1,2,3,4,5], weights=racial_weights[x], k=1)[0])

df_patient.to_csv(COVID_FILE_RACE, index=False)

print('Num. of filtered patients:', len(df_patient))