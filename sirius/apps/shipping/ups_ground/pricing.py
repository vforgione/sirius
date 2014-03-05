from math import ceil

from rates import rip_rates
from zones import rip_zones


GROUND_RATES = rip_rates()
GROUND_ZONES = rip_zones()


def get_price(zipcode, weight_in_ounces):
    weight = int(ceil(weight_in_ounces / 16.0))

    try:
        zone = GROUND_ZONES[zipcode]
    except KeyError:
        raise Exception("zipcode '%s' not found in ups ground zone conversion" % zipcode)

    try:
        rates = GROUND_RATES[zone]
    except KeyError:
        Exception("zone '%s' not found in rate conversion -- this should not have happened!" % zone)

    try:
        price = rates[weight]
    except KeyError:
        raise Exception("weight '%s' not found in rates for zone '%s'" % (weight, zone))

    return price
