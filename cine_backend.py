import threading
import time
import random as rd

class Asiento:
    def __init__(self, id_asiento):
        self.id_asiento = id_asiento
        self.libre = True
        self.dueno = None

    def __str__(self):
        if self.libre:
            return f"[{self.id_asiento}: Libre]"
        else:
            return f"[{self.id_asiento}: Ocupado por {self.dueno}]"

class SalaCine:
    def __init__(self, pelicula, filas, asientos_por_fila):
        self.pelicula = pelicula
        self.asientos_disponibles = filas * asientos_por_fila 
        self.mapa_asientos = {} 
        self.candado = threading.Lock()

        letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i in range(filas):
            letra = letras[i]
            for j in range(1, asientos_por_fila + 1):
                id_asiento = f"{letra}{j}"
                self.mapa_asientos[id_asiento] = Asiento(id_asiento)

    def reservar_asiento(self, id_asiento, nombre_usuario):
        with self.candado: 
            if id_asiento not in self.mapa_asientos:
                return False, f"Error: El asiento {id_asiento} no existe."
            asiento = self.mapa_asientos[id_asiento]

            if asiento.libre:
                time.sleep(rd.randint(1,5)) 
                asiento.libre = False
                asiento.dueno = nombre_usuario
                self.asientos_disponibles -= 1
                print(f"Éxito: {nombre_usuario} reservó el asiento {id_asiento}.")
                return True
            else:
                print(f"Rechazado: {nombre_usuario} intentó reservar {id_asiento}, pero ya es de {asiento.dueno}.")
                return False
            

    def mostrar_estado_sala(self):
        print(f"\n-ESTADO FINAL: {self.pelicula} ---")
        print(f"Asientos restantes: {self.asientos_disponibles}")
        for id_asiento, asiento in self.mapa_asientos.items():
            print(asiento)
        print("---------------------------------------\n")