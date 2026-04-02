import time
import logging
from cine_backend import CineCentral, RelojGlobal
from usuario import Usuario
from operator import attrgetter

def main():
    print("\n========================================================")
    print("                  SIMULACIÓN DE CINE            ")
    print("========================================================\n")
    
    # Limpiamos el archivo de bitacora anterior
    with open('bitacora.log', 'w') as f:
        f.write("--- INICIO DE LOS REGISTROS DEL SISTEMA ---\n")

    duracion_pelicula = 225
    reloj = RelojGlobal(duracion_pelicula)
    cine = CineCentral(reloj)
    
    amigos = [
        "Paula", "Leonor", "Juan Diego", "Justin", "Daniel", "Raul", "Karel", "Jeremy", "Sebastian", "Carlos", "Christian", "Xavier"]
    
    print(f"[SISTEMA] Iniciando proyeccion. Duracion total: {duracion_pelicula} minutos.")
    print(f"[SISTEMA] Quantum establecido: 20 minutos.")
    print("[SISTEMA] Iniciando reloj...\n")
    
    reloj.iniciar()
    
    hilos = []
    for nombre in amigos:
        hilo = Usuario(nombre=nombre, cine=cine)
        hilos.append(hilo)
        hilo.start()
        # micro-delay para garantizar que lleguen exactamente en el orden de la lista
        time.sleep(0.05) 
        
    for h in hilos:
        h.join()
        
    print("\n========================================================")
    print("   RANKING FINAL DE MINUTOS VISTOS")
    print("========================================================")
    
    logging.info("\n--- RESUMEN  ---")
    
    # Ordenamiento de hilos 
    hilos.sort(key=attrgetter('tiempo_visto'), reverse=True)
    
    for rank, usuario in enumerate(hilos, 1):
        resultado = f"{rank}. {usuario.nombre:15} | Total visto: {usuario.tiempo_visto:3} min | Entradas a sala: {usuario.veces_entrado}"
        print(resultado)
        logging.info(resultado)

if __name__ == "__main__":
    main()