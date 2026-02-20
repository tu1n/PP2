def sum_all(*args):
    total = 0
    for num in args:
        total += num
    return total


def show_info(**kwargs):
    for key in kwargs:
        print(key, kwargs[key])
