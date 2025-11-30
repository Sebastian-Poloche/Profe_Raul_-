from .herramientas import HerramientasController
from .prestamos import PrestamosController
from .busqueda import BusquedaController

class AppController:
    def __init__(self):
        self.herramientas = HerramientasController()
        self.prestamos = PrestamosController()
        self.busqueda = BusquedaController()

    def iniciar(self):
        pass
