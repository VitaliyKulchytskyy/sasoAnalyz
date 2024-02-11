import os
import argparse
from cli.command_interface import *


def invoke_by_command(parser):
    if CommandHandler.command_list.get(parser.command) is not None:
        CommandHandler.command_list[parser.command](parser)
    else:
        raise Exception("Unknown command")


def cli_parser():
    parser = argparse.ArgumentParser(prog="saso",
                                     description='The utils to work with .saso files')

    subparsers = parser.add_subparsers(dest='command',
                                       help='Available commands')
    sub = [subparsers]

    cli_saso_visualizer(sub)
    cli_saso_pattern(sub)
    cli_saso_match(sub)
    cli_saso_gen(sub)

    parsed = parser.parse_args()

    if (hasattr(parsed, "file_path")
            and not os.path.exists(parsed.file_path)):
        raise FileNotFoundError(f"The file '{parsed.file_path}' does not exist")

    return parsed
