"""
2) Temporizador con reinicio (clases + Event)
Objetivo: usar Event para reiniciar el temporizador cuando el usuario presiona Enter.

Enunciado: crea una clase Temporizador que cuente segundos hasta un límite.
Cada vez que el usuario presione Enter, el tiempo se reinicia a 0.
"""
import threading
import time

class Temporizador(threading.Thread):

    def __init__(self, limite, reset_event, stop_event):
        super().__init__()
        self.limite = limite
        self.reset_event = reset_event
        self.stop_event = stop_event

    def run(self):
        contador = 0
        # Bucle principal: para que se ejecute el programa cada 0.1 seg pero cada vez
        # que el usuario oprima enter se reinicie el programa y si no lo oprime que el programa
        # se termine cuando el tiempo sea 0
        while contador < self.limite and not self.stop_event.is_set():
            print(f"Tiempo {contador} segundos.")

            for tiempo_ejecucion in range(0, 10):
                time.sleep(0.1)

                # Si se detecta un reinicio el programa del {contador} volvera a cero hasta
                # que el programa se cierre o termine su ciclo
                if self.reset_event.is_set():
                    print(f"Temporizador reiniciado")
                    contador = 0
                    self.reset_event.clear() # Se limpia el evento
                    break
                
                # Si se activa el stop, entonces salimos directamente del programa
                if self.stop_event.is_set():
                    break
            
            # Si no hubo reset ni stop, incrementamos el contador
            if not self.reset_event.is_set() and not self.stop_event.is_set():
                contador += 1
        
        # Si llegamos al limite naturalmente el programa terminara el temporizador
        if contador >= self.limite:
            print(f"El Temporizador ha terminado el tiempo final fue: {self.limite}")
            self.stop_event.set() # Se determina que el programa termino o finalizo


class Reiniciador(threading.Thread):
    def __init__(self, reset_event, stop_event):
        super().__init__(daemon=True)
        self.reset_event = reset_event
        self.stop_event = stop_event

    def run(self):
        # Ciclo infinito esperando que el usuario presione enter
        while not self.stop_event.is_set():
            try:
                input("Presiona enter para reiniciar o Ctrl+C para salir...\n")
                # Si el usuario oprime enter, activa el evento y reinicia el contador
                if not self.stop_event.is_set():
                    self.reset_event.set()
            except EOFError:
                # Si hay errores de entrada, salimos
                break

def main():
    print("=" * 50)
    print("Temporizador de reinicio")
    print("=" * 50)

    reset_event = threading.Event()
    stop_event = threading.Event()

    limite = 10

    temporizador = Temporizador(limite, reset_event, stop_event)
    reiniciar = Reiniciador(reset_event, stop_event)

    temporizador.start()
    reiniciar.start()

    try:
        temporizador.join()
    except KeyboardInterrupt:
        print("Interrupcion detectada, deteniendo")
        stop_event.set()
        temporizador.join(timeout=2)

    print("Programa finalizado")
    print("=" * 50)

if __name__ == "__main__":
    main()