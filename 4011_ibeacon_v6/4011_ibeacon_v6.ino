#include <M5Unified.h>
#include <BLEDevice.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>
#include "4011_ibeacon_config.h"

int loop_counter = 0;

void displayArrow(int gesture_id);

class MyAdvertisedDeviceCallbacks : public BLEAdvertisedDeviceCallbacks {
public:
  MyAdvertisedDeviceCallbacks() {}

  void onResult(BLEAdvertisedDevice advertisedDevice) {
    if (advertisedDevice.getAddress().toString() == targetMAC) {
      // Parse the iBeacon data
      uint8_t* payload = advertisedDevice.getPayload();
      int payloadLength = advertisedDevice.getPayloadLength();

      // Extract Major and Minor
      if (payloadLength > 25) {
        // Major is the update count and minor is the gesture ID
        int major = (payload[25] << 8) | payload[26];
        int minor = (payload[27] << 8) | payload[28];

        if (last_count < major) {
          if (minor > 0 && minor <= NUM_GESTURES) {
            Serial.println(gestures[minor - 1]);  // Adjusting index for 0-based array
            last_count = major;
            displayArrow(minor);
            loop_counter = 0;
          }
        }
      }
    }
  }

private:
  int last_count = 0;
};

void setup() {
  // Initialize M5Core2 and Serial
  M5.begin();
  // Clear the screen with a black background
  M5.Lcd.fillScreen(SCREEN_BACKGROUND);
  Serial.begin(115200);

  // Initialize BLE
  BLEDevice::init("");
  BLEScan* pBLEScan = BLEDevice::getScan();
  MyAdvertisedDeviceCallbacks* pCallbacks = new MyAdvertisedDeviceCallbacks();
  pBLEScan->setAdvertisedDeviceCallbacks(pCallbacks);
  pBLEScan->setActiveScan(true);
}

void loop() {
  // Main loop can handle other tasks
  BLEDevice::getScan()->start(1);
  M5.update();

  // Prints a "-" on the screen to show that it is actively searching for a gesture
  loop_counter++;
  if (loop_counter >= 10) {
    M5.Lcd.print("- ");
    loop_counter = 0;
  }
  delay(100);
}

/**
 * Displays an arrow on the M5Core2 display based on the gesture ID.
 * The screen is cleared before drawing the new arrow.
 *
 * @param gesture_id The ID of the gesture.
 */
void displayArrow(int gesture_id) {
  // Clear the screen with a black background
  M5.Lcd.fillScreen(SCREEN_BACKGROUND);

  // Set the color of the arrow to white
  M5.Lcd.setTextColor(TEXT_COLOR);

  switch (gesture_id) {
    case LEFT:
      // Draw the shaft of the arrow
      M5.Lcd.fillRect(110, 115, 100, 10, TEXT_COLOR);
      // Draw the tip of the arrow
      M5.Lcd.fillTriangle(110, 100, 110, 140, 60, 120, TEXT_COLOR);
      break;

    case RIGHT:
      // Draw the shaft of the arrow
      M5.Lcd.fillRect(90, 115, 100, 10, TEXT_COLOR);
      // Draw the tip of the arrow
      M5.Lcd.fillTriangle(190, 100, 190, 140, 240, 120, TEXT_COLOR);
      break;

    case UP:
      // Draw the shaft of the arrow
      M5.Lcd.fillRect(140, 50, 10, 100, TEXT_COLOR);
      // Draw the tip of the arrow
      M5.Lcd.fillTriangle(120, 50, 170, 50, 145, 5, TEXT_COLOR);
      break;

    case DOWN:
      // Draw the shaft of the arrow
      M5.Lcd.fillRect(140, 90, 10, 100, TEXT_COLOR);
      // Draw the tip of the arrow
      M5.Lcd.fillTriangle(120, 190, 170, 190, 145, 240, TEXT_COLOR);
      break;

    case R_LEFT:
      // Draw 3/4 of a hollow circle starting from the top (12 o'clock position)
      for (int angle = 270; angle <= 540; angle++) {
        int x1 = 160 + 50 * cos(angle * PI / 180);
        int y1 = 120 + 50 * sin(angle * PI / 180);
        M5.Lcd.drawPixel(x1, y1, TEXT_COLOR);
      }
      // Draw a triangle pointing left on the top part of the circle
      M5.Lcd.fillTriangle(160 + 20 - 30, 120 - 50, 160 + 40 - 30, 120 - 30, 160 + 40 - 30, 120 - 70, TEXT_COLOR);
      break;

    case R_RIGHT:
      // Draw 3/4 of a hollow circle starting from the right (3 o'clock position)
      for (int angle = 0; angle <= 270; angle++) {
        int x1 = 160 + 50 * cos(angle * PI / 180);
        int y1 = 120 + 50 * sin(angle * PI / 180);
        M5.Lcd.drawPixel(x1, y1, TEXT_COLOR);
      }
      // Draw a triangle pointing right on the right part of the circle
      M5.Lcd.fillTriangle(160 - 20 + 30, 120 - 50, 160 - 40 + 30, 120 - 30, 160 - 40 + 30, 120 - 70, TEXT_COLOR);
      break;

    default:
      // Optionally handle unexpected gesture IDs
      M5.Lcd.print("Unknown gesture ID");
      break;
  }
}
