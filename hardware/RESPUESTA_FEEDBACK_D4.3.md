# Respuesta a la revisión de PCB — G7 · Control proyecto 2

**Revisión revisada:** D3.1 (20/10/2026) · **Revisión entregada:** D4.3 (26/10/2026)  
**Grupo 7 (G7) · IND474** · V. Kohler, G. Hidalgo, F. Guaita, E. Rojas

Este documento recorre, en el mismo orden, cada punto de *Sugerencias de corrección*, del *Reporte de revisión* y del *Estudio ergonómico* (22/10/2026). Para cada uno indica qué se hizo y dónde verificarlo. Los detalles están en `3_Instrucciones/README.pdf`.

**Verificación de D4.3 (KiCad 9.0.3):**

- ERC: 0 errores y 0 advertencias. Ahora hay símbolos de potencia y PWR_FLAG, así que el ERC sí valida la alimentación.
- DRC con `--schematic-parity --severity-all`: 0 violaciones, 0 pads sin conectar, 0 problemas de paridad y 0 `lib_footprint_mismatch`.
- Gerbers releídos con un lector independiente: contorno de 125,0 × 70,0 mm, 85 PTH y 8 NPTH.
- Pinout de J1–J4 y SW1–SW7 comparado con la tabla GPIO por script: 0 diferencias.

---

## 1. Correcciones bloqueantes (Sugerencias §2)

| # | Pedido | Qué se hizo | Dónde verificar |
|---|---|---|---|
| 2.1 | Confirmar el pinout del RP2350-Plus-M y el espejo; serigrafía PIN 1 / PIN 40 / USB | Pinout comparado con Waveshare: el RP2350-Plus es *pinout compatible* con la Pico 2 y "-M" trae las tiras soldadas. Se crearon símbolos propios con el nombre de cada pin (GPx [pin físico]). En B.Silkscreen van "PIN 1", "PIN 40", "^ USB-C ^" y el nombre del módulo | `1_Diseno_KiCad/Control_proyecto_2.kicad_sym`, `3_Instrucciones/planos/D4.3_render_dorso.png`, `…/D4.3_dorso_1a1_espejo.pdf`, tabla GPIO del README |
| 2.2 | Confirmar el pinout del TFT y del KY-023 contra los módulos comprados; puente BLK | Se fotografió la serigrafía real: TFT = GND VCC SCL SDA RES DC BLK (7 pines, sin CS; plano del vendedor: VCC 3,3 V y BLK encendido por defecto). KY = GND +5V VRx VRy SW. J3 y J4 coinciden. Se agregó **JP1** (BLK→3V3, abierto). El KY se alimenta a 3V3 | `3_Instrucciones/fotos/`, README → "Conectores", esquemático bloque 3 |
| 2.3 | Montar C4/C5 y ubicarlos a ≤10 mm de J4 | Ahora son **C1 = 100 nF** y **C2 = 10 µF**, **montados** (sin DNP), a **4,3 mm** y **7,5 mm** de J4.2. Se renombraron de C4/C5 a C1/C2 | PCB, BOM (Montaje = Sí), README |
| 2.4 | Fijación mecánica del TFT y del KY-023 | **TFT atornillado a la placa** (opción recomendada): 4 × M2 (H5–H8) en el patrón del plano ZJY. Además, el TFT **se enchufa directo** en J4 (zócalo 1×7 bajo sus pines), así que ya no hay cable. **KY-023:** se usa la alternativa que el profesor aceptaba (fijación a la tapa) y **se entrega el plano de la tapa**: KY atornillado desde abajo con 4 × M2,5 a torres de la tapa, patrón 26,5 × 20,5, alturas definidas y cable JST XH a J3. El esfuerzo del stick lo soporta la tapa, no el cable | `3_Instrucciones/planos/D4.3_plano_mecanico_1a1.pdf` (hojas 1 y 2), README → "Mecánica" |
| 2.5 | Mantener 3V3 a 0,6 mm con netclass PWR | Se creó la netclass **PWR (0,6 mm)** asignada a +3V3. Todos los segmentos de 3V3 miden 0,6 mm | `1_Diseno_KiCad/Control proyecto 2.kicad_pro`, inspector de red |

## 2. Correcciones recomendadas (Sugerencias §3)

| # | Pedido | Qué se hizo |
|---|---|---|
| 3.1 | Serigrafía: pinout de J3/J4, funciones de los botones, pin 1, G7/rev | UP / DOWN / LEFT / RIGHT / A / B / MENU. Pines de J3 rotulados uno por uno. Leyenda de J4 junto al zócalo (los pines quedan bajo el TFT) con marca "1". Título "CONTROL PROYECTO 2 – MANDO ARCADE / G7 – IND474 – rev D4.3 – 2026-10". B.Silk según 2.1 |
| 3.2 | Esquemático: símbolos de potencia, PWR_FLAG, nombres de pin, reanotación, texto | Hay `power:+3V3` / `power:GND` y 2 × PWR_FLAG. El módulo usa símbolos con nombres GPx. C4/C5 pasan a C1/C2. Textos de 1,4–3 mm en A3. ERC 0/0 |
| 3.3 | Vías de cosido GND | **18 vías GND** de 0,6/0,3 mm, ubicadas por script con ≥ 0,6 mm de holgura. B.Cu quedó en 3 fragmentos (antes 6). Los dos fragmentos pequeños contienen un pad THT GND del módulo, que los une al plano de la otra cara. DRC sin cobre aislado |
| 3.4 | Cajetín e identidad | Esquemático y PCB dicen "Grupo 7 (G7) – IND474 Desarrollo de Productos Físicos", con autores. El nombre es "Control proyecto 2 – Mando arcade USB" en todos los archivos. Revisión D4.3 |

## 3. Mejoras menores (Sugerencias §4)

| Pedido | Qué se hizo |
|---|---|
| Separadores del módulo trasero y ventana USB | Se calculó el apilado: zócalo 8,5 + plástico 2,5 + PCB 1,0 + USB-C 3,2 = **16,8 mm** detrás. Se especifican separadores M3 de **18 mm** y ventana de 12 × 7 mm (plano, hoja 2) |
| TFT sin CS: SPI modo 3; BLK | Documentado en README y esquemático. JP1 queda disponible |
| 100 nF opcional en cada línea ADC | **No se agregó**, por la indicación anterior del curso de minimizar pasivos externos. Si las lecturas son ruidosas se resuelve por firmware (promedio e histéresis, ya implementados); queda como mejora futura si la prueba lo exige |
| `lib_footprint_mismatch` en J1/J2 | Eliminado: todas las huellas vienen de la biblioteca actual o de la biblioteca propia del proyecto. El DRC no da avisos |
| F.Paste | No se genera (soldadura manual) |

## 4. Entregables (Sugerencias §5)

| # | Pedido | Entregado |
|---|---|---|
| 5.1 | BOM con MPN en las columnas indicadas | `3_Instrucciones/BOM_D4.3.csv` y `.xlsx` con **las mismas columnas** pedidas (Item, Ref, Cant, Descripción, Valor, Huella KiCad, Fabricante, MPN, Proveedor / código, Montaje, Notas). Incluye módulos, cables, tornillería, separadores y PCB |
| 5.2 | README | `3_Instrucciones/README.pdf`: descripción, estado, historial, diagrama de bloques, tabla GPIO, conectores con fotos, mecánica y alturas, orden de montaje, verificación 1:1, prueba eléctrica, notas de firmware y pendientes. PDF del esquemático y renders frontal/posterior en `3_Instrucciones/planos/` |
| 5.3 | Gerbers regenerados y comprimidos | `2_Gerber_Produccion/` con `G7_Gerber_D4.3_para_fabricante.zip`: 7 capas, PTH.drl, NPTH.drl, mapas y job. **NPTH = 8** (4 × M3 de la portadora y 4 × M2 del TFT). Los 4 M3 del KY de la propuesta no van, porque el KY se fija a la tapa |
| 5.4 | Impresión 1:1 | `3_Instrucciones/planos/D4.3_frente_1a1.pdf` y `D4.3_dorso_1a1_espejo.pdf`, con barra de control de 50 mm verificada en el PDF (125,0 y 50,0 mm medidos) |

## 5. Hallazgos del Reporte de revisión

| Hallazgo | Estado |
|---|---|
| 6.1 Crítico: pinout de módulos y arneses sin validar; fijaciones; cierre; C4/C5 | Pinouts confirmados con fotos y con la documentación del fabricante (2.1, 2.2). Fijaciones resueltas (2.4). Decisión de C1/C2 tomada (2.3). Cierre y carcasa con alturas en el plano mecánico |
| 6.2.1 C4/C5 lejos y DNP | Resuelto (2.3) |
| 6.2.2 Arneses sin rotular | Resuelto (3.1). El TFT ya no usa cable |
| 6.2.3 KY sin fijación | Resuelto (2.4) |
| 6.2.4 Sin README/BOM/PDF | Resuelto (§4) |
| 6.2.5 ERC sin validar alimentación | Resuelto (3.2) |
| 6.3.1 Sin vías de cosido | Resuelto (3.3) |
| 6.3.2 / 6.3.3 Identidad y serigrafía | Resuelto (3.4, 3.1) |
| 6.3.4 Salto de anotación / texto pequeño | Resuelto (3.2) |
| 6.3.5 Separadores y USB | Resuelto (§3) |
| 6.3.6 TFT sin CS / BLK | Documentado; JP1 disponible |

## 6. Estudio ergonómico — se aplicó la propuesta 5.1 y se mejoró

Medido con el mismo modelo del estudio (bases del pulgar en (70,120) y (155,120); radio cómodo de 44,5 mm):

| Problema del estudio | D3.1 | D4.3 |
|---|---|---|
| 1. TFT/KY sin posición ni fijación; stick a ~44 mm | Sin definir | TFT atornillado y enchufado. KY en la tapa con alturas definidas: pomo de 20,2 a 38,2 mm, tapa a 19 mm |
| 2. UP fuera del alcance cómodo | 54,8 mm | **45,8 mm** (la propuesta 5.1 daba 47,8). Se compactó el D-pad a un paso de 12,75 mm, el mínimo sin solapar courtyards |
| 3. A/B demasiado separados; A arrinconado | A–B 25,5 · A 42,0 | **A–B 17,9 · A 35,2** |
| 4. LEFT pegado al canto | cuerpo a 2,5 mm del borde | **3,75 mm** |
| 5. Stick cerca del D-pad | 7,5 mm de aire | Stick en (110,5; 105) global = propuesta 5.1, a **43,2 mm** del pulgar izquierdo |
| 6. J4 y su Dupont entre TFT, MENU y A | Conector vertical expuesto | **Sin cable**: el TFT se enchufa en J4, bajo la pantalla |
| 7. Pantalla descentrada | — | Se mantiene, como sugería el estudio (sin pantalla tapada; MENU lejos a propósito) |

## 7. Problemas adicionales encontrados y corregidos al aplicar el feedback

1. **Los pulsadores de 12 mm del kit son SMD** (patas dobladas, patrón 14 × 5 según el plano del vendedor). La huella THT de 12,5 × 5 no habría servido. Se cambió a `SW_Push_1P1T_NO_CK_PTS125Sx73SMTR`.
2. **El TFT por cable no cabía en altura**: un Dupont recto bajo sus pines traseros exigía unos 16 mm libres. Se resolvió con el zócalo J4 directo bajo los pines.
3. **La cabeza del tornillo M2 de H5/H7 (cara trasera) pisaba 0,3 mm el zócalo J1 del módulo.** El TFT se corrió 1 mm y ahora quedan 0,66 mm libres. Los courtyards de H5–H8 representan el separador real de Ø3,5 + tornillo (huella propia).
4. **Los pines acodados del KY y su conector chocaban con J3.** J3 se reubicó abajo a la derecha (D4.3).

## 8. Pendientes que requieren las piezas físicas (antes de pedir la PCB)

Ninguno cambia el esquema eléctrico. Son verificaciones con las piezas reales, con el procedimiento descrito en el README. El patrón de agujeros del KY y el conector JST XH ya se confirmaron con las piezas (26/10):

- Impresión 1:1 con pulsadores, módulo y TFT reales sobre el papel.
- Maqueta ergonómica con 3 personas.
- Prueba eléctrica escalonada sobre la placa armada.
- Compilar el firmware e integrar la ST7789.
