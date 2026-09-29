"""
CAPA VISTA (consola). Solo muestra datos y lee la entrada del usuario.
Toda la lógica vive en el controlador.
"""
from controlador.modulo_despacho import ModuloDespacho


class VistaConsola:
    """Interfaz de texto del módulo de despacho."""

    def __init__(self):
        self.controlador = ModuloDespacho()

    def iniciar(self) -> None:
        """Ciclo principal del menú."""
        while True:
            servicios = self.controlador.servicios_disponibles()
            print("\n=== MÓDULO DE DESPACHO (Abstract Factory) ===")
            for i, s in enumerate(servicios, 1):
                print(f"{i}. {s.capitalize()}")
            print("0. Salir")
            op = input("Elija una opción: ").strip()
            if op == "0":
                print("¡Hasta luego!")
                break
            if op.isdigit() and 1 <= int(op) <= len(servicios):
                self._despachar(servicios[int(op) - 1])
            else:
                print("Opción inválida.")

    def _despachar(self, servicio: str) -> None:
        """Pide los datos del servicio y muestra el resultado."""
        datos = {c: input(f"  {c.capitalize()}: ").strip()
                 for c in self.controlador.campos_requeridos(servicio)}
        try:
            r = self.controlador.despachar(servicio, datos)
        except ValueError as e:
            print(f"Error: {e}")
            return
        print(f"\n--- Despacho de {r['servicio']} ---")
        print(r["documento"])
        print(f"Valor: ${r['valor']:,}")
        print(r["manifiesto"])
