# Bring-up de la PCB D4.4

Encendido paso a paso: un periférico a la vez, comprobando cada uno antes de sumar el siguiente.

| Paso | Prueba | Resultado | Evidencia |
|---|---|---|---|
| 1 | Blink del LED GP25 + log serie | ✅ | — |
| 2 | 7 botones (GP2–GP8) | ✅ | `firmware/pruebas/prueba_1_botones` |
| 3 | Rebote de MENU | Una soltada de 31,7 ms → antirrebote de 40 ms | `firmware/pruebas/prueba_4_rebote` |
| 4 | Joystick X/Y/SW | ✅ (arriba = Y−, derecha = X+). Hallazgo: **falso contacto en el cable XH** | `firmware/pruebas/lecturas/` |
| 5 | Pantalla ST7789 | ✅ `setRotation(1)`; algunos píxeles muertos | `firmware/pruebas/prueba_3_pantalla` |
| 6 | Firmware completo v1.2 | ✅ gamepad-tester, SuperTux, dinosaurio de Chrome | `firmware/G7_Gamepad` |

## Mediciones

El USB entrega 5 V (VBUS) y el módulo los regula a 3,3 V. Todo el circuito, incluido el joystick, trabaja a 3,3 V: el ADC del RP2350 admite hasta 3,3 V, así que el KY-023 no debe alimentarse con 5 V.


⏳ **Pendiente.** Con el control enchufado por USB y el multímetro:

| Medición | Dónde | Esperado | Medido | Foto |
|---|---|---|---|---|
| 3V3 | Pin 36 del módulo ↔ GND | 3,3 V ± 5 % | | |
| 5V (VBUS) | Pin 40 del módulo ↔ GND | 5,0 V ± 5 % | | |
| Alimentación del joystick | Pin "+5V" del KY-023 ↔ GND | **3,3 V** (J3 lo alimenta desde 3V3; el rótulo "+5V" es solo serigrafía) | | |
| Consumo en reposo | Medidor USB en serie | — | | |
| Consumo con la pantalla actualizando | Medidor USB en serie | — | | |

Agregar las fotos en esta carpeta y una captura del log serie (`log_serie.txt`).
