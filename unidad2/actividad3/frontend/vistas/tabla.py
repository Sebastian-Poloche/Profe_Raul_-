import tkinter as tk
from tkinter import ttk

class Tabla():
    """
    Clase para crear una tabla (Treeview) en Tkinter de manera simple y funcional.
    
    Parámetros:
        root: Ventana padre
        titulos: Lista con los nombres de las columnas a mostrar
        columnas: Lista con los identificadores técnicos de las columnas
        data: Lista de tuplas con los datos a mostrar
        anchos: Lista con los anchos de cada columna (opcional)
    """
    
    def __init__(self, root, titulos, columnas, data, anchos=None):
        # Crear el Treeview (tabla)
        self.tabla = ttk.Treeview(root, columns=columnas, show='headings', height=15)
        
        # Configurar los anchos de las columnas (si no se proporcionan, usar valores por defecto)
        if anchos is None:
            anchos = [80] * len(columnas)  # Ancho por defecto de 80 píxeles
        
        # Configurar encabezados y anchos
        for i, columna in enumerate(columnas):
            self.tabla.heading(columna, text=titulos[i])
            self.tabla.column(columna, width=anchos[i], anchor='center')
        
        # Insertar datos iniciales
        for elemento in data:
            self.tabla.insert(parent='', index='end', values=elemento)
        
        # Agregar scrollbar vertical (se posicionará en grid)
        self.scrollbar = ttk.Scrollbar(root, orient='vertical', command=self.tabla.yview)
        self.tabla.configure(yscroll=self.scrollbar.set)
    
    def grid(self, row, column, columnspan=1, rowspan=1, sticky='nsew', padx=0, pady=0):
        """Posicionar la tabla en la ventana usando grid"""
        self.tabla.grid(row=row, column=column, columnspan=columnspan, rowspan=rowspan, sticky=sticky, padx=padx, pady=pady)
        self.scrollbar.grid(row=row, column=column+columnspan, rowspan=rowspan, sticky='ns', padx=(0, padx))
    
    def refrescar(self, data):
        """Limpiar y actualizar la tabla con nuevos datos"""
        # Eliminar todos los elementos
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        # Insertar nuevos datos
        for elemento in data:
            self.tabla.insert(parent='', index='end', values=elemento)
    
    def obtener_widget(self):
        """Retorna el widget Treeview para manipulación directa"""
        return self.tabla
    
    def obtener_fila_seleccionada(self):
        """Retorna los valores de la fila seleccionada, o None si no hay selección"""
        seleccion = self.tabla.selection()
        if seleccion:
            item = seleccion[0]
            return self.tabla.item(item)['values']
        return None
    
    def vincular_clic(self, callback):
        """
        Vincular una función que se ejecute cuando se haga clic en una fila.
        La función callback recibe los valores de la fila como parámetro.
        """
        def al_hacer_clic(event):
            fila = self.obtener_fila_seleccionada()
            if fila:
                callback(fila)
        
        self.tabla.bind('<ButtonRelease-1>', al_hacer_clic)