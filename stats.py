import pandas as pd

COVID_FILE_RACE = r"E:\Data\Covid\patient_with_race_081020.csv"
VOTER_FILE = r"E:\Data\Covid\voterside_filtered_053020.csv"

for file in [COVID_FILE_RACE, VOTER_FILE]:

    df = pd.read_csv(file, header=0)

    freq = [0] * 5

    for race, race_df in df.groupby('race'):

        freq[race - 1] = len(race_df)

    tot = sum(freq)

    print(freq)

    print([round(x * 100/tot, 2) for x in freq])

