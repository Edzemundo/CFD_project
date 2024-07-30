#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// Constants
const int analogPin = A0;  // Pin where the voltage signal is connected
const int sampleDelay = 100;  // Delay between samples in milliseconds

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 32 // OLED display height, in pixels
#define OLED_RESET     -1 // Reset pin # (or -1 if sharing Arduino reset pin)
#define SCREEN_ADDRESS 0x3C ///< See datasheet for Address; 0x3D for 128x64, 0x3C for 128x32
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);



void setup() {
  Serial.begin(9600);

  if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Don't proceed, loop forever
  }
}

void loop() {
  int analogValue = analogRead(analogPin);  // Read the analog value from the sensor
  float voltage = analogValue * (5.0 / 1023.0);  // Convert the analog value to voltage
  Serial.println(voltage, 4);  // Print the voltage to the Serial Monitor
  printVoltage(voltage);
  delay(sampleDelay);  // Wait for the specified sample delay
}

void printVoltage(float number){
  display.clearDisplay();
  display.setTextSize(2);             // Normal 1:1 pixel scale
  display.setTextColor(SSD1306_WHITE);        // Draw white text
  display.setCursor(0,0);             // Start at top-left corner
  display.println("Voltage: ");
  display.println(number,4);   
  display.display();
}