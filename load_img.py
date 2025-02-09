import pygame

# Загрузка изображений
def load_image(name):
    try:
        image = pygame.image.load(name)
    except pygame.error as message:
        print("Не удалось загрузить изображение:", name)
        raise SystemExit(message)
    return image.convert_alpha()
