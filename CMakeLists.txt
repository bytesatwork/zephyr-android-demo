# SPDX-License-Identifier: Apache-2.0

cmake_minimum_required(VERSION 3.28.0)

set(EXTRA_CONF_FILE "../zephyr/samples/bluetooth/peripheral_esp/prj.conf")

find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project(android_demo)

target_sources(app PRIVATE
  ../zephyr/samples/bluetooth/peripheral_esp/src/main.c
)
