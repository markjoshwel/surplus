{
  description = "development environment for surplus on wheels: Telegram Bridge";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryEnv;

        poetryEnv = mkPoetryEnv {
          python = pkgs.python311;
          projectDir = self;
          preferWheels = true;
        };
      in
      {
        # nix develop
        devShells.default = pkgs.mkShellNoCC {
          packages = [
            pkgs.poetry
            poetryEnv
          ];
        };
      }
    );
}
