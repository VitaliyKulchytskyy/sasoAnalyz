import codecs
import struct
from saso.formatBase import FormatBase
from saso.sliceType import SliceType


class PatternType(FormatBase):
    @staticmethod
    def serialize(byte_array: []):
        shift = 4
        comment_len = struct.unpack('i', byte_array[:shift])[0]
        comment = struct.unpack("%ds" % comment_len, byte_array[shift:shift + comment_len])[0]
        shift += comment_len

        return PatternType(**{
            'comment': codecs.decode(comment, 'utf-8'),
            'slice_obj': SliceType.serialize(byte_array[shift:])
        })

    def deserialize(self) -> bytes:
        command_len = struct.pack('i', len(self.comment))
        return command_len + self.comment.encode() + self.slice_obj.deserialize()

    def __init__(self, slice_obj=None, comment="", **kwargs):
        if slice_obj is None:
            slice_obj = []

        self.slice_obj = kwargs.get('slice_obj', slice_obj)
        self.comment: str = kwargs.get('comment', comment)

    def size(self):
        return 4 + len(self.comment) + self.slice_obj.size()

    def __repr__(self):
        return repr((len(self.comment), self.comment, self.slice_obj))