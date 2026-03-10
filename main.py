from info_estudiantes import nombres_estudiantes
from info_proyecto import descripcion_proyecto

def main():
    print("MENÚ DEL PROYECTO")
    print("\n--- Estudiantes ---")
    nombres_estudiantes()
    
    print("\n--- Detalles ---")
    descripcion_proyecto()

if __name__ == "__main__":
    main()