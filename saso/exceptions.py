class ValueNotEqualException(Exception):
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2

    def __str__(self):
        return f'{self.v1} != {self.v2}'


class ValueLessZeroException(Exception):
    def __init__(self, v, param):
        self.v = v
        self.param = param

    def __str__(self):
        return f'{self.v}: {self.param} < 0'
