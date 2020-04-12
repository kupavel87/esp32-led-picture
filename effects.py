import settings
import led_init
import random


class Fire:
    def __init__(self, size=9):
        self.matrixValue = [[0] * settings.led_width for _ in range(settings.led_height)]
        self.size = size
        self.valueMask = [
            [16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16],
            [32, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 32],
            [64, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 64],
            [96, 32, 16, 0, 0, 0, 0, 0, 0, 16, 32, 96],
            [128, 64, 32, 16, 0, 0, 0, 0, 16, 32, 64, 128],
            [160, 96, 64, 32, 16, 0, 0, 16, 32, 64, 96, 160],
            [192, 128, 96, 64, 32, 16, 16, 32, 64, 96, 128, 192],
            [255, 160, 128, 96, 64, 32, 32, 64, 96, 128, 160, 255],
            [255, 192, 160, 128, 96, 64, 64, 96, 128, 160, 192, 255]
        ]
        self.hueMask = [
            [1, 1, 11, 19, 25, 25, 27, 22, 11, 1, 1, 1],
            [1, 1, 8, 13, 19, 25, 25, 19, 8, 1, 1, 1],
            [0, 1, 8, 8, 13, 16, 19, 16, 8, 1, 1, 0],
            [0, 1, 1, 5, 11, 13, 13, 13, 5, 1, 1, 0],
            [0, 1, 1, 5, 11, 11, 11, 11, 5, 1, 1, 0],
            [0, 0, 0, 1, 5, 8, 8, 5, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 5, 5, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0]
        ]


# Эффект падающего снега
def snowRoutine(scale, pcnt, hsv):
    for x in range(settings.led_width):
        for y in range(settings.led_height - 1):
            led_init.setColorXY(x, y, led_init.getColorXY(x, y + 1))

    for x in range(settings.led_width):
        if led_init.getColorXY(x, settings.led_height - 2) and not random.randint(0, scale):
            h, s, v = hsv
            newV = int(v * (100 - random.randint(0, pcnt)) / 100)
            color = led_init.hsv2rgb_rainbow(h, s, newV)
            led_init.setColorXY(x, settings.led_height - 1, color)
        else:
            led_init.setColorXY(x, settings.led_height - 1, (0, 0, 0))


# Эффект матрицы, падающих букв
def matrixRoutine(scale):
    for x in range(settings.led_width):
        for y in range(settings.led_height - 1):
            led_init.setColorXY(x, y, led_init.getColorXY(x, y + 1))

    for x in range(settings.led_width):
        _, g, _ = led_init.getColorXY(x, settings.led_height - 1)
        if not g:
            if not random.randint(0, scale):
                led_init.setColorXY(x, settings.led_height - 1, (0, 92, 0))
        elif g <= 16:
            led_init.setColorXY(x, settings.led_height - 1, (0, 0, 0))
        else:
            led_init.setColorXY(x, settings.led_height - 1, (0, g - 16, 0))


def rainbowRoutine(status, type_):
    for x in reversed(range(1, settings.led_width)):
        for y in range(settings.led_height):
            led_init.setColorXY(x, y, led_init.getColorXY(x - 1, y))
    if type_:
        color = led_init.hsv2rgb_rainbow(int(status * 255 / (settings.led_width - 1)), 255, 128)
    else:
        color = led_init.hsv2rgb(int(status * 255 / (settings.led_width - 1)), 255, 128)
    for y in range(settings.led_height):
        led_init.setColorXY(0, y, color)
    return (status + 1) % (settings.led_width - 1)


def drawFire(fire, pcnt, scale):
    for y in reversed(range(1, min(settings.led_height, fire.size))):
        fire.matrixValue[y] = fire.matrixValue[y - 1]
    line = [random.randint(64, 255) for _ in range(settings.led_width)]
    fire.matrixValue[0] = [_ for _ in line]
    # each row interpolates with the one before it
    for y in reversed(range(1, min(settings.led_height, fire.size))):
        for x in range(settings.led_width):
            nextV = int((((100.0 - pcnt) * fire.matrixValue[y][x] + pcnt * fire.matrixValue[y - 1][x]) / 100.0) - fire.valueMask[y][x % 12])
            color = led_init.hsv2rgb(int(scale * 2.3 + fire.hueMask[y][x % 12]), 255, max(0, nextV))
            led_init.setColorXY(x, y, color)
    # first row interpolates with the "next" line
    for x in range(settings.led_width):
        nextV = int(((100.0 - pcnt) * fire.matrixValue[0][x] + pcnt * line[x]) / 100.0)
        color = led_init.hsv2rgb(int(scale * 2.3 + fire.hueMask[0][x % 12]), 255, nextV)
        led_init.setColorXY(x, 0, color)
    return fire


def cubeRoutine(coord, speed, size, color):
    new_x = coord[0] + speed[0]
    if new_x + size >= settings.led_width:
        new_x = settings.led_width - size
        speed[0] *= -1
    if new_x <= 0:
        new_x = 0
        speed[0] *= -1
    new_y = coord[1] + speed[1]
    if new_y + size >= settings.led_height:
        new_y = settings.led_height - size
        speed[1] *= -1
    if new_y <= 0:
        new_y = 0
        speed[1] *= -1

    for x in range(size):
        for y in range(size):
            led_init.setColorXY(coord[0] + x, coord[1] + y, (0, 0, 0))
    for x in range(size):
        for y in range(size):
            led_init.setColorXY(new_x + x, new_y + y, color)
    return (new_x, new_y), speed


def move_cars(status, size, frontColor, rearColor, carColor):
    for x in range(settings.led_width):
        for y in reversed(range(1, settings.led_height)):
            led_init.setColorXY(x, y, led_init.getColorXY(x, y - 1))
    remainder = settings.led_width % (size + 3)
    for i in range(len(status)):
        val = status[i] + 1
        if val == 0:
            r = random.randint(0, 2)
            val = r * 10
            led_init.setColorXY(remainder + r + i * (size + 3), 0, frontColor)
            led_init.setColorXY(remainder + r + i * (size + 3) + size - 1, 0, frontColor)
            for j in range(1, size - 1):
                led_init.setColorXY(remainder + r + i * (size + 3) + j, 0, carColor)
        elif val % 10 == size - 1:
            r = val // 10
            val = random.randint(-size, -size // 2)
            led_init.setColorXY(remainder + r + i * (size + 3), 0, rearColor)
            led_init.setColorXY(remainder + r + i * (size + 3) + size - 1, 0, rearColor)
            for j in range(1, size - 1):
                led_init.setColorXY(remainder + r + i * (size + 3) + j, 0, carColor)
        elif val > 0:
            r = val // 10
            for j in range(0, size):
                led_init.setColorXY(remainder + r + i * (size + 3) + j, 0, carColor)
        else:
            for j in range(0, size + 2):
                led_init.setColorXY(remainder + i * (size + 3) + j, 0, (0, 0, 0))
        status[i] = val
    return status


def move_clouds(status, size, color):
    for x in reversed(range(1, settings.led_width)):
        for y in range(settings.led_height):
            led_init.setColorXY(x, y, led_init.getColorXY(x - 1, y))
    val = status + 1
    if val >= 0:
        if val == 0:
            val = random.randint(0, settings.led_height - 2) * 10
        k = val // 10
        led_init.setColorXY(0, k, color)
        led_init.setColorXY(0, k + 1, color)
        if val % 10 == 2 or val % 10 == 3:
            led_init.setColorXY(0, k + 2, color)
        else:
            led_init.setColorXY(0, k + 2, (0, 0, 0))

        if val % 10 == 5:
            val = -1 * size
    else:
        for y in range(settings.led_height):
            led_init.setColorXY(0, y, (0, 0, 0))
    return val
