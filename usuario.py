import threading
import time
import random as rd
import logging

class Usuario(threading.Thread):
    def __init__(self, nombre, cine):
        super().__init__()
        self.nombre = nombre
        self.cine = cine
        self.tiempo_visto = 0
        self.veces_entrado = 0
        self.quantum = 20 # Tiempo maximo de CPU por turno
        
    def log(self, mensaje):
        texto = f"{self.cine.reloj.obtener_tiempo()} {mensaje}"
        print(texto)
        logging.info(texto)

    def run(self):
        self.log(f"[LISTO] {self.nombre} llego al cine y entro a la fila de espera.")

        while not self.cine.reloj.pelicula_terminada.is_set():
            # Intentar entrar usando el Semaforo. 
            # El timeout evita que el hilo se quede congelado si la pelicula se acaba
            adquirido = self.cine.semaforo.acquire(timeout=1.0)
            
            if not adquirido:
                continue 
                
            if self.cine.reloj.pelicula_terminada.is_set():
                self.cine.semaforo.release()
                break

            # --- ENTRA A LA SECCION CRITICA ---
            asiento_idx = self.cine.ocupar_asiento(self.nombre)
            self.veces_entrado += 1
            self.log(f"[ASIGNACION] {self.nombre} ocupo el Asiento {asiento_idx + 1} (Visita #{self.veces_entrado}).")

            #  ¿Ira al bano (I/O) o consumira todo el Quantum?
            va_al_bano = rd.random() < 0.5 # 50% de probabilidad de interrupcion voluntaria
            
            if va_al_bano:
                tiempo_en_asiento = rd.randint(5, 15)
            else:
                tiempo_en_asiento = self.quantum

            # Bucle de visualizacion segundo a segundo para poder cortar si se acaba el tiempo global
            minutos_reales_vistos = 0
            for _ in range(tiempo_en_asiento):
                if self.cine.reloj.pelicula_terminada.is_set():
                    break
                time.sleep(1) 
                minutos_reales_vistos += 1
                self.tiempo_visto += 1

            # --- LIBERA LA SECCION CRITICA ---
            self.cine.liberar_asiento(asiento_idx)
            self.cine.semaforo.release()

            if self.cine.reloj.pelicula_terminada.is_set():
                break

            # Procesamiento de la salida
            if va_al_bano:
                self.log(f"[I/O WAIT] {self.nombre} se levanto al bano. Libero Asiento {asiento_idx + 1}. Vio: {minutos_reales_vistos} min.")
                tiempo_bano = rd.randint(5, 15)
                for _ in range(tiempo_bano):
                    if self.cine.reloj.pelicula_terminada.is_set():
                        break
                    time.sleep(1)
                
                if not self.cine.reloj.pelicula_terminada.is_set():
                    self.log(f"[LISTO] {self.nombre} regreso del bano y se formo al final de la fila.")
            else:
                self.log(f"[EXPULSION] {self.nombre} alcanzo el limite de Quantum ({self.quantum} min). Fue enviado al final de la fila.")