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
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Carga de imágenes
vincent_image = pygame.image.load("vincent.png/vincent.png")
monstruo_image = pygame.image.load("monstruo.png/monstruo.png")
bala_image = pygame.image.load("bala.png/bala.png")
vincent_victory_image = pygame.image.load("vincent_victory.png/vincent_victory.png")  # Nueva imagen de Vincent

# Escalar la imagen de los enemigos
monstruo_image = pygame.transform.scale(monstruo_image, (int(monstruo_image.get_width() * 0.8), int(monstruo_image.get_height() * 0.8)))

# Clase del jugador
class Player:
    def _init_(self):
        self.image = vincent_image
        self.rect = self.image.get_rect(center=(WIDTH // 2, 50))  # Parte superior
        self.speed = 5

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def update_image(self, remaining_time):
        # Cambia la imagen a la de victoria cuando queden 20 segundos o menos
        if remaining_time <= 20:
            self.image = vincent_victory_image

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Clase del enemigo
class Enemy:
    def _init_(self):
        self.image = monstruo_image
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), HEIGHT))  # Parte inferior
        # Aseguramos que la velocidad mínima sea mayor que 0
        self.speed = random.uniform(0.5, 1.0)  # Reducir la velocidad a la mitad con mínimo de 0.5

    def move(self):
        self.rect.y -= self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Clase de la bala
class Bullet:
    def _init_(self, x, y):
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

# Variables del juego
game_over = False
victory = False

# Configurar tiempo de juego a 3 minutos y 40 segundos
game_duration = 1 * 60 + 5  # 3 minutos y 40 segundos en segundos
start_ticks = pygame.time.get_ticks()

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over and not victory:
        keys = pygame.key.get_pressed()
        player.move(keys)

        # Genera enemigos
        enemy_spawn_counter += 1
        if enemy_spawn_counter >= enemy_spawn_time:
            enemies.append(Enemy())
            enemy_spawn_counter = 0

        # Mueve enemigos y balas
        for enemy in enemies[:]:
            enemy.move()
            if enemy.rect.bottom < 0:
                game_over = True  # Fin del juego si un enemigo alcanza el tope

        for bullet in bullets[:]:
            bullet.move()
            if bullet.rect.top > HEIGHT:
                bullets.remove(bullet)

        # Manejo de colisiones entre balas y enemigos
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    break

        # Manejo de colisiones entre enemigos y el jugador
        for enemy in enemies:
            if enemy.rect.colliderect(player.rect):
                game_over = True  # Fin del juego si un enemigo impacta al jugador

        # Calcula el tiempo restante
        elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000
        remaining_time = game_duration - elapsed_time
        if remaining_time <= 0:
            game_over = True  # Fin del juego si se acaba el tiempo
        
        # Cambia la imagen del jugador si quedan 20 segundos o menos
        player.update_image(remaining_time)

        # Dibuja todo
        screen.fill(BLACK)
        player.draw(screen)

        for enemy in enemies:
            enemy.draw(screen)

        for bullet in bullets:
            bullet.draw(screen)

        # Dibuja la barra de balas más pequeña
        bullet_bar_width = 12  # Ancho más pequeño de la barra de balas
        bullet_bar_height = 25  # Altura más pequeña de la barra de balas
        for i in range(max_bullets):
            color = WHITE if i < bullets_loaded else (100, 100, 100)
            pygame.draw.rect(screen, color, (10 + i * (bullet_bar_width + 5), 10, bullet_bar_width, bullet_bar_height))

        # Dibuja el temporizador con fuente más pequeña
        font = pygame.font.SysFont(None, 18)
        timer_text = font.render(f"Tiempo Restante: {remaining_time}", True, WHITE)
        screen.blit(timer_text, (10, 50))

    elif game_over:
        font = pygame.font.SysFont(None, 55)
        text = font.render("Game Over", True, RED)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

    elif victory:
        font = pygame.font.SysFont(None, 55)
        text = font.render("¡Has Ganado!", True, GREEN)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(60)

    # Manejo de disparos
    if keys[pygame.K_SPACE]:
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