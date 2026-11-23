# Experiencia de uso

## Perfil de usuario

Estudiante universitario de 20 a 25 años que juega juegos 2D y retro en su PC, con ambas manos.

| Necesidad | Requisito | Valor | Estado |
|---|---|---|---|
| Agarre cómodo | Sección del grip en la raíz | 41 × 31 mm | Diseñado en CAD; ⏳ validar |
| Saber si funciona | Reconocido por el PC sin drivers; modo visible en pantalla | Gamepad HID + modo teclado | ✅ probado |
| Alcance de botones | Distancia del pulgar a cruceta y A/B | ≤ 44,5 mm (radio cómodo del pulgar) | ⏳ medir con usuarios |

**Evidencia hasta hoy:** pruebas informales con los integrantes del grupo y familiares, sin registro (sin video, tiempos ni fotos). No cuentan como evidencia del perfil.

## Protocolo de la prueba con 5 personas

- **Participantes:** 5 personas del perfil, **fuera del grupo**.
- **Antes:** pedir permiso para grabar las manos (no la cara) y medir el largo de la mano (muñeca a punta del dedo medio).
- **Sin explicar los atajos**, salvo que la persona se quede trabada más de 60 s.

| Tarea | Qué se le pide | Qué se registra |
|---|---|---|
| T1 | Jugar SuperTux 1 minuto con el control en modo gamepad | Errores de botón, si suelta los grips, comentarios |
| T2 | Cambiar a modo teclado (MENU + B) | Tiempo hasta lograrlo, si mira la pantalla |
| T3 | Recalibrar el stick (MENU + A) | Tiempo, si entiende "CENTRO OK" |

Al final, 3 preguntas: ¿qué fue lo más incómodo?, ¿llegabas a todos los botones sin soltar el control?, ¿cambiarías algo de la forma?

La planilla está en [`planilla_prueba_usuarios.csv`](planilla_prueba_usuarios.csv).

## Resultados

⏳ **Pendiente** (prueba planificada para el 25/11/2026).

Cuando se haga, completar:

1. Los 3 hallazgos principales, con cuántas de las 5 personas los mostraron.
2. Al menos 3 cambios aplicados, cada uno con foto o render de **antes** y **después**.

## Cambios ya aplicados en el CAD (revisiones internas, no de usuarios)

| Cambio | Antes | Después |
|---|---|---|
| Grips unificados | Patas a otra altura que la cara de botones | Un solo movimiento desde la cara superior |
| Joystick con cúpula | Perilla 22 mm sobre la cara, mecanismo visible | Cúpula que tapa el mecanismo |
| Cierre a presión | M3 con tuerca cautiva | 6 clips + faldón |
| BOOT y RESET | Había que abrir la carcasa | Agujero de aguja |
