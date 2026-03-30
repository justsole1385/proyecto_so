from cine_backend import CineCentral
from usuario import Usuario

def main():
    print("\n--- INICIANDO SIMULACIÓN CONCURRENTE AUTOMÁTICA ---")
    cine = CineCentral()
    
    # Lanzamos 12 usuarios para solo 8 asientos totales (4 por función). 
    # Esto garantiza que habrá asincronía, rebosamiento y exclusión mutua.
    cant_usuarios = 12 
    hilos = []
    
    for i in range(cant_usuarios):
        hilos.append(Usuario(nombre=f"Cliente-{i+1}", cine=cine))
    
    print("Abriendo las puertas del cine...\n")
    
    for h in hilos: 
        h.start()
        
    for h in hilos: 
        h.join()
        
    print("\n--- SIMULACIÓN FINALIZADA ---")

if __name__ == "__main__":
    main()