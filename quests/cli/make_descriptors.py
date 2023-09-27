import json
import time

import click
import numba as nb
import numpy as np
from ase.io import read

from .log import format_time
from .log import logger
from quests.descriptor import DEFAULT_CUTOFF
from quests.descriptor import DEFAULT_K
from quests.descriptor import get_descriptors
from quests.entropy import DEFAULT_BANDWIDTH
from quests.entropy import DEFAULT_BATCH
from quests.entropy import perfect_entropy
from quests.tools.time import Timer


@click.command("make_descriptors")
@click.argument("file", required=1)
@click.option(
    "-c",
    "--cutoff",
    type=float,
    default=DEFAULT_CUTOFF,
    help=f"Cutoff (in Å) for computing the neighbor list (default: {DEFAULT_CUTOFF:.1f})",
)
@click.option(
    "-k",
    "--nbrs",
    type=int,
    default=DEFAULT_K,
    help=f"Number of neighbors when creating the descriptor (default: {DEFAULT_K})",
)
@click.option(
    "-j",
    "--jobs",
    type=int,
    default=None,
    help="Number of jobs to distribute the calculation in (default: all)",
)
@click.option(
    "-r",
    "--reshape",
    is_flag=True,
    default=False,
    help=(
        "If set, reshapes the descriptors to match the length of the dataset."
        + "Only valid if all frames in the dataset have the same number of atoms."
    ),
)
@click.option(
    "-o",
    "--output",
    type=str,
    default=None,
    help="path to the json file that will contain the output\
            (default: no output produced)",
)
def make_descriptors(
    file,
    cutoff,
    nbrs,
    reshape,
    jobs,
    output,
):
    if jobs is not None:
        nb.set_num_threads(jobs)

    logger(f"Loading and creating descriptors for file {file}")
    dset = read(file, index=":")

    with Timer() as t:
        x = get_descriptors(dset, k=nbrs, cutoff=cutoff)
    descriptor_time = t.time
    logger(f"Descriptors built in: {format_time(descriptor_time)}")

    natoms = set([len(atoms) for atoms in dset])

    if reshape and len(natoms) == 1:
        n = list(natoms)[0]
        x = x.reshape(len(dset), n, -1)

    logger(f"Descriptors shape: {x.shape}")

    if output is not None:
        with open(output, "wb") as f:
            np.save(f, x)