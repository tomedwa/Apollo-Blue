#include <stdio.h>
#include <zephyr/kernel.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/device.h>
#include <zephyr/drivers/uart.h>
#include <string.h>
#include "../include/nrf52840_uart.h"

#define MSG_SIZE 32

/* queue to store up to 10 messages (aligned to 4-byte boundary) */
K_MSGQ_DEFINE(uart_msgq, MSG_SIZE, 10, 4);

static void _thread_function(void* arg1, void* arg2, void* arg3);
static void serial_cb(const struct device *dev, void *user_data);
static uint8_t check_incoming_serial(char* message);
static void send_message(char* message);

struct k_thread NRF52840_UART_THREAD;
k_tid_t NRF52840_UART_THREAD_ID;

K_THREAD_STACK_DEFINE(NRF52840_UART_THREAD_STACK, NRF_UART_STACK_SIZE);

static const struct device *const uart_dev = DEVICE_DT_GET(DT_NODELABEL(uart0));

static char rx_buf[MSG_SIZE];
static int rx_buf_pos;

K_MSGQ_DEFINE(uart_q, sizeof(char*), MSG_Q_SIZE, 4);

void print_uart(char *buf)
{
	int msg_len = strlen(buf);

	for (int i = 0; i < msg_len; i++) {
		uart_poll_out(uart_dev, buf[i]);
	}
}

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

    char tx_buf[MSG_SIZE];

	if (!device_is_ready(uart_dev)) {
		printk("UART device not found!");
		return;
	}

    /* configure interrupt and callback to receive data */
	int ret = uart_irq_callback_user_data_set(uart_dev, serial_cb, NULL);

    if (ret < 0) {
		if (ret == -ENOTSUP) {
			printk("Interrupt-driven UART API support not enabled\n");
		} else if (ret == -ENOSYS) {
			printk("UART device does not support interrupt-driven API\n");
		} else {
			printk("Error setting UART callback: %d\n", ret);
		}
		return;
	}
	uart_irq_rx_enable(uart_dev);

    for (;;) {

        while (k_msgq_get(&uart_msgq, &tx_buf, K_FOREVER) == 0) {
            print_uart("Echo: ");
            print_uart(tx_buf);
            print_uart("\r\n");
        }
        k_msleep(UART_THREAD_SLEEP_MS);
    }
}

static void serial_cb(const struct device *dev, void *user_data)
{
	uint8_t c;

	if (!uart_irq_update(uart_dev)) {
		return;
	}

	if (!uart_irq_rx_ready(uart_dev)) {
		return;
	}

	/* read until FIFO empty */
	while (uart_fifo_read(uart_dev, &c, 1) == 1) {
		if ((c == '\n' || c == '\r' || c == '$') && rx_buf_pos > 0) {
			/* terminate string */
			rx_buf[rx_buf_pos] = '\0';

            check_incoming_serial(rx_buf);

            /* if queue is full, message is silently dropped */
            k_msgq_put(&uart_msgq, &rx_buf, K_NO_WAIT);

			/* reset the buffer (it was copied to the msgq) */
			rx_buf_pos = 0;
		} else if (rx_buf_pos < (sizeof(rx_buf) - 1)) {
			rx_buf[rx_buf_pos++] = c;
		}
		/* else: characters beyond buffer size are dropped */
	}
}

static uint8_t check_incoming_serial(char* message) {
    uint8_t ret = 0;
    char msg_to_send[2] = {'X', '\0'};

    if (strlen(message) == 1) {
        for (uint8_t i = 1; i <= 6; i++) {
            if (message[0] == i + '0') {
                ret = 1;
                msg_to_send[0] = i + '0';
                send_message(msg_to_send);
                break;
            }
        }
    }
    return ret;
}

static void send_message(char* message) {
    char* msg = k_malloc(strlen(message) + 1);
    if (!msg) {
        return;
    }
    strcpy(msg, message);
    k_msgq_put(&uart_q, &msg, K_NO_WAIT);
}