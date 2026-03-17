#!/usr/bin/env python

import sys
import os
import argparse
from collections import Counter  # Import Counter for easy counting

import argcomplete
from rich import print as rprint
from rich.status import Status

import pysbf

rich_status = Status("", spinner="aesthetic")
rich_status.start()


def argument_parser(script_name: str, args: list) -> argparse.Namespace:
    """parses the arguments

    Args:
        argv (list): list of arguments

    Returns:
        argparse.Namespace: parsed arguments
    """
    help_txt = script_name + " show SBF blocks in a SBF file."

    # create the parser for command line arguments
    parser = argparse.ArgumentParser(description=help_txt)

    parser.add_argument("-V", "--version", action="version", version="%(prog)s v0.1")
    # parser.add_argument(
    #     "-v",
    #     "--verbose",
    #     action="count",
    #     default=None,
    #     help="verbose level... repeat up to three times.",
    # )

    parser.add_argument(
        "--sbf_ifn",
        help="SBF filename",
        type=str,
        required=True,
        default=None,
    )

    # allow argument completion
    argcomplete.autocomplete(parser)
    args = parser.parse_args(args)

    return args


def sbfblock_decode(sbf_ifn: str):
    block_counts = Counter()  # Use Counter to store counts
    # Alternatively, you could use a standard dictionary:
    # block_counts = {}

    with open(sbf_ifn, "rb") as fd_sbf:  # Open in binary mode 'rb'
        for block_name, block in pysbf.load(fd_sbf):
            rich_status.update(f"parsing [green]{block_name}[/green]")
            block_counts[block_name] += 1
            # If using a standard dictionary:
            # block_counts[block_name] = block_counts.get(block_name, 0) + 1

    rich_status.stop()

    print("Block Name Counts:")
    # To print in a more readable format, you can iterate through the dictionary
    for name, count in block_counts.items():
        rprint(f"  {name}: {count}")
    # If you just want to print the dictionary directly:
    # print(dict(block_counts)) # Convert Counter to dict for printing if you prefer


if __name__ == "__main__":
    # get the name of this script for naming the logger
    script_name = os.path.splitext(os.path.basename(__file__))[0]

    parsed_args = argument_parser(script_name=script_name, args=sys.argv[1:])
    sbfblock_decode(sbf_ifn=parsed_args.sbf_ifn)
