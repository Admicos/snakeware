#!/bin/sh -eu

RAM="2G"
ISO="snakeware.iso"

AUDIO="pa" # also available: alsa

exec qemu-system-x86_64 \
	-drive file="$ISO",media=cdrom,if=virtio \
	-m "$RAM" \
	-cpu host \
	-machine type=q35,accel=kvm \
	-smp $(nproc) \
	-audiodev "$AUDIO,id=snd" \
	-device ich9-intel-hda \
	-device hda-output,audiodev=snd
