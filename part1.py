import pygame
import sys
import os

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Catherine: El Juego")

# Cargar imagen de fondo
ruta_imagen_fondo = "C:/Users/USER/Desktop/Nueva carpeta/Catherine-Full-Body_Header1.png"
if not os.path.isfile(ruta_imagen_fondo):
    print(f"Error: No se pudo cargar la imagen de fondo en {ruta_imagen_fondo}")
    sys.exit()

imagen_fondo = pygame.image.load(ruta_imagen_fondo)
imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO, ALTO))

# Fuentes y colores
fuente_titulo = pygame.font.SysFont("Georgia", 40, bold=True)
fuente_boton = pygame.font.SysFont("Georgia", 28)
color_texto = (255, 255, 255)
color_fondo = (51, 51, 51)
color_hover = (255, 255, 255)
color_boton_normal = (0, 51, 102)
color_boton_hover = (0, 76, 153)

# Función para dibujar botones redondeados con efecto hover
def dibujar_boton(texto, x, y, ancho, alto, color_fondo, color_hover, funcion):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Verificar si el mouse está sobre el botón
    if x < mouse[0] < x + ancho and y < mouse[1] < y + alto:
        pygame.draw.rect(pantalla, color_hover, (x, y, ancho, alto), border_radius=10)
        if click[0] == 1:
            funcion()
    else:
        pygame.draw.rect(pantalla, color_fondo, (x, y, ancho, alto), border_radius=10)

    # Dibujar el texto del botón
    texto_boton = fuente_boton.render(texto, True, color_texto)
    pantalla.blit(texto_boton, (x + (ancho - texto_boton.get_width()) // 2, y + (alto - texto_boton.get_height()) // 2))

# Función para mostrar el menú principal con botones de dificultad
def show_main_menu():
    pantalla.fill(color_fondo)
    draw_text("Elige tu dificultad:", fuente_titulo, color_texto, pantalla, ANCHO // 2, 100)

    # Dibujar los botones con estilos mejorados
    dibujar_boton("Easy", 300, 250, 200, 60, color_boton_normal, color_boton_hover, lambda: seleccionar_dificultad("Easy"))
    dibujar_boton("Normal", 300, 350, 200, 60, color_boton_normal, color_boton_hover, lambda: seleccionar_dificultad("Normal"))
    dibujar_boton("Hard", 300, 450, 200, 60, color_boton_normal, color_boton_hover, lambda: seleccionar_dificultad("Hard"))

    pygame.display.flip()

    # Bucle de eventos del menú
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Función para seleccionar la dificultad
def seleccionar_dificultad(dificultad):
    pantalla.fill(color_fondo)
    draw_text(f"Has seleccionado el modo {dificultad}", fuente_boton, color_texto, pantalla, ANCHO // 2, ALTO // 2)
    pygame.display.flip()
    pygame.time.delay(2000)
    show_start_screen()  # Volver a la pantalla de inicio

# Función para dibujar texto centrado
def draw_text(text, font, color, surface, x, y):
    texto = font.render(text, True, color)
    rect = texto.get_rect(center=(x, y))
    surface.blit(texto, rect)

# Mostrar la pantalla de inicio con un fondo elegante
def show_start_screen():
    pantalla.blit(imagen_fondo, (0, 0))

    # Crear un fondo difuminado para el texto
    overlay = pygame.Surface((ANCHO, ALTO))
    overlay.set_alpha(200)  # Transparencia del fondo
    overlay.fill((0, 0, 0))  # Fondo negro con transparencia
    pantalla.blit(overlay, (0, 0))

    draw_text("Catherine: El Juego", fuente_titulo, color_texto, pantalla, ANCHO // 2, 150)
    draw_text("Presiona cualquier tecla para comenzar", fuente_boton, color_texto, pantalla, ANCHO // 2, 300)
    pygame.display.flip()

    # Esperar a que el usuario presione una tecla
    esperar_tecla()

# Función para esperar a que el usuario presione una tecla
def esperar_tecla():
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                esperando = False
                show_main_menu()

# Pantalla de inicio
show_start_screen()
