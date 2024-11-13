# intro2.py
import pygame
import sys

def mostrar_seleccion_modo():
    # Configuración de la ventana de selección
    ANCHO, ALTO = 1300, 900
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Seleccionar Modo de Juego")

    # Cargar nueva imagen de fondo
    fondo_dificultad = pygame.image.load("logo 1/logo 1.png")
    fondo_dificultad = pygame.transform.scale(fondo_dificultad, (ANCHO, ALTO))

    # Crear una capa oscura para reducir el brillo en la segunda ventana
    capa_oscura = pygame.Surface((ANCHO, ALTO))
    capa_oscura.set_alpha(150)  # Nivel de transparencia
    capa_oscura.fill((0, 0, 0))  # Color negro para oscurecer

    # Configuración de los botones y sus descripciones
    fuente_botones = pygame.font.Font(None, 30)
    descripciones = [
        "Golden Theater: ¡Disfruta de la historia, metete en la piel del atormentado protagonista y guialo a la libertad!",
        "Babel: ¡Cuando te hayas familiarizado con el juego, enfrentate a los retos!",
        "Facil: Si eres de los jugadores a quienes lo que mas les interesa es el argumento, esto es para ti. ¡Perfecto para principiantes!",
        "Normal: ¡Enfrentate a dificiles rompecabezas y vive las emociones que solo puedes experimentar en Catherine! Equilibrado para jugadores de nivel medio.",
        "Dificil: ¿Eres un masoquista total? Los rompecabezas de este modo son endiabladamente dificiles, y estan destinados a los mejores jugadores."
    ]

    # Botones de selección
    botones_modo = [
        {"texto": "Golden Theater", "rect": pygame.Rect(100, ALTO // 2 - 100, 300, 30), "activo": True},
        {"texto": "Babel", "rect": pygame.Rect(100, ALTO // 2, 300, 30), "activo": False}
    ]
    botones_dificultad = [
        {"texto": "Facil", "rect": pygame.Rect(500, ALTO // 2 - 100, 300, 30), "activo": True},
        {"texto": "Normal", "rect": pygame.Rect(500, ALTO // 2, 300, 30), "activo": False},
        {"texto": "Dificil", "rect": pygame.Rect(500, ALTO // 2 + 100, 300, 30), "activo": False}
    ]

    # Variables de control
    seleccion_modo = 0
    seleccion_dificultad = 0
    modo_seleccionado = False
    texto_descripcion = ""

    def dividir_texto(texto, fuente, max_ancho):
        """ Divide el texto en múltiples líneas si es necesario. """
        palabras = texto.split(' ')
        lineas = []
        linea_actual = palabras[0]
        for palabra in palabras[1:]:
            prueba_linea = f"{linea_actual} {palabra}"
            if fuente.size(prueba_linea)[0] <= max_ancho:
                linea_actual = prueba_linea
            else:
                lineas.append(linea_actual)
                linea_actual = palabra
        lineas.append(linea_actual)
        return lineas

    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if not modo_seleccionado:
                    if evento.key == pygame.K_DOWN:
                        seleccion_modo = (seleccion_modo + 1) % len(botones_modo)
                    elif evento.key == pygame.K_UP:
                        seleccion_modo = (seleccion_modo - 1) % len(botones_modo)
                    elif evento.key == pygame.K_RETURN and botones_modo[seleccion_modo]["activo"]:
                        modo_seleccionado = True
                else:
                    if evento.key == pygame.K_DOWN:
                        seleccion_dificultad = (seleccion_dificultad + 1) % len(botones_dificultad)
                    elif evento.key == pygame.K_UP:
                        seleccion_dificultad = (seleccion_dificultad - 1) % len(botones_dificultad)
                    elif evento.key == pygame.K_RETURN and botones_dificultad[seleccion_dificultad]["activo"]:
                        print("Dificultad seleccionada:", botones_dificultad[seleccion_dificultad]["texto"])
                        corriendo = False

        # Actualizar la descripción según el botón seleccionado
        if not modo_seleccionado:
            texto_descripcion = descripciones[seleccion_modo]
        else:
            texto_descripcion = descripciones[seleccion_dificultad + 2]

        # Dibujar fondo y capa oscura
        ventana.blit(fondo_dificultad, (0, 0))
        ventana.blit(capa_oscura, (0, 0))

        # Dibujar botones de selección de modo
        for i, boton in enumerate(botones_modo):
            color = (0, 0, 204) if i == seleccion_modo else (255, 255, 255)
            if not boton["activo"]:
                color = (255, 0, 0)
            pygame.draw.rect(ventana, color, boton["rect"])
            texto_boton = fuente_botones.render(boton["texto"], True, (0, 0, 0))
            ventana.blit(texto_boton, texto_boton.get_rect(center=boton["rect"].center))

        # Dibujar botones de dificultad si Golden Theater ha sido seleccionado
        if modo_seleccionado:
            for i, boton in enumerate(botones_dificultad):
                color = (0, 0, 204) if i == seleccion_dificultad else (255, 255, 255)
                if not boton["activo"]:
                    color = (255, 0, 0)
                pygame.draw.rect(ventana, color, boton["rect"])
                texto_boton = fuente_botones.render(boton["texto"], True, (0, 0, 0))
                ventana.blit(texto_boton, texto_boton.get_rect(center=boton["rect"].center))

        # Mostrar el texto descriptivo en varias líneas, en verde y alineado con los botones
        fuente_descripcion = pygame.font.Font(None, 33)
        lineas_descripcion = dividir_texto(texto_descripcion, fuente_descripcion, 300)  # Ajusta el ancho máximo si es necesario
        inicio_y = ALTO // 2 - 100  # Alineación a la altura de los botones
        for i, linea in enumerate(lineas_descripcion):
            texto_descripcion_render = fuente_descripcion.render(linea, True, (255, 255, 255))
            ventana.blit(texto_descripcion_render, (900, inicio_y + i * 40))

        pygame.display.flip()

pygame.quit()