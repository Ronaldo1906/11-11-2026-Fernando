# ALQUILAPC – Alquiler de equipos portátiles

Aplicación en Python (Flask) que liquida el alquiler de portátiles por días ($35.000 por equipo/día),
aplica descuentos e incrementos y genera el recibo. **No usa base de datos**: los servicios
liquidados se guardan en memoria mientras el servidor está encendido.

## Estructura

```
AlquilaPC/
├── proyecto1.py          # Lógica de negocio + modo consola
├── app.py                # Servidor web Flask (liquidar / consultar / recibo)
├── templates/            # Vistas HTML
├── test_proyecto1.py     # Pruebas unitarias: caja blanca, caja negra, regresión
├── test_app.py           # Pruebas de integración/sistema de la web
├── requirements.txt
└── docs/
    ├── Descripcion_funcional.md
    ├── prompts.md                 # Prompts para IA (backlog, UML/testing, plan, casos)
    ├── uml/                       # Diagramas UML (PlantUML + Mermaid)
    ├── casos_de_prueba.md         # Casos manuales caja negra / caja blanca / regresión
    ├── informe_hallazgos.md       # Resultado de la ejecución y hallazgos
    └── evidencias/                # Capturas de pantalla
```

## Instalación desde cero

### Windows (PowerShell / CMD)
```bat
cd AlquilaPC
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Linux / macOS
```bash
cd AlquilaPC
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Migraciones

No aplica: el enunciado exige liquidar y consultar **sin base de datos**, por lo que no hay modelos
ni tablas que migrar. Los datos viven en el diccionario `SERVICIOS` de `app.py`.

## Arrancar el proyecto

```bash
python app.py
```
Abrir <http://127.0.0.1:5000>

| Ruta | Función |
|------|---------|
| `/` | Formulario para liquidar |
| `/servicios` | Consultar servicios (filtro `?nombre=`) |
| `/servicios/<id>` | Recibo imprimible |
| `/api/servicios/<id>` | Servicio en JSON |

Modo consola (sin servidor):
```bash
python proyecto1.py
```

## Ejecutar las pruebas

```bash
python -m unittest -v
```
Con cobertura:
```bash
python -m coverage run -m unittest
python -m coverage report -m --include=proyecto1.py,app.py
```

Resultado actual: **40 pruebas, 40 OK**.

## Reglas de negocio implementadas

| Regla | Cálculo |
|-------|---------|
| Valor base | equipos × días iniciales × $35.000 |
| Días adicionales | equipos × días adicionales × $35.000 |
| Dto. días adicionales | 2 % sobre el valor de los días adicionales |
| Dto. establecimiento | 5 % sobre el subtotal (base + adicionales) |
| Domicilio fuera de ciudad | +5 % sobre el valor ya descontado |
| Total | subtotal − descuentos + incremento |
| Validaciones | nombre obligatorio, equipos ≥ 2, días iniciales > 0, adicionales ≥ 0, tipo 1-3 |
