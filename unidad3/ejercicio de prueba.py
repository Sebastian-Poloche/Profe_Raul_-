"""Simular varios cajeros automáticos (threads) atendiendo a una lista de clientes al mismo tiempo.
Cada cajero tarda un poco en atender y muestra el progreso en consola."""""
import threading
import queue
import time
import random

# Centinela para indicar fin del trabajo
SENTINEL = object()

# Lock global para sincronizar impresiones
print_lock = threading.Lock()

# Clase que simula el banco productor de clientes
class Banco(threading.Thread):
    def __init__(self, cola_clientes: queue.Queue, total_clientes: int, num_cajeros: int):
        super().__init__()
        self.cola_clientes = cola_clientes
        self.total_clientes = total_clientes
        self.num_cajeros = num_cajeros

    def run(self):
        for i in range(1, self.total_clientes + 1):
            cliente = f"Cliente-{i}"
            with print_lock:
                print(f"[Banco] Llega {cliente} y entra a la fila.")
            self.cola_clientes.put(cliente)
            time.sleep(random.uniform(0.3, 0.8))  # simulamos tiempo de llegada

        # Enviar un centinela por cada cajero
        for _ in range(self.num_cajeros):
            self.cola_clientes.put(SENTINEL)
        with print_lock:
            print("[Banco] Todos los clientes han sido atendidos. Fin de la jornada.")


# Clase que simula a un cajero que atiende clientes
class Cajero(threading.Thread):
    def __init__(self, nombre: str, cola_clientes: queue.Queue):
        super().__init__()
        self.nombre = nombre
        self.cola_clientes = cola_clientes

    def run(self):
        while True:
            cliente = self.cola_clientes.get()
            if cliente is SENTINEL:
                with print_lock:
                    print(f"[{self.nombre}] Recibió centinela. Cierra su ventanilla.")
                self.cola_clientes.task_done()
                break

            tiempo_servicio = random.uniform(1, 3)
            with print_lock:
                print(f"[{self.nombre}] Atiende a {cliente} (tardará {tiempo_servicio:.2f}s)")
            time.sleep(tiempo_servicio)
            with print_lock:
                print(f"[{self.nombre}] Finalizó atención de {cliente}")
            self.cola_clientes.task_done()


def main():
    # Crear cola compartida
    cola_clientes = queue.Queue()

    # Parámetros del sistema
    total_clientes = 10
    num_cajeros = 3

    # Crear productor y consumidores
    banco = Banco(cola_clientes, total_clientes, num_cajeros)
    cajeros = [Cajero(f"Cajero-{i+1}", cola_clientes) for i in range(num_cajeros)]

    # Iniciar todos los hilos
    banco.start()
    for c in cajeros:
        c.start()

    # Esperar a que todo termine
    banco.join()
    cola_clientes.join()

    with print_lock:
        print("\n[TODOS] Todos los clientes fueron atendidos correctamente.\n")


if __name__ == "__main__":
    main()
