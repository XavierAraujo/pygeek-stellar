
USER_INPUT_YES = 'y'
USER_INPUT_NO = 'n'


def int_input(msg):
    try:
        return int(safe_input(msg), base=10)
    except ValueError:
        print('Input must be a valid integer value')
        int_input(msg)


def yes_or_no_input(msg):
    full_msg = '{} ({}/{})'.format(msg, USER_INPUT_YES, USER_INPUT_NO)
    answer = safe_input(full_msg)
    while answer.lower() not in [USER_INPUT_YES, USER_INPUT_NO]:
        answer = safe_input(full_msg)
    return answer


def safe_input(msg):
    """
    This method extends the system built input() method to process KeyboardInterrupt
    signals (ctr+c) and exiting the script gracefully.
    """
    try:
        return input('{}: '.format(msg))
    except KeyboardInterrupt:
        print('\n\nExiting..')
        raise SystemExit
