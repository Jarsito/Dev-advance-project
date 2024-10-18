import pygame
import random
import sys

# Inicializa Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 1200, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter Espacial")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Carga de imágenes
vincent_image = pygame.image.load("vincent.png/vincent.png")
monstruo_image = pygame.image.load("monstruo.png/monstruo.png")
bala_image = pygame.image.load("bala.png/bala.png")
vincent_victory_image = pygame.image.load("vincent_victory.png/vincent_victory.png")

# Escalar la imagen de los enemigos
monstruo_image = pygame.transform.scale(monstruo_image, (int(monstruo_image.get_width() * 0.8), int(monstruo_image.get_height() * 0.8)))

# Clase del jugador
class Player:
    def __init__(self):
        self.image = vincent_image
        self.rect = self.image.get_rect(center=(WIDTH // 2, 50))  # Parte superior
        self.speed = 5
        self.victory_mode = False  # Indica si está en modo victoria

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def activate_victory(self):
        """Cambia a la imagen de victoria."""
        self.image = vincent_victory_image
        self.victory_mode = True

# Clase del enemigo
class Enemy:
    def __init__(self):
        self.image = monstruo_image
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), HEIGHT))  # Parte inferior
        self.speed = random.uniform(0.5, 1.0)  # Velocidad mínima

    def move(self):
        self.rect.y -= self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Clase de la bala
class Bullet:
    def __init__(self, x, y):
        self.image = bala_image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10  # Bala hacia abajo

    def move(self):
        self.rect.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Inicializa objetos
player = Player()
enemies = []
bullets = []
enemy_spawn_time = 60
enemy_spawn_counter = 0
dialog_started = False
dialog_done = False
enemies_killed = 0
kill_limit_per_stage = 25
stage = 0

# Variables para recarga de balas
max_bullets = 5
reload_time = 1000
bullets_loaded = max_bullets
reload_start_time = pygame.time.get_ticks()

# Temporizador para el disparo
last_shot_time = 0
shot_delay = 500

# Reloj para controlar la velocidad de fotogramas
clock = pygame.time.Clock()

# Diálogos por etapa
dialog_texts = [
    [
        "juego: Utiliza las teclas <- y -> para moverte hacia la izquierda y derecha, además del botón ESPACIO para disparar.",
        "Vincent: ¡Ayuda! ¿¡Hay alguien ahí!?",
        "voz: Por abajo se están acercando monstruos.",
        "Voz: ¡Date prisa y ponte a disparar!",
        "Vincent: ¿¡Quién eres!? ¿¡Dónde estamos!?",
        "Voz: ¡No malgastes fuerzas! ¡Si te tocan, te mueres!",
        "Vincent: ¿¡Me muero!? ¡Joder! ¿¡lo dices en serio!?"
    ],
    [
        "Voz: ¡Muévete rápido! No todos los monstruos son lentos, ¿estamos?",
        "Vincent: ¿Y cómo se supone que voy a matarlos?",
        "juego: Mantén pulsado ESPACIO para disparo continuo.",
        "juego: Te puedes mover mientras disparas.",
        "juego: Al principio los monstruos serán más lentos.",
        "juego: Adaptate o muere en el siguiente encuentro.",
        "voz: ¡No dispares sin pensar! Si te quedas sin balas, ¿qué harás?",
        "Vincent: ¿Sin balas?"
    ],
    [
        "juego: Sé preciso al apuntar, controla tu pulso.",
        "juego: La recarga es lenta.",
        "Vincent: ¿¡Por qué cambió mi imagen!?",
        "Voz: Estás cerca del final, ¡apresúrate!",
        "Voz: Que sea lo que tenga que ser. Buena suerte.",
        "Voz: Si sales vivo de aquí, nos volveremos a ver.",
        "Vincent: ¡Espera!"
    ]
]
current_dialog_index = 0
dialog_timer = 0
dialog_duration = 1500  # Duración de cada línea de diálogo en milisegundos
dialog_showing = True
dialog_paused = True  # Para pausar el juego durante el diálogo

# Función para reanudar el juego después del diálogo
def reanudar_juego():
    global dialog_showing, current_dialog_index, dialog_timer, enemies_killed, dialog_paused
    dialog_showing = False
    current_dialog_index = 0
    dialog_timer = 0
    enemies_killed = 0  # Reiniciar los enemigos matados para la siguiente fase
    dialog_paused = False

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if dialog_showing:
        # Mostrar líneas del diálogo progresivamente
        current_time = pygame.time.get_ticks()
        if current_time - dialog_timer >= dialog_duration:
            dialog_timer = current_time
            current_dialog_index += 1
            if current_dialog_index >= len(dialog_texts[stage]):
                reanudar_juego()

    else:
        if not dialog_paused:  # Solo moverse si no está en pausa
            player.move(keys)

            # Generar enemigos
            enemy_spawn_counter += 1
            if enemy_spawn_counter >= enemy_spawn_time:
                enemies.append(Enemy())
                enemy_spawn_counter = 0

            # Mover enemigos y balas
            for enemy in enemies[:]:
                enemy.move()
                if enemy.rect.bottom < 0:
                    game_over = True  # Fin del juego si un enemigo llega al tope

            for bullet in bullets[:]:
                bullet.move()
                if bullet.rect.top > HEIGHT:
                    bullets.remove(bullet)

            # Definir el límite de monstruos que debe matar Vincent en modo victoria
            final_kill_limit = 25

            # Dentro del bucle principal del juego, después de matar monstruos
            for bullet in bullets[:]:
                for enemy in enemies[:]:
                    if bullet.rect.colliderect(enemy.rect):
                        bullets.remove(bullet)
                        enemies.remove(enemy)
                        enemies_killed += 1

                        # Verifica si está en el modo victoria y si ha matado los últimos 25 monstruos
                        if player.victory_mode and enemies_killed >= final_kill_limit:
                            pygame.quit()  # Cerrar la ventana de Pygame
                            sys.exit()  # Salir del programa
                        break

            # Condición para siguiente diálogo
            if enemies_killed >= kill_limit_per_stage:
                stage += 1
                if stage >= len(dialog_texts):
                    # Asegúrate de que stage no exceda el número de diálogos disponibles
                    stage = len(dialog_texts) - 1
                dialog_showing = True
                dialog_timer = pygame.time.get_ticks()
                current_dialog_index = 0
                dialog_paused = True  # Pausar durante el diálogo

                # Cambiar a Vincent Victory después del tercer diálogo (cuando stage es 2, ya que empieza desde 0)
                if stage == 2:
                    player.activate_victory()  # Cambia a la imagen de victoria después del tercer diálogo

        # Dentro del bloque donde el juego se reanuda
        if not dialog_showing and stage == 2:
            #Asegúrate de que Vincent esté en modo victoria
            player.activate_victory()

    # Dibuja todo
    screen.fill(BLACK)
    player.draw(screen)

    if dialog_showing:
        # Mostrar texto del diálogo en pantalla con letras pequeñas
        font = pygame.font.SysFont(None, 24)
        for i in range(current_dialog_index + 1):
            dialog_text = font.render(dialog_texts[stage][i], True, WHITE)
            screen.blit(dialog_text, (20, 20 + i * 30))
    else:
        # Mostrar enemigos y balas solo cuando no haya diálogo
        for enemy in enemies:
            enemy.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)

    pygame.display.flip()
    clock.tick(60)

    # Manejo de disparos
    if keys[pygame.K_SPACE] and not dialog_showing:
        current_time = pygame.time.get_ticks()
        if bullets_loaded > 0 and (current_time - last_shot_time >= shot_delay):
            bullets.append(Bullet(player.rect.centerx, player.rect.bottom))
            bullets_loaded -= 1
            last_shot_time = current_time

    # Manejo de recarga de balas
    if bullets_loaded < max_bullets:
        if pygame.time.get_ticks() - reload_start_time >= reload_time:
            bullets_loaded += 1
            reload_start_time = pygame.time.get_ticks()