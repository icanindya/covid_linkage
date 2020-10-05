import datetime
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import collections

def get_yob(age, event_date):
    event_datetime = datetime.strptime(event_date, '%Y/%m/%d') #  %H:%M:%S
    birth_datetime = event_datetime - relativedelta(years=age)
    return birth_datetime.year

def get_age(dob, event_date):
    dob_datetime = datetime.strptime(dob, '%m/%d/%Y')
    event_datetime = datetime.strptime(event_date, '%Y/%m/%d')

    return event_datetime.year - dob_datetime.year - \
           ((event_datetime.month, event_datetime.day) < (dob_datetime.month, dob_datetime.day))