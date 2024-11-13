import intro1  # Importamos el módulo intro.py
import intro2
import cinematicas  # Importamos el módulo cinematicas.py

def main():
    # Llamamos a la función de intro.py
    intro1.mostrar_intro()  # Asumimos que esta función muestra la intro del juego
    intro2.mostrar_seleccion_modo()

    # Luego, podrías llamar a la función de cinematicas.py para reproducir una cinemática
    cinematicas.iniciar_cinematica(1)  # Aquí inicias la primera cinemática

    # Puedes agregar más funcionalidades y llamadas a otras funciones aquí
    # Por ejemplo, si más adelante tienes más cinemáticas:
    # cinematicas.iniciar_cinematica(2)  # Para la segunda cinemática

# Ejecutar la función principal
if __name__ == "__main__":
    main()

