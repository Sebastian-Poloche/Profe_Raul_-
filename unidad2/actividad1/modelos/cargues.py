import tkinter as tk

class Cargue():
    def __init__(self, root):
        self.root = root
        self.placa_vehiculo = tk.StringVar(root)
        self.valor_cargue = tk.IntVar(root)
        self.tipo_carga = tk.StringVar(root)
        self.vencimiento_soat = tk.StringVar(root)