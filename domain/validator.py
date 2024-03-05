import ipaddress
import os.path


class Validator(object):
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
