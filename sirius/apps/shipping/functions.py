from functools import wraps

from models import Item, Box, Order
from price_matrices import get_box_price, get_box_price_irregular


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
            return {'error': e.message}
    return wrapper


def partitions(items):
    """
    produces a generator that contains a full combination of the input items

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
def shipping_optimization(order):
    """
    finds the cheapest means of shipping an order

    @arg order  : a dictionary -- see example for details
    @returns    : a models.Order object -- see example for details
    @raises     : AssertionError
                : Exception (generic with custom messages)
    """
    # pull zipcode
    zipcode = str(order['zip'])
    assert len(zipcode) >= 5

    # pull items
    items = order['items']
    assert isinstance(items, (list, tuple))

    # short out system in # of items > 9 -- force ground in 1 box
    num_items = 0
    for item in items:
        if 'qty' in item:
            num_items += int(item['qty'])
        else:
            num_items += 1
    if num_items > 9:
        shorted = Box()
        for item in items:
            try:
                qty = int(item['qty'])
                del item['qty']
            except (KeyError, ValueError):
                qty = 1
            for _ in range(qty):
                shorted.items.append(Item(**item))
        shorted.shipping_cost, shorted.shipping_method = get_box_price_irregular(zipcode, shorted.weight)
        order = Order()
        order.boxes.append(shorted)
        return order

    # build lists of items
    regular_items = []
    irregular_items = []
    for item in items:
        # determine quantity and weight
        if 'qty' in item:
            if int(item['qty']) <= 0:
                raise Exception("qty<=0 -- illegal value")
        try:
            assert 'uid' in item
        except:
            raise Exception("missing uid in item")

        try:
            assert 'weight' in item
        except:
            raise Exception("missing weight in item")

        try:
            assert int(item['weight']) > 0
        except:
            raise Exception("weight<=0 -- illegal value")

        try:
            assert int(item['weight']) <= 2400  # max weight of 150 for ups
        except:
            raise Exception("weight>2400 -- illegal value")

        try:
            qty = int(item['qty'])
            del item['qty']
        except (KeyError, ValueError):
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
        box.shipping_cost, box.shipping_method = get_box_price_irregular(zipcode, box.weight)
        box.shipping_cost += LABOR_COST + PACKAGING_COST
        irregular_boxes.append(box)

    # make orders of boxes of regular items
    orders = []
    for combination in partitions(regular_items):
        order = Order()
        for partition in combination:
            box = Box()
            box.items.extend(partition)
            box.shipping_cost, box.shipping_method = get_box_price(zipcode, box.weight)
            box.shipping_cost += LABOR_COST + PACKAGING_COST
            order.boxes.append(box)
        orders.append(order)

    # find cheapest order
    cheapest = min(orders, key=lambda o: o.shipping_cost)
    # add irregular boxes to order
    cheapest.boxes.extend(irregular_boxes)

    # return cheapest order
    return cheapest
