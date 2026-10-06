#!/bin/sh
set -e

BASEDIR=$(realpath "$(dirname "$0")")

docker build \
    --tag zephyr-android-demo \
    --build-arg KVM_GID="$(getent group kvm | cut -d: -f3)" \
    "${BASEDIR}"

docker run \
    --rm \
    --volume "${BASEDIR}/..:/workspace" \
    --device /dev/kvm \
    --group-add kvm \
    zephyr-android-demo \
    west twister -civT demo
