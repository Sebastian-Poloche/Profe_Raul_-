"""
1) Mezclador de tareas simples (threading directo)
Objetivo: practicar creación de hilos, start() y join() con funciones y argumentos.
Enunciado: crea 3 hilos que ejecuten funciones simples y de distinta duración (simuladas
con sleep).
Cada función imprime su inicio y fin. No uses Event, Lock, Queue ni daemon.
"""
import threading
import time

def tarea (hilacos, duracion):
    print(f"Inicio de la tarea {hilacos}")
    time.sleep(duracion)  
    print(f"Fin de la tarea {hilacos}")

def main():
    hilo1 = threading.Thread(target=tarea, args=("hilito 1", 1.3))
    hilo2 = threading.Thread(target=tarea, args=("hilito 2", 2.8))
    hilo3 = threading.Thread(target=tarea, args=("hilito 3", 1.5))


    hilo1.start()
    hilo2.start()
    hilo3.start()

    hilo1.join()
    hilo2.join()
    hilo3.join()

    print("Terminaron los procesos que se lanzaron ")

if __name__ == "__main__":
    main()