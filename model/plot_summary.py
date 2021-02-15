#!/usr/bin/env python3

from math import ceil
from os import environ
from os.path import join
from random import sample
from sys import argv

from matplotlib.pyplot import close, savefig, subplots, tight_layout
from numpy import mean, median
from pandas import read_csv

FILENAME = {
    "samples": join(environ["WD"], "model", "out", "samples_{}.csv"),
    "summary": join(environ["WD"], "model", "out", "summary_{}.png"),
}


def plot(ax, samples, column):
    ax.set_title(column)
    ax.plot(samples[column], color="black", alpha=0.35)
    kwargs = {
        "ls": "--",
    }
    x = median(samples[column])
    ax.axhline(x, label=f"median => {x:.2f}", c="dodgerblue", **kwargs)
    x = mean(samples[column])
    ax.axhline(x, label=f"mean   => {x:.2f}", c="tomato", **kwargs)
    ax.legend(loc="lower right", prop={"family": "monospace"})


def main():
    assert len(argv) == 2
    year = int(argv[1])
    samples = read_csv(FILENAME["samples"].format(year), low_memory=False)
    n = 20
    w = 4
    h = ceil(n / w)
    if n < len(samples.columns):
        columns = [
            column for column in samples.columns
            if column.endswith("__") or ("." not in column)
        ]
        m = len(columns)
        assert m < n
        samples = samples[columns + sample([
            column for column in samples.columns
            if ("." in column) and ("_pred" not in column)
        ], n - m)].copy()
        assert len(samples.columns) == n
    (_, axs) = subplots(h, w, figsize=(18, 10))
    for i in range(h):
        iw = i * w
        for j in range(w):
            m = iw + j
            if m < n:
                plot(axs[i, j], samples, samples.columns[m])
            else:
                axs[i, j].set_axis_off()
    tight_layout()
    savefig(FILENAME["summary"].format(year))
    close()


if __name__ == "__main__":
    main()
