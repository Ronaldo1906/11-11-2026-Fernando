"""
ALQUILAPC - Aplicación web (Flask).
Los servicios liquidados se guardan EN MEMORIA (no se usa base de datos).

Rutas:
    GET  /                    Formulario para liquidar un servicio
    POST /liquidar            Valida, liquida y guarda el servicio en memoria
    GET  /servicios           Consultar servicios liquidados (filtro ?nombre=)
    GET  /servicios/<id>      Recibo del servicio (imprimible)
    GET  /api/servicios/<id>  Servicio en JSON
"""
from flask import Flask, abort, jsonify, redirect, render_template, request, url_for

import proyecto1 as negocio

app = Flask(__name__)

# "Almacenamiento" en memoria: se pierde al reiniciar el servidor.
SERVICIOS = {}
_siguiente_id = [1]


def guardar_servicio(liq):
    sid = _siguiente_id[0]
    _siguiente_id[0] += 1
    SERVICIOS[sid] = {"id": sid, **liq}
    return sid


def _a_entero(valor):
    """Convierte texto del formulario a int; devuelve el texto si no es convertible
    para que validar_datos reporte el error."""
    try:
        return int(str(valor).strip())
    except (TypeError, ValueError):
        return valor


@app.template_filter("moneda")
def filtro_moneda(valor):
    return negocio.formato_moneda(valor)


@app.get("/")
def index():
    return render_template("index.html", tipos=negocio.TIPOS_SERVICIO, datos={}, errores=[])


@app.post("/liquidar")
def liquidar():
    f = request.form
    datos = {
        "nombre": f.get("nombre", ""),
        "equipos": _a_entero(f.get("equipos", "")),
        "dias_iniciales": _a_entero(f.get("dias_iniciales", "")),
        "dias_adicionales": _a_entero(f.get("dias_adicionales", "0") or "0"),
        "tipo_servicio": _a_entero(f.get("tipo_servicio", "")),
    }
    try:
        liq = negocio.calcular_valores(**datos)
    except negocio.ValidacionError as e:
        return (
            render_template("index.html", tipos=negocio.TIPOS_SERVICIO, datos=f, errores=e.errores),
            400,
        )
    sid = guardar_servicio(liq)
    return redirect(url_for("ver_servicio", sid=sid))


@app.get("/servicios")
def listar_servicios():
    filtro = request.args.get("nombre", "").strip().lower()
    servicios = [s for s in SERVICIOS.values() if filtro in s["nombre"].lower()]
    return render_template("servicios.html", servicios=servicios, filtro=filtro)


@app.get("/servicios/<int:sid>")
def ver_servicio(sid):
    servicio = SERVICIOS.get(sid) or abort(404)
    return render_template("recibo.html", s=servicio, texto=negocio.generar_factura(servicio))


@app.get("/api/servicios/<int:sid>")
def api_servicio(sid):
    servicio = SERVICIOS.get(sid) or abort(404)
    return jsonify(servicio)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
