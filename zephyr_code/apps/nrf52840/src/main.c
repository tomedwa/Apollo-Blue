#include <stdio.h>
#include <zephyr/kernel.h>
#include <zephyr/drivers/gpio.h>
#include "../../../include/nrf52840_ibeacon_adv.h"
#include "../../../include/nrf52840_uart.h"
#include "../../../include/nrf52840_leds.h"


int main(void) {
	
    nrf52840_leds_init();
    nrf52840_ibeacon_adv_init();
    nrf52840_uart_init();

    while (1) {
        k_sleep(K_FOREVER);
    }

	return 0;
}
