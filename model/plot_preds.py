#!/usr/bin/env python3

from json import load
from os import environ
from os.path import join
from random import randrange
from sys import argv

from matplotlib.pyplot import close, savefig, subplots, tight_layout
from numpy import array, mean, median
from pandas import read_csv
from seaborn import histplot

import export_data
import plot_summary

FILENAME = {
    "preds": join(environ["WD"], "out", "preds_{}.png"),
}


def set_hist(ax, x):
    histplot(
        x,
        discrete=True,
        kde=True,
        color="dimgray",
        edgecolor="none",
        ax=ax,
    )
    kwargs = {
        "ls": "--",
    }
    m = median(x)
    ax.axvline(m, label="median => {:.2f}".format(m), c="dodgerblue", **kwargs)
    m = mean(x)
    ax.axvline(m, label="mean   => {:.2f}".format(m), c="tomato", **kwargs)
    ax.legend(prop={"family": "monospace"})


def main():
    assert len(argv) == 2
    year = int(argv[1])
    with open(export_data.FILENAME["data"].format(year), "r") as file:
        data = load(file)
    samples = read_csv(
        plot_summary.FILENAME["samples"].format(year),
        low_memory=False,
    )
    i = randrange(0, len(samples))
    (_, axs) = subplots(2, 2, sharex=True, sharey=True, figsize=(18, 10))
    axs[0, 0].set_title("team_1")
    axs[0, 1].set_title("team_2")
    axs[0, 0].set_ylabel("observed")
    axs[1, 0].set_ylabel("predicted")
    set_hist(axs[0, 0], array(data["team_1_score"]))
    set_hist(axs[0, 1], array(data["team_2_score"]))
    set_hist(axs[1, 0], samples[list(filter(
        lambda x: x.startswith("team_1_score_pred"),
        samples.columns,
    ))].iloc[i].values)
    set_hist(axs[1, 1], samples[list(filter(
        lambda x: x.startswith("team_2_score_pred"),
        samples.columns,
    ))].iloc[i].values)
    tight_layout()
    savefig(FILENAME["preds"].format(year))
    close()


if __name__ == "__main__":
    main()
