#!/usr/bin/env python3

from json import load
from os import environ
from os.path import join
from sys import argv

from numpy import exp
from numpy.random import default_rng
from pandas import read_csv

import export_data
import plot_summary
import unpack

FILENAME = {
    "sims": join(environ["WD"], "out", "sims_{}.png"),
}
BRACKET = {
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
WINNERS = {
    2017: {
        0: [
            "villanova",
            "wisonsin",
            "virginia",
            "florida",
            "southern-california",
            "baylor",
            "south-carolina",
            "duke",
            "gonzaga",
            "northwestern",
            "notre-dame",
            "west-virginia",
            "xavier",
            "florida-state",
            "saint-marys-ca",
            "arizona",
            "kansas",
            "michigan-state",
            "iowa-state",
            "purdue",
            "rhode-island",
            "oregon",
            "michigan",
            "louisville",
            "north-carolina",
            "arkansas",
            "middle-tennessee",
            "butler",
            "cincinnati",
            "ucla",
            "wichita-state",
            "kentucky",
        ],
        1: [
            "wisonsin",
            "florida",
            "baylor",
            "south-carolina",
            "gonzaga",
            "west-virginia",
            "xavier",
            "arizona",
            "kansas",
            "purdue",
            "oregon",
            "michigan",
            "north-carolina",
            "butler",
            "ucla",
            "kentucky",
        ],
        2: [
            "florida",
            "south-carolina",
            "gonzaga",
            "xavier",
            "kansas",
            "oregon",
            "north-carolina",
            "kentucky",
        ],
        3: [
            "south-carolina",
            "gonzaga",
            "oregon",
            "north-carolina",
        ],
        4: [
            "gonzaga",
            "north-carolina",
        ],
        5: [
            "north-carolina",
        ],
    },
    2018: {
        0: [
            "maryland-baltimore-county",
            "kansas-state",
            "kentucky",
            "buffalo",
            "loyola-il",
            "tennessee",
            "nevada",
            "cincinnati",
            "xavier",
            "florida-state",
            "ohio-state",
            "gonzaga",
            "houston",
            "michigan",
            "texas-am",
            "north-carolina",
            "villanova",
            "alabama",
            "west-virginia",
            "marshall",
            "florida",
            "texas-tech",
            "butler",
            "purdue",
            "kansas",
            "seton-hall",
            "clemson",
            "auburn",
            "syracuse",
            "michigan-state",
            "rhode-island",
            "duke",
        ],
        1: [
            "kansas-state",
            "kentucky",
            "loyola-il",
            "nevada",
            "florida-state",
            "gonzaga",
            "michigan",
            "texas-am",
            "villanova",
            "west-virginia",
            "texas-tech",
            "purdue",
            "kansas",
            "clemson",
            "syracuse",
            "duke",
        ],
        2: [
            "kansas-state",
            "loyola-il",
            "florida-state",
            "michigan",
            "villanova",
            "texas-tech",
            "kansas",
            "duke",
        ],
        3: [
            "loyola-il",
            "michigan",
            "villanova",
            "kansas",
        ],
        4: [
            "michigan",
            "villanova",
        ],
        5: [
            "villanova",
        ],
    },
    2019: {
        0: [
            "duke",
            "central-florida",
            "liberty",
            "virginia-tech",
            "maryland",
            "louisiana-state",
            "minnesota",
            "michigan-state",
            "gonzaga",
            "baylor",
            "murray-state",
            "florida-state",
            "buffalo",
            "texas-tech",
            "florida",
            "michigan",
            "virginia",
            "oklahoma",
            "oregon",
            "california-irvine",
            "villanova",
            "purdue",
            "iowa",
            "tennessee",
            "north-carolina",
            "washington",
            "auburn",
            "kansas",
            "ohio-state",
            "houston",
            "wofford",
            "kentucky",
        ],
        1: [
            "duke",
            "virginia-tech",
            "louisiana-state",
            "michigan-state",
            "gonzaga",
            "florida-state",
            "texas-tech",
            "michigan",
            "virginia",
            "oregon",
            "purdue",
            "tennessee",
            "north-carolina",
            "auburn",
            "houston",
            "kentucky",
        ],
        2: [
            "duke",
            "michigan-state",
            "gonzaga",
            "texas-tech",
            "virginia",
            "purdue",
            "auburn",
            "kentucky",
        ],
        3: [
            "michigan-state",
            "texas-tech",
            "virginia",
            "auburn",
        ],
        4: [
            "texas-tech",
            "virginia",
        ],
        5: [
            "virginia",
        ],
    }
}


def get_data(year):
    schedule = read_csv(unpack.FILENAME["schedule"])
    schedule = \
        schedule.loc[(schedule.year == year) & (schedule.type == "NCAA")]
    for team_id in BRACKET[year]:
        assert team_id in schedule.team_id.unique()
    assert len(BRACKET[year]) == 64
    assert len(set(BRACKET[year])) == 64
    with open(export_data.FILENAME["team_ids"].format(year), "r") as file:
        team_ids = load(file)
    samples = read_csv(
        plot_summary.FILENAME["samples"].format(year),
        low_memory=False,
    )
    return (schedule, team_ids, samples)


def sim(schedule, team_ids, samples, bracket):
    rng = default_rng()
    mu_offset = samples.mu_offset
    results = []
    for _ in range(6):
        n = len(bracket)
        winners = {i: {} for i in range(0, n, 2)}
        next_bracket = []
        for i in range(0, n, 2):
            team_1_id = bracket[i]
            team_2_id = bracket[i + 1]
            team_1_index = team_ids[team_1_id]
            team_2_index = team_ids[team_2_id]
            [team_1_score, team_2_score] = rng.poisson(exp([
                mu_offset +
                samples[f"att.{team_1_index}"] +
                samples[f"def.{team_2_index}"],
                mu_offset +
                samples[f"att.{team_2_index}"] +
                samples[f"def.{team_1_index}"],
            ]))
            team_1_wins = (team_2_score < team_1_score).sum()
            team_2_wins = (team_1_score < team_2_score).sum()
            if team_1_wins == team_2_wins:
                if rng.random() < 0.5:
                    team_1_wins += 1
                else:
                    team_2_wins += 1
            m = team_1_wins + team_2_wins
            winners[i][team_1_id] = team_1_wins / m
            winners[i][team_2_id] = team_2_wins / m
            if team_2_wins < team_1_wins:
                next_bracket.append(team_1_id)
            else:
                next_bracket.append(team_2_id)
        bracket = next_bracket
        results.append(winners)
    return results


def main():
    assert len(argv) == 2
    year = int(argv[1])
    (schedule, team_ids, samples) = get_data(year)
    for (j, results) in enumerate(sim(
        schedule,
        team_ids,
        samples,
        BRACKET[year],
    )):
        winners = WINNERS[year][j]
        correct = 0
        print("")
        for (i, result) in enumerate(results.values()):
            [(team_1_id, team_1_pct), (team_2_id, team_2_pct)] = result.items()
            assert team_1_pct != team_2_pct
            winner = winners[i]
            if team_2_pct < team_1_pct:
                predicted = team_1_id
                print(
                    f"{team_1_id:>26}  {team_1_pct:.2f}  <|         "
                    f"{team_2_id:<26}",
                    end="",
                )
            else:
                predicted = team_2_id
                print(
                    f"{team_1_id:>26}         |>  {team_2_pct:.2f}  "
                    f"{team_2_id:<26}",
                    end="",
                )
            if predicted == winner:
                correct += 1
                print("")
            else:
                print(f"... wrong! ({winner})")
        total = len(winners)
        print(f"\n  {correct} out of {total} ~ {correct / total:.2f}")
        print("=" * 79)


if __name__ == "__main__":
    main()
