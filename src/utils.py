def find(data: list, fun):
    for i in data:
        if fun(i):
            return i


class DuplicateError(Exception):
    pass
