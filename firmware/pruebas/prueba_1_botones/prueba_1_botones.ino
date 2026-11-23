// G7 - Control proyecto 2 - PRUEBA 1: BOTONES
// Placa: Waveshare RP2350 Plus (Arduino-Pico de Earle Philhower)
// Monitor Serie a 115200: cada vez que presionas o sueltas un boton aparece en pantalla.
// Los botones van a GND, por eso se usan las resistencias pull-up internas: presionado = LOW.

const uint8_t PINES[8]   = {2, 3, 4, 5, 6, 7, 8, 9};
const char*   NOMBRES[8] = {"UP", "DOWN", "LEFT", "RIGHT", "A", "B", "MENU", "JOY_SW"};
bool anterior[8];

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  for (int i = 0; i < 8; i++) {
    pinMode(PINES[i], INPUT_PULLUP);
    anterior[i] = false;
  }
  delay(1500);
  Serial.println("Prueba de botones lista. Presiona cada boton:");
}

void loop() {
  bool alguno = false;
  for (int i = 0; i < 8; i++) {
    bool presionado = (digitalRead(PINES[i]) == LOW);
    if (presionado) alguno = true;
    if (presionado != anterior[i]) {
      Serial.print(NOMBRES[i]);
      Serial.print(" (GP");
      Serial.print(PINES[i]);
      Serial.println(presionado ? ") PRESIONADO" : ") suelto");
      anterior[i] = presionado;
    }
  }
  digitalWrite(LED_BUILTIN, alguno);  // el LED de la placa se enciende mientras haya un boton presionado
  delay(10);                          // antirrebote simple
}
