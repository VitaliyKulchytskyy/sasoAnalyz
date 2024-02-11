import struct
from saso.sliceCollection import SliceCollectionType


class RecordType(SliceCollectionType):
    @staticmethod
    def serialize(byte_array: []):
        metadata = {
            'slicing_per': struct.unpack('Q', byte_array[:8])[0],
            'duration': struct.unpack('i', byte_array[8:12])[0],
        }
        output = RecordType(**metadata)
        temp = SliceCollectionType.serialize(byte_array[12:])
        output.slices = temp.slices
        return output

    def deserialize(self) -> bytes:
        slicing_per = struct.pack('Q', self.slicing_per)
        duration = struct.pack('i', self.duration)
        return slicing_per + duration + super().deserialize()

    def __init__(self, slices=None, slicing_per=0, duration=0, **kwargs):
        super().__init__(slices)
        self.slicing_per = kwargs.get('slicing_per', slicing_per)
        self.duration = kwargs.get('duration', duration)

    def print(self):
        print(f"Slicing Period: {self.slicing_per} mcs\nDuration: {self.duration} ms")
        for count, s in enumerate(self.slices):
            print(f"Slice [{count}]:")
            s.print('\t')

    def size(self):
        return 8 + 4 + super().size()

    def __repr__(self):
        return repr((self.slicing_per, self.duration, super().__repr__()))
