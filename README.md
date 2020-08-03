# Multidict
## [From a tweet by @mkennedy](https://twitter.com/mkennedy/status/1288961022724734976)

A collection of objects retrievable by their attribute values via dictionary lookup.

```python
from multidict import Multidict

from collections import namedtuple

Person = namedtuple("Person", "name address")
Address = namedtuple("Address", "city")

address = Address(city='Portland')
michael = Person(name='Michael', address=address)
kennedy = Person(name='Kennedy', address=address)

d = Multidict('name', 'address.city')

d.add(michael)
d.add(kennedy)

assert d['Portland'] == {michael, kennedy}
assert d['Michael'] == {michael}

```