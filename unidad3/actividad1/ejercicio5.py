"""
5) Logger en segundo plano (clases + daemon)
Objetivo: usar hilos daemon que no bloqueen el cierre del programa.
Enunciado: crea un LoggerDaemon que imprima mensajes periódicos de estado
y un hilo TrabajoPesado que simule una tarea principal.
El daemon se detiene automáticamente al terminar el programa.
"""
import threading
import time

class Logger_daemon(threading.Thread):
    def _init_(self, intervalo):
        super()._init_(daemon=True)  
        self.intervalo = intervalo

    def run(self):
        while True:
            print(" El programa sigue ejecutándose...")
            time.sleep(self.intervalo)


class Trabajo_pesado(threading.Thread):
    def _init_(self, pasos):
        super()._init_()
        self.pasos = pasos

    def run(self):
        for i in range(1, self.pasos + 1):
            print(f" Ejecutando paso {i}/{self.pasos}...")
            time.sleep(1.2)  
        print("trabajo pesado a terminado.")


def main():
    logger = Logger_daemon(intervalo=2)
    trabajo = Trabajo_pesado(pasos=5)


    logger.start()
    trabajo.start()

    
    trabajo.join()

    print("el programa principal a terminado.")


if __name__ == "_main_":
    main()