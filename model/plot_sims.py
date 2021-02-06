#!/usr/bin/env python3

from collections import Counter
from json import load
from os import environ
from os.path import join
from sys import argv, stderr

from matplotlib.pyplot import close, savefig, subplots, tight_layout
from numpy import exp
from numpy.random import default_rng
from pandas import read_csv

import export_data
import plot_summary
import unpack

FILENAME = {
    "sims": join(environ["WD"], "out", "sims_{}.png"),
}
COUNT_SIMS = 5000
REMAINING = {
    2017: [
        "villanova",
        "mount-st-marys",
        "wisconsin",
        "virginia-tech",
        "virginia",
        "north-carolina-wilmington",
        "florida",
        "east-tennessee-state",
        "southern-methodist",
        "southern-california",
        "baylor",
        "new-mexico-state",
        "south-carolina",
        "marquette",
        "duke",
        "troy",
        "gonzaga",
        "south-dakota-state",
        "northwestern",
        "vanderbilt",
        "notre-dame",
        "princeton",
        "west-virginia",
        "bucknell",
        "maryland",
        "xavier",
        "florida-state",
        "florida-gulf-coast",
        "saint-marys-ca",
        "virginia-commonwealth",
        "arizona",
        "north-dakota",
        "kansas",
        "california-davis",
        "miami-fl",
        "michigan-state",
        "iowa-state",
        "nevada",
        "purdue",
        "vermont",
        "creighton",
        "rhode-island",
        "oregon",
        "iona",
        "michigan",
        "oklahoma-state",
        "louisville",
        "jacksonville-state",
        "north-carolina",
        "texas-southern",
        "arkansas",
        "seton-hall",
        "minnesota",
        "middle-tennessee",
        "butler",
        "winthrop",
        "cincinnati",
        "kansas-state",
        "ucla",
        "kent-state",
        "dayton",
        "wichita-state",
        "kentucky",
        "northern-kentucky",
    ],
    2018: [
        "virginia",
        "maryland-baltimore-county",
        "creighton",
        "kansas-state",
        "kentucky",
        "davidson",
        "arizona",
        "buffalo",
        "miami-fl",
        "loyola-il",
        "tennessee",
        "wright-state",
        "nevada",
        "texas",
        "cincinnati",
        "georgia-state",
        "xavier",
        "texas-southern",
        "missouri",
        "florida-state",
        "ohio-state",
        "south-dakota-state",
        "gonzaga",
        "north-carolina-greensboro",
        "houston",
        "san-diego-state",
        "michigan",
        "montana",
        "texas-am",
        "providence",
        "north-carolina",
        "lipscomb",
        "villanova",
        "radford",
        "virginia-tech",
        "alabama",
        "west-virginia",
        "murray-state",
        "wichita-state",
        "marshall",
        "florida",
        "st-bonaventure",
        "texas-tech",
        "stephen-f-austin",
        "arkansas",
        "butler",
        "purdue",
        "cal-state-fullerton",
        "kansas",
        "pennsylvania",
        "seton-hall",
        "north-carolina-state",
        "clemson",
        "new-mexico-state",
        "auburn",
        "college-of-charleston",
        "texas-christian",
        "syracuse",
        "michigan-state",
        "bucknell",
        "rhode-island",
        "oklahoma",
        "duke",
        "iona",
    ],
    2019: [
        "duke",
        "north-dakota-state",
        "virginia-commonwealth",
        "central-florida",
        "mississippi-state",
        "liberty",
        "virginia-tech",
        "saint-louis",
        "maryland",
        "belmont",
        "louisiana-state",
        "yale",
        "louisville",
        "minnesota",
        "michigan-state",
        "bradley",
        "gonzaga",
        "fairleigh-dickinson",
        "syracuse",
        "baylor",
        "marquette",
        "murray-state",
        "florida-state",
        "vermont",
        "buffalo",
        "arizona-state",
        "texas-tech",
        "northern-kentucky",
        "nevada",
        "florida",
        "michigan",
        "montana",
        "virginia",
        "gardner-webb",
        "mississippi",
        "oklahoma",
        "wisconsin",
        "oregon",
        "kansas-state",
        "california-irvine",
        "villanova",
        "saint-marys-ca",
        "purdue",
        "old-dominion",
        "cincinnati",
        "iowa",
        "tennessee",
        "colgate",
        "north-carolina",
        "iona",
        "utah-state",
        "washington",
        "auburn",
        "new-mexico-state",
        "kansas",
        "northeastern",
        "iowa-state",
        "ohio-state",
        "houston",
        "georgia-state",
        "wofford",
        "seton-hall",
        "kentucky",
        "abilene-christian",
    ],
}


def main():
    assert len(argv) == 2
    year = int(argv[1])
    schedule = read_csv(unpack.FILENAME["schedule"])
    schedule = \
        schedule.loc[(schedule.year == year) & (schedule.type == "NCAA")]
    for team_id in REMAINING[year]:
        assert team_id in schedule.team_id.unique()
    assert len(REMAINING[year]) == 64
    assert len(set(REMAINING[year])) == 64
    with open(export_data.FILENAME["team_ids"].format(year), "r") as file:
        team_ids = load(file)
    samples = read_csv(
        plot_summary.FILENAME["samples"].format(year),
        low_memory=False,
    )
    rng = default_rng()
    sims = []
    for (t, i) in enumerate(rng.integers(0, len(samples), COUNT_SIMS)):
        print(f"\r{((t + 1) / COUNT_SIMS) * 100:>7.1f}%", end="", file=stderr)
        sample = samples.iloc[i]
        mu_offset = sample.mu_offset
        remaining = REMAINING[year]
        for _ in range(6):
            winners = []
            for j in range(0, len(remaining), 2):
                team_1_id = remaining[j]
                team_2_id = remaining[j + 1]
                team_1_index = team_ids[team_1_id]
                team_2_index = team_ids[team_2_id]
                [team_1_score, team_2_score] = rng.poisson(exp([
                    mu_offset +
                    sample[f"att.{team_1_index}"] +
                    sample[f"def.{team_2_index}"],
                    mu_offset +
                    sample[f"att.{team_2_index}"] +
                    sample[f"def.{team_1_index}"],
                ]))
                if team_1_score == team_2_score:
                    if rng.random() < 0.5:
                        winners.append(team_1_id)
                    else:
                        winners.append(team_2_id)
                elif team_2_score < team_1_score:
                    winners.append(team_1_id)
                else:
                    winners.append(team_2_id)
            remaining = winners
        sims.append(remaining[0])
    print("\n", end="", file=stderr)
    (_, ax) = subplots(figsize=(6, 9))
    ax.set_title(f"{COUNT_SIMS} simulations", family="monospace")
    ax.barh(*zip(*Counter(sims).most_common()), color="dimgray")
    ax.invert_yaxis()
    tight_layout()
    savefig(FILENAME["sims"].format(year))
    close()


if __name__ == "__main__":
    main()
