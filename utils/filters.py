

def number_split(num):
    """
    12345678 => 12,345,678
    :param num: the number needs to be formulated
    :return: the string converted from formulated number
    """
    return '{:,}'.format(int(num))
