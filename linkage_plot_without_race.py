# numpy is used for creating fake data
import numpy as np
import matplotlib as mpl
import pandas as pd
import matplotlib.pyplot as plt

RESULT_FILE = r"E:\Data\Covid\Results\result_{}_120720_053020.txt"

## combine these different collections into a list
num_patients =[]

for eq_class_limit in [1, 3, 5, 10, 15, 20]:

    df = pd.read_csv(RESULT_FILE.format(eq_class_limit), header=0)

    num_patients.append(df['num_patients'].mean())

# Create a figure instance
fig = plt.figure(1, figsize=(9, 6))

# Create an axes instance
ax = fig.add_subplot(111)

ax.bar([1,2,3,4,5,6], num_patients, align='center', alpha=0.5)

## Remove top axes and right axes ticks
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
ax.set_xlabel('k')
ax.set_ylabel('Num. of patients at risk')
ax.set_xticks([1,2,3,4,5,6])
ax.set_xticklabels(['1', '3', '5', '10', '15', '20'])
plt.title('Num. of Vulnerable Patients vs. Bucket size (without race)')
plt.show()
