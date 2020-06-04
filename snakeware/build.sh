#!/bin/sh -eu
# This script builds a snakeware image using buildroot.
# The first and only argument should be the platform (ie x86-64)

if [ $# != 1 ]; then
  echo "Invalid number of parameters."
  echo "Usage: ./build.sh <platform>"
  exit
fi

IMG_SIZE=400M

SNAKEWARE=$PWD
IMG=snakeware.img

# check for existence of .git to make sure empty directories can still
# be cloned to
if [ ! -d "buildroot/.git" ]; then
  git clone https://github.com/buildroot/buildroot.git buildroot --depth 1
fi

if [ ! -f "$SNAKEWARE/external/configs/$1_defconfig" ]; then
  echo "Unsupported platform: $1"
  exit
fi

# run build
cd buildroot

# br2_external needs to be set only once
make BR2_EXTERNAL="$SNAKEWARE/external" "$1_defconfig"
make

cd $SNAKEWARE

cp buildroot/output/images/rootfs.iso9660 snakeware.iso

echo ""
echo "Build Successful. See snakeware.iso"
