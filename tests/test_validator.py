import unittest

from validator import Validator


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


if __name__ == '__main__':
    unittest.main()
