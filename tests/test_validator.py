import unittest

from domain.validator import Validator


class BanIpTestCase(unittest.TestCase):
    def test_validation_ip(self):
        data = [
            ("10.10.15.20", True),
            ("260.250.230.1", False),
            ("", False),
            (" ", False),
            ("  20.10 0.25.3", False),
            (";id", False),
            (" 210.25.10.3", False)
        ]

        for case, expected in data:
            out = Validator.validate_ip(case)
            self.assertEqual(out, expected, f"Should be {expected} for {case}")


class KillProcessTestCase(unittest.TestCase):
    def test_validation_pid(self):
        data = [
            ("10", True),
            ("-29", False),
            ("0", False),
            ("-0", False),
            ("Abracadabra", False),
            ("17test", False),
            ("", False),
            (" ", False),
            (" 18", True)
        ]

        for case, expected in data:
            out = Validator.validate_pid(case)
            self.assertEqual(out, expected, f"Should be {expected} for {case}")


class RemoveThreatTestCase(unittest.TestCase):
    def test_validation_path(self):
        data = [
            ("../../abc", False),
            ("/var/log/", True),
            ("hello", False),
            ("C:\\test", True),
            (" /test", False),
            ("", False),
            (" ", False)
        ]

        for case, expected in data:
            out = Validator.validate_path(case)
            self.assertEqual(out, expected, f"Should be {expected} for {case}")


class IsolateDeviceTestCase(unittest.TestCase):
    def test_validation_mac(self):
        data = [
            ("e7:0f:9b:44:23:86", True),
            ("68:d6:ef:f5:09:ed", True),
            ("de:7a:7d:0d:46:d8", True),
            ("14:c0:ec:f1:6b:99", True),
            ("68:9d:ae:31:ab:a4", True),
            ("db-aa-52-10-c6-fc", True),
            ("eb-62-2e-a9-00-da", True),
            ("9e-c2-65-ef-19-dc", True),
            ("9b-d6-d8-8f-06-b3", True),
            ("ba-18-da-ee-5b-0a", True)
        ]

        for case, expected in data:
            out = Validator.validate_mac(case)
            self.assertEqual(out, expected, f"Should be {expected} for {case}")


if __name__ == '__main__':
    unittest.main()
