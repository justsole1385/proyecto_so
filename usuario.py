import threading
import time
import random as rd

class Usuario(threading.Thread):
    def __init__(self, nombre, cine):
        super().__init__() 
        self.nombre = nombre
        self.cine = cine

#Agregacioin de codigo para simular la aleatoriedad dentro del sistmema 
    def run(self):
        # Simula que los clientes llegan en distintos momentos
        time.sleep(rd.uniform(0.1, 1.5)) 
        vio_pelicula = False
        
        for funcion in self.cine.funciones:
            if vio_pelicula:
                break
                
            print(f"[{self.nombre}] Entrando a buscar lugar en {funcion.nombre_funcion}...")
            
            # Mientras la función tenga asientos, intenta pescar uno al azar
            while not funcion.esta_llena():
                asiento_azar = funcion.obtener_asiento_aleatorio()
                exito = funcion.intentar_reservar(asiento_azar, self.nombre)
                
                if exito:
                    print(f"[{self.nombre}] EXITO Ocupando asiento {asiento_azar} en {funcion.nombre_funcion}")
                    
                    # FUERA DEL MUTEX: Aquí el usuario "ve la película" (Ocupa el recurso compartido)
                    # Al estar fuera del candado, otros hilos pueden seguir comprando otros asientos
                    time.sleep(rd.uniform(2.0, 4.0)) 
                    
                    # Termina la película, libera el asiento para otros 
                    funcion.liberar_asiento(asiento_azar, self.nombre)
                    print(f"[{self.nombre}] Terminó y liberó el asiento {asiento_azar} de {funcion.nombre_funcion}")
                    vio_pelicula = True
                    break
                else:
                    # Chocó con otro hilo por el mismo asiento, espera un microsegundo y reintenta
                    time.sleep(rd.uniform(0.1, 0.3))
                    
        if not vio_pelicula:
            print(f"[{self.nombre}] Me quedé sin entradas. Todas las funciones están llenas")