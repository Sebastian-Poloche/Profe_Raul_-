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
root.configure(bg="#f0f0f0")

style = ttk.Style()
style.theme_use("clam")
style.configure("TNotebook", background="#f0f0f0")
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

tab_herramientas = ttk.Frame(notebook)
tab_prestamos = ttk.Frame(notebook)
tab_busqueda = ttk.Frame(notebook)

notebook.add(tab_herramientas, text="Herramientas")
notebook.add(tab_prestamos, text="Préstamos")
notebook.add(tab_busqueda, text="Búsqueda")

form_herr = ttk.LabelFrame(tab_herramientas, text="Registro / Edición de Herramienta")
form_herr.pack(fill="x", padx=5, pady=5)

campos_herr = [("Código:", "codigo"), ("Nombre:", "nombre"), ("Categoría:", "categoria"), ("Ubicación:", "ubicacion"), ("Estado:", "estado")]
entradas_herr = {}
for i, (label, key) in enumerate(campos_herr):
    ttk.Label(form_herr, text=label).grid(row=i, column=0, padx=5, pady=3, sticky="e")
    entry = ttk.Entry(form_herr, width=50)
    entry.grid(row=i, column=1, padx=5, pady=3)
    entradas_herr[key] = entry

btns_herr = ttk.Frame(form_herr)
btns_herr.grid(row=5, column=0, columnspan=2, pady=10)
ttk.Button(btns_herr, text="Guardar").pack(side="left", padx=5)
ttk.Button(btns_herr, text="Limpiar").pack(side="left", padx=5)

tabla_herr = ttk.LabelFrame(tab_herramientas, text="Lista de Herramientas")
tabla_herr.pack(fill="both", expand=True, padx=5, pady=5)

tree_herr = ttk.Treeview(tabla_herr, columns=("c","n","cat","u","e"), show="headings")
for col, text in zip(("c","n","cat","u","e"), ("Codigo","Nombre","Categoría","Ubicacion","Estado")):
    tree_herr.heading(col, text=text)
    tree_herr.column(col, width=150, anchor="center")
tree_herr.pack(fill="both", expand=True)

btns_tabla_herr = ttk.Frame(tabla_herr)
btns_tabla_herr.pack(pady=5)
ttk.Button(btns_tabla_herr, text="Cargar").pack(side="left", padx=3)
ttk.Button(btns_tabla_herr, text="Editar").pack(side="left", padx=3)
ttk.Button(btns_tabla_herr, text="Eliminar").pack(side="left", padx=3)

form_pres = ttk.LabelFrame(tab_prestamos, text="Registro / Edición de Préstamo")
form_pres.pack(fill="x", padx=5, pady=5)

campos_pres = [("Número:", "numero"), ("Código Herramienta:", "herramienta_codigo"), ("Responsable:", "responsable"),
               ("Fecha Salida (YYYY-MM-DD):", "fecha_salida"), ("Fecha Esperada (YYYY-MM-DD):", "fecha_esperada"),
               ("Fecha Devolución (YYYY-MM-DD):", "fecha_devolucion")]
entradas_pres = {}
for i, (label, key) in enumerate(campos_pres):
    ttk.Label(form_pres, text=label).grid(row=i, column=0, padx=5, pady=3, sticky="e")
    entry = ttk.Entry(form_pres, width=50)
    entry.grid(row=i, column=1, padx=5, pady=3)
    entradas_pres[key] = entry

btns_pres = ttk.Frame(form_pres)
btns_pres.grid(row=6, column=0, columnspan=2, pady=10)
ttk.Button(btns_pres, text="Guardar").pack(side="left", padx=5)
ttk.Button(btns_pres, text="Limpiar").pack(side="left", padx=5)

tabla_pres = ttk.LabelFrame(tab_prestamos, text="Lista de Préstamos")
tabla_pres.pack(fill="both", expand=True, padx=5, pady=5)

tree_pres = ttk.Treeview(tabla_pres, columns=("n","c","r","fs","fe","fd"), show="headings")
for col, text in zip(("n","c","r","fs","fe","fd"), ("Numero","Cod. Herr.","Responsable","Salida","Esperada","Devolucion")):
    tree_pres.heading(col, text=text)
    tree_pres.column(col, width=140, anchor="center")
tree_pres.pack(fill="both", expand=True)

btns_tabla_pres = ttk.Frame(tabla_pres)
btns_tabla_pres.pack(pady=5)
ttk.Button(btns_tabla_pres, text="Cargar").pack(side="left", padx=3)
ttk.Button(btns_tabla_pres, text="Editar").pack(side="left", padx=3)
ttk.Button(btns_tabla_pres, text="Eliminar").pack(side="left", padx=3)
ttk.Button(btns_tabla_pres, text="Nuevo Prestamo").pack(side="left", padx=3)
ttk.Button(btns_tabla_pres, text="Registrar Devolucion").pack(side="left", padx=3)

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

tree_busq = ttk.Treeview(tab_busqueda, show="headings")
tree_busq.pack(fill="both", expand=True, padx=5, pady=5)

footer = tk.Frame(root, bg="#2d2d2d", height=30)
footer.pack(fill="x")
footer.pack_propagate(False)

tk.Label(footer, text=" 2025 TecnoGestion S.A.S. | RFP-IHEP-2025 | v1.0",
         fg="#aaaaaa", bg="#2d2d2d", font=("Consolas", 9)).pack(side="left", padx=10, pady=5)

tk.Label(footer, text="Backend: http://127.0.0.1:8000/api/",
         fg="#66b3ff", bg="#2d2d2d", font=("Consolas", 9)).pack(side="right", padx=10, pady=5)

""" falta crear un respaldo con daemon y darle su respectivo tiempo de intervalo """
root.mainloop()