import unittest

from domain.utils import filter_dictionary


class UtilsTestCase(unittest.TestCase):
    def test_filter_dictionary(self):
        data = [
            {},
            {'name': 'John', 'age': 25, 'city': 'New York'},
            {'name': 'Greg', 'age': 25, 'city': 'New York', 'occupation': 'Programmer'},
            {'name': 'Alice', 'age': 30, 'city': 'Los Angeles'},
            {'name': 'Bob', 'age': 20},
            {'name': 'Charlie', 'age': 35, 'city': 'Chicago'},
            {'name': 'David', 'age': 40, 'city': 'San Francisco'},
            {'name': 'Eve', 'age': 45, 'city': 'Boston', 'occupation': 'Engineer'}
        ]

        filters = {'city': 'New York', 'age': 25}
        expected = [{'name': 'John', 'age': 25, 'city': 'New York'},
                    {'name': 'Greg', 'age': 25, 'city': 'New York', 'occupation': 'Programmer'}]

        actual = filter_dictionary(data, filters)
        self.assertEqual(len(expected), len(actual))
        self.assertEqual(expected, actual)

    def test_filter_dictionary_when_filter_is_empty(self):
        data = [
            {},
            {'name': 'John', 'age': 25, 'city': 'New York'},
            {'name': 'Greg', 'age': 25, 'city': 'New York', 'occupation': 'Programmer'},
            {'name': 'Alice', 'age': 30, 'city': 'Los Angeles'},
            {'name': 'Bob', 'age': 20},
            {'name': 'Charlie', 'age': 35, 'city': 'Chicago'},
            {'name': 'David', 'age': 40, 'city': 'San Francisco'},
            {'name': 'Eve', 'age': 45, 'city': 'Boston', 'occupation': 'Engineer'}
        ]

        filters = {}

        # Empty filter act as 'no filter' so we get the data back
        expected = data
        actual = filter_dictionary(data, filters)

        self.assertEqual(len(expected), len(actual))
        self.assertEqual(expected, actual)
