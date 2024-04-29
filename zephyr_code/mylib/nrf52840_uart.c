#include <stdio.h>
#include <zephyr/kernel.h>
#include <zephyr/drivers/gpio.h>
#include "../include/nrf52840_uart.h"

static void _thread_function(void* arg1, void* arg2, void* arg3);

struct k_thread NRF52840_UART_THREAD;
k_tid_t NRF52840_UART_THREAD_ID;

K_THREAD_STACK_DEFINE(NRF52840_UART_THREAD_STACK, NRF_UART_STACK_SIZE);

void nrf52840_uart_init() {

    NRF52840_UART_THREAD_ID = k_thread_create(
        &NRF52840_UART_THREAD,
        NRF52840_UART_THREAD_STACK,
        NRF_UART_STACK_SIZE,
        _thread_function,
        NULL, NULL, NULL,
        NRF_UART_PRIORITY,
        0, K_NO_WAIT
    );

    k_thread_start(NRF52840_UART_THREAD_ID);
}

static void _thread_function(void* arg1, void* arg2, void* arg3) {
    ARG_UNUSED(arg1);
    ARG_UNUSED(arg2);
    ARG_UNUSED(arg3);

    for (;;) {
        k_msleep(UART_THREAD_SLEEP_MS);
    }
}