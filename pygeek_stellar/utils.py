

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
