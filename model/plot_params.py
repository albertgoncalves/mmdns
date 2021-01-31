#!/usr/bin/env python3

from json import load
from os import environ
from os.path import join
from sys import argv

from matplotlib.pyplot import close, savefig, subplots, tight_layout
from pandas import DataFrame, read_csv

import export_data
import plot_summary

FILENAME = {
    "params": join(environ["WD"], "out", "params_{}.png"),
}
TEAM_IDS = {
    2019: [
        "auburn",
        "duke",
        "gonzaga",
        "kentucky",
        "michigan-state",
        "purdue",
        "texas-tech",
        "virginia",
    ],
    2018: [
        "duke",
        "florida-state",
        "kansas",
        "kansas-state",
        "loyola-il",
        "michigan",
        "texas-tech",
        "villanova",
    ],
    2017: [
        "florida",
        "gonzaga",
        "kansas",
        "kentucky",
        "north-carolina",
        "oregon",
        "south-carolina",
        "xavier",
    ],
}


def main():
    assert len(argv) == 2
    year = int(argv[1])
    with open(export_data.FILENAME["team_ids"].format(year), "r") as file:
        team_ids = {value: key for (key, value) in load(file).items()}
    samples = read_csv(
        plot_summary.FILENAME["samples"].format(year),
        low_memory=False,
    )
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
    rows = params.team_id.isin(TEAM_IDS[year])
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
        "color": "k",
        "alpha": 0.125,
        "linestyle": "--",
    }
    ax.axvline(samples[columns["att"]].values.mean(), **kwargs)
    ax.axhline(samples[columns["def"]].values.mean(), **kwargs)
    for (_, row) in params.iterrows():
        if row.team_id in TEAM_IDS[year]:
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
    tight_layout()
    savefig(FILENAME["params"].format(year))
    close()


if __name__ == "__main__":
    main()
