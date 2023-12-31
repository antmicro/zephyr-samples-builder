#!/usr/bin/env python3

import sys
import config
from common import flatten


def get_boards() -> list:
    """
    Get a list of boards from the Zephyr project.
    Virtual and posix platforms (apart from QEMU) are filtered out.

    Returns:
        list: A filtered list of pairs (arch, board).
    """
    # the Zephyr utility has its own argument parsing, so avoid args clash
    sys.path.append(f"{config.project_path}/scripts")
    from list_boards import find_arch2boards
    from pathlib import Path

    class Args:
        arch_roots = [Path(config.project_path)]
        board_roots = [Path(config.project_path)]

    zephyr_boards = find_arch2boards(Args())
    boards_to_run = flatten(zephyr_boards).values()

    omit_arch = ("posix",)
    boards_to_run = filter(lambda x: x.arch not in omit_arch, boards_to_run)

    # Do not build for simulation targets (apart from QEMU).
    omit_board = ("nsim", "xenvm", "xt-sim", "fvp_")
    boards_to_run = list(filter(lambda x: all(map(lambda y: y not in x.name, omit_board)), boards_to_run))

    return [(board.dir, board.name) for board in boards_to_run]


def generate_samples() -> None:
    """
    Generate combinations of boards and samples based on configuration file

    If sample has defined 'boards' key, only generate the samples for given boards,
    otherwise generate the sample for all boards
    """
    all_boards_data = get_boards()
    for dir, board in all_boards_data:
        for sample, sample_data in config.samples.items():
            sample_boards = sample_data.get("boards", [board])
            if board in sample_boards:
                print(f"{dir} {board} {sample}")

if __name__ == "__main__":
    config.load()
    generate_samples()
