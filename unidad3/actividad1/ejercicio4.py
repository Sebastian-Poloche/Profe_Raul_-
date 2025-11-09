# JHOONY WAS HERE
"""
4) Pipeline productor-consumidor (clases + Queue)
Objetivo: comunicar hilos mediante Queue.
Enunciado: implementa GeneradorTareas que produzca números 1..N y Trabajador que
procese cada número
(por ejemplo, calcular su cuadrado). Usa centinelas None para terminar los consumidores.
"""

import queue
import threading
import time

# Sentinela para indicar el fin de la producción
SENTINEL = object()

# Lock global para sincronizar las impresiones
print_lock = threading.Lock()


class GeneradorTareas(threading.Thread):
    def __init__(self, out_queue: queue.Queue, n: int, delay: float = 0.8, num_consumidores: int = 1):
        super().__init__()
        self.out_queue = out_queue
        self.n = n
        self.delay = delay
        self.num_consumidores = num_consumidores

    def run(self):
        for i in range(1, self.n + 1):
            with print_lock:
                print(f"[Productor] Generando número: {i}")
            self.out_queue.put(i)
            time.sleep(self.delay)

        # Enviar tantos centinelas como consumidores existan
        for _ in range(self.num_consumidores):
            self.out_queue.put(SENTINEL)

        with print_lock:
            print("[Productor] Producción finalizada.")


class Trabajador(threading.Thread):
    def __init__(self, in_queue: queue.Queue, delay: float = 0.8, nombre: str = ""):
        super().__init__()
        self.in_queue = in_queue
        self.delay = delay
        self.nombre = nombre

    def run(self):
        while True:
            item = self.in_queue.get()
            if item is SENTINEL:
                with print_lock:
                    print(f"[{self.nombre}] Recibió sentinela. Finalizado.")
                self.in_queue.task_done()
                break

            resultado = item ** 2
            with print_lock:
                print(f"[{self.nombre}] Procesó {item} --> {resultado}")

            time.sleep(self.delay)
            self.in_queue.task_done()


def main():
    # Cola compartida entre los hilos
    q = queue.Queue()
    n = 10
    num_consumidores = 3

    # Crear productor y consumidores
    productor = GeneradorTareas(q, n=n, delay=0.6, num_consumidores=num_consumidores)
    consumidores = [
        Trabajador(q, delay=0.5, nombre=f"Consumidor-{i+1}") for i in range(num_consumidores)
    ]

    # Iniciar todos los hilos
    productor.start()
    for c in consumidores:
        c.start()

    # Esperar a que todas las tareas sean procesadas
    q.join()

    with print_lock:
        print("\n[TODOS] Todas las tareas fueron procesadas correctamente.\n")


if __name__ == "__main__":
    main()
