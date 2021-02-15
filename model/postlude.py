#!/usr/bin/env python3

from json import load
from sys import argv

from pandas import read_csv

import export_data
import plot_params
import plot_preds
import plot_summary
import print_sims
import unpack


def main():
    assert len(argv) == 2
    year = int(argv[1])
    with open(export_data.FILENAME["team_ids"].format(year), "r") as file:
        team_ids = load(file)
    with open(export_data.FILENAME["data"].format(year), "r") as file:
        data = load(file)
    kwargs = {
        "compression": None,
        "low_memory": False,
        "memory_map": True,
    }
    schedule = read_csv(unpack.FILENAME["schedule"], **kwargs)
    samples = read_csv(plot_summary.FILENAME["samples"].format(year), **kwargs)
    plot_summary.run(year, samples)
    plot_params.run(
        year,
        {value: key for (key, value) in team_ids.items()},
        samples,
    )
    plot_preds.run(year, data, samples)
    print_sims.run(
        year,
        schedule.loc[(schedule.year == year) & (schedule.type == "NCAA")],
        team_ids,
        samples,
    )


if __name__ == "__main__":
    main()
