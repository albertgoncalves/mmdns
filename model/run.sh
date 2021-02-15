#!/usr/bin/env bash

set -eu



(
    "$WD/scripts/install_cmdstan.sh"
    if ! cmp -s "$WD/model/model.stan" "$WD/build/model.stan"; then
        cp "$WD/model/model.stan" "$WD/build"
        "$WD/cmdstan/bin/stanc" \
            --warn-uninitialized \
            --warn-pedantic \
            "$WD/build/model.stan"
    fi
)
(
    . "$WD/scripts/build_flags.sh"
    cd "$WD/cmdstan"
    make "$WD/build/model"
)
(
    years=(
        2017
        2018
        2019
    )
    for year in "${years[@]}"; do
        (
            "$WD/model/export_data.py" "$year"
            "$WD/build/model" \
                sample \
                num_warmup=1000 \
                num_samples=5000 \
                data file="$WD/out/data_$year.json" \
                output file="$WD/out/output_$year.csv"
            grep -v "#" "$WD/out/output_$year.csv" \
                > "$WD/out/samples_$year.csv"
            "$WD/cmdstan/bin/stansummary" "$WD/out/output_$year.csv" \
                > "$WD/out/summary_$year.txt"
            "$WD/model/plot_summary.py" "$year"
            "$WD/model/plot_params.py" "$year"
            "$WD/model/plot_preds.py" "$year"
            "$WD/model/print_sims.py" "$year" > "$WD/out/sims_$year.txt"
        ) &
    done
    wait
    for year in "${years[@]}"; do
        less "$WD/out/summary_$year.txt"
        feh "$WD/out/summary_$year.png"
        feh "$WD/out/params_$year.png"
        feh "$WD/out/preds_$year.png"
        less "$WD/out/sims_$year.txt"
    done
)
