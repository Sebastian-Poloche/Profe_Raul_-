import tkinter as tk

class Cargue():

    def __init__(self, root):
        self.root = root
        self.id = tk.StringVar(root)
        self.placa_del_vehiculo = tk.StringVar(root)
        self.valor_del_cargue = tk.IntVar(root)
        self.tipo_de_carga = tk.StringVar(root)
        self.vencimiento_de_soat = tk.StringVar(root)