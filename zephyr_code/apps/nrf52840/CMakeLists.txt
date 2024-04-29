# SPDX-License-Identifier: Apache-2.0

cmake_minimum_required(VERSION 3.20.0)
find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project(nrf52840)

target_sources(app PRIVATE
    src/main.c
    ${CMAKE_CURRENT_SOURCE_DIR}/../../mylib/nrf52840_ibeacon_adv.c
    ${CMAKE_CURRENT_SOURCE_DIR}/../../mylib/nrf52840_uart.c
    ${CMAKE_CURRENT_SOURCE_DIR}/../../mylib/nrf52840_leds.c
)
