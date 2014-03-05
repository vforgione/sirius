import csv
import os


ZONE_44_FILENAME = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'zone_configs', 'ups_ground_zone_44_zipcodes.txt'))
ZONE_46_FILENAME = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'zone_configs', 'ups_ground_zone_46_zipcodes.txt'))
REGULAR_ZONES_FILENAME = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'zone_configs', 'ups_ground_regular_zipcodes_to_zones.csv'))


def rip_zones(zone_44_filename=ZONE_44_FILENAME,
              zone_46_filename=ZONE_46_FILENAME,
              regular_zones_filename=REGULAR_ZONES_FILENAME):
    """
    rips through the zone files and returns a dictionary of zipcode keys and zone values --

    {
        "00400": 2, ...
        "00534": 3, ...
        "96762": 44, ...
    }
    """

    zone_44 = dict((line.rstrip(), 44) for line in open(zone_44_filename, 'r'))
    zone_46 = dict((line.rstrip(), 46) for line in open(zone_46_filename, 'r'))

    regular = {}
    with open(regular_zones_filename, 'r') as fh:
        reader = csv.reader(fh)
        for zipcode, zone in reader:
            ## zipcode can either be a distinct zipcode or a range
            # stright zipcode
            if '-' not in zipcode:
                regular[str(zipcode)] = zone
            # it's a range
            else:
                start, stop = zipcode.split('-')
                start = int(start)
                stop = int(stop)
                # iterate range
                for i in xrange(start, stop + 1):
                    key = str(i)
                    # pad out zipcode
                    while len(key) < 3:
                        key = '0' + key
                    regular[key] = zone

    # normalize regular zones -- they only have the first 3 digits
    normalized = {}
    for key, zone in regular.iteritems():
        start = int(key + '00')
        stop = int(key + '99')
        for zipcode in xrange(start, stop+1):
            while len(str(zipcode)) < 5:
                zipcode = '0' + str(zipcode)
            normalized[str(zipcode)] = int(zone)

    # add / overwrite normalized zip-zones with alaska/hawaii zones
    normalized.update(zone_44)
    normalized.update(zone_46)

    return normalized
