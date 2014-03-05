import csv
import os


REGULAR_ZONES_FILENAME = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'zone_configs', 'ups_mi_regular_zipcodes.csv'))
IRREGULAR_ZONES_FILENAME = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'zone_configs', 'ups_mi_irregular_zipcodes.csv'))


def rip_zones(regular_zones_filename=REGULAR_ZONES_FILENAME, irregular_zones_file_name=IRREGULAR_ZONES_FILENAME):
    """
    rips through the zone files and returns a dictionary of zipcode keys and zone values --

    {
        "00400": 2, ...
        "00534": 3, ...
        "96762": 44, ...
    }
    """

    regular = {}
    with open(regular_zones_filename, 'r') as fh:
        reader = csv.reader(fh)
        for zipcode, zone in reader:
            ## zipcode can either be a distinct zipcode or a range
            # stright zipcode
            if '---' not in zipcode:
                regular[str(zipcode)] = int(zone[0])
            # it's a range
            else:
                start, stop = zipcode.split('---')
                start = int(start)
                stop = int(stop)
                # iterate range
                for i in xrange(start, stop + 1):
                    key = str(i)
                    # pad out zipcode
                    while len(key) < 3:
                        key = '0' + key
                    regular[key] = int(zone[0])

    # normalize regular zones -- they only have the first 3 digits
    normalized = {}
    for key, zone in regular.iteritems():
        start = int(key + '00')
        stop = int(key + '99')
        for zipcode in xrange(start, stop+1):
            while len(str(zipcode)) < 5:
                zipcode = '0' + str(zipcode)
            normalized[str(zipcode)] = zone

    # irregular zipcodes are always 5 digits for ups mi
    irregular = {}
    with open(irregular_zones_file_name, 'r') as fh:
        reader = csv.reader(fh)
        for zipcode, zone in reader:
            ## zipcode can either be a distinct zipcode or a range
            # stright zipcode
            if '---' not in zipcode:
                irregular[str(zipcode)] = int(zone[0])
            # it's a range
            else:
                start, stop = zipcode.split('---')
                start = int(start)
                stop = int(stop)
                # iterate range
                for i in xrange(start, stop + 1):
                    irregular[str(i)] = int(zone[0])
    normalized.update(irregular)

    return normalized
