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


def decode_json_content(content):
    try:
        return json.loads(content) if content is not None else None
    except JSONDecodeError:
        print("The given content could not be decoded as a JSON file")
        return None
