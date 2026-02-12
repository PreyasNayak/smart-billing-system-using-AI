#include "HX711.h"

const int LOADCELL_DOUT_PIN = 2;
const int LOADCELL_SCK_PIN = 3;

HX711 scale;

float calibration_factor = -8192.0; // Your calculated factor (negative)

void setup() {
  Serial.begin(9600);
  Serial.println("HX711 Scale Ready");
  Serial.println("Send 't' to tare (zero)");
  
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  scale.set_scale(calibration_factor);
  
  delay(2000); // Let it stabilize
  scale.tare(20); // Auto-tare on startup
  
  Serial.println("Scale zeroed!");
}

void loop() {
  if (scale.is_ready()) {
    float weight = scale.get_units(10);
    Serial.print("Weight: ");
    Serial.print(weight, 1);
    Serial.println(" g");
  }
  
  // Manual tare command
  if (Serial.available()) {
    char cmd = Serial.read();
    if (cmd == 't') {
      scale.tare(20);
      Serial.println("Tared!");
    }
  }
  
  delay(500);
}