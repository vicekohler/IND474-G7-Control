// =====================================================================================
// G7 - Control proyecto 2 - FIRMWARE DEL CONTROL (gamepad USB)  v1.2  (PCB D4.4) - 16/11/2026
// Placa: Waveshare RP2350 Plus - Arduino-Pico 6.3.2 (Earle Philhower)
// Librerias: Adafruit ST7735 and ST7789, Adafruit GFX (pantalla). Joystick y Keyboard vienen con el nucleo.
//
// - Nucleo 0: lee botones y joystick a 1 kHz y los envia por USB (sin esperar a la pantalla).
// - Nucleo 1: dibuja el estado en la pantalla TFT.
// - Modo GAMEPAD (por defecto): stick = ejes X/Y, cruceta = hat (POV), A=1, B=2, MENU=8, JOY=9.
// - Modo TECLADO (alternativo): cruceta/stick = flechas, A=Z, B=X, MENU=Enter, JOY=Espacio.
//   Cambiar de modo: mantener MENU + B durante 1,5 s. El modo se recuerda al desenchufar.
// - Recalibrar el centro del stick: soltar el stick y mantener MENU + A 1,5 s (provisorio; antes MENU + clic del stick).
// - Monitor Serie (115200): estado cada 250 ms para diagnostico.
// =====================================================================================
#include <Joystick.h>
#include <Keyboard.h>
#include <EEPROM.h>
#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ST7789.h>

// ---------------- Pines (PCB D4.4) ----------------
enum { B_UP, B_DOWN, B_LEFT, B_RIGHT, B_A, B_B, B_MENU, B_JOY, NB };
const uint8_t  PIN_BTN[NB] = {2, 3, 4, 5, 6, 7, 8, 9};
const char*    NOMBRE[NB]  = {"UP", "DOWN", "LEFT", "RIGHT", "A", "B", "MENU", "JOY"};
const uint16_t BLOQUEO_MS[NB] = {20, 20, 20, 20, 20, 20, 40, 30};  // antirrebote (MENU rebota hasta ~32 ms)
const uint8_t  PIN_X = 26, PIN_Y = 27;
const int TFT_SCK = 18, TFT_MOSI = 19, TFT_DC = 20, TFT_RST = 21;

// ---------------- Ajustes del stick ----------------
const bool INTERCAMBIAR_XY = false;  // ajustar segun como quede montado el KY-023
const bool INVERTIR_X = false;
const bool INVERTIR_Y = false;
const int  ZONA_MUERTA = 160;        // cuentas ADC (~4 %); el ruido medido en reposo es +-30
const int  ADC_MIN = 15, ADC_MAX = 4080;
const int  UMBRAL_TECLA = 16000;     // en modo teclado, inclinacion para "apretar" una flecha (~50 %)

// ---------------- Botones HID en modo gamepad ----------------
const uint8_t HID_A = 1, HID_B = 2, HID_MENU = 8, HID_JOY = 9;

// ---------------- Estado compartido entre nucleos ----------------
enum { MODO_GAMEPAD = 0, MODO_TECLADO = 1 };
volatile bool    estBtn[NB];
volatile int16_t estX = 0, estY = 0;
volatile int     estRawX = 0, estRawY = 0;
volatile uint8_t modo = MODO_GAMEPAD;
volatile bool    pantallaRedibujar = true;
volatile uint32_t avisoCalibrado = 0;      // millis() del ultimo recalibrado (para mostrarlo en pantalla)

Adafruit_ST7789 tft(&SPI, -1, TFT_DC, TFT_RST);

// =====================================================================================
// NUCLEO 0: entradas + USB
// =====================================================================================
bool     estable[NB];
uint32_t tCambio[NB];
int      centroX = 2048, centroY = 2048;

int leerADC(uint8_t pin) {                 // promedio de 4 lecturas
  int s = 0;
  for (int i = 0; i < 4; i++) s += analogRead(pin);
  return s / 4;
}

void calibrarCentro() {                    // el stick debe estar suelto al enchufar
  long sx = 0, sy = 0;
  for (int i = 0; i < 64; i++) { sx += analogRead(PIN_X); sy += analogRead(PIN_Y); delay(3); }
  centroX = sx / 64; centroY = sy / 64;
  if (centroX < 1500 || centroX > 2600) centroX = 2048;   // si estaba movido, usar el centro teorico
  if (centroY < 1500 || centroY > 2600) centroY = 2048;
}

int16_t aEje(int raw, int c) {             // ADC 0-4095 -> HID -32767..32767 con zona muerta
  int d = raw - c;
  if (abs(d) < ZONA_MUERTA) return 0;
  long rango = (d > 0) ? (ADC_MAX - c) : (c - ADC_MIN);
  long v = (long)(abs(d) - ZONA_MUERTA) * 32767L / (rango - ZONA_MUERTA);
  if (v > 32767) v = 32767;
  return (d > 0) ? (int16_t)v : (int16_t)-v;
}

void leerBotones(uint32_t ms) {            // antirrebote: acepta el cambio al tiro y bloquea N ms
  for (int i = 0; i < NB; i++) {
    bool v = (digitalRead(PIN_BTN[i]) == LOW);
    if (v != estable[i] && (ms - tCambio[i]) >= BLOQUEO_MS[i]) { estable[i] = v; tCambio[i] = ms; }
  }
}

int anguloHat(bool u, bool d, bool l, bool r) {
  if (u && d) { u = d = false; }
  if (l && r) { l = r = false; }
  if (u && r) return 45;
  if (d && r) return 135;
  if (d && l) return 225;
  if (u && l) return 315;
  if (u) return 0;
  if (r) return 90;
  if (d) return 180;
  if (l) return 270;
  return -1;
}

// ---- modo teclado: presiona/suelta solo cuando cambia ----
const uint8_t TECLAS[8] = {KEY_UP_ARROW, KEY_DOWN_ARROW, KEY_LEFT_ARROW, KEY_RIGHT_ARROW, 'z', 'x', KEY_RETURN, ' '};
bool teclaEnviada[8];

void soltarTodo() {
  Keyboard.releaseAll();
  for (int i = 0; i < 8; i++) teclaEnviada[i] = false;
  Joystick.X(0); Joystick.Y(0); Joystick.hat(-1);
  for (int b = 1; b <= 32; b++) Joystick.button(b, false);
  Joystick.send_now();
}

void setup() {
  Serial.begin(115200);
  for (int i = 0; i < NB; i++) { pinMode(PIN_BTN[i], INPUT_PULLUP); estable[i] = false; tCambio[i] = 0; }
  analogReadResolution(12);
  EEPROM.begin(256);
  uint8_t m = EEPROM.read(0);
  modo = (m == MODO_TECLADO) ? MODO_TECLADO : MODO_GAMEPAD;
  calibrarCentro();
  Joystick.use16bit();
  Joystick.useManualSend(true);
  Joystick.begin();
  Keyboard.begin();
}

void loop() {
  static uint32_t tPrev = 0, tEnvio = 0, tSerie = 0, tCombo = 0;
  static bool comboHecho = false;
  static uint32_t tCal = 0; static bool calHecho = false;
  static int16_t ultX = 0, ultY = 0; static int ultHat = -2; static uint8_t ultBtns = 0xFF;
  uint32_t ms = millis();
  if (ms == tPrev) return;                 // 1 kHz
  tPrev = ms;

  leerBotones(ms);
  int rx = leerADC(PIN_X), ry = leerADC(PIN_Y);
  int16_t x = aEje(rx, centroX), y = aEje(ry, centroY);
  if (INTERCAMBIAR_XY) { int16_t t = x; x = y; y = t; }
  if (INVERTIR_X) x = -x;
  if (INVERTIR_Y) y = -y;

  // cambio de modo: MENU + B mantenidos 1,5 s
  if (estable[B_MENU] && estable[B_B]) {
    if (tCombo == 0) tCombo = ms;
    if (!comboHecho && ms - tCombo >= 1500) {
      soltarTodo();
      modo = (modo == MODO_GAMEPAD) ? MODO_TECLADO : MODO_GAMEPAD;
      EEPROM.write(0, modo); EEPROM.commit();
      comboHecho = true; pantallaRedibujar = true;
    }
  } else { tCombo = 0; comboHecho = false; }

  // recalibrar centro: MENU + A mantenidos 1,5 s (con el stick suelto)
  if (estable[B_MENU] && estable[B_A]) {
    if (tCal == 0) tCal = ms;
    if (!calHecho && ms - tCal >= 1500) { soltarTodo(); calibrarCentro(); avisoCalibrado = millis(); calHecho = true; }
  } else { tCal = 0; calHecho = false; }

  if (modo == MODO_GAMEPAD) {
    int hat = anguloHat(estable[B_UP], estable[B_DOWN], estable[B_LEFT], estable[B_RIGHT]);
    uint8_t btns = estable[B_A] | (estable[B_B] << 1) | (estable[B_MENU] << 2) | (estable[B_JOY] << 3);
    if (x != ultX || y != ultY || hat != ultHat || btns != ultBtns || ms - tEnvio >= 20) {
      Joystick.X(x); Joystick.Y(y); Joystick.hat(hat);
      Joystick.button(HID_A, estable[B_A]);   Joystick.button(HID_B, estable[B_B]);
      Joystick.button(HID_MENU, estable[B_MENU]); Joystick.button(HID_JOY, estable[B_JOY]);
      Joystick.send_now();
      ultX = x; ultY = y; ultHat = hat; ultBtns = btns; tEnvio = ms;
    }
  } else {
    bool quiero[8] = {
      estable[B_UP]    || y < -UMBRAL_TECLA, estable[B_DOWN]  || y > UMBRAL_TECLA,
      estable[B_LEFT]  || x < -UMBRAL_TECLA, estable[B_RIGHT] || x > UMBRAL_TECLA,
      estable[B_A], estable[B_B], estable[B_MENU] && !estable[B_B] && !estable[B_A], estable[B_JOY]};
    for (int i = 0; i < 8; i++) {
      if (quiero[i] != teclaEnviada[i]) {
        if (quiero[i]) Keyboard.press(TECLAS[i]); else Keyboard.release(TECLAS[i]);
        teclaEnviada[i] = quiero[i];
      }
    }
  }

  // estado compartido con el nucleo 1
  for (int i = 0; i < NB; i++) estBtn[i] = estable[i];
  estX = x; estY = y; estRawX = rx; estRawY = ry;

  if (ms - tSerie >= 250 && Serial && Serial.availableForWrite() > 80) {
    tSerie = ms;
    Serial.printf("%s rawX=%d rawY=%d X=%d Y=%d btn=", modo == MODO_GAMEPAD ? "GAMEPAD" : "TECLADO", rx, ry, x, y);
    for (int i = 0; i < NB; i++) Serial.print(estable[i] ? '1' : '0');
    Serial.println();
  }
}

// =====================================================================================
// NUCLEO 1: pantalla (240x240, girada para leerse horizontal)
// =====================================================================================
const int CAJA_X = 10, CAJA_Y = 42, CAJA_L = 110;          // recuadro del stick
const uint16_t GRIS = 0x4208, VERDE = ST77XX_GREEN, FONDO = ST77XX_BLACK;
struct Zona { int16_t x, y, w, h; bool circulo; };
const Zona ZONA[NB] = {
  {168, 42, 24, 24, false}, {168, 94, 24, 24, false},       // UP, DOWN
  {142, 68, 24, 24, false}, {194, 68, 24, 24, false},       // LEFT, RIGHT
  {205, 175, 16, 0, true},  {162, 195, 16, 0, true},        // A, B (centro y radio)
  {10, 168, 64, 22, false}, {10, 198, 64, 22, false}};      // MENU, JOY
bool dibujado[NB];
int puntoX = -1, puntoY = -1;

void dibujarBoton(int i, bool p) {
  const Zona& z = ZONA[i];
  uint16_t c = p ? VERDE : GRIS;
  if (z.circulo) {
    tft.fillCircle(z.x, z.y, z.w, c);
    tft.setTextColor(p ? FONDO : ST77XX_WHITE); tft.setTextSize(2);
    tft.setCursor(z.x - 5, z.y - 7); tft.print(NOMBRE[i]);
  } else {
    tft.fillRoundRect(z.x, z.y, z.w, z.h, 4, c);
    if (i >= B_MENU) {
      tft.setTextColor(p ? FONDO : ST77XX_WHITE); tft.setTextSize(2);
      tft.setCursor(z.x + 8, z.y + 4); tft.print(NOMBRE[i]);
    }
  }
  dibujado[i] = p;
}

void dibujarFondo() {
  tft.fillScreen(FONDO);
  tft.setTextSize(2);
  tft.setTextColor(modo == MODO_GAMEPAD ? ST77XX_CYAN : ST77XX_ORANGE);
  tft.setCursor(10, 10);
  tft.print(modo == MODO_GAMEPAD ? "G7  GAMEPAD" : "G7  TECLADO");
  tft.drawRect(CAJA_X, CAJA_Y, CAJA_L, CAJA_L, ST77XX_WHITE);
  for (int i = 0; i < NB; i++) dibujarBoton(i, estBtn[i]);
  tft.setTextSize(1); tft.setTextColor(GRIS);
  tft.setCursor(82, 168); tft.print("MENU+B");
  tft.setCursor(82, 178); tft.print("= modo");
  tft.setCursor(82, 198); tft.print("MENU+A");
  tft.setCursor(82, 208); tft.print("= centro");
  puntoX = puntoY = -1;
}

void dibujarPunto() {
  int cx = CAJA_X + CAJA_L / 2, cy = CAJA_Y + CAJA_L / 2, r = CAJA_L / 2 - 8;
  int px = cx + (long)estX * r / 32767, py = cy + (long)estY * r / 32767;
  if (px == puntoX && py == puntoY) return;
  if (puntoX >= 0) tft.fillCircle(puntoX, puntoY, 6, FONDO);
  tft.drawFastHLine(CAJA_X + 1, cy, CAJA_L - 2, GRIS);
  tft.drawFastVLine(cx, CAJA_Y + 1, CAJA_L - 2, GRIS);
  tft.fillCircle(px, py, 6, ST77XX_YELLOW);
  puntoX = px; puntoY = py;
}

void setup1() {
  delay(200);
  SPI.setSCK(TFT_SCK);
  SPI.setTX(TFT_MOSI);
  tft.init(240, 240, SPI_MODE3);
  tft.setRotation(1);
}

void loop1() {
  static uint32_t tTexto = 0;
  if (pantallaRedibujar) { pantallaRedibujar = false; dibujarFondo(); }
  for (int i = 0; i < NB; i++) if (estBtn[i] != dibujado[i]) dibujarBoton(i, estBtn[i]);
  dibujarPunto();
  if (millis() - tTexto > 200) {
    tTexto = millis();
    tft.setTextSize(1); tft.setTextColor(ST77XX_WHITE, FONDO);
    tft.setCursor(10, 228); tft.printf("X:%4d Y:%4d   centro %d/%d  ", estRawX, estRawY, centroX, centroY);
    tft.setCursor(130, 128);
    if (avisoCalibrado && millis() - avisoCalibrado < 2000) { tft.setTextColor(ST77XX_GREEN, FONDO); tft.print("CENTRO OK  "); }
    else tft.print("           ");
  }
  delay(15);
}
