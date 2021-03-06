#!/usr/bin/env python3

from json import load
from os import environ
from os.path import join
from sys import argv

from matplotlib.pyplot import close, savefig, subplots, tight_layout
from pandas import DataFrame, read_csv

import export_data
import plot_summary
import print_sims

FILENAME = {
    "params": join(environ["WD"], "model", "out", "params_{}.png"),
}


def run(year, team_ids, samples):
    params = {}
    columns = {
        "att": list(filter(lambda x: x.startswith("att."), samples.columns)),
        "def": list(filter(lambda x: x.startswith("def."), samples.columns)),
    }
    for key in columns["att"]:
        param = team_ids[int(key.replace("att.", ""))]
        params[param] = {
            "att_mean": samples[key].mean(),
            "att_2_std": samples[key].std() * 2.0,
        }
    for key in columns["def"]:
        param = team_ids[int(key.replace("def.", ""))]
        params[param]["def_mean"] = samples[key].mean()
        params[param]["def_2_std"] = samples[key].std() * 2.0
    params = DataFrame(params).T
    params.reset_index(drop=False, inplace=True)
    params.rename(columns={
        "index": "team_id",
    }, inplace=True)
    (_, ax) = subplots(figsize=(10, 10))
    rows = params.team_id.isin(print_sims.WINNERS[year][2])
    ax.scatter(
        params.loc[rows].att_mean,
        params.loc[rows].def_mean,
        color="none",
        edgecolor="k",
        alpha=1.0,
        linewidth=0.5,
    )
    ax.scatter(
        params.loc[~rows].att_mean,
        params.loc[~rows].def_mean,
        color="none",
        edgecolor="k",
        alpha=0.25,
        linewidth=0.5,
    )
    kwargs = {
        "alpha": 0.35,
        "linestyle": "--",
    }
    m = samples[columns["att"]].values.mean()
    ax.axvline(m, label=f"att mean => {m:.2f}", c="dodgerblue", **kwargs)
    m = samples[columns["def"]].values.mean()
    ax.axhline(m, label=f"def mean => {m:.2f}", c="tomato", **kwargs)
    for (_, row) in params.iterrows():
        if row.team_id in print_sims.WINNERS[year][2]:
            ax.annotate(
                row.team_id,
                (row.att_mean, row.def_mean),
                xytext=(0, 6.5),
                textcoords='offset points',
                ha="center",
                va="center",
            )
    kwargs = {
        "alpha": 0.175,
        "color": "k",
    }
    ax.hlines(
        params.loc[rows, "def_mean"],
        params.loc[rows, "att_mean"] - params.loc[rows, "att_2_std"],
        params.loc[rows, "att_mean"] + params.loc[rows, "att_2_std"],
        label="2 standard deviations",
        **kwargs,
    )
    ax.vlines(
        params.loc[rows, "att_mean"],
        params.loc[rows, "def_mean"] - params.loc[rows, "def_2_std"],
        params.loc[rows, "def_mean"] + params.loc[rows, "def_2_std"],
        **kwargs,
    )
    ax.set_xlabel("attack")
    ax.set_ylabel("defense")
    ax.legend(prop={"family": "monospace"})
    tight_layout()
    savefig(FILENAME["params"].format(year))
    close()


def main():
    assert len(argv) == 2
    year = int(argv[1])
    with open(export_data.FILENAME["team_ids"].format(year), "r") as file:
        team_ids = load(file)
    samples = read_csv(
        plot_summary.FILENAME["samples"].format(year),
        compression=None,
        low_memory=False,
        memory_map=True,
    )
    run(year, {value: key for (key, value) in team_ids.items()}, samples)


if __name__ == "__main__":
    main()
