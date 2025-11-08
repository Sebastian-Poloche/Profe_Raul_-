import tkinter as tk
from tkinter.messagebox import askyesno
from controladores.comunicacion import Comunicacion
from modelos.cargues import Cargue
from controladores.validaciones import Validaciones

class Interfaz():

    def __init__(self):
        self.root = tk.Tk()
        self.comunicacion = Comunicacion(self.root)
        pass

    def mostrar_interfaz(self):
        camiones = Cargue(self.root)
        # Creacion de la ventana
        self.root.title("Ventana Principal")
        self.root.geometry("620x410")
        self.root.resizable(0,0)
        self.root.config(padx=5, pady=20)
        # Variables de entrada
        variables = {
            'placa': tk.StringVar(self.root),
            'valor': tk.StringVar(self.root),
            'tipo': tk.StringVar(self.root),
            'soat': tk.StringVar(self.root)
        }

        # Variables de error
        errores = {
            'placa': tk.StringVar(self.root),
            'valor': tk.StringVar(self.root),
            'tipo': tk.StringVar(self.root),
            'soat': tk.StringVar(self.root)
        }

        # Crear instancia de validaciones
        validador = Validaciones(variables, errores)

        # Funcion para verificar si el usuario desea salir del formulario
        def el_usuario_quiere_salir():
            if askyesno("Salir de la aplicacion", "Estas seguro que quieres cerrar la aplicacion"):
                self.root.destroy()

        # Funcion para consultar sobre un solo un registro
        def accion_consultar_boton(self, labelConsulta, consulta_id):
            """
            Ejecuta la consulta en un hilo para no bloquear la interfaz.
            Actualiza `labelConsulta` con el valor de 'numero_clase' o con un
            mensaje significativo en caso de error o no encontrado.
            """
            def worker():
                text = 'Error'
                try:
                    resultado = self.comunicacion.consultar(consulta_id)
                    if resultado and isinstance(resultado, dict):
                        numero = resultado.get('numero_clase')
                        text = str(numero) if numero is not None else 'No encontrado'
                    else:
                        text = 'No encontrado'
                except Exception as e:
                    # registrar para depuración
                    print('Error al consultar:', e)
                    text = 'Error conexión'
                # actualizar el widget desde el hilo principal
                labelConsulta.after(0, lambda: labelConsulta.config(text=text))

        # Helper para añadir un campo con su etiqueta de error justo debajo
        def add_field(row, label_text, var_key, err_key, validate_cb=None):
            lbl = tk.Label(self.root, text=label_text)
            lbl.grid(row=row, column=0, sticky="w", padx=(0,10), pady=(6,2))
            entry = tk.Entry(self.root, textvariable=variables[var_key])
            entry.grid(row=row, column=1, sticky="we", pady=(6,2))
            err_lbl = tk.Label(self.root, textvariable=errores[err_key], fg="#c1121f")
            err_lbl.grid(row=row+1, column=1, sticky="w", pady=(0,8))
            if validate_cb:
                entry.bind("<KeyRelease>", lambda e: validate_cb())
            return entry

        # Column configuration to give space to entries
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=1)

        # Título
        titulo = tk.Label(self.root, text="Formulario de Cargue de Camiones", font=(None, 12, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0,10))

        # Campos (cada campo usa 2 filas: fila de input y fila de error)
        entry_placa = add_field(1, "Placa del vehículo (AAA-123)", 'placa', 'placa', validador.val_placa_vehiculo)
        entry_valor = add_field(3, "Valor del cargue", 'valor', 'valor', validador.val_valor_cargue)
        entry_tipo = add_field(5, "Tipo de carga", 'tipo', 'tipo', validador.val_tipo_carga)
        entry_soat = add_field(7, "Vencimiento SOAT (YYYY-MM-DD)", 'soat', 'soat', validador.val_vencimiento_soat)

        # Botones
        btn_validar = tk.Button(self.root, text="Guardar", command=validador.enviar)
        btn_validar.grid(row=9, column=0, columnspan=2, sticky="we", pady=(10,6))

        btn_consultar_1 = tk.Button(self.root, text="Consultar 1", command=lambda:accion_consultar_boton)
        btn_validar.grid(row=9, column=0, columnspan=2, sticky="we", pady=(10,6))
        btn_validar = tk.Button(self.root, text="Guardar", command=validador.enviar)
        btn_validar.grid(row=9, column=0, columnspan=2, sticky="we", pady=(10,6))
        btn_limpiar = tk.Button(self.root, text="Limpiar", command=validador.limpiar_campos_texto)
        btn_limpiar.grid(row=1¿, column=0, columnspan=2, sticky="we")

        # Funcion para confirmar la salida de un usuario del Formulario
        self.root.protocol("WM_DELETE_WINDOW", el_usuario_quiere_salir)

        # Fin de la ventana
        self.root.mainloop()