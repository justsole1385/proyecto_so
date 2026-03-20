import threading
import time
import random as rd
import logging  # Importamo el módulo para la bitácora

# Configuración de la bitácora se crea el archivo físico 'bitácora.log'
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
        # Registro del intento de reserva 
        logging.info(f"[SOLICITUD] {nombre_usuario} intenta reservar el asiento {id_asiento}.")
        
        with self.candado: 
            # Registro de entrada a sección crítica
            logging.info(f"[ENTRADA] {nombre_usuario} entró a la sección crítica (adquirió Mutex).")
            
            if id_asiento not in self.mapa_asientos:
                logging.error(f"[ERROR] {nombre_usuario}: Asiento {id_asiento} no existe.")
                return False
            
            asiento = self.mapa_asientos[id_asiento]

            if asiento.libre:
                time.sleep(rd.randint(1,5)) 
                asiento.libre = False
                asiento.dueno = nombre_usuario
                self.asientos_disponibles -= 1

                # Registro del éxito en hacer la reserva
                logging.info(f"[ÉXITO] {nombre_usuario} reservó el asiento {id_asiento}.")

                print(f"Éxito: {nombre_usuario} reservó el asiento {id_asiento}.")
                res= True
            else:
                # Registro del fallo
                logging.warning(f"[RECHAZADO] {nombre_usuario}: {id_asiento} ya ocupado por {asiento.dueno}.")
                print(f"Rechazado: {nombre_usuario} intentó reservar {id_asiento}, pero ya es de {asiento.dueno}.")
                res= False
        
        # Registro: Salida de sección crítica
        logging.info(f"[LIBERACIÓN] {nombre_usuario} salió de la sección crítica y liberó el Mutex.")
        return res

    def mostrar_estado_sala(self):
        print(f"\n-ESTADO FINAL: {self.pelicula} ---")
        print(f"Asientos restantes: {self.asientos_disponibles}")
        for id_asiento, asiento in self.mapa_asientos.items():
            print(asiento)
        print("---------------------------------------\n")