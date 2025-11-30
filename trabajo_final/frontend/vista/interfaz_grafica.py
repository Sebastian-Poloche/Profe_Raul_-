import tkinter as tk
from tkinter import ttk, messagebox
import os
import threading
import time
from datetime import datetime
from ..controladores import api_cliente
from ..controladores.backup_thread import iniciar_hilo_backup


class InterfazIHEP:
    def __init__(self, root):
        self.root = root
        self.root.title("IHEP - Inventario de Herramientas y Préstamos")
        self.root.geometry("1200x720")
        self.root.minsize(1000, 600)
        self.root.configure(bg="#C9E5F2")
        
        self.api = api_cliente.APIClient()
        self.running = True
        self.selected_tool = None
        self.selected_loan = None
        
        
        iniciar_hilo_backup()
        
        self._crear_ui()
        self._cargar_datos_iniciales()
        self._iniciar_actualizaciones_automaticas()
        
    def _crear_ui(self):
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background="#98D0EB")
        style.configure("TNotebook.Tab", padding=[15, 8], font=("Segoe UI", 11, "bold"))
        style.map("TNotebook.Tab",
                  background=[("selected", "#0078d7"), ("active", "#e1f5fe")],
                  foreground=[("selected", "white"), ("active", "black")])
        
        
        header = tk.Frame(self.root, bg="#0078d7", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="IHEP - Inventario de Herramientas y Préstamos",
                fg="white", bg="#0078d7", font=("Segoe UI", 16, "bold")).pack(side="left", padx=20, pady=10)
        
        info_frame = tk.Frame(header, bg="#0078d7")
        info_frame.pack(side="right", padx=20)
        
        self.status_label = tk.Label(info_frame, text="Cargando...", fg="#ffff99", bg="#0078d7",
                font=("Segoe UI", 10))
        self.status_label.pack(side="left", padx=10)
        
        self.backup_label = tk.Label(info_frame, text="Respaldo: --:--",
                fg="#ffff99", bg="#0078d7", font=("Segoe UI", 9))
        self.backup_label.pack(side="left")
        
    
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Tab Herramientas
        self.tab_herramienta = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_herramienta, text="Herramientas")
        self._crear_tab_herramientas()
        
        self.tab_prestamos = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_prestamos, text="Préstamos")
        self._crear_tab_prestamos()
        
        # Tab Búsqueda
        self.tab_busqueda = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_busqueda, text="Búsqueda")
        self._crear_tab_busqueda()
        
        footer = tk.Frame(self.root, bg="#2d2d2d", height=30)
        footer.pack(fill="x")
        footer.pack_propagate(False)
        
        tk.Label(footer, text="© 2025 TecnoGestion S.A.S. | RFP-IHEP-2025 | v1.0",
                 fg="#aaaaaa", bg="#2d2d2d", font=("Consolas", 9)).pack(side="left", padx=10, pady=5)
        
        tk.Label(footer, text="Backend: http://127.0.0.1:8000/api/",
                 fg="#66b3ff", bg="#2d2d2d", font=("Consolas", 9)).pack(side="right", padx=10, pady=5)
        
    def _crear_tab_herramientas(self):

        form_herramienta = ttk.LabelFrame(self.tab_herramienta, text="Registro / Edición de Herramienta")
        form_herramienta.pack(fill="x", padx=5, pady=5)
        
        campos_herramienta = [("Código:", "codigo"), ("Nombre:", "nombre"), 
                             ("Categoría:", "categoria"), ("Ubicación:", "ubicacion"), 
                             ("Estado:", "estado")]
        self.entradas_herramienta = {}
        
        for i, (label, key) in enumerate(campos_herramienta):
            ttk.Label(form_herramienta, text=label).grid(row=i, column=0, padx=5, pady=3, sticky="e")
            if key == "categoria":
                entry = ttk.Combobox(form_herramienta, values=["Enviar", "Devolver"], state="readonly", width=47)
            elif key == "estado":
                entry = ttk.Combobox(form_herramienta, values=["Disponible", "En préstamo", "En mantenimiento", "Inactivo"], 
                                   state="readonly", width=47)
            else:
                entry = ttk.Entry(form_herramienta, width=50)
            entry.grid(row=i, column=1, padx=5, pady=3)
            self.entradas_herramienta[key] = entry
        
        btns_herramienta = ttk.Frame(form_herramienta)
        btns_herramienta.grid(row=5, column=0, columnspan=2, pady=15, sticky="ew")
        ttk.Button(btns_herramienta, text="Guardar", command=self.guardar_herramienta, width=20).pack(side="left", padx=10, pady=8)
        ttk.Button(btns_herramienta, text="Limpiar", command=self.limpiar_herramienta, width=20).pack(side="left", padx=10, pady=8)
        ttk.Button(btns_herramienta, text="Editar Seleccionado", command=self.editar_herramienta, width=20).pack(side="left", padx=10, pady=8)
        ttk.Button(btns_herramienta, text="Eliminar Seleccionado", command=self.eliminar_herramienta, width=20).pack(side="left", padx=10, pady=8)
        
        tabla_herramienta = ttk.LabelFrame(self.tab_herramienta, text="Lista de Herramientas")
        tabla_herramienta.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.tree_herramienta = ttk.Treeview(tabla_herramienta, columns=("id","c","n","cat","u","e"), show="headings", height=12)
        for col, text, width in zip(("id","c","n","cat","u","e"), 
                                    ("ID", "Código","Nombre","Categoría","Ubicación","Estado"),
                                    (40, 80, 120, 100, 150, 120)):
            self.tree_herramienta.heading(col, text=text)
            self.tree_herramienta.column(col, width=width, anchor="center")
        
        self.tree_herramienta.pack(fill="both", expand=True)
        self.tree_herramienta.bind("<ButtonRelease-1>", self._seleccionar_herramienta)
        
    def _crear_tab_prestamos(self):
        form_prestamo = ttk.LabelFrame(self.tab_prestamos, text="Registro / Edición de Préstamo")
        form_prestamo.pack(fill="x", padx=5, pady=5)
        
        campos_prestamo = [("Número:", "numero"), ("Código Herramienta:", "herramienta_codigo"), 
                          ("Responsable:", "responsable"), ("Fecha Salida (YYYY-MM-DD):", "fecha_salida"), 
                          ("Fecha Esperada (YYYY-MM-DD):", "fecha_esperada"),
                          ("Fecha Devolución (YYYY-MM-DD):", "fecha_devolucion")]
        self.entradas_prestamo = {}
        
        for i, (label, key) in enumerate(campos_prestamo):
            ttk.Label(form_prestamo, text=label).grid(row=i, column=0, padx=5, pady=3, sticky="e")
            entry = ttk.Entry(form_prestamo, width=50)
            entry.grid(row=i, column=1, padx=5, pady=3)
            self.entradas_prestamo[key] = entry
        
        btns_prestamo = ttk.Frame(form_prestamo)
        btns_prestamo.grid(row=6, column=0, columnspan=2, pady=15, sticky="ew")
        ttk.Button(btns_prestamo, text="Guardar", command=self.guardar_prestamo, width=20).pack(side="left", padx=10, pady=8)
        ttk.Button(btns_prestamo, text="Limpiar", command=self.limpiar_prestamo, width=20).pack(side="left", padx=10, pady=8)
        ttk.Button(btns_prestamo, text="Registrar Devolución", command=self.registrar_devolucion, width=22).pack(side="left", padx=10, pady=8)
        ttk.Button(btns_prestamo, text="Editar Seleccionado", command=self.editar_prestamo, width=20).pack(side="left", padx=10, pady=8)
        ttk.Button(btns_prestamo, text="Eliminar Seleccionado", command=self.eliminar_prestamo, width=20).pack(side="left", padx=10, pady=8)
        
        tabla_prestamo = ttk.LabelFrame(self.tab_prestamos, text="Lista de Préstamos")
        tabla_prestamo.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.tree_prestamo = ttk.Treeview(tabla_prestamo, columns=("id","n","c","r","fs","fe","fd"), show="headings", height=12)
        for col, text, width in zip(("id","n","c","r","fs","fe","fd"), 
                                    ("ID", "Número","Cod. Herr.","Responsable","Salida","Esperada","Devolución"),
                                    (40, 80, 100, 120, 120, 120, 120)):
            self.tree_prestamo.heading(col, text=text)
            self.tree_prestamo.column(col, width=width, anchor="center")
        
        self.tree_prestamo.pack(fill="both", expand=True)
        self.tree_prestamo.bind("<ButtonRelease-1>", self._seleccionar_prestamo)
        
    def _crear_tab_busqueda(self):
        """Crear tab de búsqueda con filtros para herramientas y préstamos"""
        filtros_frame = ttk.LabelFrame(self.tab_busqueda, text="Filtros de Búsqueda")
        filtros_frame.pack(fill="x", padx=5, pady=5)
        
        # Tipo de búsqueda
        ttk.Label(filtros_frame, text="Buscar en:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.tipo_busqueda = tk.StringVar(value="Herramientas")
        tipo_combo = ttk.Combobox(filtros_frame, textvariable=self.tipo_busqueda, 
                                  values=["Herramientas", "Préstamos"], state="readonly", width=30)
        tipo_combo.grid(row=0, column=1, padx=5, pady=5)
        tipo_combo.bind("<<ComboboxSelected>>", lambda e: self._actualizar_campos_busqueda())
        
        # Campo de búsqueda dinámico
        ttk.Label(filtros_frame, text="Campo:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.campo_busqueda = tk.StringVar(value="codigo")
        self.campo_combo = ttk.Combobox(filtros_frame, textvariable=self.campo_busqueda, 
                                        values=["codigo", "nombre"], state="readonly", width=20)
        self.campo_combo.grid(row=0, column=3, padx=5, pady=5)
        
        # Término de búsqueda
        ttk.Label(filtros_frame, text="Término:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.termino_busqueda = tk.StringVar()
        ttk.Entry(filtros_frame, textvariable=self.termino_busqueda, width=35).grid(row=1, column=1, padx=5, pady=5)
        
        # Botones
        btns_busqueda = ttk.Frame(filtros_frame)
        btns_busqueda.grid(row=1, column=2, columnspan=2, padx=5, pady=5)
        ttk.Button(btns_busqueda, text="Buscar", command=self._ejecutar_busqueda, width=12).pack(side="left", padx=4, pady=5)
        ttk.Button(btns_busqueda, text="Limpiar", command=self._limpiar_busqueda, width=12).pack(side="left", padx=4, pady=5)
        
        # Resultados
        resultados_frame = ttk.LabelFrame(self.tab_busqueda, text="Resultados de la Búsqueda")
        resultados_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.tree_busqueda = ttk.Treeview(resultados_frame, show="headings", height=15)
        self.tree_busqueda.pack(fill="both", expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(resultados_frame, orient="vertical", command=self.tree_busqueda.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree_busqueda.config(yscroll=scrollbar.set)
        
    def _actualizar_campos_busqueda(self):
        """Actualizar campos disponibles según el tipo de búsqueda"""
        tipo = self.tipo_busqueda.get()
        if tipo == "Herramientas":
            self.campo_combo.config(values=["codigo", "nombre", "categoria", "ubicacion"])
            self.campo_busqueda.set("codigo")
        else:  # Préstamos
            self.campo_combo.config(values=["numero", "responsable", "herramienta_codigo"])
            self.campo_busqueda.set("numero")
    
    def _ejecutar_busqueda(self):
        """Ejecutar búsqueda según filtros seleccionados"""
        tipo = self.tipo_busqueda.get()
        campo = self.campo_busqueda.get()
        termino = self.termino_busqueda.get().lower()
        
        if not termino:
            messagebox.showwarning("Advertencia", "Ingrese un término de búsqueda")
            return
        
        # Limpiar tabla
        for item in self.tree_busqueda.get_children():
            self.tree_busqueda.delete(item)
        
        threading.Thread(target=self._buscar_en_api, args=(tipo, campo, termino), daemon=True).start()
    
    def _buscar_en_api(self, tipo, campo, termino):
        """Buscar en la API y mostrar resultados"""
        try:
            if tipo == "Herramientas":
                data, error = self.api.get("herramientas/")
                if error or not data:
                    messagebox.showerror("Error", "No se pudo obtener datos")
                    return
                
                # Configurar columnas
                self.tree_busqueda.config(columns=("id","c","n","cat","u","e"))
                for col in ("id","c","n","cat","u","e"):
                    self.tree_busqueda.heading(col, text=col.upper())
                
                # Filtrar resultados
                for h in data:
                    valor = str(h.get(campo, "")).lower()
                    if termino in valor:
                        self.tree_busqueda.insert("", "end", values=(
                            h.get("id", ""),
                            h.get("codigo", ""),
                            h.get("nombre", ""),
                            h.get("categoria", ""),
                            h.get("ubicacion", ""),
                            h.get("estado", "")
                        ))
                
                if not self.tree_busqueda.get_children():
                    messagebox.showinfo("Búsqueda", "No se encontraron resultados")
            else:  # Préstamos
                data, error = self.api.get("prestamos/")
                if error or not data:
                    messagebox.showerror("Error", "No se pudo obtener datos")
                    return
                
                # Configurar columnas
                self.tree_busqueda.config(columns=("id","n","c","r","fs","fe","fd"))
                for col in ("id","n","c","r","fs","fe","fd"):
                    self.tree_busqueda.heading(col, text=col.upper())
                
                # Filtrar resultados
                for p in data:
                    valor = str(p.get(campo, "")).lower()
                    if termino in valor:
                        self.tree_busqueda.insert("", "end", values=(
                            p.get("id", ""),
                            p.get("numero", ""),
                            p.get("herramienta_codigo", ""),
                            p.get("responsable", ""),
                            p.get("fecha_salida", ""),
                            p.get("fecha_esperada", ""),
                            p.get("fecha_devolucion", "")
                        ))
                
                if not self.tree_busqueda.get_children():
                    messagebox.showinfo("Búsqueda", "No se encontraron resultados")
        except Exception as e:
            messagebox.showerror("Error", f"Error en búsqueda: {str(e)}")
    
    def _limpiar_busqueda(self):
        """Limpiar campos de búsqueda y resultados"""
        self.termino_busqueda.set("")
        for item in self.tree_busqueda.get_children():
            self.tree_busqueda.delete(item)
        
    def _cargar_datos_iniciales(self):
        threading.Thread(target=self._cargar_herramientas, daemon=True).start()
        threading.Thread(target=self._cargar_prestamos, daemon=True).start()
        
    def _cargar_herramientas(self):
        try:
            data, error = self.api.get("herramientas/")
            if error:
                self.status_label.config(text=f"Error: {error}", fg="#ff6b6b")
                return
            
            for item in self.tree_herramienta.get_children():
                self.tree_herramienta.delete(item)
            
            if data:
                for h in data:
                    self.tree_herramienta.insert("", "end", values=(
                        h.get("id", ""),
                        h.get("codigo", ""),
                        h.get("nombre", ""),
                        h.get("categoria", ""),
                        h.get("ubicacion", ""),
                        h.get("estado", "")
                    ))
            
            self.status_label.config(text="Conectado ✓", fg="#90ee90")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}", fg="#ff6b6b")
            
    def _cargar_prestamos(self):
        try:
            data, error = self.api.get("prestamos/")
            if error:
                return
            
            for item in self.tree_prestamo.get_children():
                self.tree_prestamo.delete(item)
            
            if data:
                for p in data:
                    self.tree_prestamo.insert("", "end", values=(
                        p.get("id", ""),
                        p.get("numero", ""),
                        p.get("herramienta_codigo", ""),
                        p.get("responsable", ""),
                        p.get("fecha_salida", ""),
                        p.get("fecha_esperada", ""),
                        p.get("fecha_devolucion", "")
                    ))
        except Exception as e:
            pass
            
    def _seleccionar_herramienta(self, event):
        selection = self.tree_herramienta.selection()
        if selection:
            item = self.tree_herramienta.item(selection[0])
            values = item['values']
            self.selected_tool = values[0]  
            
            self.entradas_herramienta["codigo"].delete(0, tk.END)
            self.entradas_herramienta["codigo"].insert(0, values[1])
            self.entradas_herramienta["nombre"].delete(0, tk.END)
            self.entradas_herramienta["nombre"].insert(0, values[2])
            self.entradas_herramienta["categoria"].set(values[3])
            self.entradas_herramienta["ubicacion"].delete(0, tk.END)
            self.entradas_herramienta["ubicacion"].insert(0, values[4])
            self.entradas_herramienta["estado"].set(values[5])
            
    def _seleccionar_prestamo(self, event):
        selection = self.tree_prestamo.selection()
        if selection:
            item = self.tree_prestamo.item(selection[0])
            values = item['values']
            self.selected_loan = values[0]  
            
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
        try:
            data = {
                "codigo": self.entradas_herramienta["codigo"].get(),
                "nombre": self.entradas_herramienta["nombre"].get(),
                "categoria": self.entradas_herramienta["categoria"].get(),
                "ubicacion": self.entradas_herramienta["ubicacion"].get(),
                "estado": self.entradas_herramienta["estado"].get()
            }
            
            if not data["codigo"] or not data["nombre"]:
                messagebox.showerror("Error", "Código y nombre son obligatorios")
                return
            
            if self.selected_tool:
                result, error = self.api.put(f"herramientas/{self.selected_tool}/", data)
                if error:
                    messagebox.showerror("Error", f"No se pudo actualizar: {error}")
                else:
                    messagebox.showinfo("Éxito", "Herramienta actualizada correctamente")
                    self.limpiar_herramienta()
                    self._cargar_herramientas()
            else:
                result, error = self.api.post("herramientas/", data)
                if error:
                    messagebox.showerror("Error", f"No se pudo crear: {error}")
                else:
                    messagebox.showinfo("Éxito", "Herramienta creada correctamente")
                    self.limpiar_herramienta()
                    self._cargar_herramientas()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def editar_herramienta(self):
        if not self.selected_tool:
            messagebox.showerror("Error", "Seleccione una herramienta primero")
            
    def eliminar_herramienta(self):
        if not self.selected_tool:
            messagebox.showerror("Error", "Seleccione una herramienta para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", "¿Desea eliminar esta herramienta?"):
            result, error = self.api.delete(f"herramientas/{self.selected_tool}/")
            if error:
                messagebox.showerror("Error", f"No se pudo eliminar: {error}")
            else:
                messagebox.showinfo("Éxito", "Herramienta eliminada correctamente")
                self.limpiar_herramienta()
                self._cargar_herramientas()
                
    def limpiar_herramienta(self):
        self.selected_tool = None
        for entry in self.entradas_herramienta.values():
            if isinstance(entry, ttk.Combobox):
                entry.set("")
            else:
                entry.delete(0, tk.END)
                
    def guardar_prestamo(self):
        try:
            # Obtener datos del formulario
            numero = self.entradas_prestamo["numero"].get().strip()
            herramienta_codigo = self.entradas_prestamo["herramienta_codigo"].get().strip()
            responsable = self.entradas_prestamo["responsable"].get().strip()
            fecha_salida = self.entradas_prestamo["fecha_salida"].get().strip()
            fecha_esperada = self.entradas_prestamo["fecha_esperada"].get().strip()
            fecha_devolucion = self.entradas_prestamo["fecha_devolucion"].get().strip()
            
            # Validaciones básicas
            if not numero or not herramienta_codigo or not responsable:
                messagebox.showerror("Error", "Número, herramienta y responsable son obligatorios")
                return
            
            if not fecha_salida:
                messagebox.showerror("Error", "La fecha de salida es obligatoria")
                return
            
            # Validar formato de fechas (YYYY-MM-DD)
            for campo, valor in [("Salida", fecha_salida), ("Esperada", fecha_esperada)]:
                if valor:
                    try:
                        from datetime import datetime
                        datetime.strptime(valor, "%Y-%m-%d")
                    except ValueError:
                        messagebox.showerror("Error", f"Fecha {campo} debe estar en formato YYYY-MM-DD")
                        return
            
            # Validar que la herramienta existe
            herramientas, _ = self.api.get("herramientas/")
            herramineta_existe = any(h.get("codigo") == herramienta_codigo for h in (herramientas or []))
            if not herramineta_existe:
                messagebox.showerror("Error", f"Herramienta con código '{herramienta_codigo}' no existe")
                return
            
            # Construir datos para enviar
            data = {
                "numero": numero,
                "herramienta_codigo": herramienta_codigo,
                "responsable": responsable,
                "fecha_salida": fecha_salida if fecha_salida else None,
                "fecha_esperada": fecha_esperada if fecha_esperada else None,
                "fecha_devolucion": fecha_devolucion if fecha_devolucion else None,
            }
            
            if self.selected_loan:
                result, error = self.api.put(f"prestamos/{self.selected_loan}/", data)
                if error:
                    messagebox.showerror("Error", f"No se pudo actualizar: {error}")
                else:
                    messagebox.showinfo("Éxito", "Préstamo actualizado correctamente")
                    self.limpiar_prestamo()
                    self._cargar_prestamos()
            else:
                result, error = self.api.post("prestamos/", data)
                if error:
                    messagebox.showerror("Error", f"No se pudo crear: {error}")
                else:
                    messagebox.showinfo("Éxito", "Préstamo creado correctamente")
                    self.limpiar_prestamo()
                    self._cargar_prestamos()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def editar_prestamo(self):
        if not self.selected_loan:
            messagebox.showerror("Error", "Seleccione un préstamo primero")
            
    def eliminar_prestamo(self):
        """Eliminar préstamo seleccionado"""
        if not self.selected_loan:
            messagebox.showerror("Error", "Seleccione un préstamo para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", "¿Desea eliminar este préstamo?"):
            result, error = self.api.delete(f"prestamos/{self.selected_loan}/")
            if error:
                messagebox.showerror("Error", f"No se pudo eliminar: {error}")
            else:
                messagebox.showinfo("Éxito", "Préstamo eliminado correctamente")
                self.limpiar_prestamo()
                self._cargar_prestamos()
                
    def registrar_devolucion(self):
        if not self.selected_loan:
            messagebox.showerror("Error", "Seleccione un préstamo para registrar devolución")
            return
        
        fecha_dev = self.entradas_prestamo["fecha_devolucion"].get()
        if not fecha_dev:
            messagebox.showerror("Error", "Ingrese fecha de devolución")
            return
        
        data = {"fecha_devolucion": fecha_dev}
        result, error = self.api.put(f"prestamos/{self.selected_loan}/", data)
        if error:
            messagebox.showerror("Error", f"No se pudo registrar: {error}")
        else:
            messagebox.showinfo("Éxito", "Devolución registrada correctamente")
            self._cargar_prestamos()
            
    def limpiar_prestamo(self):
        self.selected_loan = None
        for entry in self.entradas_prestamo.values():
            entry.delete(0, tk.END)
            
    def _iniciar_actualizaciones_automaticas(self):
        def actualizar():
            intervalo_backup = int(os.getenv("INTERVALO_BACKUP_SEG", "300"))
            start_time = time.time()
            
            while self.running:
                self._cargar_herramientas()
                self._cargar_prestamos()
                
                elapsed = int(time.time() - start_time) % intervalo_backup
                remaining = intervalo_backup - elapsed
                mins, secs = divmod(remaining, 60)
                self.backup_label.config(text=f"Respaldo: {mins:02d}:{secs:02d}")
                
                time.sleep(10)  
        
        threading.Thread(target=actualizar, daemon=True).start()
