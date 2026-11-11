# -*- coding: utf-8 -*-
"""
Programa: ALQUILAPC - Pruebas de software SENA.
Sistema de facturación de alquiler de equipos de cómputo portátiles.
Valor base: $35.000 por equipo por día.
"""

# Variables globales
nom = ""
opcion = 0
equipos = 0
diasal = 0
diasad = 0
alqui = 35000.0
tipo = ""
descuentos = 0.0
domi = 0.0
total = 0.0


def calculo_alquiler():
    """Valor del alquiler de los días iniciales (sin descuentos)."""
    return equipos * diasal * alqui


def calculo_alquiler_adicional():
    """
    Valor de los días adicionales.
    Se aplica un descuento único del 2% sobre el valor total
    de los días adicionales.
    """
    if diasad <= 0:
        return 0.0

    valor_base_adicional = equipos * diasad * alqui
    descuento_adicional = valor_base_adicional * 0.02

    descuento_adicional = min(
        descuento_adicional,
        valor_base_adicional
    )

    return valor_base_adicional - descuento_adicional


def calculo_alquiler_adicional_dto():
    """Retorna solo el monto del descuento aplicado a los días adicionales."""
    if diasad <= 0:
        return 0.0

    valor_base_adicional = equipos * diasad * alqui
    descuento_adicional = valor_base_adicional * 0.02

    return min(descuento_adicional, valor_base_adicional)


def calculo_descuento():
    """
    Descuentos totales:
    - Descuento del 2% sobre los días adicionales.
    - Si es Dentro del Establecimiento: descuento adicional del 5%.
    """
    global descuentos

    dto_adicional = calculo_alquiler_adicional_dto()
    dto_establecimiento = 0.0

    if opcion == 3:  # Dentro del Establecimiento
        valor_despues_dto_adicional = (
            calculo_alquiler() + calculo_alquiler_adicional()
        )

        dto_establecimiento = valor_despues_dto_adicional * 0.05

    descuentos = dto_adicional + dto_establecimiento

    return descuentos


def calculo_domicilio():
    """
    Incremento por domicilio del 5% solo si el servicio es Fuera de la ciudad.
    Se aplica después de los descuentos.
    """
    global domi

    if opcion == 2:  # Fuera de la ciudad
        valor_base_para_domi = (
            calculo_alquiler() + calculo_alquiler_adicional()
        )

        domi = valor_base_para_domi * 0.05

    else:
        domi = 0.0

    return domi


def calculo_dentro_establecimiento():
    """Descuento del 5% exclusivo para Dentro del Establecimiento."""
    if opcion == 3:
        valor_despues_dto_adicional = (
            calculo_alquiler() + calculo_alquiler_adicional()
        )

        return valor_despues_dto_adicional * 0.05

    return 0.0


def calcular_valores():
    """
    Calcula el total a pagar aplicando todas las reglas de negocio:
    1. Valor días iniciales.
    2. Valor días adicionales con descuento del 2%.
    3. Descuento adicional del 5% si es Dentro del Establecimiento.
    4. Incremento del 5% por domicilio si es Fuera de la ciudad.
    """
    global total, descuentos, domi

    valor_inicial = calculo_alquiler()
    valor_adicional_neto = calculo_alquiler_adicional()

    subtotal = valor_inicial + valor_adicional_neto

    # Descuento del establecimiento (5%)
    dto_estab = 0.0

    if opcion == 3:
        dto_estab = subtotal * 0.05
        subtotal -= dto_estab

    # Domicilio (5%) solo para Fuera de la ciudad
    domi = 0.0

    if opcion == 2:
        domi = subtotal * 0.05
        subtotal += domi

    # Suma de todos los descuentos aplicados
    descuentos = calculo_alquiler_adicional_dto() + dto_estab

    total = subtotal

    return total


def encabezado():
    print("\t\t\t************** SENA PRUEBAS DE SOFTWARE 2020 ************")
    print("\t\t\tANÁLISIS Y DESARROLLO DE SISTEMAS DE INFORMACIÓN CGMLTI\n")


def tipo_servicio():
    global opcion, tipo

    print("\nTipos de servicios ofrecidos")
    print("[1] Dentro de la Ciudad")
    print("[2] Fuera de la ciudad")
    print("[3] Dentro del Establecimiento")

    while True:
        try:
            opcion = int(input("Tipo de servicio tomado por el cliente: "))

            if opcion == 1:
                tipo = "Dentro de la Ciudad"
                break

            elif opcion == 2:
                tipo = "Fuera de la ciudad"
                break

            elif opcion == 3:
                tipo = "Dentro del Establecimiento"
                break

            else:
                print("Opción no válida. Seleccione 1, 2 o 3.")

        except ValueError:
            print("Ingrese un número válido.")


def leer_entero_positivo(mensaje):
    while True:
        try:
            valor = int(input(mensaje))

            if valor > 0:
                return valor

            print("Ingrese un número mayor que cero.")

        except ValueError:
            print("Ingrese un número entero válido.")


def equipos_alquiler():
    """Solicita número de equipos. Mínimo 2 según regla de negocio."""
    global equipos

    while True:
        equipos = leer_entero_positivo(
            "Número de equipos que desea alquilar (mínimo 2): "
        )

        if equipos >= 2:
            break

        print("Debe alquilar mínimo 2 equipos.")


def dias_alquiler():
    global diasal

    diasal = leer_entero_positivo(
        "Número de días que desea tomar el alquiler: "
    )


def dias_adicionales():
    global diasad

    while True:
        try:
            valor = int(
                input("Número de días adicionales que toma el alquiler: ")
            )

            if valor >= 0:
                diasad = valor
                return

            print("Los días adicionales no pueden ser negativos.")

        except ValueError:
            print("Ingrese un número entero válido.")


def datos_basicos():
    global nom

    nom = input("Nombre Cliente: ").strip()

    while not nom:
        print("El nombre no puede estar vacío.")
        nom = input("Nombre Cliente: ").strip()

    equipos_alquiler()
    dias_alquiler()
    dias_adicionales()


def mostrar_datos():
    # Asegura que los valores estén calculados
    calcular_valores()

    print("\n\t\t\tA L Q U I L A P C")
    print(f"Nombre: {nom}")
    print(f"Tipo de servicio: {tipo}")
    print(f"Número de Equipos: {equipos}")
    print(f"No. Días Iniciales: {diasal}")
    print(f"Valor Alquiler: ${calculo_alquiler():,.2f}")
    print(f"No. Días adicionales: {diasad}")
    print(f"Valor días adicionales: ${calculo_alquiler_adicional():,.2f}")
    print(f"Descuentos: ${calculo_descuento():,.2f}")
    print(f"Domicilio: ${calculo_domicilio():,.2f}")
    print(f"Total a pagar: ${calcular_valores():,.2f}")

    print("Factura generada por el S E N A")
    print("Gracias por utilizar nuestros servicios...!!!")


def main():
    encabezado()
    datos_basicos()
    tipo_servicio()
    calcular_valores()
    mostrar_datos()


if __name__ == "__main__":
    main()
    