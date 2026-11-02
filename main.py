
from flask import Flask, render_template, request, redirect, url_for,jsonify
from copy import copy

app = Flask(__name__)

# Arreglos para almacenar las instancias
lista_empleados = []
lista_conductores = []
lista_viajes=[]
lista_paquetes_ligeros=[]
lista_paquetes_pesados=[]
lista_paquetes_empacados=[]
lista_paquetes_enruta=[]
contador_state=0
paquete_state = None
#---------------------------------------------------PATRONES DE COMPORTAMIENTO-------------------------------------------------------------------
#PATRON CHAIN OF RESPONSABILITY----------------------
"""Para este patorn, nuestro objetivo es centrarlo en brindar soporte a la simulacion de registro de paquetes para la empres transportadora. 
Esto mediante dos soportes donde 1 se encarga de registrar los paquetes que sean iguales o menores al peso maximo y otro para que se encargue 
de aquellos paquetes que pesen mas que el peso maximo llegando hasta un limite de 40kg."""

class Soportepaqueteria:
    def __init__(self, siguiente=None):
        self.siguiente = siguiente

    def atender(self, fecha_envio,descripcion,peso,ancho,alto,profundo, valor, categoria):
        if self.siguiente:
            return self.siguiente.atender(fecha_envio,descripcion,peso,ancho,alto,profundo, valor, categoria)

        return "El paquete no puede ser transportado por exceso de peso"

class Soportepaqueteligero(Soportepaqueteria):
    def atender(self, fecha_envio,descripcion,peso,ancho,alto,profundo, valor, categoria):
        if int(peso) <= 20:
            paqueteligero=[fecha_envio,descripcion,peso,ancho,alto,profundo, valor, categoria]
            lista_paquetes_ligeros.append(paqueteligero)
            return "Paquete ligero registrado"
        return super().atender(fecha_envio,descripcion,peso,ancho,alto,profundo, valor, categoria)


class Soportepaquetepesado(Soportepaqueteria):
    def atender(self, fecha_envio,descripcion,peso,ancho,alto,profundo, valor, categoria):
        if int(peso) <= 40:
            paquetepesado=[fecha_envio,descripcion,peso,ancho,alto,profundo, valor, categoria]
            lista_paquetes_pesados.append(paquetepesado)
            return "Paquete pesado registrado"
        return super().atender(fecha_envio,descripcion,peso,ancho,alto,profundo, valor, categoria)

#PATRON STATE--------------------------------------------------------------------------------------------------------------------------------------
"""ESte patorn solventa el seguimiento del paquete, migrando todos los paquetes a unas tablas llamadas empcadando y 
en camino, para simular el patorn state que se solicita"""

#Interfaz primaria 
class EstadoPaquete:

    def procesar(self, paquete):
        pass


# Estado registrado
class Registrado(EstadoPaquete):

    def procesar(self, paquete):
        paquete.estado = Empaque()
        return "Los paquetes se encuentran registrados"


# Estado en empque
class Empaque(EstadoPaquete):

    def procesar(self, paquete):
        lista_paquetes_empacados.extend(lista_paquetes_pesados)
        lista_paquetes_empacados.extend(lista_paquetes_ligeros)
        lista_paquetes_ligeros.clear()
        lista_paquetes_pesados.clear()
        paquete.estado = enRuta()
        return "Los paquetes estan siendo empacados"


# Estado en ruta
class enRuta(EstadoPaquete):

    def procesar(self, paquete):
        lista_paquetes_enruta.extend(lista_paquetes_empacados)
        lista_paquetes_empacados.clear()
        return "Los paquetes estan en ruta"


# Contexto
class Paquete:

    def __init__(self):
        self.estado = Registrado()

    def procesar(self):
        return self.estado.procesar(self)



#---------------------------------------------------PATRONES DE COMPORTAMIENTO-------------------------------------------------------------------
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
    global contador_state,paquete_state

    lista_empleados.clear()

    lista_conductores.clear()

    lista_viajes.clear()

    lista_paquetes_ligeros.clear()
    lista_paquetes_pesados.clear()

    lista_paquetes_empacados.clear()
    lista_paquetes_enruta.clear()
    contador_state=0
    paquete_state = None



# PÁGINA PRINCIPAL


@app.route("/")
def hello_world():
    reiniciar_listas()
    conexionDB.instancia = None
    return render_template(
        "index.html",
        empleados=lista_empleados,
        conductores=lista_conductores,
        viajes=lista_viajes,
        paquetes_ligeros=lista_paquetes_ligeros,
        paquetes_pesados=lista_paquetes_pesados,
        lista_empacados=lista_paquetes_empacados,
        lista_enruta=lista_paquetes_enruta
        
    )


@app.route("/empleados")
def empleados():
    return render_template(
        "index.html",
        empleados=lista_empleados,
        conductores=lista_conductores,
        viajes=lista_viajes,
        paquetes_ligeros=lista_paquetes_ligeros,
        paquetes_pesados= lista_paquetes_pesados,
        lista_empacados=lista_paquetes_empacados,
        lista_enruta=lista_paquetes_enruta
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

@app.route("/chain",methods=["POST"] )
def chain1():
    soporte2 = Soportepaquetepesado()
    soporte1 = Soportepaqueteligero(soporte2)

    fecha_envio = request.form.get("fecha_envio")
    descripcion = request.form.get("descripcion")
    peso = request.form.get("peso")
    ancho = request.form.get("ancho")
    alto = request.form.get("alto")
    profundo = request.form.get("profundo")
    valor = request.form.get("valor")
    categoria = request.form.get("categoria")

    soportepaqueteria=soporte1.atender(fecha_envio,descripcion,peso,ancho,alto,profundo, valor, categoria)
    mensaje=soportepaqueteria

    return jsonify({
        "mensaje": mensaje,
        "estado": True,
        "redirect": url_for('empleados')
    })

@app.route("/state", methods=["POST"])
def state1():
    global contador_state, paquete_state

    if len(lista_paquetes_ligeros) == 0 and len(lista_paquetes_pesados) == 0 and paquete_state== None:
        return jsonify({
            "mensaje": "Listas despachadas o vacías",
            "estado": True,
            "redirect": url_for('empleados')
        })

    if contador_state == 0:
        paquete_state = Paquete()

    mensaje = paquete_state.procesar()
    contador_state += 1

    if contador_state >= 3:
        contador_state = 0
        paquete_state = None

    return jsonify({
        "mensaje": mensaje,
        "estado": True,
        "redirect": url_for('empleados')
    })



@app.route("/reboot", methods=["POST"])
def reboot1():
   return redirect(url_for("hello_world"))
    


if __name__ == "__main__":
    app.run(debug=True)

