#include "M5Unified.h"

enum direction {
  UP = 0,
  RIGHT = 1,
  DOWN = 2,
  LEFT = 3
};

void setup() {
  // Initialize the M5Core2
  M5.begin();

  // Clear the screen with a black background
  M5.Lcd.fillScreen(BLACK);
}

int counter = UP;
void loop() {
  counter += 1;
  counter = counter % 5;
  displayArrow(counter);
  delay(1000);
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

    default:
      // Optionally handle unexpected direction
      M5.Lcd.print("Don't know that number");

      break;
  }
}