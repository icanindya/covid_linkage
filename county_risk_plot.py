import plotly.figure_factory as ff
import numpy as np
import pandas as pd
import collections
from utils import county_dict, fips_dict

MATCH_FILE_RACE = r'E:\Data\Covid\Results\matched_with_race_{}_{}_081020_053020.csv'
FIG_FILE = r'E:\Data\Covid\Results\risk_county_{}_081020_053020.png'
NUM_SIMULATIONS = 100

code_to_fips = {}

for county_name in county_dict:

    code_to_fips[county_dict[county_name]] = int('12' + fips_dict[county_name])

for eq_class_limit in [1, 3, 5, 10, 15, 20]:

    risk_dict = collections.defaultdict(int)

    for i in range(1, NUM_SIMULATIONS + 1):

        df = pd.read_csv(MATCH_FILE_RACE.format(eq_class_limit, i), header=0)

        # print(df)

        for group, df_group in df.groupby(['county', 'gender', 'age', 'race', 'event_date']):

            df_group['risks'] = df_group['patient_counts'] / df_group['voter_counts']

            county = group[0]

            county_fips = code_to_fips[county]

            risk_dict[county_fips] += df_group['risks']

    for k in risk_dict:

        risk_dict[k] /= NUM_SIMULATIONS

        print(k, risk_dict[k])

    values = [risk_dict[code_to_fips[county_code]] * 10 + 0.001 for county_code in county_dict.values()]
    fips = [code_to_fips[county_code] for county_code in county_dict.values()]

    print(values)

    endpts = list(np.mgrid[min(values):max(values):5j])

    colorscale = ['#ff0000',
                  # '#ff1919',
                  '#ff3232',
                  # '#ff4c4c',
                  '#ff6666',
                  # '#ff7f7f',
                  '#ff9999',
                  # '#ffb2b2',
                  '#ffcccc',
                  '#ffe5e5',
                  # '#ffffff'
                  ][::-1]

    fig = ff.create_choropleth(
        fips=fips, values=values, scope=['Florida'], show_state_data=True,
        colorscale=colorscale,
        binning_endpoints=endpts,
        round_legend_values=True,
        # plot_bgcolor='rgb(229,229,229)',
        # paper_bgcolor='rgb(229,229,229)',
        title='Equivalence class size limit {}'.format(eq_class_limit),
        legend_title='Risk by County * 10',
        county_outline={'color': 'rgb(255,0,0)', 'width': 0.5},
        exponent_format=True,
    )
    fig.layout.template = None
    fig.show()
    # fig.write_image(FIG_FILE.format(eq_class_limit))