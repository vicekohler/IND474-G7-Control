// G7 - Control proyecto 2 - PRUEBA 3: PANTALLA TFT 1.3" ST7789 240x240 (7 pines, sin CS)
// Placa: Waveshare RP2350 Plus. Librerias: Adafruit ST7735 and ST7789 + Adafruit GFX.
// J4: 1 GND, 2 3V3, 3 SCL->GP18, 4 SDA->GP19, 5 RES->GP21, 6 DC->GP20, 7 BLK (sin conectar).
// Sin CS la pantalla necesita SPI modo 3.
// Secuencia: rojo, verde, azul, blanco; luego texto y una vista en vivo de botones y joystick.

#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ST7789.h>

const int TFT_SCK = 18, TFT_MOSI = 19, TFT_DC = 20, TFT_RST = 21, TFT_CS = -1;
Adafruit_ST7789 tft(&SPI, TFT_CS, TFT_DC, TFT_RST);

const uint8_t PINES[8]   = {2, 3, 4, 5, 6, 7, 8, 9};
const char*   NOMBRES[8] = {"UP", "DOWN", "LEFT", "RIGHT", "A", "B", "MENU", "JOY"};

void setup() {
  Serial.begin(115200);
  for (int i = 0; i < 8; i++) pinMode(PINES[i], INPUT_PULLUP);
  analogReadResolution(12);

  SPI.setSCK(TFT_SCK);
  SPI.setTX(TFT_MOSI);
  tft.init(240, 240, SPI_MODE3);
  tft.setRotation(1);   // contenido girado 90 grados para leerlo horizontal
  Serial.println("TFT iniciada");

  uint16_t colores[4] = {ST77XX_RED, ST77XX_GREEN, ST77XX_BLUE, ST77XX_WHITE};
  const char* nombres[4] = {"rojo", "verde", "azul", "blanco"};
  for (int i = 0; i < 4; i++) {
    tft.fillScreen(colores[i]);
    Serial.print("Pantalla en "); Serial.println(nombres[i]);
    delay(800);
  }
  tft.fillScreen(ST77XX_BLACK);
  tft.setTextColor(ST77XX_WHITE);
  tft.setTextSize(3);
  tft.setCursor(20, 10);  tft.print("G7 - D4.4");
  tft.setTextSize(2);
  tft.setCursor(20, 45);  tft.print("Pantalla OK");
}

void loop() {
  int x = analogRead(26), y = analogRead(27);
  Serial.printf("X=%d Y=%d\n", x, y);
  tft.setTextSize(2);
  tft.setTextColor(ST77XX_YELLOW, ST77XX_BLACK);
  tft.setCursor(10, 80);  tft.printf("X:%4d  Y:%4d ", x, y);
  for (int i = 0; i < 8; i++) {
    bool p = (digitalRead(PINES[i]) == LOW);
    tft.setCursor(10 + (i % 2) * 120, 110 + (i / 2) * 30);
    tft.setTextColor(p ? ST77XX_BLACK : ST77XX_WHITE, p ? ST77XX_GREEN : ST77XX_BLACK);
    tft.printf("%-6s", NOMBRES[i]);
  }
  delay(50);
}
