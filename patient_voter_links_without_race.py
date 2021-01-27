import random

import pandas as pd

from county_race_stat import racial_weights
from utils import get_yob, get_age

COVID_FILE = r"E:\Data\Covid\patient_with_race_120720.csv"
VOTER_FILE = r"E:\Data\Covid\voterside_filtered_053020.csv"

MATCH_FILE = r'E:\Data\Covid\matched_120720_053020.csv'
MATCH_FILE_RACE = r'E:\Data\Covid\Results\matched_{}_120720_053020.csv'

RESULT_FILE = r"E:\Data\Covid\Results\result_{}_120720_053020.txt"

NUM_SIMULATIONS = 100

df_patient = pd.read_csv(COVID_FILE, header=0)
df_patient['yob'] = df_patient.apply(lambda x: get_yob(x['age'], x['event_date']), axis=1)

print('Num. of filtered patients: {}'.format(len(df_patient)))

df_voter = pd.read_csv(VOTER_FILE, header=0)

print('Num. of filtered voters: {}'.format(len(df_voter)))

df_voter['yob'] = df_voter['dob'].apply(lambda x: int(x[-4:]))

for eq_class_limit in [1, 3, 5, 10, 15, 20]:

    with open(RESULT_FILE.format(eq_class_limit), 'w') as wf:

        wf.write('eq_class_limit,i,num_patients,num_voters,num_links,num_patients_nto1,num_patients_1to1\n')

        df_voter_filtered = pd.concat([group_df for group, group_df in df_voter.groupby(['county', 'yob', 'gender'])
                              if len(group_df) <= eq_class_limit])

        df_patient_copy = df_patient.copy(deep=True)
        df_patient_copy['yob'] = df_patient_copy['yob'].apply(lambda x: x - 1)

        df_patient_double = df_patient.append(df_patient_copy, ignore_index=True)

        print('Num. of patients with two YOBs:', len(df_patient_double))

        df_joined = pd.merge(df_patient_double, df_voter_filtered, on=['county', 'yob', 'gender'])  # race

        # print('Initial join size: {}'.format(len(df_joined)))

        df_joined['voter_age'] = df_joined.apply(lambda x: get_age(x['dob'], x['event_date']), axis=1)

        df_joined = df_joined.loc[df_joined['voter_age'] == df_joined['age']]

        # print('Intermediate join size: {}'.format(len(df_joined)))

        patient_serial_counts = df_joined['patient_serial'].value_counts().to_dict()

        filtered_patient_serials = [k for k, v in patient_serial_counts.items() if v <= eq_class_limit]

        df_joined = df_joined.loc[df_joined['patient_serial'].isin(filtered_patient_serials)]

        voter_serial_counts = df_joined['voter_serial'].value_counts().to_dict()

        num_links = len(df_joined)

        unique_patients = df_joined['patient_serial'].unique()

        num_unique_patients = len(unique_patients)

        unique_voters = df_joined['voter_serial'].unique()

        num_unique_voters = len(unique_voters)

        exclusively_linked_patients =  [k for k, v in patient_serial_counts.items() if v == 1]

        exclusively_linked_voters =  [k for k, v in voter_serial_counts.items() if v == 1]

        df_joined_nto1 = df_joined.loc[df_joined['patient_serial'].isin(exclusively_linked_patients)]

        num_unique_patients_nto1 = len(df_joined_nto1['patient_serial'].unique())

        df_joined_1to1 = df_joined.loc[(df_joined['voter_serial'].isin(exclusively_linked_voters)) &
                                       (df_joined['patient_serial'].isin(exclusively_linked_patients))]

        num_unique_patients_1to1 = len(df_joined_1to1['patient_serial'].unique())

        patient_counts = df_joined.groupby(['county', 'gender', 'age', 'event_date'])[
            'patient_serial'].nunique()  # race

        voter_counts = df_joined.groupby(['county', 'gender', 'age', 'event_date'])[
            'voter_serial'].nunique()  # race

        matches = pd.concat([patient_counts, voter_counts], axis=1)

        matches.reset_index(inplace=True)

        matches.columns = ['county', 'gender', 'age', 'event_date'] + ['patient_counts', 'voter_counts']

        # print(matches)

        matches.to_csv(MATCH_FILE_RACE.format(eq_class_limit), index=False)

        print(eq_class_limit, num_unique_patients, num_unique_voters, num_links, num_unique_patients_nto1,
              num_unique_patients_1to1)

        wf.write('{}, {}, {}, {}, {}, {}\n'.format(
            eq_class_limit,
            num_unique_patients,
            num_unique_voters,
            num_links,
            num_unique_patients_nto1,
            num_unique_patients_1to1))

        wf.flush()



