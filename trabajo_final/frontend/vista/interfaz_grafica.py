import tkinter as tk
from tkinter import ttk, messagebox
import os
import threading
import time
from datetime import datetime


root = tk.Tk()
root.title("IHEP - Inventario de Herramientas y Préstamos")
root.geometry("1200x720")
root.minsize(1000, 600)
root.configure(bg="#C9E5F2")

style = ttk.Style()
style.theme_use("clam")
style.configure("TNotebook", background="#98D0EB")
style.configure("TNotebook.Tab", padding=[15, 8], font=("Segoe UI", 11, "bold"))
style.map("TNotebook.Tab",
          background=[("selected", "#0078d7"), ("active", "#e1f5fe")],
          foreground=[("selected", "white"), ("active", "black")])

header = tk.Frame(root, bg="#0078d7", height=60)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(header, text="IHEP - Inventario de Herramientas y Préstamos",
fg="white", bg="#0078d7", font=("Segoe UI", 16, "bold")).pack(side="left", padx=20, pady=10)

info_frame = tk.Frame(header, bg="#0078d7")
info_frame.pack(side="right", padx=20)

tk.Label(info_frame, text="Conectado", fg="#90ee90", bg="#0078d7",
font=("Segoe UI", 10)).pack(side="left", padx=10)

backup_label = tk.Label(info_frame, text="Respaldo: 05:00",
fg="#ffff99", bg="#0078d7", font=("Segoe UI", 9))
backup_label.pack(side="left")

def actualizar_reloj():
    intervalo = int(os.getenv("INTERVALO_BACKUP_SEG", "300"))
    elapsed = int(time.time()) % intervalo
    mins, secs = divmod(intervalo - elapsed, 60)
    backup_label.config(text=f"Respaldo: {mins:02d}:{secs:02d}")
    root.after(1000, actualizar_reloj)

actualizar_reloj()

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=15, pady=15)

tab_herramienta = ttk.Frame(notebook)
tab_prestamos = ttk.Frame(notebook)
tab_busqueda = ttk.Frame(notebook)

notebook.add(tab_herramienta, text="Herramientas")
notebook.add(tab_prestamos, text="Préstamos")
notebook.add(tab_busqueda, text="Búsqueda")

form_herramienta = ttk.LabelFrame(tab_herramienta, text="Registro / Edición de Herramienta")
form_herramienta.pack(fill="x", padx=5, pady=5)

campos_herramienta = [("Código:", "codigo"), ("Nombre:", "nombre"), ("Categoría:", "categoria"), ("Ubicación:", "ubicacion"), ("Estado:", "estado")]
entradas_herramienta = {}
for i, (label, key) in enumerate(campos_herramienta):
    ttk.Label(form_herramienta, text=label).grid(row=i, column=0, padx=5, pady=3, sticky="e")
    entry = ttk.Entry(form_herramienta, width=50)
    entry.grid(row=i, column=1, padx=5, pady=3)
    entradas_herramienta[key] = entry

btns_herramienta = ttk.Frame(form_herramienta)
btns_herramienta.grid(row=5, column=0, columnspan=2, pady=10)
ttk.Button(btns_herramienta, text="Guardar").pack(side="left", padx=5)
ttk.Button(btns_herramienta, text="Limpiar").pack(side="left", padx=5)

tabla_herramienta = ttk.LabelFrame(tab_herramienta, text="Lista de Herramientas")
tabla_herramienta.pack(fill="both", expand=True, padx=5, pady=5)

tree_herramienta = ttk.Treeview(tabla_herramienta, columns=("c","n","cat","u","e"), show="headings")
for col, text in zip(("c","n","cat","u","e"), ("Codigo","Nombre","Categoría","Ubicacion","Estado")):
    tree_herramienta.heading(col, text=text)
    tree_herramienta.column(col, width=150, anchor="center")
tree_herramienta.pack(fill="both", expand=True)

btns_tabla_herramienta = ttk.Frame(tabla_herramienta)
btns_tabla_herramienta.pack(pady=5)
ttk.Button(btns_tabla_herramienta, text="Cargar").pack(side="left", padx=3)
ttk.Button(btns_tabla_herramienta, text="Editar").pack(side="left", padx=3)
ttk.Button(btns_tabla_herramienta, text="Eliminar").pack(side="left", padx=3)

form_prestamo = ttk.LabelFrame(tab_prestamos, text="Registro / Edición de Préstamo")
form_prestamo.pack(fill="x", padx=5, pady=5)

campos_prestamo = [("Número:", "numero"), ("Código Herramienta:", "herramienta_codigo"), ("Responsable:", "responsable"),
               ("Fecha Salida (YYYY-MM-DD):", "fecha_salida"), ("Fecha Esperada (YYYY-MM-DD):", "fecha_esperada"),
               ("Fecha Devolución (YYYY-MM-DD):", "fecha_devolucion")]
entradas_prestamo = {}
for i, (label, key) in enumerate(campos_prestamo):
    ttk.Label(form_prestamo, text=label).grid(row=i, column=0, padx=5, pady=3, sticky="e")
    entry = ttk.Entry(form_prestamo, width=50)
    entry.grid(row=i, column=1, padx=5, pady=3)
    entradas_prestamo[key] = entry

btns_prestamo = ttk.Frame(form_prestamo)
btns_prestamo.grid(row=6, column=0, columnspan=2, pady=10)
ttk.Button(btns_prestamo, text="Guardar").pack(side="left", padx=5)
ttk.Button(btns_prestamo, text="Limpiar").pack(side="left", padx=5)

tabla_prestamo = ttk.LabelFrame(tab_prestamos, text="Lista de Préstamos")
tabla_prestamo.pack(fill="both", expand=True, padx=5, pady=5)

tree_prestamo = ttk.Treeview(tabla_prestamo, columns=("n","c","r","fs","fe","fd"), show="headings")
for col, text in zip(("n","c","r","fs","fe","fd"), ("Numero","Cod. Herr.","Responsable","Salida","Esperada","Devolucion")):
    tree_prestamo.heading(col, text=text)
    tree_prestamo.column(col, width=140, anchor="center")
tree_prestamo.pack(fill="both", expand=True)

btns_tabla_prestamo = ttk.Frame(tabla_prestamo)
btns_tabla_prestamo.pack(pady=5)
ttk.Button(btns_tabla_prestamo, text="Cargar").pack(side="left", padx=3)
ttk.Button(btns_tabla_prestamo, text="Editar").pack(side="left", padx=3)
ttk.Button(btns_tabla_prestamo, text="Eliminar").pack(side="left", padx=3)
ttk.Button(btns_tabla_prestamo, text="Nuevo Prestamo").pack(side="left", padx=3)
ttk.Button(btns_tabla_prestamo, text="Registrar Devolucion").pack(side="left", padx=3)

busq_frame = ttk.LabelFrame(tab_busqueda, text="Busqueda Global")
busq_frame.pack(fill="x", padx=5, pady=5)

ttk.Label(busq_frame, text="Tipo:").grid(row=0, column=0, padx=5)
combo = ttk.Combobox(busq_frame, values=["Herramientas", "Prestamos"], state="readonly")
combo.set("Herramientas")
combo.grid(row=0, column=1, padx=5)

ttk.Label(busq_frame, text="Termino:").grid(row=0, column=2, padx=5)
termino_entry = ttk.Entry(busq_frame, width=30)
termino_entry.grid(row=0, column=3, padx=5)

ttk.Button(busq_frame, text="Buscar").grid(row=0, column=4, padx=5)

tree_busqueda = ttk.Treeview(tab_busqueda, show="headings")
tree_busqueda.pack(fill="both", expand=True, padx=5, pady=5)

footer = tk.Frame(root, bg=
"#2d2d2d", height=30)
footer.pack(fill="x")
footer.pack_propagate(False)

tk.Label(footer, text=" 2025 TecnoGestion S.A.S. | RFP-IHEP-2025 | v1.0",
         fg="#aaaaaa", bg="#2d2d2d", font=("Consolas", 9)).pack(side="left", padx=10, pady=5)

tk.Label(footer, text="Backend: http://127.0.0.1:8000/api/",
         fg="#66b3ff", bg="#2d2d2d", font=("Consolas", 9)).pack(side="right", padx=10, pady=5)

""" falta crear un respaldo con daemon y darle su respectivo tiempo de intervalo """
root.mainloop()