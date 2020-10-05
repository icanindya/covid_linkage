import pandas as pd
from utils import get_yob, get_age

COVID_FILE = r"E:\Data\Covid\patient_with_race_081020.csv"
VOTER_FILE = r"E:\Data\Covid\voterside_filtered_053020.csv"

MATCH_FILE = r'E:\Data\Covid\matched_081020_053020.csv'

MATCH_FILE_RACE = r'E:\Data\Covid\matched_with_race_081020_053020.csv'

EQ_CLASS_SIZE_LIMIT = 10

df_patient = pd.read_csv(COVID_FILE, header=0)
df_patient['yob'] = df_patient.apply(lambda x: get_yob(x['age'], x['event_date']), axis=1)

print('Num. of filtered patients: {}'.format(len(df_patient)))

df_patient_copy = df_patient.copy(deep=True)
df_patient_copy['yob'] = df_patient_copy['yob'].apply(lambda x: x - 1)

df_patient = df_patient.append(df_patient_copy, ignore_index=True)

print('Num. of patients with two YOBs:', len(df_patient))

df_voter = pd.read_csv(VOTER_FILE, header=0)

print('Num. of filtered voters: {}'.format(len(df_voter)))

df_voter['yob'] = df_voter['dob'].apply(lambda x: int(x[-4:]))

# df_voter['filter_key'] = list(zip(df_voter['county'], df_voter['yob'], df_voter['gender'], df_voter['race'])) # race
#
# filter_key_counts = df_voter['filter_key'].value_counts().to_dict()
#
# filtered_keys = [k for k, v in filter_key_counts.items() if v <= EQ_CLASS_SIZE_LIMIT]
#
# df_voter = df_voter.loc[df_voter['filter_key'].isin(filtered_keys)]
#
# print('Num. of voters within small eq class: {}'.format(len(df_voter)))

df_voter = pd.concat([group_df for group, group_df in df_voter.groupby(['county', 'yob', 'gender', 'race']) if len(group_df) <= EQ_CLASS_SIZE_LIMIT])

# for i in range(NUM_SIMULATIONS):

df_joined = pd.merge(df_patient, df_voter, on=['county', 'yob', 'gender', 'race']) # race

print('Intial join size: {}'.format(len(df_joined)))

df_joined['voter_age'] = df_joined.apply(lambda x: get_age(x['dob'], x['event_date']), axis=1)

df_joined = df_joined.loc[df_joined['voter_age'] == df_joined['age']]

print('Intermediate join size: {}'.format(len(df_joined)))

patient_serial_counts = df_joined['patient_serial'].value_counts().to_dict()

filtered_patient_serials = [k for k, v in patient_serial_counts.items() if v <= EQ_CLASS_SIZE_LIMIT]

df_joined = df_joined.loc[df_joined['patient_serial'].isin(filtered_patient_serials)]

print('Num. of unique patients: {}'.format(len(df_joined['patient_serial'].unique())))

print('Num. of unique voters: {}'.format(len(df_joined['voter_serial'].unique())))

patient_counts = df_joined.groupby(['county', 'gender', 'age', 'race', 'event_date'])['patient_serial'].nunique() # race

voter_counts = df_joined.groupby(['county', 'gender', 'age', 'race', 'event_date'])['voter_serial'].nunique() # race

matches = pd.concat([patient_counts, voter_counts], axis=1)

matches.columns = ['patient_counts', 'voter_counts']

matches.reset_index(inplace=True)

print(matches)

matches.to_csv(MATCH_FILE_RACE)

