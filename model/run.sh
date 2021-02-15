#!/usr/bin/env bash

set -eu

wd="$WD/model"

for x in build out; do
    if [ ! -d "$wd/$x" ]; then
        mkdir "$wd/$x"
    fi
done

(
    "$WD/scripts/install_cmdstan.sh"
    if ! cmp -s "$wd/model.stan" "$wd/build/model.stan"; then
        cp "$wd/model.stan" "$wd/build"
        "$WD/cmdstan/bin/stanc" \
            --warn-uninitialized \
            --warn-pedantic \
            "$wd/build/model.stan"
    fi
)
(
    . "$WD/scripts/build_flags.sh"
    cd "$WD/cmdstan"
    make "$wd/build/model"
)
(
    years=(
        2017
        2018
        2019
    )
    for year in "${years[@]}"; do
        (
            "$wd/export_data.py" "$year"
            "$wd/build/model" \
                sample \
                num_warmup=1000 \
                num_samples=5000 \
                data file="$wd/out/data_$year.json" \
                output file="$wd/out/output_$year.csv"
            grep -v "#" "$wd/out/output_$year.csv" \
                > "$wd/out/samples_$year.csv"
            "$WD/cmdstan/bin/stansummary" "$wd/out/output_$year.csv" \
                > "$wd/out/summary_$year.txt"
            "$wd/postlude.py" "$year" > "$wd/out/sims_$year.txt"
        ) &
    done
    wait
    for year in "${years[@]}"; do
        less "$wd/out/summary_$year.txt"
        feh "$wd/out/summary_$year.png"
        feh "$wd/out/params_$year.png"
        feh "$wd/out/preds_$year.png"
        less "$wd/out/sims_$year.txt"
    done
)
