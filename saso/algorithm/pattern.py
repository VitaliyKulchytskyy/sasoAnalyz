import inspect
from enum import Enum
from saso.recordType import RecordType
from saso.sliceType import SliceType


def slice_sum(slices: [], **kwargs) -> SliceType:
    sum_ = slices[0]
    for count, s in enumerate(slices):
        if count == 0:
            continue

        sum_ += s

    return SliceType(array=sum_)


def pattern_ray(slices: [], *, k: float = 1, **kwargs) -> SliceType:
    k = kwargs.get('k', k)

    if len(slices) == 1:
        output = slices[0]
        return output * k

    output = slice_sum(slices) // len(slices)
    return output * k


def pattern_pyramid(record: RecordType, *, n: int = 0, k: float = 1, **kwargs) -> RecordType | SliceType:
    k = kwargs.get('k', k)
    n = kwargs.get('n', n)

    if len(record) == 1:
        return record
    output = record
    count = 0

    while len(output) != 1:
        r_temp = RecordType()
        for i in range(1, len(output)):
            r_temp.append(output[i - 1].merge(output[i]) * k)

        output = r_temp
        count += 1
        if 0 < n == count:
            break

    return output if n > 0 else output[0]


def pattern_contest(record: RecordType, *, n: int = 0, k: float = 1, **kwargs) -> RecordType | SliceType:
    k = kwargs.get('k', k)
    n = kwargs.get('n', n)

    if len(record) == 1:
        return record
    output = record
    count = 0

    while len(output) != 1:
        r_temp = RecordType()
        for i in range(0, len(output), 2):
            if i + 1 < len(output):
                temp = output[i].merge(output[i + 1]) * k
            else:
                temp = output[i - 1].merge(output[i]) * k
            r_temp.append(temp)

        output = r_temp
        count += 1
        if 0 < n == count:
            break

    return output if n > 0 else output[0]


def pattern_avalanche(record: RecordType, **kwargs) -> SliceType:
    output: SliceType = record.slices[0]
    if len(record.slices) == 1:
        return output

    for i in range(1, len(record)):
        output = output.merge(record.slices[i])

    return output


class Pattern(Enum):
    sum = ("sum", slice_sum)
    ray = ("ray", pattern_ray)
    pyramid = ("pyramid", pattern_pyramid)
    contest = ("contest", pattern_contest)
    avalanche = ("avalanche", pattern_avalanche)

    @staticmethod
    def from_string(s):
        try:
            return Pattern[s]
        except KeyError:
            raise ValueError()

    @staticmethod
    def get_arg_using_method(value: str) -> []:
        output = []
        for method in list(Pattern):
            if value in inspect.getfullargspec(Pattern[str(method)].get_method()).args:
                output.append(str(method))

        return output

    def get_method(self):
        return self.value[1]

    def __str__(self):
        return self.value[0]
