{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python313
    pkgs.python313Packages.pygame-ce
  ];

  shellHook = ''
    alias supermuki='python3 SuperMuki.py'
    echo "Simply run 'supermuki' to run the game!"
  '';
}
