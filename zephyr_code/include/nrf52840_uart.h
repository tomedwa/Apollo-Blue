#ifndef NRF52840_UART_H_
#define NRF52840_UART_H_

#include <zephyr/kernel.h>

#define NRF_UART_STACK_SIZE  1024
#define NRF_UART_PRIORITY    5

#define UART_THREAD_SLEEP_MS 10

#define MSG_Q_SIZE 10
extern struct k_msgq uart_q;

void nrf52840_uart_init();

#endif /* NRF52840_UART_H_ */