from cli.parser import cli_parser, invoke_by_command


def main():
    try:
        parser = cli_parser()
        invoke_by_command(parser)
    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    main()
