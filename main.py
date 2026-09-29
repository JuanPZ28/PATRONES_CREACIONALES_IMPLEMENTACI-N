
from flask import Flask, render_template, request, redirect, url_for,jsonify
from copy import copy

app = Flask(__name__)

# Arreglos para almacenar las instancias
lista_empleados = []
lista_conductores = []
lista_viajes=[]





class conexionDB:

    instancia = None

    def __init__(self, nombre_db, _interno=False):

        if not _interno:
            raise Exception(
                "No se puede crear directamente la conexión"
            )
        self.nombre_db = nombre_db

    def __str__(self):
        return f"Conexión DB: {self.nombre_db}"

    @staticmethod
    def singleton():

        if conexionDB.instancia is None:

            conexionDB.instancia = conexionDB(
                "MongoDB",
                _interno=True
            )

            return f"Creando nueva conexión a la base de datos: {conexionDB.instancia}"
            
        else:
            return f"Retornando conexión existente {conexionDB.instancia}"

class Prototype:

    @staticmethod
    def cloneable(lista_viajes):

        # Verificamos que la lista no este vacia
        if lista_viajes:

            # Obtenemos el ultimo viaje
            ultimo_viaje = lista_viajes[-1]

            # Creamos una copia del viaje
            viaje_clonado = copy(ultimo_viaje)

            return viaje_clonado

        return None

class Viaje:

    def __init__(self, fecha_salida, hora_salida, fecha_llegada, hora_llegada, estado):
        self.fecha_salida = fecha_salida
        self.hora_salida = hora_salida
        self.fecha_llegada = fecha_llegada
        self.hora_llegada = hora_llegada
        self.estado = estado

    # Clase interna Builder
    class Builder:

        def __init__(self):
            self.fecha_salida = ""
            self.hora_salida = ""
            self.fecha_llegada = ""
            self.hora_llegada = ""
            self.estado = ""

        def set_fecha_salida(self, fecha_salida):
            self.fecha_salida = fecha_salida
            return self

        def set_hora_salida(self, hora_salida):
            self.hora_salida = hora_salida
            return self

        def set_fecha_llegada(self, fecha_llegada):
            self.fecha_llegada = fecha_llegada
            return self

        def set_hora_llegada(self, hora_llegada):
            self.hora_llegada = hora_llegada
            return self

        def set_estado(self, estado):
            self.estado = estado
            return self

        def build(self):
            return Viaje(
                self.fecha_salida,
                self.hora_salida,
                self.fecha_llegada,
                self.hora_llegada,
                self.estado
            )


# =========================
# CLASE EMPLEADO
# =========================

class Empleado:

    def __init__(
        self,
        nombre="",
        apellido="",
        tipo_documento="",
        num_documento="",
        telefono="",
        email="",
        direccion="",
        fecha_ingreso="",
        cargo=""
    ):
        self.nombre = nombre
        self.apellido = apellido
        self.tipo_documento = tipo_documento
        self.num_documento = num_documento
        self.telefono = telefono
        self.email = email
        self.direccion = direccion
        self.fecha_ingreso = fecha_ingreso
        self.cargo = cargo

    def __str__(self):
        return f"Empleado: {self.nombre} {self.apellido} - Cargo: {self.cargo}"


# =========================
# CLASE CONDUCTOR
# =========================

class Conductor(Empleado):

    def __init__(
        self,
        nombre="",
        apellido="",
        tipo_documento="",
        num_documento="",
        telefono="",
        email="",
        direccion="",
        fecha_ingreso="",
        cargo="",
        num_licencia="",
        categoria="",
        fecha_vencimiento=""
    ):

        # Inicializa la parte heredada de Empleado
        super().__init__(
            nombre,
            apellido,
            tipo_documento,
            num_documento,
            telefono,
            email,
            direccion,
            fecha_ingreso,
            cargo
        )

        # Atributos propios de Conductor
        self.num_licencia = num_licencia
        self.categoria = categoria
        self.fecha_vencimiento = fecha_vencimiento

    def __str__(self):
        return f"Conductor: {self.nombre} {self.apellido} - Licencia: {self.num_licencia}"


# =========================
# FACTORY
# =========================

class FactoryEmpleado:

    @staticmethod
    def crear_empleado(tipo, **datos):

        if tipo == "empleado":

            return Empleado(
                nombre=datos.get("nombre", ""),
                apellido=datos.get("apellido", ""),
                tipo_documento=datos.get("tipo_documento", ""),
                num_documento=datos.get("num_documento", ""),
                telefono=datos.get("telefono", ""),
                email=datos.get("email", ""),
                direccion=datos.get("direccion", ""),
                fecha_ingreso=datos.get("fecha_ingreso", ""),
                cargo=datos.get("cargo", "")
            )

        elif tipo == "conductor":

            return Conductor(
                nombre=datos.get("nombre", ""),
                apellido=datos.get("apellido", ""),
                tipo_documento=datos.get("tipo_documento", ""),
                num_documento=datos.get("num_documento", ""),
                telefono=datos.get("telefono", ""),
                email=datos.get("email", ""),
                direccion=datos.get("direccion", ""),
                fecha_ingreso=datos.get("fecha_ingreso", ""),
                cargo=datos.get("cargo", ""),
                num_licencia=datos.get("num_licencia", ""),
                categoria=datos.get("categoria", ""),
                fecha_vencimiento=datos.get("fecha_vencimiento", "")
            )

        else:
            return None



# REINICIAR LISTAS


def reiniciar_listas():


    lista_empleados.clear()

    lista_conductores.clear()

    lista_viajes.clear()



# PÁGINA PRINCIPAL


@app.route("/")
def hello_world():
    reiniciar_listas()
    conexionDB.instancia = None
    return render_template(
        "index.html",
        empleados=lista_empleados,
        conductores=lista_conductores
    )


@app.route("/empleados")
def empleados():
    return render_template(
        "index.html",
        empleados=lista_empleados,
        conductores=lista_conductores,
        viajes=lista_viajes
    )

@app.route("/factory", methods=["POST"])
def factory1():

    nombre = request.form.get("nombre")
    apellido = request.form.get("apellido")
    tipo_documento = request.form.get("tipo_documento")
    num_documento = request.form.get("num_documento")
    telefono = request.form.get("telefono")
    email = request.form.get("email")
    direccion = request.form.get("direccion")
    fecha_ingreso = request.form.get("fecha_ingreso")
    cargo = request.form.get("cargo")

    # Datos adicionales del conductor
    num_licencia = request.form.get("num_licencia")
    categoria = request.form.get("categoria")
    fecha_vencimiento = request.form.get("fecha_vencimiento")

    # Determinar el tipo de empleado
    if cargo == "Conductor":
        tipo = "conductor"
    else:
        tipo = "empleado"

    # Crear la instancia mediante Factory
    instancia = FactoryEmpleado.crear_empleado(
        tipo,
        nombre=nombre,
        apellido=apellido,
        tipo_documento=tipo_documento,
        num_documento=num_documento,
        telefono=telefono,
        email=email,
        direccion=direccion,
        fecha_ingreso=fecha_ingreso,
        cargo=cargo,

        # Datos adicionales del conductor
        num_licencia=num_licencia,
        categoria=categoria,
        fecha_vencimiento=fecha_vencimiento
    )

    # Guardar en la lista correspondiente
    if tipo == "conductor":
        lista_conductores.append(instancia)
    else:
        lista_empleados.append(instancia)

    print(f"Registrado: {instancia}")

    return redirect(url_for("empleados"))


@app.route("/builder", methods=["POST"])
def builder1():

    fecha_salida = request.form.get("fecha_salida")
    hora_salida = request.form.get("hora_salida")
    fecha_llegada = request.form.get("fecha_llegada")
    hora_llegada = request.form.get("hora_llegada")
    estado = request.form.get("estado")

    viaje = Viaje.Builder() \
        .set_fecha_salida(fecha_salida) \
        .set_hora_salida(hora_salida) \
        .set_fecha_llegada(fecha_llegada) \
        .set_hora_llegada(hora_llegada) \
        .set_estado(estado) \
        .build()

    print(viaje)
    lista_viajes.append(viaje)


    return redirect(url_for("empleados"))

@app.route("/prototype", methods=["POST"])
def prototype1():
    copia= Prototype.cloneable(lista_viajes)
  

    if copia: 
        lista_viajes.append(copia) 

    return redirect(url_for("empleados"))

@app.route("/singleton")
def singleton1():
    mensaje= conexionDB.singleton()

    return jsonify({
            "mensaje": mensaje
        })

@app.route("/reboot", methods=["POST"])
def reboot1():
   return redirect(url_for("hello_world"))
    


if __name__ == "__main__":
    app.run(debug=True)

