#!/usr/bin/env python

import sys
import os
import argparse
import csv  # Import the csv module
import numpy as np  # Import numpy

import argcomplete
from rich import print as rprint
from rich.status import Status

# Import the pysbf sub-package from the main py3sbf package
# This requires src/py3sbf/__init__.py to make 'pysbf' available or use 'import py3sbf.pysbf as pysbf'
from py3sbf import pysbf

# Import the specific function from your new sbf_constants module
from py3sbf.sbf.sbf_constants import ssnerr_prn2str


rich_status = Status("", spinner="aesthetic")
rich_status.start()


def argument_parser(script_name: str, args: list) -> argparse.Namespace:
    """parses the arguments

    Args:
        argv (list): list of arguments

    Returns:
        argparse.Namespace: parsed arguments
    """
    help_txt = script_name + " decodes SVID, azimuth & elevation in a SBF file."

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
    args_parsed = parser.parse_args(args)

    return args_parsed


def sbf_azel_decode(sbf_ifn: str):
    """prints SVID/azimuth/elevation found in 'SatInfo' sbf-block
    and writes it to a CSV file.

    Args:
        sbf_ifn (str): sbf filename
    """
    # Get the directory of the input SBF file
    sbf_dir = os.path.dirname(sbf_ifn)
    # Construct the base name for the output CSV file
    base_name = os.path.splitext(os.path.basename(sbf_ifn))[0]
    # Create the full path for the output CSV file in the same directory as the input
    csv_ofn = os.path.join(sbf_dir, f"{base_name}-azel.csv")

    rprint(f"Processing SBF file: [cyan]{sbf_ifn}[/cyan]")
    rprint(f"Outputting Az/El data to CSV: [green]{csv_ofn}[/green]")

    try:
        with open(sbf_ifn, "rb") as fd_sbf, open(csv_ofn, "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            # Write header row
            csv_writer.writerow(["SVID", "PRN", "Azimuth", "Elevation"])

            for blockName, block in pysbf.load(fd_sbf, blocknames={"SatVisibility"}):
                if (
                    blockName == "SatVisibility"
                ):  # Ensure we are processing the correct block
                    for satInfo in block.get("SatInfo", []):  # Use .get for safety
                        svid = satInfo.get("SVID")
                        prn_str = ""  # Default PRN string

                        if svid is not None:
                            try:
                                # Convert SVID (integer) to string for the ssnerr_prn2str function
                                prn_str = ssnerr_prn2str(str(svid))
                            except Exception as e:
                                rprint(
                                    f"[yellow]Warning: Could not convert SVID {svid} to PRN: {e}[/yellow]"
                                )
                                # Keep prn_str as default or set to svid if preferred
                                # prn_str = str(svid) # Optionally use SVID if conversion fails

                        rich_status.update(
                            f"Parsing [yellow]{blockName}[/yellow] for SVID [green]{svid:3d}[/green] "
                            f"(PRN: [green]{prn_str}[/green])"
                        )
                        azimuth = (
                            satInfo.get("Azimuth", np.nan) / 100.0
                        )  # Default to np.nan if missing
                        elevation = (
                            satInfo.get("Elevation", np.nan) / 100.0
                        )  # Default to np.nan if missing
                        csv_writer.writerow([svid, prn_str, azimuth, elevation])
    except FileNotFoundError:
        rprint(f"[bold red]Error: Input SBF file not found: {sbf_ifn}[/bold red]")
    except Exception as e:
        rprint(f"[bold red]An error occurred: {e}[/bold red]")
    finally:
        rich_status.stop()


def main():
    """Main function to parse arguments and process the SBF file."""
    # get the name of this script for naming the logger
    script_name = os.path.splitext(os.path.basename(__file__))[0]

    parsed_args = argument_parser(script_name=script_name, args=sys.argv[1:])
    sbf_azel_decode(sbf_ifn=parsed_args.sbf_ifn)


if __name__ == "__main__":
    main()
