# Informe de hallazgos – Pruebas ALQUILAPC

**Proyecto:** ALQUILAPC v1.0 · **Norma de referencia:** ISO/IEC/IEEE 29119-3
**Responsable:** Cristian Camilo Rojas Vesga – ADSO, Ficha 3407184
**Herramientas:** Python 3, unittest, coverage, Flask test client, navegador

## 1. Resumen de ejecución

| Métrica | Criterio del plan | Resultado |
|---------|-------------------|-----------|
| Casos ejecutados | 100 % | 100 % (40 automatizados + 21 manuales caja negra) |
| Casos aprobados | ≥ 95 % | 100 % |
| Casos fallidos críticos | 0 | 0 |
| Cobertura reglas de negocio (RN01–RN07) | 100 % | 100 % |
| Cobertura de validaciones | 100 % | 100 % |
| Cobertura de código (ramas de cálculo) | — | 100 % (app.py 98 %, proyecto1.py 76 % por el menú de consola) |
| Defectos críticos abiertos | 0 | 0 |

Comando: `python -m unittest -v` → `Ran 40 tests ... OK`

## 2. Hallazgos

| ID | Tipo | Descripción | Severidad | Decisión / Estado |
|----|------|-------------|-----------|-------------------|
| H-01 | Requisito ambiguo | La descripción funcional dice "2 % sobre el total de los días adicionales", pero el backlog (PBI009) dice "2 % **por cada** día adicional". Dan resultados distintos (con 3 días: 2 % vs 6 %). | Alta | Se implementó la descripción funcional (2 % sobre el valor de los días adicionales). **Pendiente confirmar con el cliente.** |
| H-02 | Requisito ambiguo | El 5 % de establecimiento: la descripción dice "sobre el total" y PBI006 dice "sobre el valor base". | Media | Se aplica sobre el subtotal (base + adicionales). Pendiente confirmar. |
| H-03 | Requisito incompleto | El escenario S05 "máximo descuento por días adicionales" no define un tope. | Baja | Sin tope; S05 probado con 30 días adicionales. |
| H-04 | Requisito | El mínimo de 2 equipos solo aparece en el backlog/plan, no en la descripción funcional. | Baja | Implementado (RN02). |
| H-05 | Validación | Python considera `True` como entero (`True == 1`), lo que permitiría "1 equipo" o "tipo 1" con valores booleanos. | Media | **Controlado**: `validar_datos` rechaza `bool`. Prueba CB-14. |
| H-06 | Cálculo | Riesgo de errores de redondeo con `float` en porcentajes. | Media | **Controlado**: aritmética entera en pesos. Prueba CB-11. |
| H-07 | Usabilidad | Riesgo: si el campo de días adicionales se deja vacío, la conversión a número fallaría. | Baja | **Controlado**: vacío = 0. Prueba IT-08. |
| H-08 | Enunciado | El taller pide "crear migraciones" pero también "sin utilizar base de datos". | Baja | No aplica migración; documentado en README. |

## 3. Conclusiones

- Todas las reglas de negocio implementadas cumplen los resultados esperados en caja negra, caja blanca y regresión.
- El orden de cálculo exigido por RN04 (domicilio después de descuentos) se verificó (CB-10, CN-06).
- Las entradas inválidas nunca generan recibo (CN-08 a CN-18, IT-05).
- Los riesgos principales son de **requisitos** (H-01, H-02), no de código.

## 4. Recomendaciones

1. Validar H-01 y H-02 con el Product Owner y actualizar el backlog o el código según la decisión; luego re-ejecutar la suite de regresión.
2. Mantener `test_proyecto1.py` como suite de regresión obligatoria antes de cada entrega.
3. Si en el futuro se agrega persistencia, crear las migraciones y pruebas de integración con la base de datos.
