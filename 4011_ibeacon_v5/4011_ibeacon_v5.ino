#include "M5Unified.h"
#include <BLEDevice.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>

enum direction {
  LEFT = 1,
  RIGHT = 2,
  UP = 3,
  DOWN = 4,
  R_LEFT = 5,
  R_RIGHT = 6

};

//Might send this instead
const char* gestures[] = { "left", "right", "up", "down", "r_left", "r_right" };


void displayArrow(int dir);

const std::string targetMAC = "11:98:65:34:12:76";  // Replace with your iBeacon's MAC address

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
        int major = (payload[25] << 8) | payload[26];
        int minor = (payload[27] << 8) | payload[28];



        if (last_count < major) {
          Serial.println(gestures[minor]);
          last_count = major;
          displayArrow(minor);
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
  M5.Lcd.fillScreen(BLACK);
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
  delay(100);
}





/**
 * Displays an arrow on the M5Core2 display in one of four directions.
 * The screen is cleared before drawing the new arrow.
 *
 * @param dir The direction in which the arrow should point. 
 *            Use the predefined constants UP, DOWN, LEFT, or RIGHT to specify the direction.
 */
void displayArrow(int dir) {
  // Clear the screen with a black background
  M5.Lcd.fillScreen(BLACK);

  // Set the color of the arrow to white
  M5.Lcd.setTextColor(WHITE);

  switch (dir) {
    case UP:
      // Draw the shaft of the arrow
      M5.Lcd.fillRect(140, 50, 10, 100, WHITE);
      // Draw the tip of the arrow
      M5.Lcd.fillTriangle(120, 50, 170, 50, 145, 5, WHITE);
      break;

    case RIGHT:
      // Draw the shaft of the arrow
      M5.Lcd.fillRect(90, 115, 100, 10, WHITE);
      // Draw the tip of the arrow
      M5.Lcd.fillTriangle(190, 100, 190, 140, 240, 120, WHITE);
      break;

    case DOWN:
      // Draw the shaft of the arrow
      M5.Lcd.fillRect(140, 90, 10, 100, WHITE);
      // Draw the tip of the arrow
      M5.Lcd.fillTriangle(120, 190, 170, 190, 145, 240, WHITE);
      break;

    case LEFT:
      // Draw the shaft of the arrow
      M5.Lcd.fillRect(110, 115, 100, 10, WHITE);
      // Draw the tip of the arrow
      M5.Lcd.fillTriangle(110, 100, 110, 140, 60, 120, WHITE);
      break;

    case R_LEFT:
      // Draw 3/4 of a hollow circle starting from the top (12 o'clock position)
      for (int angle = 270; angle <= 540; angle++) {
        int x1 = 160 + 50 * cos(angle * PI / 180);
        int y1 = 120 + 50 * sin(angle * PI / 180);
        M5.Lcd.drawPixel(x1, y1, WHITE);
      }
      // Draw a triangle pointing left on the top part of the circle
      M5.Lcd.fillTriangle(160 + 20 - 30, 120 - 50, 160 + 40 - 30, 120 - 30, 160 + 40 - 30, 120 - 70, WHITE);

      break;

    case R_RIGHT:
      // Draw 3/4 of a hollow circle starting from the right (3 o'clock position)
      for (int angle = 0; angle <= 270; angle++) {
        int x1 = 160 + 50 * cos(angle * PI / 180);
        int y1 = 120 + 50 * sin(angle * PI / 180);
        M5.Lcd.drawPixel(x1, y1, WHITE);
      }
      // Draw a triangle pointing right on the right part of the circle
      M5.Lcd.fillTriangle(160 - 20 + 30, 120 - 50, 160 - 40 + 30, 120 - 30, 160 - 40 + 30, 120 - 70, WHITE);
      break;


    default:
      // Optionally handle unexpected direction
      M5.Lcd.print("Don't know that number");

      break;
  }
}
