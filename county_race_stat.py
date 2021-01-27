import pandas as pd
from utils import county_dict
import collections
import random

VOTER_FILE = r"E:\Data\Covid\voterside_filtered_053020.csv"

df_voter = pd.read_csv(VOTER_FILE, header=0,  usecols=['voter_serial', 'county', 'race'])

racial_weights = collections.defaultdict(list)

for county, df_county in df_voter.groupby('county'):

    orig_freq = [1] * 5

    #1 Native, 2 Asian 3 Black 4 Hispanic 5 White

    # COVID19 risk factor from CDC

    weighted_freq = [2.8, 1.1, 2.6, 2.8, 1.0]

    for race, df_race in df_county.groupby('race'):

        orig_freq[race - 1] = len(df_race)

        weighted_freq[race - 1] *= len(df_race)

    orig_tot = sum(orig_freq)

    weighted_tot = sum(weighted_freq)

    weighted_prop = [round(x * 100/weighted_tot, 2) for x in weighted_freq]

    orig_prop = [round(x * 100/orig_tot, 2) for x in orig_freq]

    print(county)

    print(orig_prop)

    print(weighted_prop)

    racial_weights[county] = weighted_prop

