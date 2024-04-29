#ifndef NRF52840_IBEACON_ADV_H_
#define NRF52840_IBEACON_ADV_H_

#include <zephyr/kernel.h>

#define NRF_IBEACON_STACK_SIZE  1024
#define NRF_IBEACON_PRIORITY    5

#define IBEACON_THREAD_SLEEP_MS 10

#define IBEACON_RSSI 0xC8

void nrf52840_ibeacon_adv_init();

#endif /* NRF52840_IBEACON_ADV_H_ */