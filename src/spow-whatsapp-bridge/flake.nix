{
  description = "development environment for surplus on wheels: WhatsApp Bridge";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    gomod2nix = {
      url = "github:nix-community/gomod2nix";
      inputs.nixpkgs.follows = "nixpkgs";
      inputs.flake-utils.follows = "flake-utils";
    };
  };

  outputs = { self, nixpkgs, flake-utils, gomod2nix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        bridge = {
          name = "spow-whatsapp-bridge";
          version = "2.2024.26";
        };

        pkgs = import nixpkgs {
          system = system;
          overlays = [
            gomod2nix.overlays.default
          ];
          config = {
            android_sdk.accept_license = true;
            allowUnfree = true;
          };
        };

        sdk = (pkgs.androidenv.composeAndroidPackages {
          includeSources = false;
          includeSystemImages = false;
          includeEmulator = false;
          includeNDK = true;
          ndkVersions = ["26.3.11579264"];
        }).androidsdk;

        androidClang = (
          "${sdk}/libexec/android-sdk/ndk-bundle/toolchains/llvm/prebuilt/"
          +
          (
            {
              "x86_64-darwin" = "darwin-x86_64";
              "x86_64-linux" = "linux-x86_64";
            }."${system}" or
              (throw "the android ndk does not support your platform... (；′⌒`) (apple silicon users see https://github.com/android/ndk/issues/1299)")
          )
          +
          "/bin/aarch64-linux-android30-clang"
        );

        bridgeBuildTermux = pkgs.buildGoApplication {
          pname = bridge.name;
          version = bridge.version;

          go = pkgs.go_1_22;
          src = ./.;
          modules = ./gomod2nix.toml;

          buildInputs = [ sdk ];
          buildPhase = ''
            runHook preBuild
            mkdir -p $out/bin
            CC="${androidClang}" CGO_ENABLED=1 GOOS=android GOARCH=arm64 go build -o $out/bin
            runHook postBuild
          '';
        };

        bridgeBuildNative = pkgs.buildGoApplication {
          pname = bridge.name;
          version = bridge.version;

          go = pkgs.go_1_22;
          src = ./.;
          modules = ./gomod2nix.toml;
        };
      in
      with pkgs; {
        # nix develop
        devShells.default = mkShell {
          buildInputs = [
            go
            golint
            gomod2nix.packages.${system}.default
          ];
        };

        # nix build .#termux
        packages.termux = stdenvNoCC.mkDerivation {
          pname = bridge.name;
          version = bridge.version;
          src = bridgeBuildTermux;

          installPhase = ''
            mkdir -p $out
            cp $src/bin/$pname $out/$pname
          '';
        };

        # nix build
        packages.default = stdenvNoCC.mkDerivation {
          pname = bridge.name;
          version = bridge.version;
          src = bridgeBuildNative;

          installPhase = ''
            mkdir -p $out
            cp $src/bin/$pname $out/$pname
          '';
        };
      }
    );
}
