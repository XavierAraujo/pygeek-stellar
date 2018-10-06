

def is_float_str(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
