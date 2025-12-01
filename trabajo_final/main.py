"""
Punto de entrada principal de la aplicación IHEP.

Inicializa y lanza la interfaz gráfica de usuario (GUI) construida con Tkinter.
Este módulo crea la ventana principal y pasa el control a la clase InterfazIHEP.
"""

import tkinter as tk

from frontend.vista.interfaz_grafica import InterfazIHEP


if __name__ == "__main__":
    """
    Bloque principal de ejecución.

    Crea la ventana raíz de Tkinter y la pasa a la clase InterfazIHEP
    que se encarga de construir toda la interfaz gráfica y funcionalidad.
    Luego inicia el mainloop que mantiene la aplicación corriendo hasta
    que el usuario cierre la ventana.
    """
    root = tk.Tk()
    app = InterfazIHEP(root)
    root.mainloop()


