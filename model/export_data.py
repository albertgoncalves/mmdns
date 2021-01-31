#!/usr/bin/env python3

from json import dump
from os import environ
from os.path import join
from sys import argv

from numpy import nan
from pandas import read_csv, to_datetime

WD = environ["WD"]
DATE_FORMAT = "%Y-%m-%d"


def main():
    assert len(argv) == 2
    year = int(argv[1])
    df = read_csv(join(WD, "out", "schedule.csv"))
    df = df.loc[(df.year == year) & (df.type == "REG")].copy()
    # NOTE: If we don't have an `id` for `opp`, let's just purge it for now to
    # keep things simple.
    df = df.loc[df.opp_team_id.notnull()].copy()
    assert df.team_id.notnull().all()
    assert set(df.team_id.tolist()) == set(df.opp_team_id.tolist())
    # NOTE: Let's create an integer `id` for all teams.
    team_ids = {
        team_id: i + 1
        for (i, team_id) in enumerate(sorted(df.team_id.unique()))
    }
    with open(join(WD, "out", "team_ids_{}.json".format(year)), "w") as file:
        dump(team_ids, file)
    df.team_id = df.team_id.map(team_ids)
    df.opp_team_id = df.opp_team_id.map(team_ids)
    # NOTE: We can create a `game_id` from the combination of the date and the
    # `id` values of the two teams.
    df.date = to_datetime(df.date, format=DATE_FORMAT)
    df["game_id"] = \
        df.date.dt.strftime(DATE_FORMAT) + \
        "_" + \
        df[["team_id", "opp_team_id"]].min(axis=1).astype(str) + \
        "_" + \
        df[["team_id", "opp_team_id"]].max(axis=1).astype(str)
    # NOTE: There should be two rows for each unique game.
    game_ids = df.groupby("game_id", as_index=False).agg({
        "date": "count",
        "loc": set,
    })
    assert game_ids.date.unique() == [2]
    assert ((game_ids["loc"] == {"N"}) | (game_ids["loc"] == {nan, "@"})).all()
    # NOTE: We only need a single record per game; we can drop one of them as
    # long as we correctly account for `home` where necessary.
    df.sort_values(["loc", "team_id"], inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.drop_duplicates("game_id", inplace=True)
    assert df["loc"].isin(["@", "N"]).all()
    # NOTE: For now, only `opp` can be `home`. Otherwise `loc` is neutral.
    df["opp_team_home"] = df["loc"].map({"@": True, "N": False})
    data = {
        "n_games": len(df),
        "n_teams": len(team_ids),
        "team_1_id": df.team_id.tolist(),
        "team_2_id": df.opp_team_id.tolist(),
        "team_1_score": df.score.tolist(),
        "team_2_score": df.opp_score.tolist(),
        "team_2_home": df.opp_team_home.astype("int32").tolist(),
    }
    with open(join(WD, "out", "data_{}.json".format(year)), "w") as file:
        dump(data, file)


if __name__ == "__main__":
    main()
