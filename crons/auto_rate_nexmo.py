# coding: utf-8

import logging
import os
import pandas as pd
import requests
import sys
from datetime import datetime

sys.path.append('..')
from flaskapp import db
from flaskapp.models import CountrySmsRate


def get_fresh_nexmo_pricing():
    try:
        os.remove('nexmo_pricing.xls')
    except OSError:
        pass
    nexmo_download_link = "https://dashboard.nexmo.com/download_pricing"
    resp = requests.get(nexmo_download_link)
    with open('nexmo_pricing.xls', 'wb') as output:
        output.write(resp.content)


#get_fresh_nexmo_pricing()


outbound_sms_data = pd.read_excel('nexmo_pricing.xls', 'Outbound SMS',
    index_col=None)


try:
    profit = float(sys.argv[1])
except:
    logging.error("Invalid argument: profit must be float")
    raise

outbound_sms_data.head()
outbound_sms_data_fix = outbound_sms_data.sort('Price (EUR) / message',
    ascending=False).groupby(['Country Code', 'Prefix'],
    as_index=False).first()


for country_cd, country_name, prefix, base_rate in zip(
    outbound_sms_data_fix['Country Code'],
    outbound_sms_data_fix['Country Name'],
    outbound_sms_data_fix['Prefix'],
    outbound_sms_data_fix['Price (EUR) / message']):

    cursor = db.engine.execute("""
        select count(*)
        from country_sms_rate
        where country_cd='%s' and prefix='%s'
    """ % (country_cd, prefix))
    profit_perc = base_rate + (base_rate * profit / 100.0)
    try:
        countResult = cursor.fetchall()[0][0]
    except:
        countResult = 0
    if(countResult == 0):
        # Insert country rate information
        db.engine.execute(CountrySmsRate.__table__.insert(),
            country_cd=country_cd, prefix=str(prefix),
            country_name=country_name, base_rate=base_rate,
            fix_rate=profit_perc, insert_date=datetime.now(),
            update_date=datetime.now())
    else:
        # Update country rate information
        db.engine.execute("""
            update country_sms_rate
            set country_name='%s',
                base_rate=%s,
                fix_rate=%s,
                update_date='%s'
            where country_cd='%s' and prefix='%s'
            """ % (country_name, base_rate, profit_perc, datetime.now(),
                country_cd, str(prefix)))
