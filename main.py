import sys
import random
import math
from time import sleep

import pygame
from pygame.locals import *

# Размеры окна
WIDTH = 800
HEIGHT = 600

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)


# Загрузка изображений
def load_image(name):
    try:
        image = pygame.image.load(name)
    except pygame.error as message:
        print("Не удалось загрузить изображение:", name)
        raise SystemExit(message)
    return image.convert_alpha()


# Инициализация мишени
def init_target(position):
    target_image = load_image('img/target.png')
    target_rect = target_image.get_rect(center=position)
    speed_x = random.randint(-4, 4)
    speed_y = random.randint(-4, 4)
    return target_image, target_rect, speed_x, speed_y


# Обновление положения мишени
def update_target(target_image, target_rect, speed_x, speed_y):
    target_rect.x += speed_x
    target_rect.y += speed_y

    if target_rect.left <= 0 or target_rect.right >= WIDTH:
        speed_x *= -1
    if target_rect.top <= 0 or target_rect.bottom >= HEIGHT:
        speed_y *= -1

    return target_image, target_rect, speed_x, speed_y


# Инициализация препятствия
def init_obstacle(position, size, color):
    obstacle_surface = pygame.Surface(size)
    obstacle_surface.fill(color)
    obstacle_rect = obstacle_surface.get_rect(center=position)
    speed_x = random.choice([-3, 3])
    speed_y = random.choice([-3, 3])
    return obstacle_surface, obstacle_rect, speed_x, speed_y


# Обновление положения препятствия
def update_obstacle(obstacle_surface, obstacle_rect, speed_x, speed_y):
    obstacle_rect.x += speed_x
    obstacle_rect.y += speed_y

    if obstacle_rect.left <= 0 or obstacle_rect.right >= WIDTH:
        speed_x *= -1
    if obstacle_rect.top <= 0 or obstacle_rect.bottom >= HEIGHT:
        speed_y *= -1

    return obstacle_surface, obstacle_rect, speed_x, speed_y


# Инициализация взрыва
def init_explosion(center):
    images = [
        load_image('img/oops1.png'),
        load_image('img/oops2.png'),
        load_image('img/oops3.png')
    ]
    index = 0
    explosion_image = images[index]
    explosion_rect = explosion_image.get_rect(center=center)
    timer = 0
    return images, index, explosion_image, explosion_rect, timer


# Обновление взрыва
def update_explosion(images, index, explosion_image, explosion_rect, timer):
    timer += 1
    if timer % 10 == 0:
        index += 1
        if index >= len(images):
            return None, None, None, None, None
        else:
            explosion_image = images[index]
            explosion_rect = explosion_image.get_rect(center=explosion_rect.center)

    return images, index, explosion_image, explosion_rect, timer



pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Тир")
icon = load_image('img/target.png')  # Загрузим иконку приложения
pygame.display.set_icon(icon)

background_color = WHITE

font = pygame.font.Font(None, 36)

# Инициализация мишени
target_image, target_rect, target_speed_x, target_speed_y = init_target(
    (random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)))

obstacles = []
for _ in range(10):
    obstacle_size = (40, 40)
    obstacle_position = (
        random.randint(obstacle_size[0], WIDTH - obstacle_size[0]),
        random.randint(obstacle_size[1], HEIGHT - obstacle_size[1]))
    obstacle_color = random.choice([RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE])
    obstacle_surface, obstacle_rect, obstacle_speed_x, obstacle_speed_y = init_obstacle(
        obstacle_position, obstacle_size, obstacle_color)
    obstacles.append((obstacle_surface, obstacle_rect, obstacle_speed_x, obstacle_speed_y))

explosions = []

score = 0

stop_game = False

clock = pygame.time.Clock()

while not stop_game:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if target_rect.collidepoint(pos):
                images, index, explosion_image, explosion_rect, timer = init_explosion(target_rect.center)
                explosions.append((images, index, explosion_image, explosion_rect, timer))

                # Увеличение счета
                score += 1

                # Перезапуск мишени
                target_image, target_rect, target_speed_x, target_speed_y = init_target(
                    (random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)))

    # Обновление мишени
    target_image, target_rect, target_speed_x, target_speed_y = update_target(
        target_image, target_rect, target_speed_x, target_speed_y)

    # Обновление препятствий
    updated_obstacles = []
    for obstacle_surface, obstacle_rect, obstacle_speed_x, obstacle_speed_y in obstacles:
        obstacle_surface, obstacle_rect, obstacle_speed_x, obstacle_speed_y = update_obstacle(
            obstacle_surface, obstacle_rect, obstacle_speed_x, obstacle_speed_y)
        updated_obstacles.append((obstacle_surface, obstacle_rect, obstacle_speed_x, obstacle_speed_y))
    obstacles = updated_obstacles

    # Обновление взрывов
    updated_explosions = []
    for images, index, explosion_image, explosion_rect, timer in explosions:
        images, index, explosion_image, explosion_rect, timer = update_explosion(
            images, index, explosion_image, explosion_rect, timer)
        if images is not None:
            updated_explosions.append((images, index, explosion_image, explosion_rect, timer))
    explosions = updated_explosions

    # Отображение фона
    screen.fill(background_color)

    # Отображение мишени
    screen.blit(target_image, target_rect)

    # Отображение препятствий
    for obstacle_surface, obstacle_rect, _, _ in obstacles:
        screen.blit(obstacle_surface, obstacle_rect)

    # Отображение взрывов
    for _, _, explosion_image, explosion_rect, _ in explosions:
        screen.blit(explosion_image, explosion_rect)

    # Отображение счета
    score_text = font.render(f"Счёт: {score}", True, BLACK)
    screen.blit(score_text, (20, 20))

    # Плавная смена цвета фона
    background_color = ((background_color[0] + 1) % 256,
                        (background_color[1] + 2) % 256,
                        (background_color[2] + 3) % 256)

    pygame.display.flip()
    clock.tick(60)


