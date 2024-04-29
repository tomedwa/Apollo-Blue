#ifndef NRF52840_LEDS_H_
#define NRF52840_LEDS_H_

#include <zephyr/kernel.h>

#define NRF_LED_STACK_SIZE  1024
#define NRF_LED_PRIORITY    5

#define LED_UPDATE_IBEACON DT_ALIAS(led0)

#define LED_ON  0x01
#define LED_OFF 0x00

#define LED_THREAD_SLEEP_MS 100

void nrf52840_leds_init();

#endif /* NRF52840_LEDS_H_ */