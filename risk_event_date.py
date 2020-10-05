import pandas as pd
from utils import get_age, get_yob
import collections
import time

COVID_FILE = r"E:\Data\Covid\patient_with_race_081020.csv"
VOTER_FILE = r"E:\Data\Covid\voterside_filtered_053020.csv"

df_voter = pd.read_csv(VOTER_FILE, header=0, usecols=['voter_serial', 'county', 'dob', 'gender', 'race'])

print('Num. of filtered voters: {}'.format(len(df_voter)))

df_voter['yob'] = df_voter['dob'].apply(lambda x: int(x[-4:]))

voter_group_freq = collections.defaultdict(int)

for group, df_group in df_voter.groupby(['county', 'gender', 'race']):

    print(group, len(df_group))

    voter_group_freq[group] = len(df_group)

voter_group_total_freq = len(df_voter)

df_patient = pd.read_csv(COVID_FILE, header=0)

print('Num. of filtered patients: {}'.format(len(df_patient)))

group_risk_dict = collections.defaultdict(float)

num_dates = 0

for date, df_date in df_patient.groupby('event_date'):

    num_dates += 1

    for group, df_group in df_date.groupby(['county', 'gender', 'race']):

        if voter_group_freq[group] == 0:

            continue

        patient_group_freq = len(df_group)

        group_risk_dict += min(1, len(patient_group_freq) / len(voter_group_freq))

tot_risk = 0

for group in group_risk_dict:

    group_risk_dict

