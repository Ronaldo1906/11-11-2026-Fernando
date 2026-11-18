# Descripción funcional – ALQUILAPC

## Contexto
La empresa **ALQUILAPC** presta el servicio de alquiler de equipos de cómputo portátiles **por días**
(no existe la opción por horas). El valor del alquiler es de **$35.000 por equipo por día**.

## Actores
- **Cliente**: solicita el servicio.
- **Empleado de ALQUILAPC**: registra los datos, liquida y entrega el recibo.

## Datos que se registran
1. Nombre del cliente (obligatorio).
2. Número de equipos solicitados (mínimo 2).
3. Cantidad de días iniciales (mayor a 0).
4. Cantidad de días adicionales (0 o más).
5. Tipo de servicio (solo uno):
   1. Dentro de la ciudad
   2. Fuera de la ciudad
   3. Dentro del establecimiento

## Reglas de negocio
| ID | Regla |
|----|-------|
| RN01 | Valor alquiler: $35.000 por equipo por día. |
| RN02 | Cantidad mínima: 2 equipos. |
| RN03 | Tipos de servicio: dentro de la ciudad, fuera de la ciudad, dentro del establecimiento. |
| RN04 | Fuera de la ciudad: cargo (domicilio) del 5 % sobre el total, aplicado después de los descuentos. |
| RN05 | Dentro del establecimiento: descuento del 5 % sobre el total. |
| RN06 | Si hay días adicionales: descuento del 2 % sobre el total de los días adicionales. |
| RN07 | El recibo contiene: cliente, opción de alquiler, equipos, días iniciales, días adicionales, descuentos, incrementos y total a pagar. |

## Orden de cálculo
1. Valor base = equipos × días iniciales × 35.000
2. Valor adicional = equipos × días adicionales × 35.000
3. Subtotal = base + adicional
4. Descuento días adicionales = 2 % del valor adicional
5. Descuento establecimiento = 5 % del subtotal (solo tipo 3)
6. Valor neto = subtotal − descuentos
7. Incremento domicilio = 5 % del valor neto (solo tipo 2)
8. Total = valor neto + incremento

## Salida: recibo
Debe poder imprimirse y mostrar únicamente: opción de alquiler, equipos alquilados, días iniciales,
días adicionales, descuentos o incrementos según la opción, y el valor total a cancelar.

## Restricciones
- No se usa base de datos (los servicios se guardan en memoria).
- Moneda local (COP) con separador de miles: `$1.662.500`.
