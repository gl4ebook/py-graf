import argparse
import logging
import sys
from typing import Any, Optional, Tuple, Set

from pygraf import __version__

logger = logging.getLogger(__name__)


class ArgumentParserWithDefaults(argparse.ArgumentParser):
    """
    Custom argument parser that will display the default value for an argument
    in the help message.
    """

    _action_defaults_to_ignore = {"help", "store_true", "store_false", "store_const"}

    @staticmethod
    def _is_empty_default(default: Any) -> bool:
        if default is None:
            return True
        if isinstance(default, (str, list, tuple, set)):
            return not bool(default)
        return False

    def add_argument(self, *args, **kwargs):
        # Add default value to the help message when the default is meaningful.
        default = kwargs.get("default")
        if kwargs.get(
            "action"
        ) not in self._action_defaults_to_ignore and not self._is_empty_default(default):
            description = kwargs.get("help", "")
            kwargs["help"] = f"{description} (default = {default})"
        super().add_argument(*args, **kwargs)


def parse_args(prog: Optional[str] = None) -> Tuple[argparse.ArgumentParser, argparse.Namespace]:
    """
    Creates the argument parser for the main program and uses it to parse the args.
    """
    parser = ArgumentParserWithDefaults(description="Run Py-graf", prog=prog)
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(title="Commands", metavar="")

    subcommands: Set[str] = set()

    def add_subcommands():
        raise NotImplementedError

    # Add all default registered subcommands first.
    add_subcommands()

    # Now we can parse the arguments.
    args = parser.parse_args()

    return parser, args


def main(prog: Optional[str] = None) -> None:

    parser, args = parse_args(prog)

    # If a subparser is triggered, it adds its work as `args.func`.
    # So if no such attribute has been added, no subparser was triggered,
    # so give the user some help.
    if "func" in dir(args):
        args.func(args)
    else:
        parser.print_help()