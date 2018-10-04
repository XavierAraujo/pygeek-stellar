
def yes_or_no_input(msg):
    full_msg = '{} (y/n): '.format(msg)
    answer = input(full_msg)
    while answer not in ['y','n']:
        answer = input(full_msg)
    return answer