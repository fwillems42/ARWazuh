import ipaddress
import os.path


class Validator(object):
    """
    This class is used to validate data provided through AR in a cross-platform way
    """
    @staticmethod
    def validate_ip(ip_to_validate: str):
        try:
            ipaddress.ip_address(ip_to_validate)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_pid(pid_to_validate: str):
        try:
            pid = int(pid_to_validate)
            return pid > 0
        except ValueError as _:
            return False

    @staticmethod
    def validate_path(path_to_validate: str):
        return os.path.isabs(path_to_validate)

    @staticmethod
    def validate_mac(mac_to_validate: str):
        import re
        return re.match("([0-9a-f]{2}[:-]){5}([0-9a-f]{2})$", mac_to_validate.lower()) is not None

