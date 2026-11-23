# Cambios desde la entrega D4.4

**Grupo 7 (G7) · IND474 · actualizado 23/11/2026**

La PCB fabricada es la D4.4 entregada el 27/10/2026, sin cambios. La carpeta `01_PCB_D4.4_entregada` se conserva tal como se entregó. Este documento registra lo que cambió después, en el alcance, el armado, el firmware y la carcasa, para incorporarlo en la próxima entrega.

## Alcance: juegos de PC en general (feedback del profesor)

El profesor pidió que el control sirva para **juegos de PC en general, no solo MakeCode Arcade**. Cambios que lo resuelven:

| Tema | En la propuesta / D4.4 | Cómo quedó |
|---|---|---|
| Plataforma | Teclado para MakeCode Arcade | **Gamepad HID estándar** ("Control G7", sin drivers) + **modo teclado** para juegos que solo aceptan teclado. MENU + B 1,5 s cambia el modo (queda guardado). |
| Indicador de estado | LED RGB | **Pantalla ST7789 1,3"**: muestra el modo y las confirmaciones (recalibración, etc.). Con dos modos un LED no alcanzaba. |
| Pruebas | MakeCode Arcade | gamepad-tester, SuperTux 0.7.0 y dinosaurio de Chrome. |
| Limitación | — | HID genérico: algunos juegos piden mapear botones la primera vez. XInput queda como mejora futura. |

## Armado

| Tema | En la documentación D4.4 | Cómo quedó realmente |
|---|---|---|
| Módulo RP2350-Plus-M | Enchufado en zócalos hembra 1×20 (J1/J2), con separadores traseros de 18 mm | **Soldado directo** por la cara trasera, con sus propios pines (plástico de 2,5 mm entre placas). Los zócalos J1/J2 ya no se compran. El interior trasero baja a −7,7 mm, así que la carcasa puede ser más delgada. |
| Orientación del módulo | Serigrafía trasera "PIN 1 / PIN 40 / USB-C" | Sin cambios. Primero se soldó por la cara frontal por error y quedó espejado; se corrigió. **Mejora para una futura revisión de PCB:** agregar en la cara frontal el rótulo "MÓDULO POR DETRÁS". |
| Pines del módulo en la cara frontal | — | Cortarlos a ~1,5 mm: el joystick va encima, dentro de la carcasa. |
| C2 | Electrolítico 10 µF ≥16 V | Se usó uno de 10 µF **50 V** (sirve; verificar que mida Ø5 × ≤12 mm). |
| BLK (J4.7) | Sin conectar | Confirmado: no hace falta puente; la luz de fondo enciende sola. |
| Cable del joystick (J3 ↔ KY-023) | Cable XH | Armado a mano (XH ↔ Dupont), con falsos contactos. Pendiente rehacerlo o fijarlo. |
| Fijación de la pantalla | 4 × M2 en H5–H8 | Separadores impresos de 10,5 mm (en el CAD v6). |

## Firmware

- Nuevo firmware del control: `05_Firmware_control\G7_Gamepad` (v1.2), documentado en `05_Firmware_control\README_FIRMWARE.md`.
- Reemplaza al borrador `01_PCB_D4.4_entregada\4_Anexos\firmware\Control_proyecto_2.ino`.
- Pruebas por partes y sus resultados: `04_Firmware_pruebas\README_PRUEBAS.md`.

## Estado al 23/11/2026

| Parte | Estado |
|---|---|
| Módulo + USB | ✅ |
| 7 botones | ✅ |
| Joystick X/Y/SW | ✅ funciona; cable pendiente |
| Pantalla | ✅ |
| Firmware gamepad + teclado | ✅ probado en gamepad-tester, Chrome (dinosaurio) y SuperTux |
| Carcasa (Fusion) | **v6 diseñada, sin imprimir** (ver abajo) |
| Bring-up medido (3V3, 5V, consumo) | Pendiente |
| Prueba con 5 usuarios | Pendiente |

## Carcasa v6 (cambios respecto de la presentación 1)

| Tema | Presentación 1 (sem 8) | Carcasa v6 | Por qué |
|---|---|---|---|
| Pared | 3,2–3,6 mm | 2,4 mm sólida (6 perímetros, sin relleno) | Formas redondeadas sin caras planas grandes; hipótesis contra la deformación del primer control. Pendiente: probeta. |
| Cierre | M3 con tuerca cautiva | PCB a la tapa con 4 × M2×6; base a presión con 6 clips + faldón | Los agujeros de la PCB son M2; sin insertos ni tuercas que no ajusten. |
| Tamaño | 165 × 110 × 43 mm | 184 × 137 × 52 mm | Grips tipo DualSense para la palma; cabe en la Bambu A1. |
| Joystick | Abajo a la izquierda | Al centro, con perilla de cúpula | La PCB D4.4 fijó su posición; la cúpula tapa el mecanismo. |

Otros detalles: capuchones huecos con nervios (MENU macizo), agujeros de aguja para BOOT y RESET, ventana USB-C 13,5 × 7,5. Archivos en `06_Entrega_feedback_profe`.

## Para la próxima entrega

- Actualizar el README y la BOM: módulo soldado directo (quitar J1/J2 de la compra y los separadores de 18 mm), C2 de 50 V, firmware nuevo.
- Agregar la evidencia de las pruebas y el README del firmware.
- Documentar la carcasa (probeta, impresión, muestras CMF) y la prueba con 5 personas.
- Repositorio completo antes del 26/11: README, DECISIONES, /hardware, /firmware, /cad, /experiencia, /docs.
