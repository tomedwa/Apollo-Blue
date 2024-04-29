#include <stdio.h>
#include <zephyr/kernel.h>
#include <zephyr/drivers/gpio.h>
#include "../include/nrf52840_leds.h"

static void _thread_function(void* arg1, void* arg2, void* arg3);

static const struct gpio_dt_spec ledUpdate_ibeacon = GPIO_DT_SPEC_GET(LED_UPDATE_IBEACON, gpios);

struct k_thread NRF52840_LEDS_THREAD;
k_tid_t NRF52840_LEDS_THREAD_ID;

K_THREAD_STACK_DEFINE(NRF52840_LEDS_THREAD_STACK, NRF_LED_STACK_SIZE);

void nrf52840_leds_init() {
    if (!gpio_is_ready_dt(&ledUpdate_ibeacon)) {
        // error
    }

    gpio_pin_configure_dt(&ledUpdate_ibeacon, GPIO_OUTPUT_INACTIVE);

    NRF52840_LEDS_THREAD_ID = k_thread_create(
        &NRF52840_LEDS_THREAD,
        NRF52840_LEDS_THREAD_STACK,
        NRF_LED_STACK_SIZE,
        _thread_function,
        NULL, NULL, NULL,
        NRF_LED_PRIORITY,
        0, K_NO_WAIT
    );

    k_thread_start(NRF52840_LEDS_THREAD_ID);
}

static void _thread_function(void* arg1, void* arg2, void* arg3) {
    ARG_UNUSED(arg1);
    ARG_UNUSED(arg2);
    ARG_UNUSED(arg3);

    uint8_t on = 0x00;

    for (;;) {

        if (on == 0x00) {
            gpio_pin_configure_dt(&ledUpdate_ibeacon, GPIO_OUTPUT_ACTIVE);
        } else {
            gpio_pin_configure_dt(&ledUpdate_ibeacon, GPIO_OUTPUT_INACTIVE);
        }
        on ^= 1;

        k_msleep(LED_THREAD_SLEEP_MS);
    }
}
