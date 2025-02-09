import random
import pygame

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
