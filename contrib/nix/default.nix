{ pkgs ? import <nixpkgs> {} }:

(
  pkgs.buildFHSUserEnv {
    name = "snakeware-build";

    runScript = ''
      env NIX_LDFLAGS="$NIX_LDFLAGS -lncurses" bash
    '';

    targetPkgs = pkgs: (with pkgs; [
      # Buildroot
      which
      gnused
      gnumake
      binutils
      gcc
      bash
      gnupatch
      gzip
      bzip2
      perl
      gnutar
      cpio
      unzip
      rsync
      file
      bc
      wget
      git
      coreutils
      utillinux

      # Make menuconfig
      ncurses.dev

      # Python Dependencies
      bzip2.dev
      lzma.dev

      # Kernel Dependencies
      libelf
      openssl.dev

      # Snakeware-specific
      mercurial

      # Testing the builds
      qemu_kvm

      # Buildroot scanpypi
      (python3.withPackages (pypkg: with pypkg; [
        # Builroot utils/scanpypi
        six
        setuptools

        pip

        # SnakeWM
        pygame
        # TODO: Package pygame_gui
      ]))
  ]);
}).env
