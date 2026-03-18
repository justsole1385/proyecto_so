import main_cine
from info_estudiantes import nombres_estudiantes
from info_proyecto import descripcion_proyecto

def mostrar_menu():
    print("\n" + "="*30)
    print("      SISTEMA DE CINE")
    print("="*30)
    print("1. Ver Integrantes")
    print("2. Ver Detalles del Proyecto")
    print("3. EJECUTAR SIMULACIÓN ")
    print("4. Salir")
    return input("Seleccione una opción: ")

def main():
    while True:
        opcion = mostrar_menu()
        if opcion == "1":
            nombres_estudiantes()
        elif opcion == "2":
            descripcion_proyecto()
        elif opcion == "3":
            main_cine.main()
        elif opcion == "4":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida, intente de nuevo.")

if __name__ == "__main__":
    main()