import tkinter as tk
from subprocess import Popen
import threading
import os

# Agregar la ruta de ffplay al PATH de Python temporalmente
os.environ["PATH"] += os.pathsep + r"C:\Users\User\Downloads\ffmpeg-2024-11-11-git-96d45c3b21-essentials_build\ffmpeg-2024-11-11-git-96d45c3b21-essentials_build\bin"

# Variables globales
proceso_video = None
ventana_boton = None
ventana_temporal = None  # Agregar referencia para la ventana temporal

def iniciar_cinematica(uno):
    global proceso_video, ventana_boton, ventana_temporal

    # Verificar si ffplay está en el PATH
    if not any(os.access(os.path.join(path, 'ffplay.exe'), os.X_OK) for path in os.environ["PATH"].split(os.pathsep)):
        print("Error: 'ffplay' no se encuentra en el PATH. Asegúrate de que FFmpeg esté instalado y accesible.")
        return

    # Ruta de la cinemática específica
    ruta_video = f"Cinematica {uno}/Cinematica {uno}.mkv"

    # Función para iniciar la reproducción de video
    def reproducir_video():
        global proceso_video
        try:
            # Ejecutar el video usando ffplay
            proceso_video = Popen(['ffplay', '-autoexit', '-x', '1300', '-y', '900', ruta_video])
            proceso_video.wait()  # Esperar a que el proceso de video termine
            # Después de que el video termine, cerrar la ventana de Tkinter
            ventana_temporal.quit()  # Esto terminará el mainloop de Tkinter
        except Exception as e:
            print(f"Error al reproducir la cinemática {uno}: {e}")

    # Crear hilo para la reproducción de video
    video_thread = threading.Thread(target=reproducir_video)
    video_thread.start()

    # Función para omitir la cinemática
    def omitir_cinematica():
        global proceso_video
        if proceso_video:
            proceso_video.terminate()  # Terminar el proceso del video
        if ventana_boton and ventana_boton.winfo_exists():
            ventana_boton.destroy()  # Cerrar la ventana del botón

    # Función para mostrar el botón de "Omitir"
    def mostrar_boton():
        global ventana_boton
        ventana_boton = tk.Toplevel()
        ventana_boton.geometry("80x40+1480+900")
        ventana_boton.overrideredirect(True)
        ventana_boton.attributes("-topmost", True)
        
        # Crear y agregar el botón "Omitir"
        boton_omitir = tk.Button(ventana_boton, text="Omitir", command=omitir_cinematica)
        boton_omitir.pack(expand=True)

        # Programar el cierre automático del botón después de 10 segundos
        ventana_boton.after(10000, lambda: ventana_boton.destroy() if ventana_boton.winfo_exists() else None)

        # Comienza a observar el estado de la ventana para cerrarla junto con el botón
        observar_cierre()

    # Función para observar el estado de la ventana de la cinemática
    def observar_cierre():
        if not proceso_video or proceso_video.poll() is not None:  # Si el video ha terminado
            if ventana_boton and ventana_boton.winfo_exists():
                ventana_boton.after(500, lambda: ventana_boton.destroy())
        else:
            ventana_temporal.after(100, observar_cierre)  # Verificar cada 0.1 segundos si la ventana está cerrada

    # Crear una instancia temporal de Tk y ocultarla inmediatamente
    ventana_temporal = tk.Tk()
    ventana_temporal.withdraw()

    # Usar after para mostrar el botón "Omitir" después de 3 segundos
    ventana_temporal.after(3000, mostrar_boton)

    # Iniciar el bucle principal de la ventana temporal
    ventana_temporal.mainloop()
