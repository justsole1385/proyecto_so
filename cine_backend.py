import threading
import time
import random as rd
import logging

# Configuración de la bitácora
logging.basicConfig(
    filename='bitácora.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class Asiento:
    def __init__(self, id_asiento):
        self.id_asiento = id_asiento
        self.libre = True
        self.dueno = None

class FuncionCine:
    def __init__(self, nombre_funcion, filas, asientos_por_fila):
        self.nombre_funcion = nombre_funcion
        self.asientos_disponibles = filas * asientos_por_fila 
        self.mapa_asientos = {} 
        self.candado = threading.Lock()

        letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i in range(filas):
            letra = letras[i]
            for j in range(1, asientos_por_fila + 1):
                id_asiento = f"{letra}{j}"
                self.mapa_asientos[id_asiento] = Asiento(id_asiento)

    def intentar_reservar(self, id_asiento, nombre_usuario):
        # El Mutex SOLO  lo usamos para verificar y cambiar el estado rápidamente
        with self.candado: 
            asiento = self.mapa_asientos.get(id_asiento)
            if asiento and asiento.libre:
                asiento.libre = False
                asiento.dueno = nombre_usuario
                self.asientos_disponibles -= 1
                logging.info(f"[{self.nombre_funcion}] {nombre_usuario} reservó el {id_asiento}.")
                return True
            return False

    def liberar_asiento(self, id_asiento, nombre_usuario):
        # Mutex para liberar el recurso de forma segura
        with self.candado:
            asiento = self.mapa_asientos.get(id_asiento)
            if asiento and not asiento.libre and asiento.dueno == nombre_usuario:
                asiento.libre = True
                asiento.dueno = None
                self.asientos_disponibles += 1
                logging.info(f"[{self.nombre_funcion}] {nombre_usuario} liberó el {id_asiento}.")

    def esta_llena(self):
        with self.candado:
            return self.asientos_disponibles == 0

    def obtener_asiento_aleatorio(self):
        return rd.choice(list(self.mapa_asientos.keys()))

class CineCentral:
    def __init__(self):
        # Creamos dos funciones pequeñas en distitnso horarios de 4 asientos cada una 
        # para forzar que así se llenen rápido
        self.funciones = [
            FuncionCine("Función 14:00 (Sala 1)", filas=2, asientos_por_fila=2),
            FuncionCine("Función 16:00 (Sala 2)", filas=2, asientos_por_fila=2)
        ]