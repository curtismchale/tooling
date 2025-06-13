# shell.nix
with import <nixpkgs> {};

mkShell {
  buildInputs = [
    python3
    python3Packages.pip
  ];

  shellHook = ''
    if [ ! -d .venv ]; then
      python3 -m venv .venv
      .venv/bin/pip install --upgrade pip
      .venv/bin/pip install kobodl
    fi
    source .venv/bin/activate
  '';
}

