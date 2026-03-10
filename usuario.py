import threading
class Usuario(threading.Thread):
    def __init__(self, nombre, asiento_deseado, sala):
        super().__init__() 
        self.nombre = nombre
        self.asiento_deseado = asiento_deseado
        self.sala = sala

    def run(self):
        print(f"[{self.nombre}] Ingresando al sistema para comprar el asiento {self.asiento_deseado}...")
        self.sala.reservar_asiento(self.asiento_deseado, self.nombre)
