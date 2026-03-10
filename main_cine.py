import threading
from cine_backend import SalaCine
from usuario import Usuario

def main():
    print("--- INICIANDO SISTEMA DE RESERVAS DE CINE ---")
    sala_marvel = SalaCine(pelicula="Avengers", filas=2, asientos_por_fila=3)
    
    print("\n--- INTENTO DE COMPRAS SIMULTÁNEAS (CONDICIÓN DE CARRERA PROVOCADA ADREDE) ---")
    
    # karel, JuanDiego y Leonor intentan comprar "A1" al mismo tiempo
    hilo1 = Usuario(nombre="karel", asiento_deseado="A1", sala=sala_marvel)
    hilo2 = Usuario(nombre="JuanDiego", asiento_deseado="A1", sala=sala_marvel)
    hilo3 = Usuario(nombre="Leonor", asiento_deseado="A1", sala=sala_marvel)
    
    # Raul compra un asiento libre sin problemas
    hilo4 = Usuario(nombre="Raul", asiento_deseado="B2", sala=sala_marvel)

    # Iniciamos los hilos simultáneamente para provocar la condición de carrera
    hilo1.start()
    hilo2.start()
    hilo3.start()
    hilo4.start()

    
    hilo1.join()
    hilo2.join()
    hilo3.join()
    hilo4.join()

    # Imprimir el resumen final
    sala_marvel.mostrar_estado_sala()

if __name__ == "__main__":
    main()