# intro1.py
import pygame
import sys

def mostrar_intro():
    # Inicializa Pygame
    pygame.init()

    # Configuración de la ventana
    ANCHO, ALTO = 1300, 900
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Intro del Juego")

    # Cargar imagen de fondo
    fondo = pygame.image.load("intro 1/intro 1.png")
    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

    # Crear una capa oscura para reducir el brillo
    capa_oscura = pygame.Surface((ANCHO, ALTO))
    capa_oscura.set_alpha(150)  # Nivel de transparencia
    capa_oscura.fill((0, 0, 0))  # Color negro para oscurecer

    # Configuración del texto
    fuente_principal = pygame.font.Font(None, 60)
    texto_principal = fuente_principal.render("Catherine: El Juego", True, (255, 255, 255))
    texto_principal_rect = texto_principal.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))

    # Texto adicional debajo
    fuente_secundaria = pygame.font.Font(None, 48)
    texto_secundario = fuente_secundaria.render("Presiona cualquier tecla para comenzar", True, (255, 255, 255))
    texto_secundario_rect = texto_secundario.get_rect(center=(ANCHO // 2, ALTO // 2 + 50))

    # Bucle principal de la intro
    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                corriendo = False

        # Dibujar fondo, capa oscura y textos en la ventana
        ventana.blit(fondo, (0, 0))
        ventana.blit(capa_oscura, (0, 0))
        ventana.blit(texto_principal, texto_principal_rect)
        ventana.blit(texto_secundario, texto_secundario_rect)

        # Actualizar la pantalla
        pygame.display.flip()
        
pygame.quit()


    


