from typing import Callable
from argparse import ArgumentParser, Namespace


def main_callback(args: Namespace):
    print(f"main args: {args}")


def config_callback(args: Namespace):
    print(f"config args: {args}")


def create_callback(args: Namespace):
    print(f"create args: {args}")


def download_callback(args: Namespace):
    print(f"download args: {args}")


def tools_callback(args: Namespace):
    print(f"tools args: {args}")


def tool1_callback(args: Namespace):
    print(f"tool1 args: {args}")


def tool2_callback(args: Namespace):
    print(f"tool1 args: {args}")


def set_parser_callback(parser, callback):
    parser.set_defaults(callback=callback, parser=parser)


def add_parser(sub, name: str, callback: Callable[[Namespace], None]) -> ArgumentParser:
    """Add and return sub-parser with a callback handler.
    """
    parser = sub.add_parser(name)
    set_parser_callback(parser, callback)
    return parser


def tools_parser_init(parser: ArgumentParser):
    """Initialize tools subparser.
    """
    sub = parser.add_subparsers()
    add_parser(sub, "tool1", tool1_callback)
    add_parser(sub, "tool2", tool2_callback)


def main_parser_init(parser: ArgumentParser):
    """Initialize and return main parser.
    """
    set_parser_callback(parser, main_callback)

    # initialize sub-commands
    sub = parser.add_subparsers()
    add_parser(sub, "config", config_callback)
    add_parser(sub, "create", create_callback).add_argument("SOURCE")
    add_parser(sub, "download", download_callback)
    tools_parser_init(add_parser(sub, "tools", tools_callback))
    return parser


def parse_args():
    """Parse command-line arguments.
    """
    args = main_parser_init(ArgumentParser()).parse_args()
    args.callback(args)  # execute callback


if __name__ == "__main__":
    parse_args()
