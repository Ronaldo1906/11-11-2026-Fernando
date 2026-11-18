# Diseño y ejecución de casos de prueba – ALQUILAPC

**Aplicación:** AlquilaPC v1.0 (proyecto1.py + app.py) · **Ambiente:** Python 3.10+, Flask, navegador web
**Ejecutor:** Cristian Camilo Rojas Vesga · **Ejecución manual:** formulario en `http://127.0.0.1:5000`

> Fórmulas: base = eq × días × 35.000 · adicional = eq × días adic × 35.000 ·
> dto adic = 2 % adicional · dto est = 5 % subtotal · domicilio = 5 % (subtotal − descuentos)

---

## 1. Pruebas de CAJA NEGRA (manuales, solo entradas y salidas)

Técnicas: partición de equivalencia (PE), valores límite (VL), tabla de decisión (TD), escenarios del plan (S0x).

| ID | Ref. | Técnica | Datos de entrada (nombre, eq, días ini, días adic, tipo) | Pasos | Resultado esperado | Resultado obtenido | Estado |
|----|------|---------|------|------|------|------|------|
| CN-01 | S01 / PBI005 | Escenario | Juan, 2, 1, 0, Dentro ciudad | 1. Abrir `/` 2. Diligenciar 3. Clic *Liquidar* | Total **$70.000**, sin dtos ni incrementos | $70.000 | ✅ Pasa |
| CN-02 | S02 / PBI007 | Escenario | Ana, 2, 3, 0, Fuera ciudad | Igual | Base $210.000, incremento $10.500, total **$220.500** | $220.500 | ✅ Pasa |
| CN-03 | S03 / PBI006 | Escenario | María, 5, 10, 0, Establecimiento | Igual | Base $1.750.000, dto $87.500, total **$1.662.500** | $1.662.500 | ✅ Pasa |
| CN-04 | S04 / PBI009 | Escenario | Pedro, 2, 2, 3, Dentro ciudad | Igual | Adicional $210.000, dto $4.200, total **$345.800** | $345.800 | ✅ Pasa |
| CN-05 | S05 | Escenario | Pedro, 10, 30, 30, Establecimiento | Igual | Dtos $1.260.000, total **$19.740.000** | $19.740.000 | ✅ Pasa |
| CN-06 | RN04 | TD | Luis, 2, 1, 1, Fuera ciudad | Igual | Dto $1.400; incremento 5 % de $138.600 = $6.930; total **$145.530** | $145.530 | ✅ Pasa |
| CN-07 | RN05+RN06 | TD | Carlos, 2, 1, 1, Establecimiento | Igual | Dtos $1.400 + $7.000; total **$131.600** | $131.600 | ✅ Pasa |
| CN-08 | PBI002 | VL | X, **1**, 1, 0, 1 | Igual | Error "cantidad mínima de equipos es 2", no genera recibo | Mensaje mostrado | ✅ Pasa |
| CN-09 | PBI002 | VL | X, **2**, 1, 0, 1 | Igual | Liquida ($70.000) | $70.000 | ✅ Pasa |
| CN-10 | PBI002 | VL | X, **3**, 1, 0, 1 | Igual | Liquida ($105.000) | $105.000 | ✅ Pasa |
| CN-11 | PBI002 | PE | X, **0**, 1, 0, 1 | Igual | Error equipos mínimos | Mensaje mostrado | ✅ Pasa |
| CN-12 | PBI003 | VL | X, 2, **0**, 0, 1 | Igual | Error "días iniciales deben ser mayores a cero" | Mensaje mostrado | ✅ Pasa |
| CN-13 | PBI008 | VL | X, 2, 1, **-1**, 1 | Igual | Error "días adicionales no pueden ser negativos" | Mensaje mostrado | ✅ Pasa |
| CN-14 | PBI008 | VL | X, 2, 1, **0** / **1**, 1 | Igual | Liquida ($70.000 / $138.600) | Correcto | ✅ Pasa |
| CN-15 | PBI001 | PE | **""** (vacío o espacios), 2, 1, 0, 1 | Igual | Error "nombre del cliente es obligatorio" | Mensaje mostrado | ✅ Pasa |
| CN-16 | PBI004 | PE | Juan, 2, 1, 0, **sin seleccionar** | Igual | Error "seleccionar un tipo de servicio válido" | Mensaje mostrado | ✅ Pasa |
| CN-17 | PBI004 | PE | Consola: tipo **4** | `python proyecto1.py` | Error tipo de servicio, no imprime recibo | Mensaje mostrado | ✅ Pasa |
| CN-18 | PBI014 | PE | Juan, **abc**, 1, 0, 1 | Igual | Error "debe ser un número entero" | Mensaje mostrado | ✅ Pasa |
| CN-19 | PBI013 | Funcional | Cualquier servicio válido | Clic *Imprimir recibo* | Abre diálogo de impresión; recibo con los 8 campos de RN07 | Correcto | ✅ Pasa |
| CN-20 | Consulta | Funcional | 2 servicios (Juan, María) | `/servicios?nombre=mar` | Solo aparece María | Correcto | ✅ Pasa |
| CN-21 | Consulta | PE | — | Abrir `/servicios/99` | Error 404 | 404 | ✅ Pasa |

Evidencias: `docs/evidencias/01_inicio.png`, `02_validaciones.png`, `03_recibo.png`, `04_consulta.png`.

---

## 2. Pruebas de CAJA BLANCA (revisión del código, cobertura de ramas)

| ID | Función | Camino / rama | Entrada | Esperado | Obtenido | Estado |
|----|---------|---------------|---------|----------|----------|--------|
| CB-01 | `calculo_alquiler` | única | (2, 1) | 70.000 | 70.000 | ✅ |
| CB-02 | `calculo_alquiler_adicional` | días = 0 | (3, 0) | 0 | 0 | ✅ |
| CB-03 | `calculo_alquiler_adicional` | días > 0 | (3, 2) | 210.000 | 210.000 | ✅ |
| CB-04 | `calculo_alquiler_adicional_dto` | `if valor > 0` verdadero | 210.000 | 4.200 | 4.200 | ✅ |
| CB-05 | `calculo_alquiler_adicional_dto` | `if` falso | 0 | 0 | 0 | ✅ |
| CB-06 | `calculo_dentro_establecimiento` | `tipo == 3` verdadero | (100.000, 3) | 5.000 | 5.000 | ✅ |
| CB-07 | `calculo_dentro_establecimiento` | falso (tipo 1 y 2) | (100.000, 1/2) | 0 | 0 | ✅ |
| CB-08 | `calculo_domicilio` | `tipo == 2` verdadero | (100.000, 2) | 5.000 | 5.000 | ✅ |
| CB-09 | `calculo_domicilio` | falso (tipo 1 y 3) | (100.000, 1/3) | 0 | 0 | ✅ |
| CB-10 | `calculo_descuento` | orden dto → incremento | (70.000, 70.000, 2) | inc 6.930, total 145.530 | Igual | ✅ |
| CB-11 | `porcentaje` | redondeo .5 hacia arriba / abajo | (10,5) (9,5) | 1 / 0 | 1 / 0 | ✅ |
| CB-12 | `validar_datos` | sin errores | ("Ana",2,1,0,1) | [] | [] | ✅ |
| CB-13 | `validar_datos` | ramas "no es entero" | ("Ana","2",1.5,None,"1") | 4 errores | 4 | ✅ |
| CB-14 | `validar_datos` | `bool` no es entero | True/False | 4 errores | 4 | ✅ |
| CB-15 | `calcular_valores` | rama `raise ValidacionError` | ("",1,0,-1,4) | 5 errores | 5 | ✅ |
| CB-16 | `generar_factura` | contiene campos RN07 | servicio CN-06 | 8 campos + $145.530 | Correcto | ✅ |
| CB-17 | `formato_moneda` | miles / cero | 1.662.500 / 0 | "$1.662.500" / "$0" | Igual | ✅ |

**Cobertura** (`coverage`): app.py 98 %, proyecto1.py 76 % (las líneas no cubiertas son solo el menú de consola `main()`, probado manualmente en CN-17). Todas las ramas de cálculo y validación: **100 %**.

---

## 3. Pruebas de REGRESIÓN

Se re-ejecutan después de cada corrección (manual en la web y automática con `python -m unittest -v`).

| ID | Caso dorado | Total aprobado | Ejecución 1 | Ejecución 2 (tras correcciones) | Estado |
|----|-------------|----------------|-------------|------|------|
| RG-01 | Juan, 2, 1, 0, Ciudad | $70.000 | ✅ | ✅ | Sin regresión |
| RG-02 | María, 5, 5, 0, Ciudad | $875.000 | ✅ | ✅ | Sin regresión |
| RG-03 | Pedro, 10, 30, 0, Ciudad | $10.500.000 | ✅ | ✅ | Sin regresión |
| RG-04 | Ana, 2, 3, 0, Fuera | $220.500 | ✅ | ✅ | Sin regresión |
| RG-05 | Luis, 2, 1, 1, Fuera | $145.530 | ✅ | ✅ | Sin regresión |
| RG-06 | Sara, 5, 10, 0, Establecimiento | $1.662.500 | ✅ | ✅ | Sin regresión |
| RG-07 | Carlos, 2, 1, 1, Establecimiento | $131.600 | ✅ | ✅ | Sin regresión |
| RG-08 | Pedro, 2, 2, 3, Ciudad | $345.800 | ✅ | ✅ | Sin regresión |
| RG-09 | Constantes: $35.000, mín. 2 equipos, 3 tipos | — | ✅ | ✅ | Sin regresión |

---

## 4. Pruebas de integración web (automatizadas, `test_app.py`)

| ID | Verificación | Estado |
|----|--------------|--------|
| IT-01 | `GET /` responde 200 | ✅ |
| IT-02 | `POST /liquidar` válido → 302 al recibo con datos y total | ✅ |
| IT-03 | Consultar y filtrar servicios por nombre | ✅ |
| IT-04 | API JSON devuelve el total correcto | ✅ |
| IT-05 | Datos inválidos → 400, no guarda servicio | ✅ |
| IT-06 | Texto no numérico → 400 | ✅ |
| IT-07 | Servicio inexistente → 404 | ✅ |
| IT-08 | Días adicionales vacío se toma como 0 | ✅ |
