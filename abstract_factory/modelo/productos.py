"""
CAPA MODELO - Productos (Abstract Factory de Servicio, Figura 6).

Define las interfaces abstractas de los tres productos de cada familia
(DocumentoTransporte, Tarifa, Manifiesto) y sus implementaciones concretas
para las dos líneas de servicio: Pasajeros y Paquetería.
"""
from abc import ABC, abstractmethod
from datetime import date


# ======================================================================
# Interfaces (productos abstractos)
# ======================================================================
class DocumentoTransporte(ABC):
    """Documento que respalda el servicio (tiquete o guía de envío)."""

    @abstractmethod
    def emitir(self) -> str:
        """Devuelve el texto del documento emitido."""


class Tarifa(ABC):
    """Regla de cálculo del valor del servicio."""

    @abstractmethod
    def calcular_valor(self, datos: dict) -> int:
        """Calcula el valor en pesos según los datos del servicio."""


class Manifiesto(ABC):
    """Listado de documentos transportados en un viaje."""

    @abstractmethod
    def agregar(self, documento: DocumentoTransporte) -> None:
        """Agrega un documento al manifiesto."""

    @abstractmethod
    def generar(self) -> str:
        """Devuelve el texto del manifiesto."""


# ======================================================================
# Familia PASAJEROS
# ======================================================================
class Tiquete(DocumentoTransporte):
    """Tiquete de un pasajero."""

    def __init__(self, pasajero: str, ruta: str, silla: str):
        self.pasajero = pasajero
        self.ruta = ruta
        self.silla = silla
        self.fecha_compra = date.today()
        self.precio = 0            # lo asigna el controlador con la tarifa
        self.estado = "Emitido"

    def emitir(self) -> str:
        return (f"TIQUETE | {self.pasajero} | {self.ruta} | Silla {self.silla} | "
                f"{self.fecha_compra} | ${self.precio:,} | {self.estado}")


class TarifaPasajero(Tarifa):
    """Tarifa por ruta; la silla preferencial tiene 20 % de recargo."""

    TARIFAS_RUTA = {
        "Bogotá-Medellín": 65000,
        "Bogotá-Cali": 90000,
        "Bogotá-Bucaramanga": 70000,
    }

    def calcular_valor(self, datos: dict) -> int:
        base = self.TARIFAS_RUTA.get(datos["ruta"], 50000)
        if datos["silla"].lower() == "preferencial":
            base = int(base * 1.2)
        return base


class ManifiestoPasajeros(Manifiesto):
    """Listado de pasajeros del viaje."""

    def __init__(self):
        self._tiquetes: list[Tiquete] = []

    def agregar(self, documento: DocumentoTransporte) -> None:
        self._tiquetes.append(documento)

    def generar(self) -> str:
        lineas = [f"  {i}. {t.pasajero} (silla {t.silla})"
                  for i, t in enumerate(self._tiquetes, 1)]
        return "MANIFIESTO DE PASAJEROS\n" + "\n".join(lineas)


# ======================================================================
# Familia PAQUETERÍA
# ======================================================================
class GuiaEnvio(DocumentoTransporte):
    """Guía de envío de un paquete."""

    _consecutivo = 0

    def __init__(self, remitente: str, destinatario: str, peso: int):
        GuiaEnvio._consecutivo += 1
        self.numero_guia = f"GE-{GuiaEnvio._consecutivo:06d}"
        self.remitente = remitente
        self.destinatario = destinatario
        self.peso = peso
        self.valor = 0             # lo asigna el controlador con la tarifa

    def emitir(self) -> str:
        return (f"GUIA {self.numero_guia} | De: {self.remitente} | "
                f"Para: {self.destinatario} | {self.peso} kg | ${self.valor:,}")


class TarifaPaqueteria(Tarifa):
    """Tarifa por peso: $3.000 por kg, mínimo $8.000."""

    VALOR_KILO = 3000
    MINIMO = 8000

    def calcular_valor(self, datos: dict) -> int:
        return max(self.MINIMO, int(datos["peso"]) * self.VALOR_KILO)


class ManifiestoCarga(Manifiesto):
    """Listado de guías de carga del viaje."""

    def __init__(self):
        self._guias: list[GuiaEnvio] = []

    def agregar(self, documento: DocumentoTransporte) -> None:
        self._guias.append(documento)

    def generar(self) -> str:
        lineas = [f"  {i}. {g.numero_guia} - {g.peso} kg -> {g.destinatario}"
                  for i, g in enumerate(self._guias, 1)]
        return "MANIFIESTO DE CARGA\n" + "\n".join(lineas)
