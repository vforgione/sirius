import csv
import re
import yaml


def parse_file(infile, outfile):
    """
    parses a csv that has row 1 as the zones and column 1 as the weights into a dictionary and spits that into a yaml
    config file
    """
    with open(infile, 'r') as fh:
        reader = csv.reader(fh)
        rows = [row for row in reader]

    zs = [row.rstrip() for row in rows[0][1:]]
    zones = []
    for z in zs:
        while len(z) < 3:
            z = '0' + z
        zones.append(z)

    weights = [int(row[0].rstrip()) for row in rows[1:]]

    zone_weight_dict = {}
    for i, row in enumerate(rows[1:]):
        for j, cell in enumerate(row[1:]):
            cell = re.sub(r'[^\w\.]', '', cell.strip())
            zone_weight_dict.setdefault(zones[j], {})
            zone_weight_dict[zones[j]][weights[i]] = float(cell)

    yaml.dump(zone_weight_dict, open(outfile, 'w'))
