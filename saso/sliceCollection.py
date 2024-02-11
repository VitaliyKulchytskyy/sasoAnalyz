import struct
from saso.formatBase import FormatBase
from saso.sliceType import SliceType


class SliceCollectionType(FormatBase):
    @staticmethod
    def serialize(byte_array: []):
        size = struct.unpack('i', byte_array[:4])[0]
        offset = 4
        output = SliceCollectionType()

        for i in range(size):
            temp = SliceType.serialize(byte_array[offset:])
            output.slices.append(temp)
            offset += temp.size()

        return output

    def deserialize(self) -> bytes:
        size_bytes = struct.pack('i', len(self.slices))
        deserialized_slices = b''
        for item in self.slices:
            deserialized_slices += item.deserialize()
        return size_bytes + deserialized_slices

    def __init__(self, slices=None, **kwargs):
        if slices is None:
            slices = []
        self.slices = kwargs.get('slices', slices)

    def size(self):
        return sum(map(lambda x: x.size(), self.slices))

    def append(self, s: SliceType):
        self.slices.append(s)

    def __repr__(self):
        return repr((len(self.slices), self.slices))

    def __len__(self):
        return len(self.slices)

    def __getitem__(self, item):
        return self.slices[item]
