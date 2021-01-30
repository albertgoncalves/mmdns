#!/usr/bin/env python3

from glob import glob
from multiprocessing import Pool
from os import environ
from os.path import join
from pickle import load
from re import compile
from sys import stderr

from bs4 import BeautifulSoup
from pandas import DataFrame

from scrape import URL

SIZE_POOL = 3
FILENAME = {
    "schedule": join(environ["WD"], "out", "schedule.csv"),
}
GLOB = {
    "schedule": join(environ["WD"], "out", "schedule_*.pkl"),
}
PATTERN = {
    "schedule": compile(r".+schedule_([0-9]{4})_([^\.]+)\.pkl$"),
}


def nullable(x):
    if x == "":
        return None
    return x


def parse_link(element):
    if (link := element.find("a")) is not None:
        return {
            "name": link.text,
            "id": link["href"].rsplit("/", 2)[-2],
            "link": "{}{}".format(URL["base"], link["href"]),
        }
    return {
        "name": element.text,
    }


def parse_schedule(team, year, row):
    date = row.find("td", {"data-stat": "date_game"})
    opp = parse_link(row.find("td", {"data-stat": "opp_name"}))
    conf = parse_link(row.find("td", {"data-stat": "conf_abbr"}))
    return {
        "year": year,
        "date": date["csk"],
        "game_link": "{}{}".format(URL["base"], date.find("a")["href"]),
        "time": row.find("td", {"data-stat": "time_game"}).text,
        "type": row.find("td", {"data-stat": "game_type"}).text,
        "seq": int(row.find("th").text),
        "venue": row.find("td", {"data-stat": "arena"}).text,
        "team_id": team,
        "loc": nullable(row.find("td", {"data-stat": "game_location"}).text),
        "opp_team_name": opp["name"],
        "opp_team_id": opp.get("id", None),
        "opp_team_link": opp.get("link", None),
        "conf_name": conf["name"],
        "conf_id": conf.get("id", None),
        "conf_link": conf.get("link", None),
        "result": row.find("td", {"data-stat": "game_result"}).text,
        "score": int(row.find("td", {"data-stat": "pts"}).text),
        "opp_score": int(row.find("td", {"data-stat": "opp_pts"}).text),
        "overtime": nullable(row.find("td", {"data-stat": "overtimes"}).text),
        "cum_wins": int(row.find("td", {"data-stat": "wins"}).text),
        "cum_losses": int(row.find("td", {"data-stat": "losses"}).text),
    }


def get_schedule(filename, team, year):
    print(filename, file=stderr)
    with open(filename, "rb") as file:
        source = load(file)
    if source is None:
        return None
    html = BeautifulSoup(source, "lxml")
    results = []
    for row in map(
        lambda row: row.parent,
        html.find_all("td", {"data-stat": "date_game"}),
    ):
        results.append(parse_schedule(team, year, row))
    return results


def main():
    payloads = []
    for filename in glob(GLOB["schedule"]):
        if (match := PATTERN["schedule"].match(filename)) is not None:
            year = int(match.group(1))
            team = match.group(2)
            payloads.append((filename, team, year))
        else:
            print(filename, file=stderr)
            exit(1)
    with Pool(SIZE_POOL) as pool:
        results = pool.starmap(get_schedule, payloads)
    results = DataFrame([
        item
        for sublist in filter(lambda x: x is not None, results)
        for item in sublist
    ])
    results.to_csv(FILENAME["schedule"], index=False)


if __name__ == "__main__":
    main()
