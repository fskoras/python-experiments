from typing import Callable
from argparse import ArgumentParser, Namespace


class ArgumentParserCallback(ArgumentParser):
    """Argument parser that force you to use callbacks to handle parser and sub-parsers.
    """
    def __init__(self, callback: Callable[[Namespace], None], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.callback_register(callback)  # callback exist on init

    def callback_register(self, callback: Callable[[Namespace], None]):
        self.set_defaults(callback=callback)

    def parse_args(self, args=None, namespace=None) -> Namespace:
        """Method overload to implicitly call parser callback.
        """
        ns = super().parse_args(args)
        ns.callback(ns)  # ensure set on init
        return ns


def main_callback_handler(ns: Namespace):
    print(f"main callback: {ns}")


def create_callback_handler(ns: Namespace):
    print(f"create callback: {ns}")


if __name__ == "__main__":
    parser = ArgumentParserCallback(callback=main_callback_handler)
    parser.add_argument("--list", action="store_true", help="list something")

    # sub-parsers config
    sub = parser.add_subparsers()
    create = sub.add_parser("create", callback=create_callback_handler)

    args = parser.parse_args()
