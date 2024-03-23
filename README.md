# QUESTS: Quick Uncertainty and Entropy from STructural Similarity

QUESTS provides model-free uncertainty and entropy estimation methods for interatomic potentials.
Among the methods, we propose a structural descriptor based on k-nearest neighbors that is:

1. Fast to compute, as it uses only distances between atoms within an environment.
Because the descriptors are parallelized, generation of descriptors for 1.5M environments takes about 3 seconds on a 56-core computer.
2. Interpretable, as the distances correspond to directly to displacements of atoms.
3. Lead to an interpretable information entropy value.

This package also contains metrics to quantify the diversity of a dataset using this descriptor, and tools to interface with other representations and packages.

## Installation

To use the `quests` package, clone this repository from GitLab and use `pip` to install it into your virtual environment:

```bash
git clone ssh://git@czgitlab.llnl.gov:7999/dskoda/quests.git
cd quests
pip install .
```

## Usage

### Command line

Once installed, you can use the `quests` command to perform different analyses. For example, to compute the entropy of any dataset (the input can be anything that ASE reads, including xyz files), you can use the `quests entropy` command:

```
quests entropy dump.lammpstrj --bandwidth 0.015
```

For subsampling the dataset and avoiding using the entire dataset, use the `entropy_sampler` example:

```
quests entropy_sampler dump.lammpstrj --batch_size 20000 -s 100000 -n 1
```

`-s` specifies the number of sampled environments, `-n` specifies how many runs will be computed (for statistics).

For additional help with these commands, please use `quests --help`, `quests entropy --help`, and others.

### API

To integrate the QUESTS code with other codes, the easiest way is to use the functions to [get descriptors](https://lc.llnl.gov/gitlab/dskoda/quests/-/blob/main/quests/descriptor.py?ref_type=heads#L346) and [compute entropies](https://lc.llnl.gov/gitlab/dskoda/quests/-/blob/main/quests/entropy.py?ref_type=heads#L16).
More extensive documentation is to come.

### Citing 

If you use QUESTS in a publication, please cite the following paper:

```bibtex
@article{schwalbekoda2024information,
    title = {Information theory unifies atomistic machine learning, uncertainty quantification, and materials thermodynamics},
    author = {Schwalbe-Koda, Daniel and Hamel, Sebastien and Sadigh, Babak and Bulatov, Vasily and Zhou, Fei and Lordi, Vincenzo},
    year = {2024},
    journal = {arXiv:},
    doi = {},
    url = {},
    arxiv={},
}
```
## License

The mkite suite is distributed under the following license: BSD-3

All new contributions must be made under this license.

SPDX: BSD-3-Clause

LLNL-CODE-858914
