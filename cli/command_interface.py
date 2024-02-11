from cli.command_handler import CommandHandler, command_info, command_pattern, command_match, command_gen
from cli.utils import CheckExt
from saso.algorithm.pattern import Pattern


@CommandHandler('info', command_info)
def cli_saso_visualizer(parser: []):
    parser_mark = parser[0].add_parser('info',
                                       help='Print information about the file')
    parser_mark.add_argument('file_path',
                             action=CheckExt({'psaso', 'saso'}),
                             help='the path to file')

    parser_mark.add_argument('-v', '--verbose',
                             dest='is_verbose',
                             action='store_true',
                             required=False,
                             help="print verbose information")

    parser_mark.add_argument('-q', '--quiet',
                             dest='is_quiet',
                             action='store_true',
                             required=False,
                             help="don't print visualization of slices")

    parser_mark.add_argument('-w',
                             dest='w',
                             action='store',
                             default=80,
                             type=int,
                             required=False,
                             help="set width of the slice table")

    parser_mark.add_argument('-hm',
                             dest='hm',
                             action='store',
                             default=1,
                             type=int,
                             required=False,
                             help="set horizont margin of the slice table")

    parser_mark.add_argument('-vm',
                             dest='vm',
                             action='store',
                             default=1,
                             type=int,
                             required=False,
                             help="set vertical margin of the slice table")

    parser_mark.add_argument('--symbol',
                             dest='table_sym',
                             action='store',
                             default='■',
                             type=str,
                             required=False,
                             help="set cell symbol of the slice table")

    parser_mark.add_argument('--row-num',
                             dest='print_row_num',
                             action='store_false',
                             required=False,
                             help="disable row numeration of the slice table")

    parser_mark.add_argument('--cell-numeric',
                             dest='is_cell_numeric',
                             action='store_true',
                             default=False,
                             required=False,
                             help="print count in the cells")


@CommandHandler('pattern', command_pattern)
def cli_saso_pattern(parser: []):
    parser_mark = parser[0].add_parser('pattern',
                                       help="Get the pattern of the file's records")
    parser_mark.add_argument('file_path',
                             action=CheckExt({'saso'}),
                             help='the path to file')

    parser_mark.add_argument('-v', '--verbose',
                             dest='is_verbose',
                             action='store_true',
                             required=False,
                             help="print verbose information")

    parser_mark.add_argument('-q', '--quiet',
                             dest='is_quiet',
                             action='store_true',
                             required=False,
                             help="less information")

    parser_mark.add_argument('-m',
                             dest='method',
                             required=True,
                             type=Pattern.from_string,
                             choices=list(Pattern),
                             help="type of the pattern to calculate")

    parser_mark.add_argument('-c', '--comment',
                             dest='comment',
                             required=False,
                             default="",
                             type=str,
                             help="set an inner comment to the output file")

    # n_method = ", ".join(Pattern.get_arg_using_method('n'))
    # parser_mark.add_argument('-n',
    #                          dest='n',
    #                          action='store',
    #                          default=0,
    #                          type=int,
    #                          required=False,
    #                          help=f"level of merging. Uses in: {n_method}")

    k_method = ", ".join(Pattern.get_arg_using_method('k'))
    parser_mark.add_argument('-k',
                             dest='k',
                             action='store',
                             default=0,
                             type=int,
                             required=False,
                             help=f"amplification factor. Uses in: {k_method}")


@CommandHandler('match', command_match)
def cli_saso_match(parser: []):
    parser_mark = parser[0].add_parser('match',
                                       help="Calculate the matching coefficient")
    parser_mark.add_argument('file_path',
                             action=CheckExt({'saso'}),
                             help='the path to .saso file')

    parser_mark.add_argument('-v', '--verbose',
                             dest='is_verbose',
                             action='store_true',
                             required=False,
                             help="print verbose information")

    parser_mark.add_argument('-q', '--quiet',
                             dest='is_quiet',
                             action='store_true',
                             required=False,
                             help="less information")

    parser_mark.add_argument('-p',
                             dest='pattern_file',
                             action=CheckExt({'psaso'}),
                             required=True,
                             help="the .psaso file to match with")

    parser_mark.add_argument('-e',
                             dest='precision',
                             default=1,
                             type=int,
                             help="set percent precision")


@CommandHandler('gen', command_gen)
def cli_saso_gen(parser: []):
    parser_mark = parser[0].add_parser('gen',
                                       help="Generate a saso/psaso file")

    parser_mark.add_argument('-l', dest='count_list',
                             action='store',
                             required=True,
                             nargs="+",
                             type=int,
                             help="list of counts. Each index means the value")

    parser_mark.add_argument('-v', '--verbose',
                             dest='is_verbose',
                             action='store_true',
                             required=False,
                             help="print verbose information")

    parser_mark.add_argument('-q', '--quiet',
                             dest='is_quiet',
                             action='store_true',
                             required=False,
                             help="less information")

    parser_mark.add_argument('-c', '--comment',
                             dest='comment',
                             required=False,
                             default="",
                             type=str,
                             help="set an inner comment to the output .psaso file")

    parser_mark.add_argument('-sp', '--slicing-per',
                             dest='slicing_per',
                             action='store',
                             required=False,
                             default=0,
                             type=int,
                             help="set slicing period of the record (for .saso)")

    parser_mark.add_argument('-d', '--duration',
                             dest='duration',
                             action='store',
                             default=0,
                             required=False,
                             type=int,
                             help="set duration of the record (for .saso)")

    parser_mark.add_argument('--out',
                             dest='out_format',
                             action='store',
                             required=False,
                             default='saso',
                             choices=['saso', 'psaso'],
                             help="deserialize file to the desired format")