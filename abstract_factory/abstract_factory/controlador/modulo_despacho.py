"""
CAPA CONTROLADOR - ModuloDespacho (cliente del patrón).

Solo conoce las interfaces (FabricaServicio, DocumentoTransporte, Tarifa,
Manifiesto), nunca las clases concretas de productos. No imprime nada:
devuelve diccionarios para que cualquier vista (consola o interfaz gráfica)
los muestre.
"""
from modelo.fabricas import FabricaServicio, FabricaPasajeros, FabricaPaqueteria


class ModuloDespacho:
    """Coordina el despacho de un servicio usando la fábrica adecuada."""

    FABRICAS = {
        "pasajeros": FabricaPasajeros,
        "paqueteria": FabricaPaqueteria,
    }

    def __init__(self):
        # Un manifiesto por línea de servicio, creado con su propia fábrica
        self._fabricas: dict[str, FabricaServicio] = {}
        self._manifiestos: dict = {}

    def servicios_disponibles(self) -> list[str]:
        """Nombres de las líneas de servicio disponibles."""
        return list(self.FABRICAS.keys())

    def campos_requeridos(self, servicio: str) -> list[str]:
        """Campos que la vista debe solicitar según el servicio."""
        return {
            "pasajeros": ["pasajero", "ruta", "silla"],
            "paqueteria": ["remitente", "destinatario", "peso"],
        }[servicio]

    def _fabrica(self, servicio: str) -> FabricaServicio:
        """Obtiene (o crea) la fábrica del servicio indicado."""
        if servicio not in self.FABRICAS:
            raise ValueError(f"Servicio no válido: {servicio}")
        if servicio not in self._fabricas:
            self._fabricas[servicio] = self.FABRICAS[servicio]()
            self._manifiestos[servicio] = self._fabricas[servicio].crear_manifiesto()
        return self._fabricas[servicio]

    def despachar(self, servicio: str, datos: dict) -> dict:
        """
        Crea la familia de objetos del servicio y procesa el despacho.

        Retorna: texto del documento, valor calculado y manifiesto actualizado.
        """
        fabrica = self._fabrica(servicio)
        documento = fabrica.crear_documento(datos)
        valor = fabrica.crear_tarifa().calcular_valor(datos)
        # El valor calculado por la tarifa se asigna al documento
        if hasattr(documento, "precio"):
            documento.precio = valor
        else:
            documento.valor = valor
        manifiesto = self._manifiestos[servicio]
        manifiesto.agregar(documento)
        return {
            "servicio": servicio.capitalize(),
            "documento": documento.emitir(),
            "valor": valor,
            "manifiesto": manifiesto.generar(),
        }
