import tkinter as tk
from tkinter import messagebox, Tk, ttk
import requests 
import json
import threading
import queue
import os
import time
import datetime


BACKEND_URL = "http://127.0.0.1:8000/api/"


def Interfaz_grafica():
	root = Tk()
	root.title("Interfaz de App")
	root.geometry("400x200")

	texto_informativo = tk.Label(root, text="¡Bienvenido a TecnoGestión S.A.S!", anchor="center")
	texto_informativo.grid(row=0, column=0)

	root.mainloop()