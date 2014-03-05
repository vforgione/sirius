import csv
import os
import re


RATING_OZ_FILENAME = os.path.abspath(os.path.join(os.path.dirname(__file__), 'rate_configs', 'ups_mi_rates_oz.csv'))
RATING_LB_FILENAME = os.path.abspath(os.path.join(os.path.dirname(__file__), 'rate_configs', 'ups_mi_rates_lbs.csv'))


def rip_oz(filename=RATING_OZ_FILENAME):
    """
    rips a file that is two columns - column 1 is the weight and column 2 is the rate
    """
    rates = {}
    with open(filename, 'r') as fh:
        for line in fh:
            weight, rate = line.split(',')
            weight = int(weight.rstrip())
            rate = float(rate.rstrip())
            rates[weight] = rate
    return rates


def rip_lbs(filename=RATING_LB_FILENAME):
    """
    rips a file that is formatted with zone columns and weight rows into a dictionary --

    a csv like this:
    ,1,2,3,4,5,6,7,8
    1,4.89,4.89,5.62,5.9,6.09,6.25,6.3,7.01
    2,5.21,5.21,5.97,6.53,7.09,7.4,7.57,7.64
    3,5.46,5.46,6.59,7.62,8.32,8.5,8.72,8.89
    4,5.93,5.93,7.43,8.62,9.3,9.48,9.64,9.72

    becomes a dict like this:
    {
        1: {
            1: 4.98,
            2: 5.21, ...
        }, ...
    }

    ideally, you can use this dictionary to then get the rate of a package by accessing via the zone key and the weight
    """
    with open(filename, 'r') as fh:
        reader = csv.reader(fh)
        rows = [row for row in reader]

    zones = [int(row.rstrip()) for row in rows[0][1:]]

    weights = [int(row[0].rstrip()) for row in rows[1:]]

    zone_weight_dict = {}
    for i, row in enumerate(rows[1:]):
        for j, cell in enumerate(row[1:]):
            cell = re.sub(r'[^\d\.]', '', cell.strip())
            zone_weight_dict.setdefault(zones[j], {})
            zone_weight_dict[zones[j]][weights[i]] = float(cell)

    return zone_weight_dict
