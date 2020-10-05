import pandas as pd

VOTER_FILE = r"E:\Data\Covid\voterside_053020.csv"
VOTER_FILTERED_FILE = r"E:\Data\Covid\voterside_filtered_053020.csv"

df_voter = pd.read_csv(VOTER_FILE, header=0, usecols=['voter_serial', 'county', 'dob', 'gender', 'race'])

print('Num. of voters: {}'.format(len(df_voter)))

df_voter.dropna(subset=['county', 'dob', 'gender', 'race'], how='any', inplace=True)

df_voter = df_voter.loc[(1 <= df_voter['race']) & (df_voter['race'] <= 5)]

# df_voter['yob'] = df_voter['dob'].apply(lambda x: int(x[-4:]))

df_voter.to_csv(VOTER_FILTERED_FILE)

print('Num. of filtered voters: {}'.format(len(df_voter)))