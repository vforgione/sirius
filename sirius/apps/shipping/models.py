class Item:
    """
    represents a sku/product -- whatever you want to call a singular sellable thing
    """

    def __init__(self, uid, weight, force_ground=False, height=0, width=0, depth=0):
        """
        @arg uid            : int/str - product identifier. sku, name, doesn't matter. just an id.
        @arg weight         : float - ounces
        @arg force_ground   : bool - (optional) force this item to go ground
        @arg height         : float - (optional) inches
        @arg width          : float - (optional) inches
        @arg depth          : float - (optional) inches
        """
        self.uid = uid
        self.weight = weight
        self.force_ground = force_ground
        self.height = height
        self.width = width
        self.depth = depth

    def __str__(self):
        return self.uid

    def __repr__(self):
        return "Item(%s)" % self.uid


class Box:
    """
    represents a packed box for shipping. contains Item objects.
    """

    def __init__(self):
        self.items = []
        self.shipping_method = None
        self.shipping_cost = 0.0

    def __str__(self):
        return "Box(%s)" % ', '.join([str(item) for item in self.items])

    def __repr__(self):
        return self.__str__()

    @property
    def weight(self):
        return sum([item.weight for item in self.items])

    @property
    def volume(self):
        return sum([item.height * item.width * item.depth for item in self.items])


class Order:
    """
    represents a complete order to ship. contains Box objects.
    """

    def __init__(self):
        self.boxes = []

    def __str__(self):
        return "Order({})".format(', '.join([str(box) for box in self.boxes]))

    def __repr__(self):
        return self.__str__()

    @property
    def shipping_cost(self):
        return round(sum([box.shipping_cost for box in self.boxes]), 2)

    def to_json(self):
        """
        converts internals to json output

        @returns    : a dictionary
        """
        output = {'cost': self.shipping_cost, 'boxes': []}
        for box in self.boxes:
            items = {}
            for item in box.items:
                items.setdefault(item.uid, 0)
                items[item.uid] += 1
            output['boxes'].append({
                'cost': box.shipping_cost,
                'method': box.shipping_method,
                'items': [{'uid': uid, 'qty': qty} for uid, qty in items.iteritems()],
                'weight': box.weight
            })
        return output
