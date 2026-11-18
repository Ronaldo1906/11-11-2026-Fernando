"""
ALQUILAPC - Lógica de negocio para la liquidación del alquiler de equipos portátiles.

Estructura de funciones (según el diagrama del taller):

    calcular_valores()
     ├── calculo_alquiler()
     ├── calculo_alquiler_adicional()
     └── calculo_descuento()
          ├── calculo_alquiler_adicional_dto()
          ├── calculo_dentro_establecimiento()
          └── calculo_domicilio()

Reglas de negocio:
    RN01  Valor alquiler: $35.000 por equipo por día.
    RN02  Cantidad mínima: 2 equipos.
    RN03  Tipos de servicio: 1 Dentro de la ciudad, 2 Fuera de la ciudad, 3 Dentro del establecimiento.
    RN04  Fuera de la ciudad: incremento (domicilio) del 5%, aplicado DESPUÉS de los descuentos.
    RN05  Dentro del establecimiento: descuento del 5% sobre el total (subtotal bruto).
    RN06  Días adicionales: descuento del 2% sobre el total de los días adicionales.
    RN07  El recibo contiene: cliente, tipo de servicio, equipos, días iniciales,
          días adicionales, descuentos, incrementos y total a pagar.

Se usa aritmética entera (pesos colombianos) para evitar errores de redondeo con float.
"""

VALOR_DIA = 35000
EQUIPOS_MINIMOS = 2
PORC_DTO_ADICIONAL = 2       # %
PORC_DTO_ESTABLECIMIENTO = 5  # %
PORC_DOMICILIO = 5            # %

DENTRO_CIUDAD = 1
FUERA_CIUDAD = 2
ESTABLECIMIENTO = 3

TIPOS_SERVICIO = {
    DENTRO_CIUDAD: "Dentro de la ciudad",
    FUERA_CIUDAD: "Fuera de la ciudad",
    ESTABLECIMIENTO: "Dentro del establecimiento",
}


class ValidacionError(ValueError):
    """Se lanza cuando los datos de entrada no cumplen las reglas de validación."""

    def __init__(self, errores):
        self.errores = list(errores)
        super().__init__("; ".join(self.errores))


def _es_entero(valor):
    return isinstance(valor, int) and not isinstance(valor, bool)


def porcentaje(valor, porc):
    """Calcula porc% de valor con redondeo al peso más cercano (aritmética entera)."""
    return (valor * porc + 50) // 100


# --------------------------------------------------------------------------- #
# Validaciones (PBI001, PBI002, PBI003, PBI004, PBI008, PBI014)
# --------------------------------------------------------------------------- #
def validar_datos(nombre, equipos, dias_iniciales, dias_adicionales, tipo_servicio):
    """Devuelve una lista de mensajes de error. Lista vacía = datos válidos."""
    errores = []

    if not isinstance(nombre, str) or not nombre.strip():
        errores.append("El nombre del cliente es obligatorio.")

    if not _es_entero(equipos):
        errores.append("La cantidad de equipos debe ser un número entero.")
    elif equipos < EQUIPOS_MINIMOS:
        errores.append(f"La cantidad mínima de equipos es {EQUIPOS_MINIMOS}.")

    if not _es_entero(dias_iniciales):
        errores.append("Los días iniciales deben ser un número entero.")
    elif dias_iniciales <= 0:
        errores.append("Los días iniciales deben ser mayores a cero.")

    if not _es_entero(dias_adicionales):
        errores.append("Los días adicionales deben ser un número entero.")
    elif dias_adicionales < 0:
        errores.append("Los días adicionales no pueden ser negativos.")

    if tipo_servicio not in TIPOS_SERVICIO or not _es_entero(tipo_servicio):
        errores.append("Debe seleccionar un tipo de servicio válido (1, 2 o 3).")

    return errores


# --------------------------------------------------------------------------- #
# Cálculos (PBI003, PBI005 - PBI012)
# --------------------------------------------------------------------------- #
def calculo_alquiler(equipos, dias_iniciales):
    """Valor base: equipos x días iniciales x $35.000."""
    return equipos * dias_iniciales * VALOR_DIA


def calculo_alquiler_adicional(equipos, dias_adicionales):
    """Valor de los días adicionales: equipos x días adicionales x $35.000."""
    return equipos * dias_adicionales * VALOR_DIA


def calculo_alquiler_adicional_dto(valor_adicional):
    """Descuento del 2% sobre el total de los días adicionales (0 si no hay)."""
    if valor_adicional > 0:
        return porcentaje(valor_adicional, PORC_DTO_ADICIONAL)
    return 0


def calculo_dentro_establecimiento(subtotal, tipo_servicio):
    """Descuento del 5% sobre el total cuando el servicio es en el establecimiento."""
    if tipo_servicio == ESTABLECIMIENTO:
        return porcentaje(subtotal, PORC_DTO_ESTABLECIMIENTO)
    return 0


def calculo_domicilio(valor_neto, tipo_servicio):
    """Incremento del 5% (sobre el valor ya descontado) cuando es fuera de la ciudad."""
    if tipo_servicio == FUERA_CIUDAD:
        return porcentaje(valor_neto, PORC_DOMICILIO)
    return 0


def calculo_descuento(valor_alquiler, valor_adicional, tipo_servicio):
    """Calcula descuentos e incrementos respetando el orden: descuentos -> incrementos."""
    subtotal = valor_alquiler + valor_adicional
    dto_adicional = calculo_alquiler_adicional_dto(valor_adicional)
    dto_establecimiento = calculo_dentro_establecimiento(subtotal, tipo_servicio)
    total_descuentos = dto_adicional + dto_establecimiento
    valor_neto = subtotal - total_descuentos
    incremento = calculo_domicilio(valor_neto, tipo_servicio)
    return {
        "subtotal": subtotal,
        "dto_adicional": dto_adicional,
        "dto_establecimiento": dto_establecimiento,
        "total_descuentos": total_descuentos,
        "incremento_domicilio": incremento,
        "total": valor_neto + incremento,
    }


def calcular_valores(nombre, equipos, dias_iniciales, dias_adicionales, tipo_servicio):
    """Valida y liquida un servicio completo. Lanza ValidacionError si hay errores."""
    errores = validar_datos(nombre, equipos, dias_iniciales, dias_adicionales, tipo_servicio)
    if errores:
        raise ValidacionError(errores)

    valor_alquiler = calculo_alquiler(equipos, dias_iniciales)
    valor_adicional = calculo_alquiler_adicional(equipos, dias_adicionales)
    resultado = calculo_descuento(valor_alquiler, valor_adicional, tipo_servicio)

    return {
        "nombre": nombre.strip(),
        "tipo_servicio": tipo_servicio,
        "tipo_servicio_nombre": TIPOS_SERVICIO[tipo_servicio],
        "equipos": equipos,
        "dias_iniciales": dias_iniciales,
        "dias_adicionales": dias_adicionales,
        "valor_alquiler": valor_alquiler,
        "valor_adicional": valor_adicional,
        **resultado,
    }


# --------------------------------------------------------------------------- #
# Factura / recibo (PBI013, RN07)
# --------------------------------------------------------------------------- #
def formato_moneda(valor):
    """Formato moneda local: $1.234.567"""
    return "$" + f"{valor:,}".replace(",", ".")


def generar_factura(liq):
    """Devuelve el recibo en texto plano con los datos exigidos por ALQUILAPC."""
    m = formato_moneda
    lineas = [
        "=" * 44,
        "            ALQUILAPC - RECIBO",
        "=" * 44,
        f"Cliente:               {liq['nombre']}",
        f"Opción de alquiler:    {liq['tipo_servicio_nombre']}",
        f"Equipos alquilados:    {liq['equipos']}",
        f"Días iniciales:        {liq['dias_iniciales']}",
        f"Días adicionales:      {liq['dias_adicionales']}",
        "-" * 44,
        f"Valor días iniciales:  {m(liq['valor_alquiler'])}",
        f"Valor días adicional.: {m(liq['valor_adicional'])}",
        f"Dto. días adicionales: -{m(liq['dto_adicional'])}",
        f"Dto. establecimiento:  -{m(liq['dto_establecimiento'])}",
        f"Total descuentos:      -{m(liq['total_descuentos'])}",
        f"Incremento domicilio:  +{m(liq['incremento_domicilio'])}",
        "-" * 44,
        f"TOTAL A PAGAR:         {m(liq['total'])}",
        "=" * 44,
    ]
    return "\n".join(lineas)


# --------------------------------------------------------------------------- #
# Modo consola
# --------------------------------------------------------------------------- #
def _leer_entero(mensaje):
    while True:
        texto = input(mensaje).strip()
        try:
            return int(texto)
        except ValueError:
            print("  -> Ingrese un número entero.")


def main():
    print("ALQUILAPC - Liquidación de alquiler de equipos")
    nombre = input("Nombre del cliente: ")
    equipos = _leer_entero(f"Número de equipos (mínimo {EQUIPOS_MINIMOS}): ")
    dias_iniciales = _leer_entero("Días iniciales: ")
    dias_adicionales = _leer_entero("Días adicionales (0 si no hay): ")
    for k, v in TIPOS_SERVICIO.items():
        print(f"  {k}. {v}")
    tipo = _leer_entero("Tipo de servicio: ")
    try:
        liq = calcular_valores(nombre, equipos, dias_iniciales, dias_adicionales, tipo)
    except ValidacionError as e:
        print("\nNo se puede generar el recibo:")
        for err in e.errores:
            print(" -", err)
        return
    print()
    print(generar_factura(liq))


if __name__ == "__main__":
    main()
