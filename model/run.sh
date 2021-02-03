#!/usr/bin/env bash

set -eu

if [ ! -d "$WD/cmdstan" ]; then
    (
        cd "$WD" || exit 1
        git clone https://github.com/stan-dev/cmdstan.git --recursive
        cd "$WD/cmdstan" || exit 1
        make build
    )
fi

flags=(
    "-march=native"
    "-O3"
    "-Wall"
    "-Wcast-align"
    "-Wcast-align=strict"
    "-Wcast-qual"
    "-Wdate-time"
    "-Wduplicated-branches"
    "-Wduplicated-cond"
    "-Werror"
    "-Wextra"
    "-Wfatal-errors"
    "-Wformat-signedness"
    "-Wformat=2"
    "-Winline"
    "-Wlogical-op"
    "-Wmissing-include-dirs"
    "-Wno-analyzer-possible-null-argument"
    "-Wno-deprecated-copy"
    "-Wno-type-limits"
    "-Wno-unused-but-set-variable"
    "-Wno-unused-function"
    "-Wno-unused-local-typedefs"
    "-Wno-unused-parameter"
    "-Wno-unused-variable"
    "-Wnull-dereference"
    "-Wpacked"
    "-Wpointer-arith"
    "-Wredundant-decls"
    "-Wstack-protector"
    "-Wswitch-enum"
    "-Wtrampolines"
    "-Wwrite-strings"
)
export CXXFLAGS="${flags[*]}"

(
    if ! cmp -s "$WD/model/model.stan" "$WD/build/model.stan"; then
        cp "$WD/model/model.stan" "$WD/build"
        "$WD/cmdstan/bin/stanc" \
            --warn-uninitialized \
            --warn-pedantic \
            "$WD/build/model.stan"
    fi
)
(
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
                num_samples=1000 \
                data file="$WD/out/data_$year.json" \
                output file="$WD/out/output_$year.csv"
            grep -v "#" "$WD/out/output_$year.csv" \
                > "$WD/out/samples_$year.csv"
            "$WD/model/plot_summary.py" "$year"
            "$WD/model/plot_params.py" "$year"
            "$WD/model/plot_preds.py" "$year"
            "$WD/cmdstan/bin/stansummary" "$WD/out/output_$year.csv" \
                > "$WD/out/summary_$year.txt"
        ) &
    done
    wait
    for year in "${years[@]}"; do
        less "$WD/out/summary_$year.txt"
        feh "$WD/out/summary_$year.png"
        feh "$WD/out/params_$year.png"
        feh "$WD/out/preds_$year.png"
    done
)
