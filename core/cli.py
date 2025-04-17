import argparse
import pathlib
from typing import List, Optional

from core import with_stimulus_orchestrator
from core import without_stimulus_orchestrator

def parse_arguments(args: Optional[List[str]]) -> argparse.Namespace:
    """Argument parser for mobi-motion-tracking cli.

    Args:
        args: A list of command line arguments given as strings. If None, the parser
            will take the args from `sys.argv`.

    Returns:
        Namespace object with all the input arguments and default values.

    Raises:
        SystemExit: if arguments are None.
    """
    parser = argparse.ArgumentParser(
        description="Collect ZED motion tracking data with or without a stimulus.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog="Please report issues at https://github.com/childmindresearch/zed2i_3d_capture.",
    )
    parser.add_argument(
        "-p",
        "--participant",
        type=str,
        required=True,
        help="Participant ID.",
    )

    parser.add_argument(
        "-s",
        "--sequence",
        type=str,
        required=True,
        help="Integer value representing current sequence or trial number.",
    )

    parser.add_argument(
        "--video",
        type=pathlib.Path,
        help="Optional argument. String representing the path to the stimulus video file.",
    )

    return parser.parse_args(args)



def main(args: Optional[List[str]] = None):
    
    arguments = parse_arguments(args)

    if arguments.video is None:
        without_stimulus_orchestrator.run(arguments.participant, arguments.sequence)
    else:
        with_stimulus_orchestrator.run(arguments.participant, arguments.sequence, arguments.video)

    print(f"ZED Body tracking for Participant: {arguments.participant} Sequence: {arguments.sequence} is complete")