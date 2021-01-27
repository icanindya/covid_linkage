import pandas as pd
from utils import get_age, get_yob
import collections
import datetime
import numpy as np
import matplotlib.pyplot as plt

use_race = False

COVID_FILE = r"E:\Data\Covid\patient_with_race_120720.csv"
VOTER_FILE = r"E:\Data\Covid\voterside_filtered_053020.csv"

risks = []

df_patient = pd.read_csv(COVID_FILE, header=0)

df_patient['week'] = df_patient['event_date'].apply(lambda x: datetime.datetime.strptime(x, '%Y/%m/%d').date().isocalendar()[1])

print('Num. of filtered patients: {}'.format(len(df_patient)))

df_patient['yob'] = df_patient.apply(lambda x: get_yob(x['age'], x['event_date']), axis=1)

df_voter = pd.read_csv(VOTER_FILE, header=0, usecols=['voter_serial', 'county', 'dob', 'gender', 'race'])

print('Num. of filtered voters: {}'.format(len(df_voter)))

df_voter['yob'] = df_voter['dob'].apply(lambda x: int(x[-4:]))

for use_race in [False, True]:

    risks = []

    for week in [10, 20, 30, 40, 49]:

        df_patient_week = df_patient.loc[df_patient['week'] <= week]

        if use_race:
            equivalence_class_attrs = ['county', 'gender', 'race', 'yob']
        else:
            equivalence_class_attrs = ['county', 'gender', 'yob']

        patient_counts = df_patient_week.groupby(equivalence_class_attrs)['patient_serial'].nunique().to_dict() # race

        patient_freqs = collections.defaultdict(int)

        for k, v in patient_counts.items():

            if use_race:
                new_k = (k[0], k[1], k[2], k[3] - 1, k[3])
            else:
                new_k = (k[0], k[1], k[2] - 1, k[2])

            patient_freqs[new_k] = v

        del patient_counts

        # print(patient_freqs)

        voter_counts = df_voter.groupby(equivalence_class_attrs)['voter_serial'].nunique().to_dict() # race

        voter_freqs = collections.defaultdict(int)

        for k, v in voter_counts.items():

            if use_race:

                k1 = (k[0], k[1], k[2], k[3] - 1, k[3])
                k2 = (k[0], k[1], k[2], k[3], k[3] + 1)

            else:

                k1 = (k[0], k[1], k[2] - 1, k[2])
                k2 = (k[0], k[1], k[2], k[2] + 1)

            if k1 in patient_freqs:

                voter_freqs[k1] += voter_counts[k]

            if k2 in patient_freqs:

                voter_freqs[k2] += voter_counts[k]

        del voter_counts

        # print(voter_freqs)

        sum_marketer_risk = sum([patient_freqs[k]/ voter_freqs[k] for k in patient_freqs if voter_freqs[k] != 0])
        sum_patient_freq = sum(patient_freqs[k] for k in patient_freqs if voter_freqs[k] != 0)

        marketer_risk = sum_marketer_risk / sum_patient_freq

        risks.append(marketer_risk)

        print('marketer_risk:', marketer_risk)

    weeks = [10, 20, 30, 40, 49]
    x_pos = np.arange(len(weeks))

    plt.bar(x_pos, risks, align='center', alpha=0.5)
    plt.xticks(x_pos, weeks)
    plt.xlabel('Week')
    plt.ylabel('Risk')

    if use_race:
        plt.title('Marketer Risk (with race)')
    else:
        plt.title('Marketer Risk (without race)')

    plt.show()

    # plt.savefig('marketer_risks_race_{}.png'.format(use_race), bbox_inches='tight')