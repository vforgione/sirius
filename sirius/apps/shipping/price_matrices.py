from math import ceil
import os

import yaml


CONFIG_DIR = os.path.abspath(os.path.join(__file__, '..', 'configs'))

UPS_GROUND_ZIP_TO_ZONE = yaml.load(open(os.path.join(CONFIG_DIR, 'ups_ground_zip_to_zone.yaml'), 'r'))
UPS_GROUND_ZONE_WEIGHT_PRICE = yaml.load(open(os.path.join(CONFIG_DIR, 'ups_ground_zone_weight_price.yaml'), 'r'))
UPS_GROUND_ZONE_044 = [str(line.rstrip()) for line in open(os.path.join(CONFIG_DIR, 'zone44.txt'))]
UPS_GROUND_ZONE_046 = [str(line.rstrip()) for line in open(os.path.join(CONFIG_DIR, 'zone46.txt'))]

UPS_MI_RATES_OZ = yaml.load(open(os.path.join(CONFIG_DIR, 'ups_mi_rates_oz.yaml')))
UPS_MI_RATES_LBS = yaml.load(open(os.path.join(CONFIG_DIR, 'ups_mi_rates_lbs.yaml')))


def _ups_ground(zipcode, weight):
    """
    returns price for shipping via UPS Ground

    @arg zipcode    : str/int - where the box is being sent
    @arg weight     : float - the weight of the box being sent
    @returns        : float
    @raises         : KeyError if zipcode isn't found or weight exceeds 150 lbs.
    """
    weight = ceil(float(weight) / 16)  # convert to lbs
    if zipcode in UPS_GROUND_ZONE_044:
        zone = '044'
    elif zipcode in UPS_GROUND_ZONE_046:
        zone = '046'
    else:
        zone = UPS_GROUND_ZIP_TO_ZONE[zipcode[:3]]  # ups ground conversions use first 3 digits only
    for tier in sorted(UPS_GROUND_ZONE_WEIGHT_PRICE[zone]):
        if weight <= tier:
            return UPS_GROUND_ZONE_WEIGHT_PRICE[zone][tier]


def _ups_mi(weight):
    """
    returns price for shipping via UPS Mail Innovations

    @arg weight     : float - the weight of the box being sent
    @returns        : float
    @raises         : KeyError if weight exceeds 5 lbs.
    """
    if weight <= 16:  # under a pound
        for tier in sorted(UPS_MI_RATES_OZ):
            if weight <= tier:
                return UPS_MI_RATES_OZ[tier]
    else:
        weight = ceil(float(weight) / 16)  # convert to lbs
        if weight > 5:
            return 9999999999
        for tier in sorted(UPS_MI_RATES_LBS):
            if weight <= tier:
                return UPS_MI_RATES_LBS[tier]


def get_box_price(zipcode, weight):
    """
    finds the cheapest option for all shipping methods

    METHODS INCLUDED:
        * ups ground
        * ups mail innovations
    """
    options = [
        (_ups_ground(zipcode, weight), 'UPS Ground'),
        (_ups_mi(weight), 'UPS Mail Innovations'),
    ]
    return min(options, key=lambda option: option[0])


def get_box_price_irregular(zipcode, weight):
    """
    finds the cheapest option for ground only shipping methods

    METHODS INCLUDED:
        * ups ground
    """
    options = [
        (_ups_ground(zipcode, weight), 'UPS Ground'),
    ]
    return min(options, key=lambda option: option[0])
