import pygame
import sys
import os
from moviepy.editor import VideoFileClip

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Catherine: El Juego")

# Cargar imagen de fondo
ruta_imagen_fondo = "C:/Users/USER/Documents/GitHub/Dev-advance-project/imagenes/Catherine-Full-Body_Header1.png"
if not os.path.isfile(ruta_imagen_fondo):
    print(f"Error: No se pudo cargar la imagen de fondo en {ruta_imagen_fondo}")
    sys.exit()

imagen_fondo = pygame.image.load(ruta_imagen_fondo)
imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO, ALTO))

# Colores y fuentes
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 105, 180)
GREY = (128, 128, 128)
GLOW = (255, 182, 193)
fuente_titulo = pygame.font.SysFont("Georgia", 40, bold=True)
fuente_boton = pygame.font.SysFont("Georgia", 28)
font = pygame.font.SysFont('Arial', 24)

# Cargar el logo con transparencia
logo_path = 'C:/Users/USER/Documents/GitHub/Dev-advance-project/imagenes/logo-ventanisha-catherine (1).png'
logo_image = pygame.image.load(logo_path).convert_alpha()
logo_image = pygame.transform.scale(logo_image, (100, 100))

# Variables de estado
selected_difficulty = 1
glow_effect = 0
glow_direction = 1
scaling_effect = 1
scaling_direction = 1

# Datos de dificultad
difficulties = [
    {"num": 1, "title": "Easy"},
    {"num": 2, "title": "Normal"},
    {"num": 3, "title": "Hard"}
]

# Función para reproducir video y esperar su finalización
def play_cinematic():
    video_path = 'C:/Users/USER/Documents/GitHub/Dev-advance-project/video/Cinematica 1.mp4'
    if os.path.isfile(video_path):
        clip = VideoFileClip(video_path)
        clip.preview()  # Reproducir video
        clip.close()  # Cerrar el video después de reproducirlo
    else:
        print(f"Error: No se encontró el video en {video_path}")

# Función para dibujar texto centrado
def draw_text(text, font, color, surface, x, y):
    texto = font.render(text, True, color)
    rect = texto.get_rect(center=(x, y))
    surface.blit(texto, rect)

# Función para dibujar el logo
def draw_logo():
    logo_rect = logo_image.get_rect(center=(ANCHO - 80, 80))
    pantalla.blit(logo_image, logo_rect)

# Función para dibujar ítem de dificultad con animación de resplandor y escalado
def draw_difficulty_item(num, title, is_selected, y, glow, scaling):
    color = PINK if is_selected else GREY
    rect_color = GLOW if is_selected else WHITE

    # Efecto de resplandor
    glow_alpha = max(0, min(255, 128 + int(glow)))
    glow_surface = pygame.Surface((int((ANCHO - 40) * scaling), int(50 * scaling)))
    glow_surface.set_alpha(glow_alpha)
    glow_surface.fill(rect_color)

    # Dibujar el rectángulo y el texto
    rect = pygame.Rect(20, y, int((ANCHO - 40) * scaling), int(50 * scaling))
    pygame.draw.rect(pantalla, color, rect, border_radius=5)
    pygame.draw.rect(pantalla, WHITE, rect, 2, border_radius=5)
    
    pantalla.blit(glow_surface, rect.topleft)

    title_surface = font.render(title, True, WHITE)
    shadow_surface = font.render(title, True, BLACK)
    pantalla.blit(shadow_surface, (ANCHO // 2 - title_surface.get_width() // 2 + 2, y + 12))
    pantalla.blit(title_surface, (ANCHO // 2 - title_surface.get_width() // 2, y + 10))

# Función para mostrar el menú principal
def show_main_menu():
    global selected_difficulty, glow_effect, glow_direction, scaling_effect, scaling_direction
    clock = pygame.time.Clock()

    while True:
        pantalla.fill(GREY)
        draw_logo()

        y_offset = 150
        for difficulty in difficulties:
            is_selected = selected_difficulty == difficulty["num"]
            current_scaling = scaling_effect if is_selected else 1
            draw_difficulty_item(difficulty["num"], difficulty["title"], is_selected, y_offset, glow_effect, current_scaling)
            y_offset += 70

        glow_effect += glow_direction * 2
        if glow_effect > 50 or glow_effect < -50:
            glow_direction *= -1

        scaling_effect += scaling_direction * 0.01
        if scaling_effect > 1.2 or scaling_effect < 1:
            scaling_direction *= -1

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    selected_difficulty = max(1, selected_difficulty - 1)
                if evento.key == pygame.K_DOWN:
                    selected_difficulty = min(len(difficulties), selected_difficulty + 1)
                if evento.key == pygame.K_RETURN:
                    seleccionar_dificultad()

        clock.tick(30)

# Función para seleccionar la dificultad
def seleccionar_dificultad():
    pantalla.fill(BLACK)
    selected = [d for d in difficulties if d["num"] == selected_difficulty][0]["title"]
    draw_text(f"Dificultad seleccionada: {selected}", fuente_boton, WHITE, pantalla, ANCHO // 2, ALTO // 2)
    pygame.display.flip()
    pygame.time.delay(2000)

    # Reproducir la cinemática y luego iniciar el minijuego
    play_cinematic()

    # Después de la cinemática, iniciar el minijuego
    start_minigame()

# Función para mostrar la pantalla de inicio
def show_start_screen():
    pantalla.blit(imagen_fondo, (0, 0))

    overlay = pygame.Surface((ANCHO, ALTO))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    pantalla.blit(overlay, (0, 0))

    draw_text("Catherine: El Juego", fuente_titulo, WHITE, pantalla, ANCHO // 2, 150)
    draw_text("Presiona cualquier tecla para comenzar", fuente_boton, WHITE, pantalla, ANCHO // 2, 300)
    pygame.display.flip()

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

# Función para iniciar el minijuego de shooter espacial
def start_minigame():
    print("Minijuego iniciado")
    # Aquí puedes agregar el código del minijuego

# Pantalla de inicio
show_start_screen()
