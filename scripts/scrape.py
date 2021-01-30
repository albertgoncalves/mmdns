#!/usr/bin/env python3

from os import environ
from os.path import exists, join
from pickle import dump, load
from sys import stderr
from time import sleep
from urllib.request import urlopen

from bs4 import BeautifulSoup

FILENAME = {
    "teams": join(environ["WD"], "out", "teams.pkl"),
    "schedule": join(environ["WD"], "out", "schedule_{}_{}.pkl"),
}
URL = {
    "base": "https://www.sports-reference.com",
    "teams": "{}/cbb/schools/",
    "schedule": "{}{}-schedule.html",
}
YEARS = [2018, 2019]
SLEEP_SECONDS = 2


def cache(filename, f):
    if not exists(filename):
        x = f()
        with open(filename, "wb") as file:
            dump(x, file)
        return x
    with open(filename, "rb") as file:
        return load(file)


def get_source(url):
    sleep(SLEEP_SECONDS)
    print(url, file=stderr)
    try:
        with urlopen(url) as source:
            return source.read().decode(errors="ignore")
    except Exception as error:
        print(error, "\n", sep="", file=stderr)
        return None


def get_teams():
    source = cache(
        FILENAME["teams"],
        lambda: get_source(URL["teams"].format(URL["base"])),
    )
    html = BeautifulSoup(source, "lxml")
    results = []
    for row in map(
        lambda row: row.parent.find("a"),
        html.find_all("th", {"scope": "row"}),
    ):
        results.append({
            "id": row["href"].rstrip("/").rsplit("/", 1)[-1],
            "link": "{}{}".format(URL["base"], row["href"]),
            "name": row.text,
        })
    return results


def main():
    teams = get_teams()
    for year in YEARS:
        for team in teams:
            print(year, team["id"], file=stderr)
            cache(
                FILENAME["schedule"].format(year, team["id"]),
                lambda: get_source(URL["schedule"].format(
                    team["link"],
                    year,
                )),
            )


if __name__ == "__main__":
    main()
