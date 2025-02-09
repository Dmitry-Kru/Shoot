import sys
import random
import math
from time import sleep

import pygame
from pygame.locals import *

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


