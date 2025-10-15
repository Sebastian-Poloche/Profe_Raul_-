import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import re

# Expresiones regulares para validación
VAL_NOMBRE = re.compile(r"^[A-Za-z]+$")
VAL_PRECIO = re.compile(r"^[0-9-]+$")
VAL_PLACA = re.compile(r"^[0-9A-Z-]+$")

class Validaciones:
    def __init__(self, variables, errores):
        self.variables = variables
        self.errores = errores

    def val_placa_vehiculo(self) -> bool:
        txt = self.variables['placa'].get()
        if txt == "":
            self.errores['placa'].set("")
            return True
        if VAL_PLACA.match(txt):
            self.errores['placa'].set("")
            return True
        self.errores['placa'].set("Solo se permiten letras Mayusculas, Minusculas y Números")
        return False

    def val_valor_cargue(self) -> bool:
        txt = self.variables['valor'].get()
        if txt == "":
            self.errores['valor'].set("")
            return True
        if VAL_PRECIO.match(txt):
            self.errores['valor'].set("")
            return True
        self.errores['valor'].set("Solo se permiten valores enteros")
        return False

    def val_tipo_carga(self) -> bool:
        txt = self.variables['tipo'].get()
        if txt == "":
            self.errores['tipo'].set("")
            return True
        if VAL_NOMBRE.match(txt):
            self.errores['tipo'].set("")
            return True
        self.errores['tipo'].set("Solo se puede cargue a granel, bultos o canastillas")
        return False

    def val_vencimiento_soat(self) -> bool:
        txt = self.variables['soat'].get().strip()
        if txt == "":
            self.errores['soat'].set("")
            return True
        try:
            datetime.strptime(txt, "%Y-%m-%d")
            self.errores['soat'].set("")
            return True
        except ValueError:
            self.errores['soat'].set("Fecha inválida. Usa el formato YYYY-MM-DD")
            return False
        
    def enviar(self):
        # Ejecuta todas las validaciones
        ok = all([
            self.val_placa_vehiculo(),
            self.val_valor_cargue(),
            self.val_tipo_carga(),
            self.val_vencimiento_soat()
        ])

        if not ok:
            messagebox.showerror("Errores de validación", "Por favor corrige los campos marcados en rojo.")
            return False

        messagebox.showinfo("OK", "Formulario válido. ¡Datos guardados!")
        return True

    def limpiar_campos_texto(self):
        for var in self.variables.values():
            var.set("")
        for err in self.errores.values():
            err.set("")