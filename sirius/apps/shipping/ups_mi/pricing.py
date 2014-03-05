from math import ceil, floor

from rates import rip_lbs, rip_oz
from zones import rip_zones


MI_RATES_OZ = rip_oz()
MI_RATES_LBS = rip_lbs()
MI_ZONES = rip_zones()


def get_price(zipcode, weight_in_ounces):

    woz = int(ceil(weight_in_ounces))
    wlbs = int(floor(weight_in_ounces / 16.0))

    try:
        zone = MI_ZONES[zipcode]
    except KeyError:
        raise Exception("zipcode '%s' not found in ups mi zone conversion" % zipcode)

    if woz <=16:
        # use oz rates
        try:
            return MI_RATES_OZ[woz]
        except KeyError:
            raise Exception("weight '%s' not found in oz rates" % woz)

    else:
        # use lbs rates
        try:
            rates = MI_RATES_LBS[zone]
        except KeyError:
            raise Exception("zone '%s' not found in lbs rate conversion -- this should not have happened" % zone)
        try:
            return rates[wlbs]
        except KeyError:
            raise Exception("weight '%s' not found in rates for zone '%s'" % (wlbs, zone))
