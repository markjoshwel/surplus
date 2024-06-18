{
  description = "development environment for surplus";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    # https://github.com/NixOS/nixpkgs/issues/308121
    nixpkgs-old-hatch.url = "github:NixOS/nixpkgs/fd04bea4cbf76f86f244b9e2549fca066db8ddff";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, nixpkgs-old-hatch, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        inherit (nixpkgs) lib;
        pkgs = nixpkgs.legacyPackages.${system};
        pkgs-old-hatch = nixpkgs-old-hatch.legacyPackages.${system};
      in
      {
        devShells.default = pkgs.mkShellNoCC {
          NIX_LD_LIBRARY_PATH = lib.makeLibraryPath [
            pkgs.stdenv.cc.cc
          ];
          NIX_LD = lib.fileContents "${pkgs.stdenv.cc}/nix-support/dynamic-linker";
          buildInputs =
            [
              # surplus
              pkgs.python3
              pkgs-old-hatch.hatch

              # mkdocs-exporter
              pkgs.stdenv.cc.cc.lib
              pkgs.playwright
            ];
          shellHook = ''
            export LD_LIBRARY_PATH=$NIX_LD_LIBRARY_PATH
            export PLAYWRIGHT_BROWSERS_PATH=${pkgs.playwright-driver.browsers}
            export PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS=true
            echo LD_LIBRARY_PATH=$LD_LIBRARY_PATH
            echo PLAYWRIGHT_BROWSERS_PATH=$PLAYWRIGHT_BROWSERS_PATH
            echo PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS=$PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS
          '';
        };
      }
    );
}
