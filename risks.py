import pandas as pd
from utils import get_age, get_yob
import collections
import time

COVID_FILE = r"E:\Data\Covid\patient_with_race_081020.csv"
VOTER_FILE = r"E:\Data\Covid\voterside_filtered_053020.csv"

df_patient = pd.read_csv(COVID_FILE, header=0)

print('Num. of filtered patients: {}'.format(len(df_patient)))

df_patient['yob'] = df_patient.apply(lambda x: get_yob(x['age'], x['event_date']), axis=1)

patient_counts = df_patient.groupby(['county', 'gender', 'yob', 'race'])['patient_serial'].nunique().to_dict() # race

patient_freqs = collections.defaultdict(int)

for k, v in patient_counts.items():

    new_k = (k[0], k[1], k[2] - 1, k[2])

    patient_freqs[new_k] = v

del patient_counts

print(patient_freqs)

df_voter = pd.read_csv(VOTER_FILE, header=0, usecols=['voter_serial', 'county', 'dob', 'gender', 'race'])

print('Num. of filtered voters: {}'.format(len(df_voter)))

df_voter['yob'] = df_voter['dob'].apply(lambda x: int(x[-4:]))

voter_counts = df_voter.groupby(['county', 'gender', 'yob', 'race'])['voter_serial'].nunique().to_dict() # race

voter_freqs = collections.defaultdict(int)

for k, v in voter_counts.items():

    k1 = (k[0], k[1], k[2] - 1, k[2])
    k2 = (k[0], k[1], k[2], k[2] + 1)

    if k1 in patient_freqs:

        voter_freqs[k1] += voter_counts[k]

    if k2 in patient_freqs:

        voter_freqs[k2] += voter_counts[k]

del voter_counts

print(voter_freqs)

sum_marketer_risk = sum([patient_freqs[k]/ voter_freqs[k] for k in patient_freqs if voter_freqs[k] != 0])
sum_patient_counts = sum(patient_freqs[k] for k in patient_freqs if voter_freqs[k] != 0)

print(sum_marketer_risk, sum_marketer_risk / sum_patient_counts)

min_patient_freq = min(patient_freqs.values())

print(min_patient_freq, 1/min_patient_freq)

min_voter_freq = min([v for v in voter_freqs.values() if v !=0])

print(min_voter_freq, 1/min_voter_freq)
