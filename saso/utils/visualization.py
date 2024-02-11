from rich.text import Text
from rich.console import Console
from saso.recordType import RecordType
from saso.sliceType import SliceType
from saso.utils.colorConfig import ColorConfig
from utils import static_vars


def get_cell_str(symbol: str, hm: int) -> str:
    """
    Get a formatted cell string
    :param symbol: base symbol of a cell
    :param hm: horizontal margin between cells (number of spaces)
    :return: formatted cell string
    """
    return f'{symbol}{" " * hm}'


def print_as_matrix(s: SliceType, max_value: int, per_row: int):
    i = 0

    for count in range(max_value):
        to_print = "0"
        if count == s[i].value:
            to_print = str(s[i].count)
            if i + 1 < len(s):
                i += 1

        print(f"{to_print:3}", end="\n" if (count + 1) % per_row == 0 else "")


def get_slice_table(
        s: SliceType,
        *,
        w: int = 80,  # 40 by def
        hm: int = 1,
        vm: int = 1,
        table_sym: str = '■',
        print_row_num: bool = True,
        color_config: ColorConfig = ColorConfig.green_config(),
        is_cell_numeric: bool = False,
        **kwargs
) -> Text:
    """
    Get a colored table of a slice
    :param s: slice
    :param w: width of the table (number of cells in a row)
    :param hm: horizontal margin between cells (number of spaces)
    :param vm: vertical margin between cells (number of empty strings)
    :param table_sym: cell symbol used to
    :param print_row_num: print numeration of the rows
    :param color_config: color config
    :param is_cell_numeric: print counts in the cells
    :return: the colored table to print out
    """
    w = kwargs.get('w', w)
    hm = kwargs.get('hm', hm)
    vm = kwargs.get('vm', vm)
    table_sym = kwargs.get('table_sym', table_sym)
    print_row_num = kwargs.get('print_row_num', print_row_num)
    color_config = kwargs.get('color_config', color_config)
    is_cell_numeric = kwargs.get('is_cell_numeric', is_cell_numeric)

    w = w if w > 0 else 40
    hm = hm if hm > 0 else 1
    vm = vm if vm > 0 else 1

    cell = get_cell_str(table_sym, hm)
    rows = int(SliceType.max_elements / w)
    extra = SliceType.max_elements - rows * w
    output = Text()
    s_sorted = sorted(s)
    s_len = len(s_sorted)

    @static_vars(i=0)
    def get_count(value) -> int:
        out = 0

        if get_count.i < s_len:
            if s_sorted[get_count.i].value == value:
                out = s_sorted[get_count.i].count
                get_count.i += 1
        return out

    index = 0

    for row in range(rows):
        numeration = f"{index:4} |" if print_row_num else ""
        output.append(numeration + " " * hm)
        for column in range(w):
            index = row * w + column
            count = get_count(row * w + column)
            cell = cell if not is_cell_numeric else f"{count:{hm}}"
            output.append(cell, style=color_config[count])
        output.append("\n" * vm)

    for extra_row in range(SliceType.max_elements - extra, SliceType.max_elements):
        count = get_count(extra_row)
        cell = cell if not is_cell_numeric else f"{count:{hm}}"
        output.append(cell, style=color_config[count])
    output.append("\n" * vm)

    return output


def print_record_tables(record: RecordType):
    for count, s in enumerate(record.slices):
        Console().rule(f"Slice {count}", align="center")
        Console().print(get_slice_table(s))
