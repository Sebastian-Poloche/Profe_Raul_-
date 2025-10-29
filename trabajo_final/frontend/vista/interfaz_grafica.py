import tkinter as tk
from tkinter import messagebox, Tk, ttk

def Interfaz_grafica():
	root = Tk()
	root.title("Interfaz de App")
	root.geometry("400x200")

	texto_informativo = tk.Label(root, text="¡Bienvenido a la Interfaz Gráfica!", anchor="center")
	texto_informativo.grid(row=0, column=0)

	root.mainloop()