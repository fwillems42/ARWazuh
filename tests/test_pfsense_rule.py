import unittest

from api.pfsense_api import PfSenseRule


class PfSenseApiTestCase(unittest.TestCase):
    def test_create_empty_rule(self):
        expected = {
            "type": "pass",
            "interface": "lan",
            "ipprotocol": "inet46",
            "protocol": "tcp/udp",
            "src": "any",
            "srcport": "any",
            "dst": "any",
            "dstport": "any",
            "descr": "Pattern rule",
            "top": True,
            "apply": True
        }

        actual = PfSenseRule.create_custom_rule({})

        expected_len = len(expected.keys())
        actual_len = len(actual.keys())

        self.assertEqual(expected_len, actual_len,
                         f"Wrong number of properties: expected {expected_len} got {actual_len}")

        for key, value in expected.items():
            self.assertEqual(value, actual[key], f"Should be {value} for {key} got {actual[key]}")

    def test_create_custom_rule(self):
        expected = {
            "type": "pass",
            "interface": "lan",
            "ipprotocol": "inet46",
            "protocol": "tcp/udp",
            "src": "10.10.15.55",
            "srcport": "any",
            "dst": "any",
            "dstport": "any",
            "descr": "Block all traffic from 10.10.15.55",
            "top": True,
            "apply": True
        }

        custom_data = {"interface": "lan",
                       "src": "10.10.15.55",
                       "descr": f"Block all traffic from 10.10.15.55"}

        actual = PfSenseRule.create_custom_rule(custom_data)

        expected_len = len(expected.keys())
        actual_len = len(actual.keys())

        self.assertEqual(expected_len, actual_len,
                         f"Wrong number of properties: expected {expected_len} got {actual_len}")

        for key, value in expected.items():
            self.assertEqual(value, actual[key], f"Should be {value} for {key} got {actual[key]}")
