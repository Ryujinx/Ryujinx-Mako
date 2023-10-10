import argparse
import logging

from ryujinx_mako import commands
from ryujinx_mako._const import SCRIPT_NAME
from ryujinx_mako.commands import Subcommand

parser = argparse.ArgumentParser(
    prog=SCRIPT_NAME,
    description="A python module to aid Ryujinx with project management and moderation",
)

subparsers = parser.add_subparsers(
    title="subcommands",
    required=True,
)
subcommands = []

for subcommand in commands.SUBCOMMANDS:
    subcommand_parser = subparsers.add_parser(
        subcommand.name(),
        description=subcommand.description(),
        help=subcommand.description(),
    )
    Subcommand.add_subcommand(subcommand.name(), subcommand(subcommand_parser))
    # Keep a reference to the subcommand
    subcommands.append(Subcommand.get_subcommand(subcommand.name()))


def run():
    logger = logging.getLogger(SCRIPT_NAME)
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    run()
