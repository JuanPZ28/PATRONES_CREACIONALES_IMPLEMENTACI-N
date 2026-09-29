"""
CAPA MODELO - Fábricas.

Patrón Abstract Factory: FabricaServicio declara un método de creación por
cada producto de la familia. Cada fábrica concreta garantiza que el
documento, la tarifa y el manifiesto pertenezcan a la MISMA línea de servicio.
"""
from abc import ABC, abstractmethod
from modelo.productos import (
    DocumentoTransporte, Tarifa, Manifiesto,
    Tiquete, TarifaPasajero, ManifiestoPasajeros,
    GuiaEnvio, TarifaPaqueteria, ManifiestoCarga,
)


class FabricaServicio(ABC):
    """Fábrica abstracta de la familia de objetos de un servicio."""

    @abstractmethod
    def crear_documento(self, datos: dict) -> DocumentoTransporte:
        """Crea el documento de transporte con los datos recibidos."""

    @abstractmethod
    def crear_tarifa(self) -> Tarifa:
        """Crea la tarifa de la línea de servicio."""

    @abstractmethod
    def crear_manifiesto(self) -> Manifiesto:
        """Crea el manifiesto de la línea de servicio."""


class FabricaPasajeros(FabricaServicio):
    """Fábrica concreta: Tiquete + TarifaPasajero + ManifiestoPasajeros."""

    def crear_documento(self, datos: dict) -> DocumentoTransporte:
        return Tiquete(datos["pasajero"], datos["ruta"], datos["silla"])

    def crear_tarifa(self) -> Tarifa:
        return TarifaPasajero()

    def crear_manifiesto(self) -> Manifiesto:
        return ManifiestoPasajeros()


class FabricaPaqueteria(FabricaServicio):
    """Fábrica concreta: GuiaEnvio + TarifaPaqueteria + ManifiestoCarga."""

    def crear_documento(self, datos: dict) -> DocumentoTransporte:
        return GuiaEnvio(datos["remitente"], datos["destinatario"], int(datos["peso"]))

    def crear_tarifa(self) -> Tarifa:
        return TarifaPaqueteria()

    def crear_manifiesto(self) -> Manifiesto:
        return ManifiestoCarga()
