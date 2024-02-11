import struct
from saso.algorithm.distribution import distribution
from saso.formatBase import FormatBase
from saso.mathBase import MathBase
from saso.valueType import ValueType


class SliceType(FormatBase, MathBase):
    max_elements = 2560

    @staticmethod
    def serialize(byte_array: []):
        shift = 4
        size = struct.unpack('i', byte_array[:shift])[0]
        output = SliceType()

        for i in range(size):
            temp = ValueType()
            output.array.append(temp.serialize(byte_array[shift:shift + temp.size()]))
            shift += temp.size()

        return output

    def deserialize(self) -> bytes:
        size_bytes = struct.pack('i', len(self.array))
        deserialized_slices = b''
        for item in self.array:
            deserialized_slices += item.deserialize()
        return size_bytes + deserialized_slices

    def __init__(self, array=None, **kwargs):
        if array is None:
            array = []
        self.array = kwargs.get('array', array)

    def size(self):
        temp = ValueType()
        return 4 + len(self) * temp.size()

    def print(self, start: str = ""):
        for value in self.array:
            print(start + str(value))

    def __repr__(self):
        return repr((len(self), self.array.__repr__()))

    def __iter__(self):
        return iter(self.array)

    def __getitem__(self, item) -> ValueType:
        return self.array[item]

    def __eq__(self, other):
        if len(self) != len(other):
            return False

        for value in zip(self.array, other.array):
            if not (value[0].value == value[1].value and value[0].count == value[1].count):
                return False

        return True

    def _operation(self, other, operands_handler):
        if not isinstance(other, SliceType):
            raise ValueError

        if not other.array:
            return SliceType(array=self.array)
        if not self.array:
            return SliceType(array=other.array)

        this_sorted = SliceType(array=sorted(self))
        other_sorted = SliceType(array=sorted(other))
        output = SliceType()
        i = j = k = 0

        def increment(value: int, max_value: int) -> int:
            return 1 if value + 1 < max_value else 0

        while i <= max(this_sorted[-1].value, other_sorted[-1].value):
            temp = ValueType()

            if i == this_sorted[j].value == other_sorted[k].value:
                temp = operands_handler(this_sorted[j], other_sorted[k])
                j += increment(j, len(this_sorted))
                k += increment(k, len(other_sorted))
            elif i == this_sorted[j].value:
                temp = operands_handler(this_sorted[j], ValueType(value=i))
                j += increment(j, len(this_sorted))
            elif i == other_sorted[k].value:
                temp = operands_handler(ValueType(value=i), other_sorted[k])
                k += increment(k, len(other_sorted))

            output.append(temp)
            i += 1

        return output

    def _slice_operation(self, other, operands_handler):
        if not isinstance(other, int | float):
            raise ValueError
        if other == 1:
            return self

        value_array = []
        for value in self:
            temp = operands_handler(value, other)
            if temp.count > 0:
                value_array.append(temp)

        return SliceType(array=value_array)

    def __mul__(self, other):
        if other < 0:
            raise ValueError("Cannot multiply with negative values")

        return self._slice_operation(other, lambda x, a: x * a)

    def __truediv__(self, other):
        if other < 0:
            raise ValueError("Cannot divide with negative values")

        return self._slice_operation(other, lambda x, a: x / a)

    def __floordiv__(self, other):
        if other < 0:
            raise ValueError("Cannot divide with negative values")

        return self._slice_operation(other, lambda x, a: x // a)

    def __len__(self):
        return len(self.array)

    def merge(self, other):
        if not isinstance(other, SliceType):
            raise ValueError

        return (self + other) // 2

    def append(self, other: ValueType):
        if other.count > 0:
            self.array.append(other)

    def mask(self, other):
        return self._operation(other, lambda x, a: x if a.value == x.value and a.count > 0 else ValueType())

    def union(self, other):
        return self._operation(other, lambda x, a: x if x.count > 0 else a)

    @staticmethod
    def value_to_coef_map(value: ValueType, distrub_percent, real_length):
        if value.count == 0:
            raise ValueError("The count must be greater than 0")

        length = value.count * 2 + 1
        half = length // 2
        start = value.value - half
        end = value.value + half
        shift = 0

        if end >= real_length:
            shift = real_length - length
            end -= end - real_length + 1
        if start < 0:
            shift = start
            start = 0
        if length < 0 or length > real_length:
            start = 0
            shift = 0
            end = real_length - 1

        length = end - start + 1
        d = value.value - (end + start) // 2 + shift
        coef_map = distribution(distrub_percent, int(length), d)

        temp = SliceType()
        for count, i in enumerate(coef_map):
            temp.append(ValueType(value=start + count, count=i))

        return temp

    @staticmethod
    def _get_distrub_coef_map(pattern, distrub_percent, real_length):
        output = SliceType()

        for value in pattern:
            output += SliceType.value_to_coef_map(value, distrub_percent, real_length)

        return output

    def calc_eq_coef(self, pattern, real_length=max_elements) -> float:
        if not isinstance(pattern, SliceType):
            raise ValueError
        if len(self) == 0 or len(pattern) == 0:
            return 0

        max_distribution = 1 / len(pattern)
        coef_map = self._get_distrub_coef_map(pattern, max_distribution, real_length)
        result = self._operation(coef_map, lambda x, a: a * (1 if x.count >= 1 else 0))
        return sum([x.count for x in result])

    def range_mask(self, other, e=None):
        if not isinstance(e, int | None):
            raise ValueError("e must be an integer or None")
        if e is not None and e < 0:
            raise ValueError("e must be positive")
        if e == 0:
            return self.mask(other)

        output = SliceType()

        for i in other:
            low_temp = i.value - (i.count if e is None else e)
            low_boundary = low_temp if low_temp >= 0 else 0
            high_boundary = i.value + (i.count if e is None else e) + 1
            temp_slice = SliceType(array=list(map(lambda x: ValueType(value=x, count=1), range(low_boundary,
                                                                                               high_boundary))))
            output = output.union(self.mask(temp_slice))
        return output
