codes: dict[int: str] = dict()
# following errors are rather trivial and might be logged
codes[100] = "Forced Closing Failed"
codes[200] = "No Socket Selected"
codes[300] = "Can't Send, Client Disconnected"
codes[400] = "Client Did Not Send Anything"
codes[500] = "No Socket Selected"
# following errors are less trivial and get used by the exit functions
codes[2000] = "Port Still In Use"
codes[4200] = "Socket Value is -1 After Select()"
codes[4201] = "Unknown Exception"
codes[6000] = "Broken Client List; Elem 'sockets' Not There"
codes[6001] = "Trying to delete non existing Data"
codes[7000] = "unexpected exception in close_connection"


def __set_error_code(err: int, msg: str):
    codes[err] = msg


def err_to_str(err: int) -> str:
    return codes[err]


def error_code(err: int) -> str:
    """Returns string to error code"""
    return err_to_str(err)
