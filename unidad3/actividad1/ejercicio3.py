"""
3) Cuenta bancaria segura (clases + Lock)
Objetivo: proteger secciones críticas con Lock.
Enunciado: crea una clase Cuenta con un saldo compartido y métodos depositar y retirar.
Crea hilos OperadorCuenta que hagan operaciones mixtas. Con Lock el saldo final debe ser
correcto
"""

import threading
import random
import time

class Cuenta:
    def __init__(self, saldo_inicial=0):
        self.saldo = saldo_inicial
        self.lock = threading.Lock()  

    def depositar(self, monto):
        with self.lock:  # Usa 'with' para manejar el lock automáticamente
            saldo_anterior = self.saldo
            time.sleep(0.02)  
            self.saldo = saldo_anterior + monto
            print(f" Depósito: +{monto} | Saldo: {self.saldo}")

    def retirar(self, monto):
        with self.lock:
            if self.saldo >= monto:
                saldo_anterior = self.saldo
                time.sleep(0.02)
                self.saldo = saldo_anterior - monto
                print(f" Retiro: -{monto} | Saldo: {self.saldo}")
            else:
                print(f" Retiro fallido (-{monto}) | Saldo insuficiente: {self.saldo}")


class OperacionesCuenta(threading.Thread):
    def __init__(self, cuenta, operaciones):
        super().__init__()
        self.cuenta = cuenta
        self.operaciones = operaciones

    def run(self):  # Método que ejecuta el hilo
        for _ in range(self.operaciones):
            movimiento = random.choice(["depositar", "retirar"])
            monto = random.randint(10, 100)

            if movimiento == "depositar":
                self.cuenta.depositar(monto)
            else:
                self.cuenta.retirar(monto)

            time.sleep(random.uniform(0.05, 0.2))


def main():
    cuenta = Cuenta(500)  # Saldo inicial de la cuenta 
    hilos = []

    for i in range(3):
        hilo = OperacionesCuenta(cuenta, operaciones=5)
        hilos.append(hilo)

    for hilo in hilos:
        hilo.start()

    for hilo in hilos:
        hilo.join()

    print(f"\n Saldo final: {cuenta.saldo}")


if __name__ == "__main__":
    main()


