class MathBase:
    def _operation(self, other, operands_handler):
        pass

    def __add__(self, other):
        return self._operation(other, lambda x, a: x + a)

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        return self._operation(other, lambda x, a: x * a)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __imul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        return self._operation(other, lambda x, a: x / a)

    def __floordiv__(self, other):
        return self._operation(other, lambda x, a: x // a)
