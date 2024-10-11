import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Para manejar imágenes PNG

# Función para mostrar los diálogos cinemáticos
def show_dialog(dialogs, current=0):
    if current < len(dialogs):
        dialog_label.config(text=dialogs[current])  # Actualizar el texto del diálogo
        window.after(5000, lambda: show_dialog(dialogs, current + 1))  # Muestra el siguiente diálogo cada 5 segundos

# Función para confirmar si se desea empezar en modo Easy
def confirm_easy_mode():
    response = messagebox.askyesno("Confirmar", "¿Quieres empezar en este modo?")
    if response:
        messagebox.showinfo("Catherine", "Venga, relájate y disfruta de la extraña historia de 'Catherine'.")
        start_cinematic_1()  # Inicia los diálogos cinematográficos
    else:
        show_main_menu()  # Regresa al menú principal si no confirma

# Cinemática 1: Introducción de Trisha
def start_cinematic_1():
    dialogs = [
        "El mundo entero es un teatro; y todos los hombres y mujeres simplemente comediantes.\nShakespeare (Como gustéis)",
        "Trisha: Cuando el cielo nocturno se carga de glamour ¡es porque te aguarda una bonita historia!",
        "Trisha: Buenas noches. Bienvenidos a Golden Playhouse.",
        "Trisha: Yo seré vuestra guía esta noche: Trisha; 'la Venus de Medianoche'.",
        "Trisha: ¿Habéis oído ese rumor tan tétrico?",
        "Trisha: Dicen que si te caes durante un sueño y no te despiertas antes de aterrizar...",
        "Trisha: ... ¡mueres en la vida real!",
        "Trisha: La historia de esta noche es 'Catherine', una historia de terror romántico poco convencional.",
        "Trisha: Un hombre con cierto 'hechizo' está pasando una semana terrible.",
        "Trisha: El héroe de esta historia es Vincent Brooks, de 32 años.",
        "Trisha: Es un tipo formal y amable...",
        "Trisha: Pero un día, empieza a tener pesadillas horrorosas.",
        "Trisha: Además, se le viene encima una ola de dulce seducción...",
        "Trisha: ¡Qué juguetón! ¿verdad?",
        "Trisha: ¿Será capaz de superar todos los 'bloques' de su vida?",
        "Trisha: ¡Todo depende de vosotros, espectadores!",
        "Trisha: ¡Perdonad que os mantenga en vilo! ¡Arriba el telón!",
        "Trisha: Y ahora, ¡a disfrutar del show! Hasta que nos volvamos a encontrar..."
    ]
    clear_screen()  # Limpia la pantalla antes de mostrar los diálogos
    
    # Crear la etiqueta para los diálogos si no existe ya
    global dialog_label
    dialog_label = tk.Label(window, text="", font=("Arial", 12), wraplength=500, justify="center", bg="#333333", fg="white")
    canvas.create_window(400, 300, window=dialog_label)  # Colocar la etiqueta de diálogos en el canvas
    
    show_dialog(dialogs)  # Comienza a mostrar los diálogos

# Menú principal del juego para elegir la dificultad
def show_main_menu():
    clear_screen()

    # Crear una etiqueta que diga "Elige tu dificultad" dentro del canvas
    label = tk.Label(window, text="Elige tu dificultad:", font=("Arial", 14), bg="#333333", fg="white")
    canvas.create_window(400, 100, window=label)  # Colocar el label en el canvas

    # Crear botones sobre el canvas
    easy_button = tk.Button(window, text="Easy", command=confirm_easy_mode, bg="#ff9999", fg="black", font=("Arial", 12, "bold"))
    normal_button = tk.Button(window, text="Normal", command=lambda: messagebox.showinfo("Catherine", "Modo Normal seleccionado."), bg="#ffcc66", font=("Arial", 12, "bold"))
    hard_button = tk.Button(window, text="Hard", command=lambda: messagebox.showinfo("Catherine", "Modo Hard seleccionado."), bg="#ff6666", font=("Arial", 12, "bold"))

    # Posicionar los botones dentro del canvas
    canvas.create_window(400, 200, window=easy_button)  # Botón en el centro del canvas
    canvas.create_window(400, 250, window=normal_button)  # Botón debajo
    canvas.create_window(400, 300, window=hard_button)  # Botón debajo

# Función para limpiar la pantalla antes de cambiar la interfaz
def clear_screen():
    canvas.delete("all")  # Borra todo lo que hay en el canvas

# Pantalla de inicio avanzada
def show_start_screen():
    clear_screen()

    # Título del juego
    title_label = tk.Label(window, text="Catherine: El Juego", font=("Courier", 30, "bold"), fg="white", bg="#333333")
    canvas.create_window(400, 150, window=title_label)  # Posiciona el título

    # Botón de "Comenzar juego"
    start_button = tk.Button(window, text="Comenzar juego", command=show_main_menu, bg="#00cc66", fg="white", font=("Arial", 16, "bold"), activebackground="#00b359", activeforeground="white")
    canvas.create_window(400, 250, window=start_button)  # Botón centrado en el canvas

    # Efecto hover para el botón
    def on_enter(e):
        start_button.config(bg="#00e673")

    def on_leave(e):
        start_button.config(bg="#00cc66")

    start_button.bind("<Enter>", on_enter)
    start_button.bind("<Leave>", on_leave)

    # Cargar imagen con Pillow
    try:
        image = Image.open("C:/Users/USER/Desktop/Nueva carpeta/Catherine-Full-Body_Header1.png")
        background_img = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, image=background_img, anchor="nw")  # Dibuja la imagen en el canvas

        # Mantener la referencia de la imagen
        window.background_img = background_img
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")

# Configuración básica de la ventana de Tkinter
window = tk.Tk()
window.title("Catherine: El Juego")
window.geometry("800x600")
window.config(bg="#333333")

# Crear un Canvas para manejar la imagen de fondo y los botones
canvas = tk.Canvas(window, width=800, height=600)
canvas.pack(fill="both", expand=True)  # El canvas ocupa todo el espacio de la ventana

# Mostrar pantalla de inicio avanzada
show_start_screen()

# Iniciar la interfaz
window.mainloop()
