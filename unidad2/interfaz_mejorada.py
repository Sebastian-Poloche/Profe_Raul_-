import tkinter as tk
import re
from tkinter.messagebox import askyesno
from tkinter import messagebox
from datetime import datetime

# Creacion de la ventana
root = tk.Tk()
root.title("Ventana Principal")
root.geometry("538x410")
root.resizable(0,0)
root.config(padx=5, pady=20)

# ------- FUNCIONES -----------------------------------------------------------------------------------------------------

# Funcion para verificar si el usuario desea salir del formulario
def el_usuario_quiere_salir():
    if askyesno("Salir de la aplicacion", "Estas seguro que quieres cerrar la aplicacion"):
        root.destroy()

# Funcion para validar letras, espacios y números
VAL_NOMBRE = re.compile(r"^[A-Za-z]+$")
VAL_PRECIO = re.compile(r"^[0-9-]+$")
VAL_PLACA = re.compile(r"^[0-9-A-Za-z-]+$")

# Funcion para limpiar todos los campos de texto
def limpiar_campos_texto():
    for var, err in [
        (var_placa_vehiculo, err_placa_vehiculo),
        (var_valor_cargue, err_valor_cargue),
        (var_tipo_carga, err_tipo_carga),
        (var_vencimiento_soat, err_vencimiento_soat)
    ]:
        var.set("")
        err.set("")

# Validacion de la placa del vehiculo
def val_placa_vehiculo() -> bool:
    txt = var_placa_vehiculo.get()
    # Permitir espacios vacios mientras se escribe, solo mostraremos error si hay caracteres erroneos
    if txt == "":
        err_placa_vehiculo.set("")
        return True
    if VAL_PLACA.match(txt):
        err_placa_vehiculo.set("")
        return True
    err_placa_vehiculo.set("Solo se permiten letras Mayusculas, Minusculas y Números")
    return False

def val_valor_cargue() -> bool:
    txt = var_valor_cargue.get()
    if txt == "":
        err_valor_cargue.set("")
        return True
    if VAL_PRECIO.match(txt):
        err_valor_cargue.set("")
        return True
    err_valor_cargue.set("Solo se permiten valores enteros")
    return False

def val_tipo_carga() -> bool:
    txt = var_tipo_carga.get()
    if txt == "":
        err_tipo_carga.set("")
        return True
    if VAL_NOMBRE.match(txt):
        err_tipo_carga.set("")
        return True
    err_tipo_carga.set("Solo se puede cargue a granel, bultos o canastillas")
    return False

def val_vencimiento_soat() -> bool:
    txt = var_vencimiento_soat.get().strip()
    if txt == "":
        err_vencimiento_soat.set("")
        return True
    try:
        datetime.strptime(txt, "%Y-%m-%d")
        err_vencimiento_soat.set("")
        return True
    except ValueError:
        err_vencimiento_soat.set("Fecha inválida. Usa el formato YYYY-MM-DD")
        return False


# Funcion para enviar toda la informacion
def enviar():
        # Ejecuta todas las validaciones y evita enviar si hay errores
        ok = all([
            val_placa_vehiculo(),
            val_valor_cargue(),
            val_tipo_carga(),
            val_vencimiento_soat(),
        ])

        # Mensajes vacíos cuentan como válidos solo si el campo no es obligatorio.
        obligatorios = [
            (var_placa_vehiculo.get().strip() != "", err_placa_vehiculo, "La placa es obligatoria."),
            (var_valor_cargue.get().strip() != "", err_valor_cargue, "El valor del cargue es obligatorio."),
            (var_tipo_carga.get().strip() != "", err_tipo_carga, "El tipo de carga es obligatorio."),
            (var_vencimiento_soat.get().strip() != "", err_vencimiento_soat, "La fecha de vencimiento del soat es obligatoria."),
        ]
        for lleno, err_var, msg in obligatorios:
            if not lleno and err_var.get() == "":
                err_var.set(msg)
                ok = False

        if not ok:
            messagebox.showerror("Errores de validación", "Por favor corrige los campos marcados en rojo.")
            return

        messagebox.showinfo("OK", "Formulario válido. ¡Datos guardados!")
        # Aquí podrías continuar con persistencia o lógica adicional.


# -----------------------------------------------------------------------------------------------------------------------

# Variables de entrada
var_placa_vehiculo = tk.StringVar()
var_valor_cargue = tk.StringVar()
var_tipo_carga = tk.StringVar()
var_vencimiento_soat = tk.StringVar()

# Variables de error
err_placa_vehiculo = tk.StringVar()
err_valor_cargue = tk.StringVar()
err_tipo_carga = tk.StringVar()
err_vencimiento_soat = tk.StringVar()


# Creacion de los elementos de la interfaz

# -------------- UI -----------------------------------------------------------------------------------------------------

# Placa del Vehiculo
label_placa_vehiculo = tk.Label(root, text="Placa del Vehiculo").grid(row=0, column=0, pady=(0, 20), sticky="w")
entry_placa_vehiculo = tk.Entry(root, textvariable=var_placa_vehiculo)
entry_placa_vehiculo.grid(row=0, column=1, padx=(170, 0), pady=(0, 20), sticky="e")
tk.Label(textvariable=err_placa_vehiculo, fg="#c1121f").grid(row=1, column=1, sticky="w", pady=(0,6))

# Valor de Cargue
label_valor_cargue = tk.Label(root, text="Valor del Cargue").grid(row=2, column=0, pady=(0, 20), sticky="w")
entry_valor_cargue = tk.Entry(root, textvariable=var_valor_cargue)
entry_valor_cargue.grid(row=2, column=1, pady=(0, 20), padx=(170, 0))
tk.Label(textvariable=err_valor_cargue, fg="#c1121f").grid(row=3, column=1, sticky="w", pady=(0,6))

# Tipo de Carga
label_tipo_carga = tk.Label(root, text="Tipo de Carga").grid(row=4, column=0, pady=(0, 20), sticky="w")
entry_tipo_carga = tk.Entry(root, textvariable=var_tipo_carga)
entry_tipo_carga.grid(row=4, column=1, pady=(0, 20), padx=(170, 0))
tk.Label(textvariable=err_tipo_carga, fg="#c1121f").grid(row=5, column=1, sticky="w", pady=(0,6))

# Vencimiento Soat
label_vencimiento_soat = tk.Label(root, text="Fecha de Vencimiento del Soat").grid(row=6, column=0, pady=(0, 20), sticky="w")
entry_vencimiento_soat = tk.Entry(root, textvariable=var_vencimiento_soat)
entry_vencimiento_soat.grid(row=6, column=1, pady=(0, 20), padx=(170, 0))
tk.Label(textvariable=err_vencimiento_soat, fg="#c1121f").grid(row=7, column=1, sticky="w", pady=(0,6))

# Boton para validar la informacion
boton_validar = tk.Button(root, text="Validar Informacion", command=enviar).grid(row=8, column=0, columnspan=2, sticky="we", pady=(0,20))

# Boton para limpiar todos los campos del formulario
boton_limpiar = tk.Button(root, text="Limpiar", command=limpiar_campos_texto).grid(row=9, column=0, columnspan=2, sticky="we", pady=(0,20))

# Eventos de validación en vivo (permiten escribir, solo muestran mensaje)
entry_placa_vehiculo.bind("<KeyRelease>", lambda e: val_placa_vehiculo())
entry_valor_cargue.bind("<KeyRelease>", lambda e: val_valor_cargue())
entry_tipo_carga.bind("<KeyRelease>", lambda e: val_tipo_carga())
entry_vencimiento_soat.bind("<KeyRelease>", lambda e: val_vencimiento_soat())

# Funcion para confirmar la salida de un usuario del Formulario
root.protocol("WM_DELETE_WINDOW", el_usuario_quiere_salir)

# Fin de la ventana
root.mainloop()