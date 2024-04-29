#include <stdio.h>
#include <zephyr/kernel.h>
#include <zephyr/bluetooth/bluetooth.h>
#include <zephyr/bluetooth/uuid.h>
#include <zephyr/bluetooth/conn.h>
#include <zephyr/bluetooth/gatt.h>
#include "../include/nrf52840_ibeacon_adv.h"

static void _thread_function(void* arg1, void* arg2, void* arg3);

struct k_thread NRF52840_IBEACON_THREAD;
k_tid_t NRF52840_IBEACON_THREAD_ID;

K_THREAD_STACK_DEFINE(NRF52840_IBEACON_THREAD_STACK, NRF_IBEACON_STACK_SIZE);



void nrf52840_ibeacon_adv_init() {

    NRF52840_IBEACON_THREAD_ID = k_thread_create(
        &NRF52840_IBEACON_THREAD,
        NRF52840_IBEACON_THREAD_STACK,
        NRF_IBEACON_STACK_SIZE,
        _thread_function,
        NULL, NULL, NULL,
        NRF_IBEACON_PRIORITY,
        0, K_NO_WAIT
    );

    k_thread_start(NRF52840_IBEACON_THREAD_ID);
}

static void _thread_function(void* arg1, void* arg2, void* arg3) {
    ARG_UNUSED(arg1);
    ARG_UNUSED(arg2);
    ARG_UNUSED(arg3);

    struct bt_data ad[] = {
        BT_DATA_BYTES(BT_DATA_FLAGS, BT_LE_AD_NO_BREDR),
        BT_DATA_BYTES(BT_DATA_MANUFACTURER_DATA,
                0x4c, 0x00, /* Apple */
                0x02, 0x15, /* iBeacon */
                'A', 'P', 'O', 'L', /* UUID[15..12] */
                'L', 'O', /* UUID[11..10] */
                '-', 'B', /* UUID[9..8] */
                'L', 'U', /* UUID[7..6] */
                'E', 0x01, 0x02, 0x03, 0x04, 0x05, /* UUID[5..0] */
                'A', 'B', /* Major */
                'C', 'D', /* Minor */
                IBEACON_RSSI) /* Calibrated RSSI @ 1m */
    };

    int err;

    err = bt_enable(NULL);

    struct bt_le_adv_param adv_param = BT_LE_ADV_PARAM_INIT(
        BT_LE_ADV_OPT_USE_NAME | BT_LE_ADV_OPT_USE_TX_POWER,
        BT_GAP_ADV_FAST_INT_MIN_1, BT_GAP_ADV_FAST_INT_MAX_1,
        NULL);


    err = bt_le_adv_start(&adv_param, ad, ARRAY_SIZE(ad), NULL, 0);

    for (;;) {
        k_msleep(IBEACON_THREAD_SLEEP_MS);
    }
}
