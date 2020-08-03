from collections import defaultdict


def get_deep_attr(obj, attr, default=None):
    """
    Like the built in getattr, but attr can traverse multiple dot separated attributes, e.g.:
    getattr(person, 'address.city') returns person.address.city

    get_deep_attr returns a default `None` if no value is found

    :param obj: instance whose value will be retrieved
    :param attr: string of dot separated attribute names
    :return: the value of obj.att1.attr2
    """
    first_attr, *rest = attr.split('.', 1)

    if not rest:
        # Recursion base case, attr has depth 1.
        return getattr(obj, first_attr, default)

    return get_deep_attr(getattr(obj, first_attr, None), rest[0], default=default)


class Multidict:
    def __init__(self, *indexes):
        self.dicts = {index: defaultdict(set) for index in indexes}
        self.items = set()

    def _add_item_to_index(self, item, index):
        item_value = get_deep_attr(item, index)
        if item_value:
            self.dicts[index][item_value].add(item)

    def add(self, item):
        self.items.add(item)
        for index in self.dicts.keys():
            self._add_item_to_index(item, index)

    def add_indexes(self, *indexes):
        for index in indexes:
            if index not in self.dicts:
                self.dicts[index] = defaultdict(set)
                for item in self.items:
                    self._add_item_to_index(item, index)

    def __getitem__(self, key):
        return set.union(*(items[key] for items in self.dicts.values()))

    def get(self, *keys):
        return set.intersection(*(self[key] for key in keys))
