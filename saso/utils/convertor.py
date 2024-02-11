from saso.sliceType import SliceType
from saso.valueType import ValueType


def list_to_slice(in_list: []):
    output = []

    for value, count in enumerate(in_list):
        if count == 0:
            continue
        output.append(ValueType(value=value, count=count))

    return SliceType(array=output)
