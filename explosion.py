
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

