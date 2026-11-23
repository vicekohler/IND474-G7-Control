// G7 - Control proyecto 2 - PRUEBA 2: JOYSTICK KY-023
// Placa: Waveshare RP2350 Plus. KY-023 por cable XH a J3 (GND, 3V3, VRx, VRy, SW).
// VRx -> GP26 (ADC0), VRy -> GP27 (ADC1), SW -> GP9 (a GND, pull-up interno).
// Monitor Serie a 115200: imprime X, Y (0-4095) y el boton 10 veces por segundo.
// En reposo X e Y deberian estar cerca de 2048; en los extremos cerca de 0 y 4095.

const uint8_t PIN_X = 26, PIN_Y = 27, PIN_SW = 9;

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);
  pinMode(PIN_SW, INPUT_PULLUP);
  pinMode(LED_BUILTIN, OUTPUT);
  delay(1500);
  Serial.println("Prueba de joystick lista. Mueve la palanca y presionala.");
}

void loop() {
  long sx = 0, sy = 0;
  for (int i = 0; i < 16; i++) { sx += analogRead(PIN_X); sy += analogRead(PIN_Y); }
  int x = sx / 16, y = sy / 16;
  bool sw = (digitalRead(PIN_SW) == LOW);
  digitalWrite(LED_BUILTIN, sw);
  Serial.print("X="); Serial.print(x);
  Serial.print("  Y="); Serial.print(y);
  Serial.print("  SW="); Serial.println(sw ? "PRESIONADO" : "-");
  delay(100);
}
