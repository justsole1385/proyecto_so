import threading
from cine_backend import SalaCine
from usuario import Usuario

def main():
    print("\n--- CONFIGURACIÓN DE LA SIMULACIÓN ---")
    pelicula = input("Nombre de la película: ")
    sala = SalaCine(pelicula=pelicula, filas=3, asientos_por_fila=3)
    
    try:
        cant = int(input("¿Cuántos usuarios intentarán reservar? "))
    except ValueError:
        print("Error: Ingrese un número válido.")
        return

    hilos = []
    for i in range(cant):
        print(f"\nDatos del usuario {i+1}:")
        nombre = input("Nombre: ")
        asiento = input("Asiento (Ej: A1, B2): ").upper()
        hilos.append(Usuario(nombre=nombre, asiento_deseado=asiento, sala=sala))
    
    print("\n--- INICIANDO RESERVAS SIMULTÁNEAS ---")
    for h in hilos: h.start()
    for h in hilos: h.join()
    
    sala.mostrar_estado_sala()import threading
from cine_backend import SalaCine
from usuario import Usuario

def main():
    print("\n--- CONFIGURACIÓN DE LA SIMULACIÓN ---")
    pelicula = input("Nombre de la película: ")
    sala = SalaCine(pelicula=pelicula, filas=3, asientos_por_fila=3)
    
    try:
        cant = int(input("¿Cuántos usuarios intentarán reservar? "))
    except ValueError:
        print("Error: Ingrese un número válido.")
        return

    hilos = []
    for i in range(cant):
        print(f"\nDatos del usuario {i+1}:")
        nombre = input("Nombre: ")
        asiento = input("Asiento (Ej: A1, B2): ").upper()
        hilos.append(Usuario(nombre=nombre, asiento_deseado=asiento, sala=sala))
    
    print("\n--- INICIANDO RESERVAS SIMULTÁNEAS ---")
    for h in hilos: h.start()
    for h in hilos: h.join()
    
    sala.mostrar_estado_sala()