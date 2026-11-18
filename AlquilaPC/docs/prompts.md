# Prompts usados con IA – Taller AlquilaPC

## 1. Prompt para crear el Product Backlog
> Adjuntar: `Descripcion_funcional.md`

```
Actúa como Product Owner experto en Scrum. Lee el archivo adjunto 'Descripcion_funcional.md'
del sistema ALQUILAPC (alquiler de portátiles por días a $35.000 por equipo/día).

Genera el Product Backlog en una tabla con las columnas:
PBI | Historia de Usuario | Criterios de Aceptación | Prioridad (Alta/Media/Baja) | Estimación (puntos)

Reglas:
- Numera los ítems PBI001, PBI002, ...
- Redacta cada historia con el formato: "Como <rol>, quiero <acción> para <beneficio>".
- Escribe entre 4 y 6 criterios de aceptación numerados, verificables y medibles.
- Cubre TODAS las reglas de negocio RN01-RN07, las validaciones de entrada y la
  generación/impresión del recibo.
- No inventes reglas que no estén en el documento; si encuentras ambigüedades,
  lístalas al final en una sección "Supuestos y preguntas para el cliente".
```

## 2. prompt_generaruml_testing (diagramas UML + archivo de prueba + informe)
> Adjuntar: `proyecto1.py` y `Descripcion_funcional.md`

```
Actúa como analista QA y arquitecto de software. Con base en 'proyecto1.py' y
'Descripcion_funcional.md' del sistema ALQUILAPC:

1. Genera en PlantUML los diagramas UML básicos:
   a) Casos de uso (actor Cliente; Registrar datos, Calcular alquiler base, Calcular días
      adicionales, Seleccionar tipo de servicio, Aplicar descuento días adicionales,
      Aplicar descuento establecimiento, Calcular cargo fuera de la ciudad, Generar factura;
      usa <<include>> y <<extend>>).
   b) Diagrama de clases/módulos con las funciones de proyecto1.py.
   c) Diagrama de secuencia del flujo "liquidar servicio".
   d) Diagrama de actividades del cálculo (orden: descuentos -> incremento -> total).

2. Genera el archivo 'test_proyecto1.py' con unittest (equivalente a JUnit) organizado en:
   - TestCajaBlanca: una prueba por cada rama if/else de cada función.
   - TestCajaNegra: partición de equivalencia, valores límite (equipos 1/2/3,
     días adicionales -1/0/1, días iniciales 0/1) y tabla de decisión del tipo de servicio.
   - TestRegresion: casos "dorados" con totales esperados.
   Nombra los métodos test_cbXX_, test_cnXX_, test_rgXX_.

3. Genera el 'Informe de hallazgos' con: resumen de ejecución (total, OK, fallidas),
   cobertura, tabla de hallazgos (ID, descripción, severidad, evidencia, estado) y
   recomendaciones.
```

## 3. Prompt para el Plan de Pruebas
> Adjuntar: `proyecto1.py` y `ISO-IEC-IEEE-29119-3.pdf`

```
Actúa como Líder QA. Elabora el Plan de Pruebas del sistema ALQUILAPC (versión 1.0)
siguiendo la estructura de la norma ISO/IEC/IEEE 29119-3 (Test Plan).
Aplicación bajo prueba: proyecto1.py.

Incluye: 1. Introducción (propósito, alcance: incluido/excluido), 2. Objetivos,
3. Criterios de éxito (tabla de métricas), 4. Elementos bajo prueba (CP-01..CP-11),
5. Reglas de negocio RN01-RN07, 6. Estrategia por fases (unitarias, integración,
sistema con escenarios S01-S05, UAT, regresión), 7. Técnicas de diseño (partición de
equivalencia, valores límite, tabla de decisión, basadas en reglas de negocio),
8. Datos de prueba válidos e inválidos, 9. Ambiente, 10. Riesgos y mitigación,
11. Criterios de entrada, 12. Criterios de salida, 13. Roles, 14. Cronograma,
15. Entregables, 16. Aprobación. Usa tablas donde aplique.
```

## 4. Prompt para el Diseño de Casos de Prueba
```
Con base en el Plan de Pruebas y el Product Backlog de ALQUILAPC, diseña los casos de
prueba en una tabla con: ID | PBI/RN relacionado | Técnica (caja negra/blanca/regresión)
| Precondición | Datos de entrada | Pasos | Resultado esperado | Resultado obtenido | Estado.
Incluye casos positivos, negativos y de valores límite, y los escenarios S01-S05.
Calcula los resultados esperados en pesos con separador de miles.
```

## 5. Prompt agéntico para desarrollar la aplicación (el del taller)
```
Desarrolla la aplicación ALQUILAPC y déjala ejecutable desde cero. Crea las migraciones
necesarias. Luego inicia el servidor y comprueba que la página principal responda
correctamente y que se pueda liquidar y consultar un servicio sin utilizar base de datos.
Si encuentras errores, corrígelos y vuelve a ejecutar las pruebas. Incluye en el README los
comandos exactos para instalar dependencias, aplicar migraciones y arrancar el proyecto.
No des por terminado el trabajo solo porque el código compile o las pruebas pasen.
```
