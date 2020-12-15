import pandas as pd
import datetime
import sys

COVID_FILE = r"E:\Data\Covid\patient_with_race_120720.csv"

df = pd.read_csv(COVID_FILE, header=0)

df['week'] = df['event_date'].apply(lambda x: datetime.datetime.strptime(x, '%Y/%m/%d').date().isocalendar()[1])

max_week = df['week'].max()

pros_risks = [0] * max_week

hosp_risks = [0] * max_week

covid_counts = [0] * max_week

for week, df_week in df.groupby(['week']):

    covid_counts[week - 1] = len(df_week)

    tot_pros_risk = tot_hosp_risk = 0

    week_hosp_count = 0

    num_groups = 0

    for group, df_group in df_week.groupby(['county', 'gender', 'age']):



        num_groups += 1

        tot_pros_risk += 1 / len(df_group)

        group_hosp_count = len(df_group.loc[df_group['hospitalized'] == 'YES'])

        week_hosp_count += group_hosp_count

        tot_hosp_risk += group_hosp_count / len(df_group)

    # print(pros_risk, num_groups)

    # avg_pros_risk = tot_pros_risk / covid_counts[week - 1]

    avg_pros_risk = num_groups / covid_counts[week - 1]

    # avg_hosp_risk = tot_hosp_risk / covid_counts[week - 1]

    avg_hosp_risk = week_hosp_count / covid_counts[week - 1]

    pros_risks[week - 1] = avg_pros_risk

    hosp_risks[week - 1] = avg_hosp_risk

print(pros_risks)

print(hosp_risks)


import matplotlib
import matplotlib.pyplot as plt
import numpy as np


labels = [str(w + 1) for w in range(max_week)]

x = np.arange(len(labels))  # the label locations

print(x)

width = 0.2  # the width of the bars

fig, ax = plt.subplots()
ax2 = ax.twinx()
rects1 = ax.bar(x - width/2 * 1.2, pros_risks, width, label='General')
rects2 = ax.bar(x + width/2 * 1.2, hosp_risks, width, label='Hospitalized')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_xlabel('Week')
ax.set_ylabel('Risks')
ax.set_title('Avg. Risk')
ax.set_xticks(x)
ax.set_xticklabels(labels)

ax2.plot(x, covid_counts, marker='o', color='green', label='Patients')

ax.legend(loc='upper left')
ax2.legend(loc='upper right')

fig.tight_layout()

plt.show()





