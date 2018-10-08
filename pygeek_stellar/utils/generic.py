# System imports
import json
from json import JSONDecodeError


def is_float_str(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def is_int_str(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def is_in_range(val, min, max):
    return True if min <= val <= max else False


def is_sucessful_http_status_code(status_code):
    return is_in_range(status_code, 200, 299)


def decode_json_content(content):
    try:
        return json.loads(content) if content is not None else None
    except JSONDecodeError:
        print("The given content could not be decoded as a JSON file")
        return None
