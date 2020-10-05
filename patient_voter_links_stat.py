import pandas as pd

MAX_MATCHES = 10

MATCH_FILE = r'E:\Data\Covid\matched_081020_053020.csv'


df = pd.read_csv(MATCH_FILE, header=0)

print(df['matches'].min(), df['matches'].max(), df['matches'].mean())

df = df.loc[df['matches'].isin(list(range(1)))]

print(len(df))

print(df['matches'].value_counts())

for i in range(10, MAX_MATCHES + 1):

    df_new = df.loc[df['matches'] == 0]

    print(df_new['yob'].value_counts())
    print(df_new['gender'].value_counts())
    print(df_new['county'].value_counts())

    print('\n\n\n\n')


