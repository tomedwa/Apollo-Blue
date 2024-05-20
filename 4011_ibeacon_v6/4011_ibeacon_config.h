#ifndef IBEACON_CONFIG_H
#define IBEACON_CONFIG_H

#include <string>

// Target iBeacon MAC address
// Change if the iBeacon has a different MAC address
const std::string targetMAC = "11:98:65:34:12:76";

// Enum for gesture IDs
// Change if gestures should match other numbers sent to the M5
enum GestureID {
  LEFT = 0x01,
  RIGHT = 0x02,
  UP = 0x03,
  DOWN = 0x04,
  R_LEFT = 0x05,
  R_RIGHT = 0x06
};

// Gesture names
// Change if the GUI takes in other names over UART
const char* gestures[] = {
  "left", "right", "up", "down", "r_left", "r_right"
};

// Number of gestures
const int NUM_GESTURES = sizeof(gestures) / sizeof(gestures[0]);

// Display colors
const uint16_t SCREEN_BACKGROUND = BLACK;
const uint16_t TEXT_COLOR = WHITE;

#endif  // IBEACON_CONFIG_H
