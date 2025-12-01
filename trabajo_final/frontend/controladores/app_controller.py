"""
Controlador principal de la aplicación.

Coordina la inicialización y gestión de controladores especializados
para herramientas, préstamos y búsqueda avanzada.
"""

from .busqueda import BusquedaController
from .herramientas import HerramientaModel
from .prestamos import PrestamoModel


class AppController:
    """
    Controlador principal que orquesta los sub-controladores.

    Centraliza el acceso a la lógica de negocio de diferentes módulos,
    facilitando la integración y coordinación entre herramientas,
    préstamos y funcionalidades de búsqueda.
    """

    def __init__(self):
        """
        Inicializar controladores de módulos.

        Crea instancias de controladores para herramientas, préstamos
        y búsqueda, permitiendo acceso centralizado desde la interfaz gráfica.
        """
        self.herramientas = HerramientaModel()
        self.prestamos = PrestamoModel()
        self.busqueda = BusquedaController()

    def iniciar(self):
        """
        Iniciar la aplicación y sus componentes.

        Realiza inicializaciones necesarias antes de que la aplicación
        se ejecute completamente. Actualmente es un placeholder para
        futuras funcionalidades de inicialización.
        """
        pass

