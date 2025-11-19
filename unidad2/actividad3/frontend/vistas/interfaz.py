import tkinter as tk
import tkinter.simpledialog as simpledialog
from tkinter.messagebox import askyesno, showinfo, showerror
from controladores.comunicacion import Comunicacion
from modelos.cargue import Cargue
from controladores.validaciones import Validaciones
from vistas.tabla import Tabla
import threading

class Interfaz():

    def __init__(self):
        self.root = tk.Tk()
        self.comunicacion = Comunicacion(self.root)
        self.variables_activas = None
        self.validador_activo = None
        self.tabla_cargues = None
        self.id_cargue_actual = None  # Para guardar el ID del cargue seleccionado

    def mostrar_interfaz(self):
        camiones = Cargue(self.root)
        
        # Creación de la ventana principal
        self.root.title("Gestión de Cargue de Camiones")
        self.root.geometry("1000x700")
        self.root.resizable(0, 0)
        self.root.config(padx=5, pady=10)
        
        # Crear un frame para el formulario (lado izquierdo)
        frame_formulario = tk.Frame(self.root)
        frame_formulario.grid(row=0, column=0, columnspan=1, sticky="nsew", padx=(0, 10))
        
        # Crear un frame para la tabla (lado derecho)
        frame_tabla = tk.Frame(self.root)
        frame_tabla.grid(row=0, column=1, columnspan=1, sticky="nsew")
        
        # Configurar pesos de columnas
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=1)
        
        # ==================== SECCIÓN DEL FORMULARIO ====================
        
        # Variables de entrada
        variables = {
            'placa': tk.StringVar(frame_formulario),
            'valor': tk.StringVar(frame_formulario),
            'tipo': tk.StringVar(frame_formulario),
            'soat': tk.StringVar(frame_formulario)
        }
        
        # Variables de error
        errores = {
            'placa': tk.StringVar(frame_formulario),
            'valor': tk.StringVar(frame_formulario),
            'tipo': tk.StringVar(frame_formulario),
            'soat': tk.StringVar(frame_formulario)
        }
        
        self.variables_activas = variables
        
        # Crear instancia de validaciones
        validador = Validaciones(variables, errores)
        self.validador_activo = validador
        
        # Función para verificar si el usuario desea salir
        def el_usuario_quiere_salir():
            if askyesno("Salir", "¿Estás seguro de que quieres cerrar la aplicación?"):
                self.root.destroy()
        
        # Función para refrescar la tabla con datos de la API
        def accion_refrescar_tabla(callback=None):
            """
            Refrescar la tabla desde la API en un hilo separado.
            callback: función opcional para ejecutar después de refrescar
            """
            def cargar_datos():
                try:
                    datos = self.comunicacion.consultar_todo()
                    if isinstance(datos, list) and len(datos) > 0:
                        # Convertir datos de la API a tuplas para la tabla
                        filas = []
                        for cargue in datos:
                            fila = (
                                cargue.get('id'),
                                cargue.get('Placa_del_vehiculo'),
                                cargue.get('Tipo_de_carga'),
                                f"${cargue.get('Valor_del_cargue')}",
                                cargue.get('Vencimiento_de_soat')
                            )
                            filas.append(fila)
                        self.tabla_cargues.refrescar(filas)
                    else:
                        self.tabla_cargues.refrescar([])
                except Exception as e:
                    showerror("Error", f"Error al cargar datos: {str(e)}")
                finally:
                    # Ejecutar callback si se proporciona
                    if callback:
                        callback()
            
            # Ejecutar en un hilo separado para no bloquear la interfaz
            hilo = threading.Thread(target=cargar_datos, daemon=True)
            hilo.start()
        
        # Función para guardar un cargue
        def accion_guardar():
            if validador.enviar():
                respuesta = self.comunicacion.guardar(
                    variables['placa'].get(),
                    variables['valor'].get(),
                    variables['tipo'].get(),
                    variables['soat'].get()
                )
                if respuesta and respuesta.status_code == 201:
                    validador.limpiar_campos_texto()
                    showinfo("Éxito", "¡Cargue guardado correctamente!")
                    # Refrescar tabla después de guardar exitosamente
                    accion_refrescar_tabla()
                else:
                    showerror("Error", "No se pudo guardar el cargue")

        
        # Función para consultar un cargue por ID
        def accion_consultar_id():
            consulta_id = simpledialog.askinteger("Consultar", "Ingresa el ID del cargue:", parent=self.root)
            if consulta_id is not None:
                resultado = self.comunicacion.consultar(consulta_id)
                if resultado:
                    info = f"ID: {resultado.get('id')}\n"
                    info += f"Placa: {resultado.get('Placa_del_vehiculo')}\n"
                    info += f"Valor: ${resultado.get('Valor_del_cargue')}\n"
                    info += f"Tipo: {resultado.get('Tipo_de_carga')}\n"
                    info += f"Vencimiento SOAT: {resultado.get('Vencimiento_de_soat')}\n"
                    showinfo("Cargue Encontrado", info)
                else:
                    showinfo("No Encontrado", "El cargue no existe")
        
        # Función para eliminar un cargue
        def accion_eliminar():
            eliminar_id = simpledialog.askinteger("Eliminar", "Ingresa el ID del cargue a eliminar:", parent=self.root)
            if eliminar_id is not None:
                if askyesno("Confirmar", f"¿Deseas eliminar el cargue con ID {eliminar_id}?"):
                    status = self.comunicacion.eliminar(eliminar_id)
                    if status == 204:
                        showinfo("Éxito", "¡Cargue eliminado correctamente!")
                        accion_refrescar_tabla()
        
        # Helper para añadir un campo con su etiqueta de error
        def add_field(row, label_text, var_key, err_key, validate_cb=None):
            lbl = tk.Label(frame_formulario, text=label_text, font=(None, 9))
            lbl.grid(row=row, column=0, sticky="w", padx=(0, 10), pady=(6, 2))
            entry = tk.Entry(frame_formulario, textvariable=variables[var_key], width=20)
            entry.grid(row=row, column=1, sticky="we", pady=(6, 2))
            err_lbl = tk.Label(frame_formulario, textvariable=errores[err_key], fg="#c1121f", font=(None, 8))
            err_lbl.grid(row=row + 1, column=0, columnspan=2, sticky="w", pady=(0, 8))
            if validate_cb:
                entry.bind("<KeyRelease>", lambda e: validate_cb())
            return entry
        
        # Configuración de columnas del frame formulario
        frame_formulario.grid_columnconfigure(0, weight=0)
        frame_formulario.grid_columnconfigure(1, weight=0)
        
        # Título del formulario
        titulo = tk.Label(frame_formulario, text="Formulario de Cargue", font=(None, 11, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))
        
        # Campos del formulario
        add_field(1, "Placa (AAA-123)", 'placa', 'placa', validador.val_placa_vehiculo)
        add_field(3, "Valor ($)", 'valor', 'valor', validador.val_valor_cargue)
        add_field(5, "Tipo de Carga", 'tipo', 'tipo', validador.val_tipo_carga)
        add_field(7, "Vencimiento SOAT\n(YYYY-MM-DD)", 'soat', 'soat', validador.val_vencimiento_soat)
        
        # Botones del formulario
        btn_guardar = tk.Button(frame_formulario, text="Guardar", command=accion_guardar, bg="#4CAF50", fg="white", width=15)
        btn_guardar.grid(row=9, column=0, columnspan=2, sticky="we", pady=(15, 5))
        
        btn_consultar = tk.Button(frame_formulario, text="Consultar por ID", command=accion_consultar_id, bg="#2196F3", fg="white", width=15)
        btn_consultar.grid(row=10, column=0, columnspan=2, sticky="we", pady=5)
        
        btn_eliminar = tk.Button(frame_formulario, text="Eliminar", command=accion_eliminar, bg="#f44336", fg="white", width=15)
        btn_eliminar.grid(row=11, column=0, columnspan=2, sticky="we", pady=5)
        
        btn_limpiar = tk.Button(frame_formulario, text="Limpiar", command=validador.limpiar_campos_texto, bg="#FF9800", fg="white", width=15)
        btn_limpiar.grid(row=12, column=0, columnspan=2, sticky="we", pady=5)
        
        btn_refrescar = tk.Button(frame_formulario, text="Refrescar Tabla", command=accion_refrescar_tabla, bg="#9C27B0", fg="white", width=15)
        btn_refrescar.grid(row=13, column=0, columnspan=2, sticky="we", pady=(15, 5))
        
        # ==================== SECCIÓN DE LA TABLA ====================
        
        # Título de la tabla
        titulo_tabla = tk.Label(frame_tabla, text="Cargues Almacenados", font=(None, 11, "bold"))
        titulo_tabla.pack(fill="x", pady=(0, 10))
        
        # Crear un frame SEPARADO para la tabla (para usar grid inside)
        frame_tabla_contenedor = tk.Frame(frame_tabla)
        frame_tabla_contenedor.pack(fill='both', expand=True, padx=0, pady=0)
        frame_tabla_contenedor.grid_rowconfigure(0, weight=1)
        frame_tabla_contenedor.grid_columnconfigure(0, weight=1)
        
        # Definir columnas y títulos
        columnas = ['id', 'placa', 'tipo', 'valor', 'soat']
        titulos = ['Identificador', 'Placa del Vehículo', 'Tipo de Carga', 'Valor del Cargue', 'Vencimiento del SOAT']
        anchos = [80, 120, 110, 100, 120]
        
        # Crear la tabla (vacía inicialmente) - dentro del frame contenedor
        self.tabla_cargues = Tabla(frame_tabla_contenedor, titulos, columnas, [], anchos)
        self.tabla_cargues.grid(0, 0, columnspan=1, rowspan=1, sticky='nsew', padx=0, pady=0)
        
        # Función para manejar el clic en una fila de la tabla
        def al_hacer_clic_en_fila(fila):
            """
            Cuando se hace clic en una fila de la tabla, carga sus datos en el formulario.
            fila es una tupla: (id, placa, tipo, valor, soat)
            """
            if fila and len(fila) >= 5:
                # Limpiar campos primero
                validador.limpiar_campos_texto()
                
                # Cargar datos en los campos
                # Nota: el valor tiene formato "$xxxx.xx", hay que remover el $
                valor_formateado = str(fila[3]).replace('$', '').strip()
                
                variables['placa'].set(str(fila[1]))  # placa
                variables['valor'].set(valor_formateado)  # valor
                variables['tipo'].set(str(fila[2]))  # tipo
                variables['soat'].set(str(fila[4]))  # soat
                
                # Guardar el ID actual para editar después
                self.id_cargue_actual = fila[0]
        
        # Vincular el evento de clic en la tabla
        self.tabla_cargues.vincular_clic(al_hacer_clic_en_fila)
        
        # Cargar datos inicialmente
        accion_refrescar_tabla()
        
        # Protocolo para cerrar ventana
        self.root.protocol("WM_DELETE_WINDOW", el_usuario_quiere_salir)
        
        # Iniciar la interfaz
        self.root.mainloop()