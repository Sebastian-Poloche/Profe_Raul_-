"""
Interfaz gráfica principal de IHEP.

Proporciona la interfaz de usuario Tkinter para gestionar herramientas y
préstamos. Incluye tablas interactivas, formularios de entrada y búsqueda
avanzada, con sincronización automática de datos y respaldos periódicos.
"""

import os
import threading
import time
from datetime import datetime

import tkinter as tk
from tkinter import ttk, messagebox

from ..controladores import api_cliente
from ..controladores.backup_thread import iniciar_hilo_backup


class InterfazIHEP:
    """
    Interfaz gráfica principal de la aplicación IHEP.

    Gestiona la presentación de datos de herramientas y préstamos mediante
    una interfaz con pestañas (Tkinter Notebook), incluyendo operaciones CRUD
    y búsqueda avanzada. La interfaz se actualiza automáticamente con datos
    del backend en intervalos regulares.
    """

    def __init__(self, root):
        """
        Inicializar la interfaz gráfica.

        Args:
            root (tk.Tk): Ventana raíz de Tkinter.
        """
        self.root = root
        self.root.title("IHEP - Inventario de Herramientas y Préstamos")
        self.root.geometry("1200x720")
        self.root.minsize(1000, 600)

        self.root.configure(bg="#E8F4F8")

        # Cliente API para comunicación con backend
        self.api = api_cliente.APIClient()
        
        # Control del estado de la aplicación
        self.running = True
        self.selected_tool = None
        self.selected_loan = None

        # Iniciar respaldos automáticos en segundo plano
        iniciar_hilo_backup()

        # Construir interfaz y cargar datos iniciales
        self._crear_ui()
        self._cargar_datos_iniciales()
        self._iniciar_actualizaciones_automaticas()

    def _crear_ui(self):
        """
        Crear la interfaz de usuario completa.

        Construye la estructura visual incluyendo header, notebook con pestañas
        (Herramientas, Préstamos, Búsqueda) y footer con información del estado.
        También configura el tema visual del Notebook.
        """
        # Configurar tema visual del Notebook (pestañas)
        style = ttk.Style()
        style.theme_use("clam")
        # Fondo del notebook en azul claro
        style.configure("TNotebook", background="#D4EBF2")
        style.configure(
            "TNotebook.Tab",
            padding=[15, 8],
            font=("Segoe UI", 11, "bold")
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", "#0078d7"), ("active", "#B3D9E8")],
            foreground=[("selected", "white"), ("active", "black")]
        )

        # Crear encabezado de la aplicación
        header = tk.Frame(self.root, bg="#0D5A7C", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="IHEP - Inventario de Herramientas y Préstamos",
            fg="white",
            bg="#0D5A7C",
            font=("Segoe UI", 16, "bold")
        ).pack(side="left", padx=20, pady=10)

        # Panel de información en el header
        info_frame = tk.Frame(header, bg="#0D5A7C")
        info_frame.pack(side="right", padx=20)

        self.status_label = tk.Label(
            info_frame,
            text="Cargando...",
            fg="#E8F4F8",
            bg="#0D5A7C",
            font=("Segoe UI", 10)
        )
        self.status_label.pack(side="left", padx=10)

        self.backup_label = tk.Label(
            info_frame,
            text="Respaldo: --:--",
            fg="#E8F4F8",
            bg="#0D5A7C",
            font=("Segoe UI", 9)
        )
        self.backup_label.pack(side="left")

        # Crear notebook (contenedor de pestañas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=15)

        # Pestaña de Herramientas
        self.tab_herramienta = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_herramienta, text="Herramientas")
        self._crear_tab_herramientas()

        # Pestaña de Préstamos
        self.tab_prestamos = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_prestamos, text="Préstamos")
        self._crear_tab_prestamos()

        # Pestaña de Búsqueda
        self.tab_busqueda = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_busqueda, text="Búsqueda")
        self._crear_tab_busqueda()

        # Crear pie de página con información del sistema
        footer = tk.Frame(self.root, bg="#2d2d2d", height=30)
        footer.pack(fill="x")
        footer.pack_propagate(False)

        tk.Label(
            footer,
            text=" TecnoGestion S.A.S.  RFP-IHEP-2025 ",
            fg="#aaaaaa",
            bg="#2d2d2d",
            font=("Consolas", 9)
        ).pack(side="left", padx=10, pady=5)

        tk.Label(
            footer,
            text="Backend: http://127.0.0.1:8000/api/",
            fg="#66b3ff",
            bg="#2d2d2d",
            font=("Consolas", 9)
        ).pack(side="right", padx=10, pady=5)

    def _crear_tab_herramientas(self):
        """
        Crear contenido de la pestaña Herramientas.

        Construye un formulario para registrar/editar herramientas y una
        tabla que muestra el listado de todas las herramientas disponibles
        en el sistema.
        """
        # Formulario de entrada de datos
        form_herramienta = ttk.LabelFrame(
            self.tab_herramienta,
            text="Registro / Edición de Herramienta"
        )
        form_herramienta.pack(fill="x", padx=5, pady=5)

        # Definir campos del formulario
        campos_herramienta = [
            ("Código:", "codigo"),
            ("Nombre:", "nombre"),
            ("Categoría:", "categoria"),
            ("Ubicación:", "ubicacion"),
            ("Estado:", "estado")
        ]
        self.entradas_herramienta = {}

        # Crear campos de entrada
        for i, (etiqueta, clave) in enumerate(campos_herramienta):
            ttk.Label(form_herramienta, text=etiqueta).grid(
                row=i, column=0, padx=5, pady=3, sticky="e"
            )
            
            # Crear campo específico según el tipo
            if clave == "categoria":
                entrada = ttk.Combobox(
                    form_herramienta,
                    values=["Enviar", "Devolver"],
                    state="readonly",
                    width=47
                )
            elif clave == "estado":
                entrada = ttk.Combobox(
                    form_herramienta,
                    values=[
                        "Disponible",
                        "En préstamo",
                        "En mantenimiento",
                        "Inactivo"
                    ],
                    state="readonly",
                    width=47
                )
            else:
                entrada = ttk.Entry(form_herramienta, width=50)

            entrada.grid(row=i, column=1, padx=5, pady=3)
            self.entradas_herramienta[clave] = entrada

        # Botones de acción del formulario
        btns_herramienta = ttk.Frame(form_herramienta)
        btns_herramienta.grid(row=5, column=0, columnspan=2, pady=15, sticky="ew")
        ttk.Button(
            btns_herramienta,
            text="Guardar",
            command=self.guardar_herramienta,
            width=20
        ).pack(side="left", padx=10, pady=8)
        ttk.Button(
            btns_herramienta,
            text="Limpiar",
            command=self.limpiar_herramienta,
            width=20
        ).pack(side="left", padx=10, pady=8)
        ttk.Button(
            btns_herramienta,
            text="Editar Seleccionado",
            command=self.editar_herramienta,
            width=20
        ).pack(side="left", padx=10, pady=8)
        ttk.Button(
            btns_herramienta,
            text="Eliminar Seleccionado",
            command=self.eliminar_herramienta,
            width=20
        ).pack(side="left", padx=10, pady=8)

        # Tabla de herramientas
        tabla_herramienta = ttk.LabelFrame(
            self.tab_herramienta,
            text="Lista de Herramientas"
        )
        tabla_herramienta.pack(fill="both", expand=True, padx=5, pady=5)

        # Crear Treeview con columnas específicas
        self.tree_herramienta = ttk.Treeview(
            tabla_herramienta,
            columns=("id", "c", "n", "cat", "u", "e"),
            show="headings",
            height=12
        )
        
        # Configurar columnas (nombre, ancho, alineación)
        columnas_config = [
            ("id", "ID", 50),
            ("c", "Código", 100),
            ("n", "Nombre", 200),
            ("cat", "Categoría", 120),
            ("u", "Ubicación", 250),
            ("e", "Estado", 150)
        ]
        for columna, texto, ancho in columnas_config:
            self.tree_herramienta.heading(columna, text=texto)
            self.tree_herramienta.column(columna, width=ancho, anchor="w")

        self.tree_herramienta.pack(fill="both", expand=True)
        # Permitir selección de filas para editar
        self.tree_herramienta.bind("<ButtonRelease-1>", self._seleccionar_herramienta)

    def _crear_tab_prestamos(self):
        """
        Crear contenido de la pestaña Préstamos.

        Construye un formulario para registrar/editar préstamos y una tabla
        que muestra el listado de todos los préstamos registrados en el sistema,
        incluyendo datos de seguimiento y devolución.
        """
        # Formulario de entrada de datos
        form_prestamo = ttk.LabelFrame(
            self.tab_prestamos,
            text="Registro / Edición de Préstamo"
        )
        form_prestamo.pack(fill="x", padx=5, pady=5)

        # Definir campos del formulario
        campos_prestamo = [
            ("Número:", "numero"),
            ("Código Herramienta:", "herramienta_codigo"),
            ("Responsable:", "responsable"),
            ("Fecha Salida (YYYY-MM-DD):", "fecha_salida"),
            ("Fecha Esperada (YYYY-MM-DD):", "fecha_esperada"),
            ("Fecha Devolución (YYYY-MM-DD):", "fecha_devolucion")
        ]
        self.entradas_prestamo = {}

        # Crear campos de entrada para cada dato
        for i, (etiqueta, clave) in enumerate(campos_prestamo):
            ttk.Label(form_prestamo, text=etiqueta).grid(
                row=i, column=0, padx=5, pady=3, sticky="e"
            )
            entrada = ttk.Entry(form_prestamo, width=50)
            entrada.grid(row=i, column=1, padx=5, pady=3)
            self.entradas_prestamo[clave] = entrada

        # Botones de acción del formulario
        btns_prestamo = ttk.Frame(form_prestamo)
        btns_prestamo.grid(row=6, column=0, columnspan=2, pady=15, sticky="ew")
        ttk.Button(
            btns_prestamo,
            text="Guardar",
            command=self.guardar_prestamo,
            width=20
        ).pack(side="left", padx=10, pady=8)
        ttk.Button(
            btns_prestamo,
            text="Limpiar",
            command=self.limpiar_prestamo,
            width=20
        ).pack(side="left", padx=10, pady=8)
        ttk.Button(
            btns_prestamo,
            text="Registrar Devolución",
            command=self.registrar_devolucion,
            width=22
        ).pack(side="left", padx=10, pady=8)
        ttk.Button(
            btns_prestamo,
            text="Editar Seleccionado",
            command=self.editar_prestamo,
            width=20
        ).pack(side="left", padx=10, pady=8)
        ttk.Button(
            btns_prestamo,
            text="Eliminar Seleccionado",
            command=self.eliminar_prestamo,
            width=20
        ).pack(side="left", padx=10, pady=8)

        # Tabla de préstamos
        tabla_prestamo = ttk.LabelFrame(
            self.tab_prestamos,
            text="Lista de Préstamos"
        )
        tabla_prestamo.pack(fill="both", expand=True, padx=5, pady=5)

        # Crear Treeview con columnas específicas
        self.tree_prestamo = ttk.Treeview(
            tabla_prestamo,
            columns=("id", "n", "c", "r", "fs", "fe", "fd"),
            show="headings",
            height=12
        )
        
        # Configurar columnas con sus etiquetas y anchos
        columnas_config = [
            ("id", "ID", 50),
            ("n", "Número", 100),
            ("c", "Cod. Herr.", 120),
            ("r", "Responsable", 150),
            ("fs", "Salida", 120),
            ("fe", "Esperada", 120),
            ("fd", "Devolución", 120)
        ]
        for columna, texto, ancho in columnas_config:
            self.tree_prestamo.heading(columna, text=texto)
            self.tree_prestamo.column(columna, width=ancho, anchor="w")

        self.tree_prestamo.pack(fill="both", expand=True)
        # Permitir selección de filas para editar
        self.tree_prestamo.bind("<ButtonRelease-1>", self._seleccionar_prestamo)

        
        
    def _crear_tab_busqueda(self):
        """
        Crear contenido de la pestaña Búsqueda.

        Proporciona filtros avanzados para buscar herramientas o préstamos
        por diferentes criterios. Los resultados se muestran en una tabla
        interactiva con scrollbar vertical.
        """
        # Frame para filtros de búsqueda
        filtros_frame = ttk.LabelFrame(
            self.tab_busqueda,
            text="Filtros de Búsqueda"
        )
        filtros_frame.pack(fill="x", padx=5, pady=5)

        # Selector del tipo de búsqueda (Herramientas o Préstamos)
        ttk.Label(filtros_frame, text="Buscar en:").grid(
            row=0, column=0, padx=5, pady=5, sticky="e"
        )
        self.tipo_busqueda = tk.StringVar(value="Herramientas")
        tipo_combo = ttk.Combobox(
            filtros_frame,
            textvariable=self.tipo_busqueda,
            values=["Herramientas", "Préstamos"],
            state="readonly",
            width=30
        )
        tipo_combo.grid(row=0, column=1, padx=5, pady=5)
        # Actualizar campos disponibles al cambiar tipo
        tipo_combo.bind("<<ComboboxSelected>>", lambda e: self._actualizar_campos_busqueda())

        # Selector del campo de búsqueda
        ttk.Label(filtros_frame, text="Campo:").grid(
            row=0, column=2, padx=5, pady=5, sticky="e"
        )
        self.campo_busqueda = tk.StringVar(value="codigo")
        self.campo_combo = ttk.Combobox(
            filtros_frame,
            textvariable=self.campo_busqueda,
            values=["codigo", "nombre"],
            state="readonly",
            width=20
        )
        self.campo_combo.grid(row=0, column=3, padx=5, pady=5)

        # Campo de entrada del término de búsqueda
        ttk.Label(filtros_frame, text="Término:").grid(
            row=1, column=0, padx=5, pady=5, sticky="e"
        )
        self.termino_busqueda = tk.StringVar()
        ttk.Entry(
            filtros_frame,
            textvariable=self.termino_busqueda,
            width=35
        ).grid(row=1, column=1, padx=5, pady=5)

        # Botones para ejecutar búsqueda y limpiar
        btns_busqueda = ttk.Frame(filtros_frame)
        btns_busqueda.grid(row=1, column=2, columnspan=2, padx=5, pady=5)
        ttk.Button(
            btns_busqueda,
            text="Buscar",
            command=self._ejecutar_busqueda,
            width=12
        ).pack(side="left", padx=4, pady=5)
        ttk.Button(
            btns_busqueda,
            text="Limpiar",
            command=self._limpiar_busqueda,
            width=12
        ).pack(side="left", padx=4, pady=5)

        # Frame para mostrar resultados
        resultados_frame = ttk.LabelFrame(
            self.tab_busqueda,
            text="Resultados de la Búsqueda"
        )
        resultados_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Tabla de resultados
        self.tree_busqueda = ttk.Treeview(resultados_frame, show="headings", height=15)
        self.tree_busqueda.pack(fill="both", expand=True)

        # Scrollbar vertical para tabla de resultados
        scrollbar = ttk.Scrollbar(
            resultados_frame,
            orient="vertical",
            command=self.tree_busqueda.yview
        )
        scrollbar.pack(side="right", fill="y")
        self.tree_busqueda.config(yscroll=scrollbar.set)
        
    def _actualizar_campos_busqueda(self):
        """
        Actualizar campos disponibles de búsqueda según el tipo seleccionado.

        Cuando el usuario cambia entre Herramientas y Préstamos, actualiza
        dinámicamente los campos disponibles para filtro y resetea la selección
        al campo por defecto.
        """
        tipo = self.tipo_busqueda.get()
        if tipo == "Herramientas":
            # Campos disponibles para herramientas
            self.campo_combo.config(
                values=["codigo", "nombre", "categoria", "ubicacion"]
            )
            self.campo_busqueda.set("codigo")
        else:  # Préstamos
            # Campos disponibles para préstamos
            self.campo_combo.config(
                values=["numero", "responsable", "herramienta_codigo"]
            )
            self.campo_busqueda.set("numero")

    def _ejecutar_busqueda(self):
        """
        Ejecutar búsqueda de herramientas o préstamos.

        Obtiene los parámetros de búsqueda del formulario y lanza una búsqueda
        en thread separado para no bloquear la UI mientras se comunica con la API.
        """
        tipo = self.tipo_busqueda.get()
        campo = self.campo_busqueda.get()
        termino = self.termino_busqueda.get().lower()

        if not termino:
            messagebox.showwarning(
                "Advertencia",
                "Ingrese un término de búsqueda"
            )
            return

        # Limpiar resultados anteriores
        for item in self.tree_busqueda.get_children():
            self.tree_busqueda.delete(item)

        # Ejecutar búsqueda en thread separado
        threading.Thread(
            target=self._buscar_en_api,
            args=(tipo, campo, termino),
            daemon=True
        ).start()

    def _buscar_en_api(self, tipo, campo, termino):
        """
        Buscar en la API y mostrar resultados.

        Args:
            tipo (str): Tipo de búsqueda ("Herramientas" o "Préstamos").
            campo (str): Campo en el cual buscar.
            termino (str): Término a buscar (convertido a minúsculas).

        Realiza la búsqueda contra la API, filtra resultados localmente
        y actualiza la tabla de resultados. En caso de no encontrar
        coincidencias, muestra un mensaje informativo.
        """
        try:
            if tipo == "Herramientas":
                # Obtener todas las herramientas de la API
                datos, error = self.api.get("herramientas/")
                if error or not datos:
                    messagebox.showerror("Error", "No se pudo obtener datos")
                    return

                # Configurar columnas de la tabla
                self.tree_busqueda.config(
                    columns=("id", "c", "n", "cat", "u", "e")
                )
                # Configurar encabezados y anchos de columnas
                columnas_busqueda = [
                    ("id", "ID", 50),
                    ("c", "Código", 100),
                    ("n", "Nombre", 200),
                    ("cat", "Categoría", 120),
                    ("u", "Ubicación", 250),
                    ("e", "Estado", 150)
                ]
                for columna, texto, ancho in columnas_busqueda:
                    self.tree_busqueda.heading(columna, text=texto)
                    self.tree_busqueda.column(columna, width=ancho, anchor="w")

                # Filtrar y mostrar resultados que coinciden con el término
                for herramienta in datos:
                    valor = str(herramienta.get(campo, "")).lower()
                    if termino in valor:
                        self.tree_busqueda.insert("", "end", values=(
                            herramienta.get("id", ""),
                            herramienta.get("codigo", ""),
                            herramienta.get("nombre", ""),
                            herramienta.get("categoria", ""),
                            herramienta.get("ubicacion", ""),
                            herramienta.get("estado", "")
                        ))

                if not self.tree_busqueda.get_children():
                    messagebox.showinfo(
                        "Búsqueda",
                        "No se encontraron resultados"
                    )
            else:  # Préstamos
                # Obtener todos los préstamos de la API
                datos, error = self.api.get("prestamos/")
                if error or not datos:
                    messagebox.showerror("Error", "No se pudo obtener datos")
                    return

                # Configurar columnas de la tabla
                self.tree_busqueda.config(
                    columns=("id", "n", "c", "r", "fs", "fe", "fd")
                )
                # Configurar encabezados y anchos de columnas
                columnas_busqueda = [
                    ("id", "ID", 50),
                    ("n", "Número", 100),
                    ("c", "Cod. Herr.", 120),
                    ("r", "Responsable", 150),
                    ("fs", "Salida", 120),
                    ("fe", "Esperada", 120),
                    ("fd", "Devolución", 120)
                ]
                for columna, texto, ancho in columnas_busqueda:
                    self.tree_busqueda.heading(columna, text=texto)
                    self.tree_busqueda.column(columna, width=ancho, anchor="w")

                # Filtrar y mostrar resultados que coinciden con el término
                for prestamo in datos:
                    valor = str(prestamo.get(campo, "")).lower()
                    if termino in valor:
                        self.tree_busqueda.insert("", "end", values=(
                            prestamo.get("id", ""),
                            prestamo.get("numero", ""),
                            prestamo.get("herramienta_codigo", ""),
                            prestamo.get("responsable", ""),
                            prestamo.get("fecha_salida", ""),
                            prestamo.get("fecha_esperada", ""),
                            prestamo.get("fecha_devolucion", "")
                        ))

                if not self.tree_busqueda.get_children():
                    messagebox.showinfo(
                        "Búsqueda",
                        "No se encontraron resultados"
                    )
        except Exception as error:
            messagebox.showerror("Error", f"Error en búsqueda: {str(error)}")

    def _limpiar_busqueda(self):
        """
        Limpiar campos de búsqueda y resultados.

        Resetea el término de búsqueda y elimina todos los resultados
        mostrados en la tabla.
        """
        self.termino_busqueda.set("")
        for item in self.tree_busqueda.get_children():
            self.tree_busqueda.delete(item)
        
    def _cargar_datos_iniciales(self):
        """
        Cargar datos iniciales desde la API al arrancar.

        Lanza threads separados para cargar herramientas y préstamos
        sin bloquear la interfaz gráfica.
        """
        threading.Thread(target=self._cargar_herramientas, daemon=True).start()
        threading.Thread(target=self._cargar_prestamos, daemon=True).start()

    def _cargar_herramientas(self):
        """
        Cargar lista de herramientas desde la API.

        Obtiene todas las herramientas del backend y las muestra en la tabla.
        Actualiza el indicador de estado con el resultado de la operación.
        """
        try:
            datos, error = self.api.get("herramientas/")
            if error:
                self.status_label.config(
                    text=f"Error: {error}",
                    fg="#ff6b6b"
                )
                return

            # Limpiar tabla antes de cargar nuevos datos
            for item in self.tree_herramienta.get_children():
                self.tree_herramienta.delete(item)

            # Insertar datos obtenidos en la tabla
            if datos:
                for herramienta in datos:
                    self.tree_herramienta.insert("", "end", values=(
                        herramienta.get("id", ""),
                        herramienta.get("codigo", ""),
                        herramienta.get("nombre", ""),
                        herramienta.get("categoria", ""),
                        herramienta.get("ubicacion", ""),
                        herramienta.get("estado", "")
                    ))

            # Indicar conexión exitosa
            self.status_label.config(text="Conectado ✓", fg="#90ee90")
        except Exception as error:
            self.status_label.config(
                text=f"Error: {str(error)}",
                fg="#ff6b6b"
            )

    def _cargar_prestamos(self):
        """
        Cargar lista de préstamos desde la API.

        Obtiene todos los préstamos del backend y los muestra en la tabla.
        """
        try:
            datos, error = self.api.get("prestamos/")
            if error:
                return

            # Limpiar tabla antes de cargar nuevos datos
            for item in self.tree_prestamo.get_children():
                self.tree_prestamo.delete(item)

            # Insertar datos obtenidos en la tabla
            if datos:
                for prestamo in datos:
                    self.tree_prestamo.insert("", "end", values=(
                        prestamo.get("id", ""),
                        prestamo.get("numero", ""),
                        prestamo.get("herramienta_codigo", ""),
                        prestamo.get("responsable", ""),
                        prestamo.get("fecha_salida", ""),
                        prestamo.get("fecha_esperada", ""),
                        prestamo.get("fecha_devolucion", "")
                    ))
        except Exception as error:
            pass

    def _seleccionar_herramienta(self, event):
        """
        Seleccionar herramienta de la tabla para editar.

        Args:
            event: Evento de clic del mouse en la tabla.

        Carga los datos de la herramienta seleccionada en el formulario
        para permitir su edición.
        """
        selection = self.tree_herramienta.selection()
        if selection:
            item = self.tree_herramienta.item(selection[0])
            values = item['values']
            # Guardar ID para identificar registro al actualizar
            self.selected_tool = values[0]

            # Cargar datos en campos del formulario
            self.entradas_herramienta["codigo"].delete(0, tk.END)
            self.entradas_herramienta["codigo"].insert(0, values[1])
            self.entradas_herramienta["nombre"].delete(0, tk.END)
            self.entradas_herramienta["nombre"].insert(0, values[2])
            self.entradas_herramienta["categoria"].set(values[3])
            self.entradas_herramienta["ubicacion"].delete(0, tk.END)
            self.entradas_herramienta["ubicacion"].insert(0, values[4])
            self.entradas_herramienta["estado"].set(values[5])

    def _seleccionar_prestamo(self, event):
        """
        Seleccionar préstamo de la tabla para editar.

        Args:
            event: Evento de clic del mouse en la tabla.

        Carga los datos del préstamo seleccionado en el formulario
        para permitir su edición o registrar devolución.
        """
        selection = self.tree_prestamo.selection()
        if selection:
            item = self.tree_prestamo.item(selection[0])
            values = item['values']
            # Guardar ID para identificar registro al actualizar
            self.selected_loan = values[0]

            # Cargar datos en campos del formulario
            self.entradas_prestamo["numero"].delete(0, tk.END)
            self.entradas_prestamo["numero"].insert(0, values[1])
            self.entradas_prestamo["herramienta_codigo"].delete(0, tk.END)
            self.entradas_prestamo["herramienta_codigo"].insert(0, values[2])
            self.entradas_prestamo["responsable"].delete(0, tk.END)
            self.entradas_prestamo["responsable"].insert(0, values[3])
            self.entradas_prestamo["fecha_salida"].delete(0, tk.END)
            self.entradas_prestamo["fecha_salida"].insert(0, values[4])
            self.entradas_prestamo["fecha_esperada"].delete(0, tk.END)
            self.entradas_prestamo["fecha_esperada"].insert(0, values[5])
            self.entradas_prestamo["fecha_devolucion"].delete(0, tk.END)
            self.entradas_prestamo["fecha_devolucion"].insert(0, values[6])
            
    def guardar_herramienta(self):
        """
        Guardar o actualizar herramienta.

        Valida los datos ingresados, verifica que los campos obligatorios
        estén completos y luego crea o actualiza el registro en la API.
        """
        try:
            # Recopilar datos del formulario
            datos = {
                "codigo": self.entradas_herramienta["codigo"].get(),
                "nombre": self.entradas_herramienta["nombre"].get(),
                "categoria": self.entradas_herramienta["categoria"].get(),
                "ubicacion": self.entradas_herramienta["ubicacion"].get(),
                "estado": self.entradas_herramienta["estado"].get()
            }

            # Validar campos obligatorios
            if not datos["codigo"] or not datos["nombre"]:
                messagebox.showerror(
                    "Error",
                    "Código y nombre son obligatorios"
                )
                return

            # Actualizar si hay herramienta seleccionada, crear si es nueva
            if self.selected_tool:
                resultado, error = self.api.put(
                    f"herramientas/{self.selected_tool}/",
                    datos
                )
                if error:
                    messagebox.showerror(
                        "Error",
                        f"No se pudo actualizar: {error}"
                    )
                else:
                    messagebox.showinfo(
                        "Éxito",
                        "Herramienta actualizada correctamente"
                    )
                    self.limpiar_herramienta()
                    self._cargar_herramientas()
            else:
                resultado, error = self.api.post("herramientas/", datos)
                if error:
                    messagebox.showerror(
                        "Error",
                        f"No se pudo crear: {error}"
                    )
                else:
                    messagebox.showinfo(
                        "Éxito",
                        "Herramienta creada correctamente"
                    )
                    self.limpiar_herramienta()
                    self._cargar_herramientas()
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def editar_herramienta(self):
        """
        Validar que haya herramienta seleccionada para editar.

        Este método es un placeholder. La edición real ocurre al seleccionar
        una herramienta de la tabla y modificar los campos del formulario.
        """
        if not self.selected_tool:
            messagebox.showerror(
                "Error",
                "Seleccione una herramienta primero"
            )

    def eliminar_herramienta(self):
        """
        Eliminar herramienta seleccionada.

        Solicita confirmación antes de eliminar el registro de la herramienta
        de la API.
        """
        if not self.selected_tool:
            messagebox.showerror(
                "Error",
                "Seleccione una herramienta para eliminar"
            )
            return

        if messagebox.askyesno("Confirmar", "¿Desea eliminar esta herramienta?"):
            resultado, error = self.api.delete(
                f"herramientas/{self.selected_tool}/"
            )
            if error:
                messagebox.showerror(
                    "Error",
                    f"No se pudo eliminar: {error}"
                )
            else:
                messagebox.showinfo(
                    "Éxito",
                    "Herramienta eliminada correctamente"
                )
                self.limpiar_herramienta()
                self._cargar_herramientas()

    def limpiar_herramienta(self):
        """
        Limpiar formulario de herramientas.

        Resetea todos los campos del formulario a su estado inicial
        y deselecciona la herramienta actual.
        """
        self.selected_tool = None
        for entrada in self.entradas_herramienta.values():
            if isinstance(entrada, ttk.Combobox):
                entrada.set("")
            else:
                entrada.delete(0, tk.END)
                
    def guardar_prestamo(self):
        """
        Guardar o actualizar préstamo.

        Valida todos los datos ingresados incluyendo formatos de fecha,
        y verifica que la herramienta exista antes de crear/actualizar el
        registro en la API.
        """
        try:
            # Extraer y limpiar datos del formulario
            numero = self.entradas_prestamo["numero"].get().strip()
            herramienta_codigo = (
                self.entradas_prestamo["herramienta_codigo"].get().strip()
            )
            responsable = self.entradas_prestamo["responsable"].get().strip()
            fecha_salida = self.entradas_prestamo["fecha_salida"].get().strip()
            fecha_esperada = (
                self.entradas_prestamo["fecha_esperada"].get().strip()
            )
            fecha_devolucion = (
                self.entradas_prestamo["fecha_devolucion"].get().strip()
            )

            # Validar campos obligatorios
            if not numero or not herramienta_codigo or not responsable:
                messagebox.showerror(
                    "Error",
                    "Número, herramienta y responsable son obligatorios"
                )
                return

            if not fecha_salida:
                messagebox.showerror("Error", "La fecha de salida es obligatoria")
                return

            # Validar formato de fechas (YYYY-MM-DD)
            from datetime import datetime
            for campo, valor in [
                ("Salida", fecha_salida),
                ("Esperada", fecha_esperada)
            ]:
                if valor:
                    try:
                        datetime.strptime(valor, "%Y-%m-%d")
                    except ValueError:
                        messagebox.showerror(
                            "Error",
                            f"Fecha {campo} debe estar en formato YYYY-MM-DD"
                        )
                        return

            # Validar que la herramienta existe en la BD
            herramientas, _ = self.api.get("herramientas/")
            herramienta_existe = any(
                h.get("codigo") == herramienta_codigo
                for h in (herramientas or [])
            )
            if not herramienta_existe:
                messagebox.showerror(
                    "Error",
                    f"Herramienta con código '{herramienta_codigo}' no existe"
                )
                return

            # Construir payload para la API
            datos = {
                "numero": numero,
                "herramienta_codigo": herramienta_codigo,
                "responsable": responsable,
                "fecha_salida": fecha_salida if fecha_salida else None,
                "fecha_esperada": fecha_esperada if fecha_esperada else None,
                "fecha_devolucion": fecha_devolucion if fecha_devolucion else None,
            }

            # Actualizar si hay préstamo seleccionado, crear si es nuevo
            if self.selected_loan:
                resultado, error = self.api.put(
                    f"prestamos/{self.selected_loan}/",
                    datos
                )
                if error:
                    messagebox.showerror(
                        "Error",
                        f"No se pudo actualizar: {error}"
                    )
                else:
                    messagebox.showinfo(
                        "Éxito",
                        "Préstamo actualizado correctamente"
                    )
                    self.limpiar_prestamo()
                    self._cargar_prestamos()
            else:
                resultado, error = self.api.post("prestamos/", datos)
                if error:
                    messagebox.showerror(
                        "Error",
                        f"No se pudo crear: {error}"
                    )
                else:
                    messagebox.showinfo(
                        "Éxito",
                        "Préstamo creado correctamente"
                    )
                    self.limpiar_prestamo()
                    self._cargar_prestamos()
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def editar_prestamo(self):
        """
        Validar que haya préstamo seleccionado para editar.

        Este método es un placeholder. La edición real ocurre al seleccionar
        un préstamo de la tabla y modificar los campos del formulario.
        """
        if not self.selected_loan:
            messagebox.showerror("Error", "Seleccione un préstamo primero")

    def eliminar_prestamo(self):
        """
        Eliminar préstamo seleccionado.

        Solicita confirmación antes de eliminar el registro del préstamo
        de la API.
        """
        if not self.selected_loan:
            messagebox.showerror(
                "Error",
                "Seleccione un préstamo para eliminar"
            )
            return

        if messagebox.askyesno("Confirmar", "¿Desea eliminar este préstamo?"):
            resultado, error = self.api.delete(
                f"prestamos/{self.selected_loan}/"
            )
            if error:
                messagebox.showerror(
                    "Error",
                    f"No se pudo eliminar: {error}"
                )
            else:
                messagebox.showinfo(
                    "Éxito",
                    "Préstamo eliminado correctamente"
                )
                self.limpiar_prestamo()
                self._cargar_prestamos()

    def registrar_devolucion(self):
        """
        Registrar fecha de devolución de un préstamo.

        Actualiza el préstamo seleccionado con la fecha de devolución
        ingresada, marcando efectivamente el préstamo como completado.
        """
        if not self.selected_loan:
            messagebox.showerror(
                "Error",
                "Seleccione un préstamo para registrar devolución"
            )
            return

        fecha_dev = self.entradas_prestamo["fecha_devolucion"].get()
        if not fecha_dev:
            messagebox.showerror("Error", "Ingrese fecha de devolución")
            return

        datos = {"fecha_devolucion": fecha_dev}
        resultado, error = self.api.put(
            f"prestamos/{self.selected_loan}/",
            datos
        )
        if error:
            messagebox.showerror(
                "Error",
                f"No se pudo registrar: {error}"
            )
        else:
            messagebox.showinfo(
                "Éxito",
                "Devolución registrada correctamente"
            )
            self._cargar_prestamos()

    def limpiar_prestamo(self):
        """
        Limpiar formulario de préstamos.

        Resetea todos los campos del formulario a su estado inicial
        y deselecciona el préstamo actual.
        """
        self.selected_loan = None
        for entrada in self.entradas_prestamo.values():
            entrada.delete(0, tk.END)
            
    def _iniciar_actualizaciones_automaticas(self):
        """
        Iniciar thread de actualizaciones automáticas periódicas.

        Carga herramientas y préstamos cada 10 segundos. Actualiza el
        contador regresivo que muestra el tiempo hasta el siguiente respaldo.
        """
        def loop_actualizacion():
            # Obtener intervalo de respaldo desde configuración (default 300 seg)
            intervalo_respaldo = int(os.getenv("INTERVALO_BACKUP_SEG", "300"))
            inicio = time.time()

            while self.running:
                # Cargar datos actualizados de la API
                self._cargar_herramientas()
                self._cargar_prestamos()

                # Calcular tiempo restante para próximo respaldo
                transcurrido = int(time.time() - inicio) % intervalo_respaldo
                restante = intervalo_respaldo - transcurrido
                minutos, segundos = divmod(restante, 60)

                # Actualizar etiqueta con contador regresivo
                self.backup_label.config(
                    text=f"Respaldo: {minutos:02d}:{segundos:02d}"
                )

                # Esperar 10 segundos antes de siguiente iteración
                time.sleep(10)

        threading.Thread(target=loop_actualizacion, daemon=True).start()