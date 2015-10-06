# coding: utf-8

from flaskapp import db

PREFIX_DIC = {}
MAX_PREFIX_LENGTH = 4


def get_prefix_dict():
    """Lazy load of PREFIX_DIC"""
    global PREFIX_DIC
    if len(PREFIX_DIC) == 0:
        load_rates_from_db()
    return PREFIX_DIC


def load_rates_from_db():
    """Updates MAXMAX_PREFIX_LENGTH, PREFIX_DIC"""
    global MAX_PREFIX_LENGTH, PREFIX_DIC
    cursor = db.engine.execute("""
        SELECT prefix, MAX(fix_rate) AS fix_rate
        FROM country_sms_rate
        GROUP BY prefix
        """)
    prefix_rate_dict = {}
    for result in cursor.fetchall():
        prefix_rate_dict[result['prefix']] = result['fix_rate']
        if len(result['prefix']) > MAX_PREFIX_LENGTH:
            MAX_PREFIX_LENGTH = len(result['prefix'])
    PREFIX_DIC = prefix_rate_dict


def out_sms_rate(number):
    """
    Returns the float rate for the number or -1 if number is not supported.
    """
    global MAX_PREFIX_LENGTH
    rates_data = get_prefix_dict()
    if(number.startswith('+')):
        number = number[1:]
    for i in range(MAX_PREFIX_LENGTH, 0, -1):
        # usign lazy dict
        rate = rates_data.get(number[:i], False)
        if rate:
            return float(rate)
    return -1
