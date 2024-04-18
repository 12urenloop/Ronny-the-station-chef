{
  description = "Gonny the station chef";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    devshell = {
      url = "github:numtide/devshell";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { flake-utils, nixpkgs, devshell, ... }:
    flake-utils.lib.eachDefaultSystem (system: 
      let
        pkgs = import nixpkgs {
          inherit system;

          overlays = [ devshell.overlays.default ];
        };
      in
      with pkgs; {
        devShells.default = pkgs.devshell.mkShell {
          packages = [ go postgresql ];
          commands = [
            {
              name = "pg:setup";
              category = "database";
              help = "Setup postgres in project folder";
              command = ''
                initdb --encoding=UTF8 --no-locale --no-instructions -U postgres
                echo "listen_addresses = ${"'"}${"'"}" >> $PGDATA/postgresql.conf
                echo "unix_socket_directories = '$PGDATA'" >> $PGDATA/postgresql.conf
                echo "CREATE USER ronny WITH PASSWORD 'ronnydbpassword' CREATEDB SUPERUSER;" | postgres --single -E postgres
                echo "CREATE DATABASE ronny WITH owner 'ronny';" | postgres --single -E postgres
              '';
            }
            {
              name = "pg:start";
              category = "database";
              help = "Start postgres instance";
              command = ''
                [ ! -d $PGDATA ] && pg:setup
                postgres
              '';
            }
          ];
          env = [
            { name = "DATABASE_HOST"; eval = "$PRJ_DATA_DIR/postgres"; }
            { name = "PGDATA"; eval = "$PRJ_DATA_DIR/postgres"; }
          ];
        };
      }
    );
}
