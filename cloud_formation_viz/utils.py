import collections


def flatten(x):
    result = []
    for el in x:
        if isinstance(x, collections.Iterable) and not isinstance(el, dict):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result