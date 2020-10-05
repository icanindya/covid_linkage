import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import collections
import time

COVID_FILE = r"E:\Data\Covid\Florida_COVID19_Case_Line_Data_081020.csv"
VOTER_FILE = r"E:\Data\Covid\voterside_053020.csv"
VOTER_FILTERED_FILE = r"E:\Data\Covid\voterside_filtered_053020.csv"
MATCH_FILE = r'E:\Data\Covid\matched_081020_053020.csv'

county_dict = {'Alachua': 'ALA',
               'Baker': 'BAK',
               'Bay': 'BAY',
               'Bradford': 'BRA',
               'Brevard': 'BRE',
               'Broward': 'BRO',
               'Calhoun': 'CAL',
               'Charlotte': 'CHA',
               'Citrus': 'CIT',
               'Clay': 'CLA',
               'Collier': 'CLL',
               'Columbia': 'CLM',
               'Dade': 'DAD',
               'Desoto': 'DES',
               'Dixie': 'DIX',
               'Duval': 'DUV',
               'Escambia': 'ESC',
               'Flagler': 'FLA',
               'Franklin': 'FRA',
               'Gadsden': 'GAD',
               'Gilchrist': 'GIL',
               'Glades': 'GLA',
               'Gulf': 'GUL',
               'Hamilton': 'HAM',
               'Hardee': 'HAR',
               'Hendry': 'HEN',
               'Hernando': 'HER',
               'Highlands': 'HIG',
               'Hillsborough': 'HIL',
               'Holmes': 'HOL',
               'Indian River': 'IND',
               'Jackson': 'JAC',
               'Jefferson': 'JEF',
               'Lafayette': 'LAF',
               'Lake': 'LAK',
               'Lee': 'LEE',
               'Leon': 'LEO',
               'Levy': 'LEV',
               'Liberty': 'LIB',
               'Madison': 'MAD',
               'Manatee': 'MAN',
               'Marion': 'MRN',
               'Martin': 'MRT',
               'Monroe': 'MON',
               'Nassau': 'NAS',
               'Okaloosa': 'OKA',
               'Okeechobee': 'OKE',
               'Orange': 'ORA',
               'Osceola': 'OSC',
               'Palm Beach': 'PAL',
               'Pasco': 'PAS',
               'Pinellas': 'PIN',
               'Polk': 'POL',
               'Putnam': 'PUT',
               'Santa Rosa': 'SAN',
               'Sarasota': 'SAR',
               'Seminole': 'SEM',
               'St. Johns': 'STJ',
               'St. Lucie': 'STL',
               'Sumter': 'SUM',
               'Suwannee': 'SUW',
               'Taylor': 'TAY',
               'Union': 'UNI',
               'Volusia': 'VOL',
               'Wakulla': 'WAK',
               'Walton': 'WAL',
               'Washington': 'WAS'}

def get_yob(age, event_date):
    event_datetime = datetime.strptime(event_date[:-3], '%Y/%m/%d %H:%M:%S')
    birth_datetime = event_datetime - relativedelta(years=age)
    return birth_datetime.year

def get_age(dob, event_date):
    dob_datetime = datetime.strptime(dob, '%m/%d/%Y')
    event_datetime = datetime.strptime(event_date[:-3], '%Y/%m/%d %H:%M:%S')

    return event_datetime.year - dob_datetime.year - \
           ((event_datetime.month, event_datetime.day) < (dob_datetime.month, dob_datetime.day))

df_patient = pd.read_csv(COVID_FILE, header=0, usecols=['ObjectId', 'County', 'Age', 'Gender',
                                                        'EventDate', 'Jurisdiction'])
df_patient.rename(columns={'ObjectId': 'patient_serial',
                           'County': 'county',
                           'Age': 'age',
                           'Gender': 'gender',
                           'EventDate': 'event_date',
                           'Jurisdiction': 'jurisdiction'}, inplace=True)
print('Num. of patients: {}'.format(len(df_patient)))

df_patient.dropna(inplace=True)

print('Num. of filtered patients: {}'.format(len(df_patient)))

df_patient['age'] = df_patient['age'].apply(int)
df_patient = df_patient.loc[(df_patient['county'] != 'Unknown') &
                            (df_patient['age'] >= 0) &
                            (df_patient['gender'] != 'Unknown') &
                            (df_patient['jurisdiction'] == 'FL resident')]

df_patient['county'] = df_patient['county'].apply(lambda x: county_dict[x])
df_patient['yob'] = df_patient.apply(lambda x: get_yob(x['age'], x['event_date']), axis=1)
df_patient['gender'] = df_patient['gender'].apply(lambda x: x[0])

patient_freqs = df_patient.groupby(['county', 'gender', 'age'])['patient_serial'].nunique().to_dict()

# patient_freqs = collections.defaultdict(int)

# for k, v in patient_counts.items():
#
#     new_k = (k[0], k[1], k[2] - 1, k[2])
#
#     patient_freqs[new_k] = v
#
# del patient_counts

print(patient_freqs)

df_voter = pd.read_csv(VOTER_FILE, header=0, usecols=['voter_serial', 'county', 'dob', 'gender', 'phone', 'email'])

print('Num. of voters: {}'.format(len(df_voter)))

df_voter.dropna(subset=['county', 'dob', 'gender'], how='any', inplace=True)

print('Num. of filtered voters: {}'.format(len(df_voter)))

df_voter['yob'] = df_voter['dob'].apply(lambda x: int(x[-4:]))

voter_counts = df_voter.groupby(['county', 'gender', 'yob'])['voter_serial'].nunique().to_dict()

voter_freqs = collections.defaultdict(int)

for k, v in voter_counts.items():

    k1 = (k[0], k[1], 2020 - k[2] - 1)
    k2 = (k[0], k[1], 2020 - k[2])

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

