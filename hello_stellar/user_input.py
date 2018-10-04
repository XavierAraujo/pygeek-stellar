
YES = 'y'
NO = 'n'


def yes_or_no_input(msg):
    full_msg = '{} ({}/{}): '.format(msg, YES, NO)
    answer = input(full_msg)
    while answer not in [YES, NO]:
        answer = input(full_msg)
    return answer