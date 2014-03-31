from functools import wraps
import re

from models import Item, Box, Order
from ups_ground.pricing import get_price as get_price_ups_ground
from ups_mi.pricing import get_price as get_price_ups_mi


LABOR_COST = 0.08

PACKAGING_COST = 0.17


def error2dict(f):
    """
    used as a decorator to capture error output of functions to return it as a dict
    instead of blowing up without notification on client side

    @arg f      : a function
    @returns    : the return value of the function. on error, a dictionary.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception, e:
            return {'error': str(e)}
    return wrapper


def partitions(items):
    """
    a generator that contains a full combination of the input items

    @arg items  : an iterable structure
    @generates  : an iterable structure containing partitioned sets of the list
    """
    if not len(items):
        yield []
        return
    for i in xrange(2 ** len(items)/2):
        parts = [set(), set()]
        for item in items:
            parts[i & 1].add(item)
            i >>= 1
        for partition in partitions(parts[1]):
            yield [parts[0]] + partition


@error2dict
def get_regular_box_price(zipcode, weight):
    """
    finds the cheapest option for all shipping methods
    """
    opts = []
    try:
        opt = (get_price_ups_ground(zipcode, weight), 'UPS Ground')
        opts.append(opt)
    except Exception:
        pass
    if weight <= 160:  # ups mi maxes out at 10 lbs / 160 oz
        try:
            opt = (get_price_ups_mi(zipcode, weight), 'UPS Mail Innovations')
            opts.append(opt)
        except Exception, e:
            pass
    try:
        return min(opts, key=lambda o: o[0])
    except ValueError:
        return get_irregular_box_price(zipcode, weight)


@error2dict
def get_irregular_box_price(zipcode, weight):
    """
    finds the cheapest option for shipping methods that can handle irregular boxes
    """
    opts = []
    try:
        opt = (get_price_ups_ground(zipcode, weight), 'UPS Ground')
        opts.append(opt)
    except Exception:
        raise
    return min(opts, key=lambda o: o[0])


@error2dict
def shipping_optimization(order):
    """
    finds the cheapest means of shipping an order

    @arg order  : a dictionary -- see example for details
    @returns    : a models.Order object -- see example for details
    @raises     : AssertionError
                : Exception (generic with custom messages)
    """
    # pull zipcode
    zipcode = str(order['zip'])[:5]
    try:
        assert re.match(r'\d{5}', zipcode)
    except AssertionError:
        bad_zip = Order()
        box = Box()
        for item in order['items']:
            # box.items.append(Item(**item))
            if 'qty' in item:
                qty = int(item['qty'])
                del item['qty']
                for _ in range(qty):
                    print item
                    box.items.append(Item(**item))
            else:
                box.items.append(Item(**item))
        box.shipping_cost = 0
        box.shipping_method = 'UPS Mail Innovations'
        bad_zip.boxes.append(box)
        return bad_zip

    # pull items
    items = order['items']
    try:
        assert isinstance(items, (list, tuple))
    except AssertionError:
        raise Exception("items is not an iterable structure / array")

    # assert well formed items
    for item in items:
        # uid
        try:
            assert len(str(item['uid'])) > 0
        except (KeyError, AssertionError):
            raise Exception("malformed item - uid missing: '%s'" % str(item))

        # weight
        try:
            assert item['weight'] > 0
            assert item['weight'] <= 2400
        except KeyError:
            raise Exception("malformed item - weight missing: '%s'" % str(item))
        except (ValueError, AssertionError):
            raise Exception("malformed item - weight must be a positive number and less than 2400 oz: '%s'" % str(item))

        # qty
        if 'qty' in item:
            try:
                assert item['qty'] > 0
            except (ValueError, AssertionError):
                raise Exception("malformed item - if qty is used it must be > 0: '%s'" % str(item))

    # short out system in # of items > 9 -- force ground in 1 box
    num_items = 0
    for item in items:
        if 'qty' in item:
            num_items += item['qty']
        else:
            num_items += 1
    if num_items > 9:
        shorted = Box()
        for item in items:
            try:
                qty = item['qty']
                del item['qty']
            except KeyError:
                qty = 1
            for _ in xrange(qty):
                shorted.items.append(Item(**item))
        shorted.shipping_cost, shorted.shipping_method = get_irregular_box_price(zipcode, shorted.weight)
        order = Order()
        order.boxes.append(shorted)
        return order

    # build lists of items
    regular_items = []
    irregular_items = []
    for item in items:
        try:
            qty = item['qty']
            del item['qty']
        except KeyError:
            qty = 1

        # loop over quantity to create Item objects
        for _ in xrange(qty):
            if 'force_ground' in item.keys():
                if item['force_ground']:
                    irregular_items.append(Item(**item))
                else:
                    regular_items.append(Item(**item))
            else:
                regular_items.append(Item(**item))

    # get prices for irregular items
    irregular_boxes = []
    for item in irregular_items:
        box = Box()
        box.items.append(item)
        box.shipping_cost, box.shipping_method = get_irregular_box_price(zipcode, box.weight)
        box.shipping_cost += LABOR_COST + PACKAGING_COST
        irregular_boxes.append(box)

    # make orders of boxes of regular items
    orders = []
    for combination in partitions(regular_items):
        order = Order()
        for partition in combination:
            box = Box()
            box.items.extend(partition)
            box.shipping_cost, box.shipping_method = get_regular_box_price(zipcode, box.weight)
            box.shipping_cost += LABOR_COST + PACKAGING_COST
            order.boxes.append(box)
        orders.append(order)

    # find cheapest order
    cheapest = min(orders, key=lambda o: o.shipping_cost)
    # add irregular boxes to order
    cheapest.boxes.extend(irregular_boxes)

    # return cheapest order
    return cheapest
