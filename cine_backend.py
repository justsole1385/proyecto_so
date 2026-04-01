import threading
import time
import logging

# Configuracion de la bitacora con un formato limpio
logging.basicConfig(
    filename='bitacora.log',
    level=logging.INFO,
    format='%(message)s'
)

class RelojGlobal:
    def __init__(self, duracion_total):
        self.tiempo_actual = 0
        self.duracion_total = duracion_total
        self.pelicula_terminada = threading.Event()
        self.lock = threading.Lock()

    def iniciar(self):
        # Lanza el reloj en un hilo en segundo plano 
        threading.Thread(target=self._tictac, daemon=True).start()

    def _tictac(self):
        while self.tiempo_actual < self.duracion_total:
            time.sleep(1) # 1 segundo real = 1 minuto de pelicula
            with self.lock:
                self.tiempo_actual += 1
                
        self.pelicula_terminada.set()
        mensaje = "\n[SISTEMA] >>> LA PELICULA HA TERMINADO <<<"
        print(mensaje)
        logging.info(mensaje)

    def obtener_tiempo(self):
        with self.lock:
            return f"[{self.tiempo_actual:03d}:00]"

class CineCentral:
    def __init__(self, reloj):
        self.reloj = reloj
        # El Semaforo de 4 cupos reemplaza al Mutex
        self.semaforo = threading.Semaphore(4) 
        self.lock_asientos = threading.Lock()
        self.asientos = [None, None, None, None] 

    def ocupar_asiento(self, nombre):
        # Mutex rapido solo para evitar sentarse en la misma silla fisica
        with self.lock_asientos:
            for i in range(4):
                if self.asientos[i] is None:
                    self.asientos[i] = nombre
                    return i
        return -1

    def liberar_asiento(self, indice):
        with self.lock_asientos:
            self.asientos[indice] = None