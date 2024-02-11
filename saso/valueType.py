import struct
from saso.exceptions import ValueLessZeroException, ValueNotEqualException
from saso.formatBase import FormatBase
from saso.mathBase import MathBase


class ValueType(FormatBase, MathBase):
    max_value = 4080

    @staticmethod
    def serialize(byte_array: []):
        return ValueType(**{
            'value': struct.unpack('i', byte_array[0:4])[0],
            'count': struct.unpack('i', byte_array[4:8])[0],
        })

    def deserialize(self) -> bytes:
        value_bytes = struct.pack('i', self.value)
        count_bytes = struct.pack('i', int(self.count))
        return value_bytes + count_bytes

    def __init__(self, value: int = 0, count: int | float = 0.0, **kwargs):
        self.value: int = kwargs.get('value', value)
        self.count: int | float = kwargs.get('count', count)

        if self.value < 0:
            raise ValueLessZeroException(self, self.value)
        if self.count < 0:
            raise ValueLessZeroException(self, self.count)

    def size(self):
        return 8

    def __lt__(self, other):
        return self.value < other.value

    def __repr__(self):
        return repr((self.value, self.count))

    def _operation(self, other, operands_handler):
        if not isinstance(other, ValueType):
            other = ValueType(value=self.value, count=other)

        if self.value != other.value:
            return ValueNotEqualException(self, other)
        return ValueType(value=self.value, count=operands_handler(self.count, other.count))
