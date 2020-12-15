import pandas as pd
import datetime
import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

COVID_FILE = r"E:\Data\Covid\patient_with_race_120720.csv"

df = pd.read_csv(COVID_FILE, header=0)

df['week'] = df['event_date'].apply(lambda x: datetime.datetime.strptime(x, '%Y/%m/%d').date().isocalendar()[1])

max_week = df['week'].max()

pros_risks_list = [[0] * max_week for i in range(10)]

hosp_risks_list = [[0] * max_week for i in range(10)]

covid_counts = [0] * max_week

for week, df_week in df.groupby(['week']):

    covid_counts[week - 1] = len(df_week)

    tot_pros_risk = tot_hosp_risk = 0

    week_hosp_count = 0

    num_groups = 0

    for group, df_group in df_week.groupby(['county', 'gender', 'age']):

        for k in range(1, 10, 2):

            if len(df_group) <= k:

                pros_risks_list[k][week - 1] += len(df_group)

        df_hospitalized = df_group.loc[df_group['hospitalized'] == 'YES']

        for k in range(1, 10, 2):

            if len(df_hospitalized) <= k:

                hosp_risks_list[k][week - 1] += len(df_hospitalized)

for k in range(1, 10, 2):

    pros_y_values = [y/covid_counts[i] for (i, y) in enumerate(pros_risks_list[k])]

    hosp_y_values = [y/covid_counts[i] for (i, y) in enumerate(hosp_risks_list[k])]

    labels = [str(w + 1) for w in range(max_week)]

    x = np.arange(len(labels))  # the label locations



    width = 0.2  # the width of the bars

    fig, ax = plt.subplots()
    ax2 = ax.twinx()

    rects1 = ax.bar(x - width / 2 * 1.2, pros_y_values, width, label='General')
    rects2 = ax.bar(x + width / 2 * 1.2, hosp_y_values, width, label='Hospitalized')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel('Week')
    ax.set_ylabel('Patients')
    ax.set_title('k={}'.format(k))
    ax.set_xticks(x)
    ax.set_xticklabels(labels)

    ax2.plot(x, covid_counts, marker='o', color='green', label='Patients')

    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')

    fig.tight_layout()

    plt.show()





