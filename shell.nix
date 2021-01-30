with import <nixpkgs> {};
mkShell {
    buildInputs = [
        (python38.withPackages(ps: with ps; [
            beautifulsoup4
            flake8
            pandas
        ]))
        csvkit
        shellcheck
    ];
    shellHook = ''
        . .shellhook
    '';
}
