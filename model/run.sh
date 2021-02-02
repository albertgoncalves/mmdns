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
    (
        cd "$WD/cmdstan"
        make "$WD/build/model"
    )
    for x in 2017 2018 2019; do
        "$WD/model/export_data.py" "$x"
        "$WD/build/model" \
            sample \
            num_warmup=1000 \
            num_samples=1000 \
            data file="$WD/out/data_$x.json" \
            output file="$WD/out/output_$x.csv"
        "$WD/cmdstan/bin/stansummary" "$WD/out/output_$x.csv"
        grep -v "#" "$WD/out/output_$x.csv" > "$WD/out/samples_$x.csv"
        "$WD/model/plot_summary.py" "$x"
        feh "$WD/out/summary_$x.png"
        "$WD/model/plot_params.py" "$x"
        feh "$WD/out/params_$x.png"
    done
)
