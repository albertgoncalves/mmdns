with import <nixpkgs> {};
mkShell {
    buildInputs = [
        (python38.withPackages(ps: with ps; [
            beautifulsoup4
            flake8
            matplotlib
            pandas
        ]))
        csvkit
        feh
        jq
        shellcheck
    ];
    shellHook = ''
        . .shellhook
    '';
}
