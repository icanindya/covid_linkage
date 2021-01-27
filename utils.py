import datetime
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import collections

county_dict = {'Alachua': 'ALA',
               'Baker': 'BAK',
               'Bay': 'BAY',
               'Bradford': 'BRA',
               'Brevard': 'BRE',
               'Broward': 'BRO',
               'Calhoun': 'CAL',
               'Charlotte': 'CHA',
               'Citrus': 'CIT',
               'Clay': 'CLA',
               'Collier': 'CLL',
               'Columbia': 'CLM',
               'Dade': 'DAD',
               'Desoto': 'DES',
               'Dixie': 'DIX',
               'Duval': 'DUV',
               'Escambia': 'ESC',
               'Flagler': 'FLA',
               'Franklin': 'FRA',
               'Gadsden': 'GAD',
               'Gilchrist': 'GIL',
               'Glades': 'GLA',
               'Gulf': 'GUL',
               'Hamilton': 'HAM',
               'Hardee': 'HAR',
               'Hendry': 'HEN',
               'Hernando': 'HER',
               'Highlands': 'HIG',
               'Hillsborough': 'HIL',
               'Holmes': 'HOL',
               'Indian River': 'IND',
               'Jackson': 'JAC',
               'Jefferson': 'JEF',
               'Lafayette': 'LAF',
               'Lake': 'LAK',
               'Lee': 'LEE',
               'Leon': 'LEO',
               'Levy': 'LEV',
               'Liberty': 'LIB',
               'Madison': 'MAD',
               'Manatee': 'MAN',
               'Marion': 'MRN',
               'Martin': 'MRT',
               'Monroe': 'MON',
               'Nassau': 'NAS',
               'Okaloosa': 'OKA',
               'Okeechobee': 'OKE',
               'Orange': 'ORA',
               'Osceola': 'OSC',
               'Palm Beach': 'PAL',
               'Pasco': 'PAS',
               'Pinellas': 'PIN',
               'Polk': 'POL',
               'Putnam': 'PUT',
               'Santa Rosa': 'SAN',
               'Sarasota': 'SAR',
               'Seminole': 'SEM',
               'St. Johns': 'STJ',
               'St. Lucie': 'STL',
               'Sumter': 'SUM',
               'Suwannee': 'SUW',
               'Taylor': 'TAY',
               'Union': 'UNI',
               'Volusia': 'VOL',
               'Wakulla': 'WAK',
               'Walton': 'WAL',
               'Washington': 'WAS'}

fips_dict = {'Alachua': '001',
             'Baker': '003',
             'Bay': '005',
             'Bradford': '007',
             'Brevard': '009',
             'Broward': '011',
             'Calhoun': '013',
             'Charlotte': '015',
             'Citrus': '017',
             'Clay': '019',
             'Collier': '021',
             'Columbia': '023',
             'Dade': '086',
             'Desoto': '027',
             'Dixie': '029',
             'Duval': '031',
             'Escambia': '033',
             'Flagler': '035',
             'Franklin': '037',
             'Gadsden': '039',
             'Gilchrist': '041',
             'Glades': '043',
             'Gulf': '045',
             'Hamilton': '047',
             'Hardee': '049',
             'Hendry': '051',
             'Hernando': '053',
             'Highlands': '055',
             'Hillsborough': '057',
             'Holmes': '059',
             'Indian River': '061',
             'Jackson': '063',
             'Jefferson': '065',
             'Lafayette': '067',
             'Lake': '069',
             'Lee': '071',
             'Leon': '073',
             'Levy': '075',
             'Liberty': '077',
             'Madison': '079',
             'Manatee': '081',
             'Marion': '083',
             'Martin': '085',
             'Monroe': '087',
             'Nassau': '089',
             'Okaloosa': '091',
             'Okeechobee': '093',
             'Orange': '095',
             'Osceola': '097',
             'Palm Beach': '099',
             'Pasco': '101',
             'Pinellas': '103',
             'Polk': '105',
             'Putnam': '107',
             'Santa Rosa': '113',
             'Sarasota': '115',
             'Seminole': '117',
             'St. Johns': '109',
             'St. Lucie': '111',
             'Sumter': '119',
             'Suwannee': '121',
             'Taylor': '123',
             'Union': '125',
             'Volusia': '127',
             'Wakulla': '129',
             'Walton': '131',
             'Washington': '133'}


def get_yob(age, event_date):
    event_datetime = datetime.strptime(event_date, '%Y/%m/%d') #  %H:%M:%S
    birth_datetime = event_datetime - relativedelta(years=age)
    return birth_datetime.year


def get_age(dob, event_date):
    dob_datetime = datetime.strptime(dob, '%m/%d/%Y')
    event_datetime = datetime.strptime(event_date, '%Y/%m/%d')

    return event_datetime.year - dob_datetime.year - \
           ((event_datetime.month, event_datetime.day) < (dob_datetime.month, dob_datetime.day))