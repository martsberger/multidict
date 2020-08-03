from multidict import get_deep_attr, Multidict

from collections import namedtuple

Person = namedtuple("Person", "name address")
Address = namedtuple("Address", "city")


def test_get_deep_attr():
    address = Address(city='Portland')
    person = Person(name='Michael', address=address)

    assert get_deep_attr(person, 'name') == 'Michael'
    assert get_deep_attr(person, 'address.city') == 'Portland'
    assert get_deep_attr(person, 'not.an.attribute') is None
    assert get_deep_attr(person, 'address.country') is None


def test_retrieve_one_entry():
    address = Address(city='Portland')
    person = Person(name='Michael', address=address)

    d = Multidict('name', 'address.city')

    d.add(person)

    assert d['Portland'] == {person}
    assert d['Michael'] == {person}
    assert d['No entry'] == set()


def test_retrieve_two_entries():
    address = Address(city='Portland')
    michael = Person(name='Michael', address=address)
    kennedy = Person(name='Kennedy', address=address)

    d = Multidict('name', 'address.city')

    d.add(michael)
    d.add(kennedy)

    assert d['Portland'] == {michael, kennedy}
    assert d['Michael'] == {michael}


def test_index_with_no_data():
    address = Address(city='Portland')
    person = Person(name='Michael', address=address)

    d = Multidict('name', 'address.city', 'unpopulated.field')

    d.add(person)

    assert d['Portland'] == {person}
    assert d['Michael'] == {person}
    assert d['No entry'] == set()


def test_item_has_extra_fields():
    address = Address(city='Portland')
    person = Person(name='Michael', address=address)

    d = Multidict('name')

    d.add(person)

    assert d['Portland'] == set()
    assert d['Michael'] == {person}


def test_multiple_key_get():
    address = Address(city='Portland')
    michael = Person(name='Michael', address=address)
    kennedy = Person(name='Kennedy', address=address)

    d = Multidict('name', 'address.city')

    d.add(michael)
    d.add(kennedy)

    assert d.get('Portland', 'Michael') == {michael}


def test_add_index():
    address = Address(city='Portland')
    person = Person(name='Michael', address=address)

    d = Multidict('name')

    d.add(person)

    d.add_indexes('address.city')

    assert d['Portland'] == {person}
    assert d['Michael'] == {person}
