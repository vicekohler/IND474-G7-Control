// G7 - Control proyecto 2 - PRUEBA 4: REBOTE DE BOTONES
// Lee MENU (GP8) y A (GP6, para comparar) lo mas rapido posible y registra cada cambio.
// Cada pulsacion (o soltada) se agrupa: primer cambio tras 50 ms de calma = inicio del evento.
// Se informa cuantos cambios hubo y cuanto duro el rebote (us). Un boton sano: 1 cambio o rebote < 5 ms.

const uint8_t PINES[2] = {8, 6};
const char* NOMBRES[2] = {"MENU", "A"};
bool estado[2];
uint32_t tInicio[2], tUltimo[2];
int cambios[2];
bool enEvento[2];
bool nivelInicial[2];

void setup() {
  Serial.begin(115200);
  for (int i = 0; i < 2; i++) {
    pinMode(PINES[i], INPUT_PULLUP);
    estado[i] = digitalRead(PINES[i]);
    enEvento[i] = false;
  }
  delay(1500);
  Serial.println("Prueba de rebote lista");
}

void loop() {
  uint32_t ahora = micros();
  for (int i = 0; i < 2; i++) {
    bool v = digitalRead(PINES[i]);
    if (v != estado[i]) {
      if (!enEvento[i]) {
        enEvento[i] = true; cambios[i] = 0; tInicio[i] = ahora; nivelInicial[i] = v;
      }
      cambios[i]++; tUltimo[i] = ahora; estado[i] = v;
    }
    if (enEvento[i] && (ahora - tUltimo[i]) > 50000) {
      Serial.printf("%s %s: %d cambios, rebote %lu us\n", NOMBRES[i],
                    nivelInicial[i] == LOW ? "PRESION" : "SOLTADA", cambios[i],
                    (unsigned long)(tUltimo[i] - tInicio[i]));
      enEvento[i] = false;
    }
  }
}
