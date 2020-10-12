# numpy is used for creating fake data
import numpy as np
import matplotlib as mpl
import pandas as pd
import matplotlib.pyplot as plt

RESULT_FILE = r"E:\Data\Covid\Results\result_with_race_{}_081020_053020.txt"

## combine these different collections into a list
data_to_plot =[]

for eq_class_limit in [1, 3, 5, 10, 15, 20]:

    df = pd.read_csv(RESULT_FILE.format(eq_class_limit), header=0)

    data_to_plot.append(df['num_patients'])

# Create a figure instance
fig = plt.figure(1, figsize=(9, 6))

# Create an axes instance
ax = fig.add_subplot(111)

# Create the boxplot
bp = ax.boxplot(data_to_plot)

# # Save the figure
# fig.savefig('fig1.png', bbox_inches='tight')

## add patch_artist=True option to ax.boxplot()
## to get fill color
bp = ax.boxplot(data_to_plot, patch_artist=True)

# ## change outline color, fill color and linewidth of the boxes
# for box in bp['boxes']:
#     # change outline color
#     box.set( color='#7570b3', linewidth=2)
#     # change fill color
#     box.set( facecolor = '#1b9e77' )
#
# ## change color and linewidth of the whiskers
# for whisker in bp['whiskers']:
#     whisker.set(color='#7570b3', linewidth=2)
#
# ## change color and linewidth of the caps
# for cap in bp['caps']:
#     cap.set(color='#7570b3', linewidth=2)
#
# ## change color and linewidth of the medians
# for median in bp['medians']:
#     median.set(color='#b2df8a', linewidth=2)
#
# ## change the style of fliers and their fill
# for flier in bp['fliers']:
#     flier.set(marker='o', color='#e7298a', alpha=0.5)

## Remove top axes and right axes ticks
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
ax.set_xlabel('equivalence class size limit')
ax.set_ylabel('Num. of patients at risk')
ax.set_xticks([1,2,3,4,5,6])
ax.set_xticklabels(['1', '3', '5', '10', '15', '20'])
plt.show()

# import seaborn
#
# import numpy as np
# import seaborn as sns
# import matplotlib.pyplot as plt
# import pandas as pd
#
# RESULT_FILE = r"E:\Data\Covid\Results\result_with_race_{}_081020_053020.txt"
#
# ## combine these different collections into a list
#
# x = [1, 3, 5, 10, 15, 20]
#
# y = []
#
# for eq_class_limit in x:
#
#     df = pd.read_csv(RESULT_FILE.format(eq_class_limit), header=0)
#
#     y.append(df['num_patients'].tolist())
#
#
# #create some random data
# np.random.seed(0)
#
#
# #create lineplot
# ax = sns.lineplot(x, y)
#
# plt.show()