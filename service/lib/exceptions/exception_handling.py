

import traceback
from sys import exit


class SelectException(Exception):

    __str__ = "Select Returned No Valid Socket"


def handle_exception_and_exit(e: Exception, exitcode):
    """Using this function for exceptions that make it impossible to run the server any longer"""
    print(e)
    print(traceback.format_exc())
    # print_error_code(exitcode)
    exit(exitcode)


def print_exception_str(e: Exception):
    """Might get used for logging"""
    print(f"closing failed = {e.__str__()}")
