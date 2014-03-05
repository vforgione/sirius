import csv
import os
import re


RATING_FILENAME = os.path.abspath(os.path.join(os.path.dirname(__file__), 'rate_configs', 'ups_ground_rates.csv'))


def rip_rates(filename=RATING_FILENAME):
    """
    rips a file that is formatted with zone columns and weight rows into a dictionary --

    a csv like this:
    ,2,3,4,5,6,7,8,44,45,46
    1,9.78,9.78,9.78,9.78,9.78,9.82,9.93,24.23,24.30,30.95
    2,9.78,9.78,10.08,10.23,10.60,10.70,10.97,26.61,26.61,33.31
    3,9.78,9.84,10.46,10.69,11.08,11.26,11.81,28.64,28.69,35.26
    4,9.78,10.01,10.82,11.16,11.47,11.78,12.43,31.15,31.20,37.98

    becomes a dict like this:
    {
        2: {
            1: 9.78,
            2: 9.78, ...
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
