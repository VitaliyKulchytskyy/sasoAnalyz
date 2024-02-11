import sys
from rich.console import Console
from saso.algorithm.pattern import Pattern
from saso.patternType import PatternType
from saso.recordType import RecordType
from saso.utils.convertor import list_to_slice
from saso.utils.visualization import get_slice_table


class CommandHandler(object):
    command_list = {}

    def __init__(self, *args):
        self._args = args

    def __call__(self, func):
        CommandHandler.command_list[self._args[0]] = self._args[1]

        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper


def print_pattern(parser):
    with open(parser.file_path, 'rb') as f:
        read = f.read()
        pattern = PatternType.serialize(read)

        if parser.is_verbose:
            print(f"Comment: {pattern.comment}.\n")

        if parser.is_quiet:
            return

        Console().print(get_slice_table(pattern.slice_obj, **vars(parser)))


def print_record(parser):
    with open(parser.file_path, 'rb') as f:
        read = f.read()
        record = RecordType.serialize(read)

        if not parser.is_quiet:
            Console().rule(f.name, align="center")

        if parser.is_verbose:
            print(f"Slicing period:\t{record.slicing_per} (mu);")
            print(f"Duration:\t{record.duration / 1000} (sec);")
            print(f"Slices:\t\t{len(record.slices)}.")

        if parser.is_quiet:
            return

        for count, s in enumerate(record):
            Console().rule(str(count), align="left")
            Console().print(get_slice_table(s, **vars(parser)))


def command_info(parser):
    file_ext = parser.file_path.split(".")

    match file_ext[1]:
        case 'saso':
            print_record(parser)
        case 'psaso':
            print_pattern(parser)
        case _:
            raise ValueError(f"Invalid file extension: {file_ext}")


def command_pattern(parser):
    with open(parser.file_path, 'rb') as f:
        read = f.read()
        record = RecordType.serialize(read)
        method = Pattern[str(parser.method)].get_method()
        # TODO: transmit k via kwargs into the method funct
        pattern = PatternType(comment=parser.comment, slice_obj=method(record, **vars(parser)))

    sys.stdout.buffer.write(pattern.deserialize())
    # sys.stdout.flush()


def command_match(parser):
    with open(parser.pattern_file, 'rb') as f:
        read = f.read()
        pattern = PatternType.serialize(read)

    with open(parser.file_path, 'rb') as f:
        read = f.read()
        record = RecordType.serialize(read)

    for count, s in enumerate(record):
        print(f"Slice: {count}")
        print(f"Coefficient: {s.calc_eq_coef(pattern.slice_obj):.{parser.precision}%}\n")


def command_gen(parser):
    temp = list_to_slice(parser.count_list)
    out_format = {'saso': RecordType(slices=[temp],
                                     slicing_per=parser.slicing_per,
                                     duration=parser.duration),
                  'psaso': PatternType(slice_obj=temp,
                                       comment=parser.comment)}

    sys.stdout.buffer.write(out_format[parser.out_format].deserialize())
    # sys.stdout.flush()
