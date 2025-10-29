import tkinter as tk
from tkinter.messagebox import askyesno
from controladores.validaciones import Validaciones

class Interfaz():
    def mostrar_interfaz():
        # Creacion de la ventana
        root = tk.Tk()
        root.title("Ventana Principal")
        root.geometry("565x410")
        root.resizable(0,0)
        root.config(padx=5, pady=20)

        # Variables de entrada
        variables = {
            'placa': tk.StringVar(root),
            'valor': tk.StringVar(root),
            'tipo': tk.StringVar(root),
            'soat': tk.StringVar(root)
        }

        # Variables de error
        errores = {
            'placa': tk.StringVar(root),
            'valor': tk.StringVar(root),
            'tipo': tk.StringVar(root),
            'soat': tk.StringVar(root)
        }

        # Crear instancia de validaciones
        validador = Validaciones(variables, errores)
        
        # Funcion para verificar si el usuario desea salir del formulario
        def el_usuario_quiere_salir():
            if askyesno("Salir de la aplicacion", "Estas seguro que quieres cerrar la aplicacion"):
                root.destroy()

        # UI
        # Placa del Vehiculo
        tk.Label(root, text="Placa del Vehiculo").grid(row=0, column=0, pady=(0, 20), sticky="w")
        entry_placa = tk.Entry(root, textvariable=variables['placa'])
        entry_placa.grid(row=0, column=1, padx=(170, 0), pady=(0, 20), sticky="e")
        tk.Label(root, textvariable=errores['placa'], fg="#c1121f").grid(row=1, column=1, sticky="w", pady=(0,6))

        # Valor de Cargue
        tk.Label(root, text="Valor del Cargue").grid(row=2, column=0, pady=(0, 20), sticky="w")
        entry_valor = tk.Entry(root, textvariable=variables['valor'])
        entry_valor.grid(row=2, column=1, pady=(0, 20), padx=(170, 0))
        tk.Label(root, textvariable=errores['valor'], fg="#c1121f").grid(row=3, column=1, sticky="w", pady=(0,6))

        # Tipo de Carga
        tk.Label(root, text="Tipo de Carga").grid(row=4, column=0, pady=(0, 20), sticky="w")
        entry_tipo = tk.Entry(root, textvariable=variables['tipo'])
        entry_tipo.grid(row=4, column=1, pady=(0, 20), padx=(170, 0))
        tk.Label(root, textvariable=errores['tipo'], fg="#c1121f").grid(row=5, column=1, sticky="w", pady=(0,6))

        # Vencimiento Soat
        tk.Label(root, text="Fecha de Vencimiento del Soat").grid(row=6, column=0, pady=(0, 20), sticky="w")
        entry_soat = tk.Entry(root, textvariable=variables['soat'])
        entry_soat.grid(row=6, column=1, pady=(0, 20), padx=(170, 0))
        tk.Label(root, textvariable=errores['soat'], fg="#c1121f").grid(row=7, column=1, sticky="w", pady=(0,6))

        # Botones
        tk.Button(root, text="Validar Informacion", command=validador.enviar).grid(row=8, column=0, columnspan=2, sticky="we", pady=(0,20))
        tk.Button(root, text="Limpiar", command=validador.limpiar_campos_texto).grid(row=9, column=0, columnspan=2, sticky="we", pady=(0,20))

        # Eventos de validación en vivo
        entry_placa.bind("<KeyRelease>", lambda e: validador.val_placa_vehiculo())
        entry_valor.bind("<KeyRelease>", lambda e: validador.val_valor_cargue())
        entry_tipo.bind("<KeyRelease>", lambda e: validador.val_tipo_carga())
        entry_soat.bind("<KeyRelease>", lambda e: validador.val_vencimiento_soat())

        # Funcion para confirmar la salida de un usuario del Formulario
        root.protocol("WM_DELETE_WINDOW", el_usuario_quiere_salir)

        # Fin de la ventana
        root.mainloop()