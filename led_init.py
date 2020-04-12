import asyn
import machine
import neopixel
import uasyncio as asyncio

import colorpalette
import effects
import noise
import settings

led = machine.Pin(2, machine.Pin.OUT)
pixels = neopixel.NeoPixel(machine.Pin(settings.led_pin), settings.led_width * settings.led_height)


def setColorXY(x, y, color):
    if(x % 2 == 0):
        pixels[12 * x + y] = color
    else:
        pixels[12 * x - y + 11] = color


def getColorXY(x, y):
    if(x % 2 == 0):
        return pixels[12 * x + y]
    return pixels[12 * x - y + 11]


def led_off():
    pixels.fill((0, 0, 0))
    pixels.write()


def hsl2hsv(hsl):
    h, s, l = hsl
    H = int(h * 255 / 360)
    V = int((l + s * min(l, 1 - l)) * 255)
    if V:
        S = int(2 * (1 - l / V) * 255)
    else:
        S = 0
    return (H, S, V)


def hsv2rgb(h, s, v):
    if not s:
        return (v, v, v)
    H = min(h, 255)
    i = H // 43
    f = (H - i * 43) * 6
    p = (v * (255 - s)) >> 8
    q = (v * (255 - ((s * f) >> 8))) >> 8
    t = (v * (255 - ((s * (255 - f)) >> 8))) >> 8

    if i == 0:
        return (v, t, p)
    if i == 1:
        return (q, v, p)
    if i == 2:
        return (p, v, t)
    if i == 3:
        return (p, q, v)
    if i == 4:
        return (t, p, v)
    if i == 5:
        return (v, p, q)


def hsv2rgb_rainbow(h, s, v):
    def nscale8x3_video(r, g, b, scale):
        nonzeroscale = 0
        if scale != 0:
            nonzeroscale = 1
        if r != 0:
            r = ((r * scale) >> 8) + nonzeroscale
        if g != 0:
            g = ((g * scale) >> 8) + nonzeroscale
        if b != 0:
            b = ((b * scale) >> 8) + nonzeroscale
        return (r, g, b)

    def scale8_video_LEAVING_R1_DIRTY(i, scale):
        nonzeroscale = 0
        if scale != 0:
            nonzeroscale = 1
        if i != 0:
            i = ((i * scale) >> 8) + nonzeroscale
        return i

    offset = h & 0x1F  # 0..31
    offset8 = offset * 8
    third = (offset8 * (256 // 3)) >> 8
    r, g, b = (0, 0, 0)

    if not (h & 0x80):
        if not (h & 0x40):
            if not (h & 0x20):
                r, g, b = 255 - third, third, 0
            else:
                r, g, b = 171, 85 + third, 0
        else:
            if not (h & 0x20):
                twothirds = (third << 1)
                r, g, b = 171 - twothirds, 171 + third, 0
            else:
                r, g, b = 0, 255 - third, third
    else:
        if not (h & 0x40):
            if not (h & 0x20):
                twothirds = (third << 1)
                r, g, b = 0, 171 - twothirds, 85 + twothirds
            else:
                r, g, b = third, 0, 255 - third
        else:
            if not (h & 0x20):
                r, g, b = 85 + third, 0, 171 - third
            else:
                r, g, b = 171 + third, 0, 85 - third

    if s != 255:
        r, g, b = nscale8x3_video(r, g, b, s)
        desat = 255 - s
        desat = (desat * desat) >> 8
        brightness_floor = desat
        r = r + brightness_floor
        g = g + brightness_floor
        b = b + brightness_floor

    if v != 255:
        v = scale8_video_LEAVING_R1_DIRTY(v, v)
        r, g, b = nscale8x3_video(r, g, b, v)

    return (r, g, b)


@asyn.cancellable
async def move_fire(property):
    led_off()
    fire = effects.Fire()
    while True:
        fire = effects.drawFire(fire, property['pcnt'], property['scale'])
        pixels.write()
        await asyncio.sleep(1 / property['speed'])


@asyn.cancellable
async def move_cube(property):
    led_off()
    coord = [0] * 2
    speed = [property['speed']] * 2
    while True:
        coord, speed = effects.cubeRoutine(coord, speed, property['size'], property['cubeColor'])
        pixels.write()
        await asyncio.sleep(1 / property['speed'])


@asyn.cancellable
async def move_rainbow(property):
    led_off()
    status = 0
    while True:
        status = effects.rainbowRoutine(status, property['type'])
        await asyncio.sleep(1 / property['speed'])


@asyn.cancellable
async def draw_color(property):
    led_off()
    while True:
        for x in range(settings.led_width):
            color = hsv2rgb_rainbow(hsl2hsv(property['hsl']))
            for y in range(settings.led_height // 2 + 1):
                setColorXY(x, y, color)
            color = hsv2rgb(hsl2hsv(property['hsl']))
            for y in range(settings.led_height // 2 + 1, settings.led_height):
                setColorXY(x, y, color)
            pixels.write()
            await asyncio.sleep(1 / property['speed'])
        await asyncio.sleep(5 / property['speed'])
        for x in range(settings.led_width):
            for y in range(settings.led_height):
                setColorXY(x, y, (0, 0, 0))
            pixels.write()
            await asyncio.sleep(1 / property['speed'])
        await asyncio.sleep(5 / property['speed'])


@asyn.cancellable
async def move_snow(property):
    led_off()
    while True:
        effects.snowRoutine(property['scale'], property['pcnt'], hsl2hsv(property['hsl']))
        pixels.write()
        await asyncio.sleep(1 / property['speed'])


@asyn.cancellable
async def move_matrix(property):
    led_off()
    while True:
        effects.matrixRoutine(property['scale'])
        pixels.write()
        await asyncio.sleep(1 / property['speed'])


@asyn.cancellable
async def move_cars(property):
    led_off()
    number = settings.led_width // (property['size'] + 3)
    status = [-1] * number
    while True:
        status = effects.move_cars(status, property['size'], property['frontColor'], property['rearColor'], property['carColor'])
        pixels.write()
        await asyncio.sleep(1 / property['speed'])


@asyn.cancellable
async def move_clouds(property):
    led_off()
    # number = settings.led_width // property['size']
    status = -1
    while True:
        status = effects.move_clouds(status, property['size'], property['color'])
        pixels.write()
        await asyncio.sleep(1 / property['speed'])


@asyn.cancellable
async def lavaNoise(property):
    led_off()
    current_noise = noise.NoiseOptions(max(settings.led_width, settings.led_height))
    while True:
        current_noise = noise.fillNoiseLED(current_noise, property['speed'], property['scale'], 0, colorpalette.LavaColors)
        await asyncio.sleep(1 / property['speed'])


@asyn.cancellable
async def plasmaNoise(property):
    led_off()
    current_noise = noise.NoiseOptions(max(settings.led_width, settings.led_height))
    while True:
        current_noise = noise.fillNoiseLED(current_noise, property['speed'], property['scale'], 1, colorpalette.PartyColors)
        await asyncio.sleep(1 / property['speed'])


@asyn.cancellable
async def cloudNoise(property):
    led_off()
    current_noise = noise.NoiseOptions(max(settings.led_width, settings.led_height))
    while True:
        current_noise = noise.fillNoiseLED(current_noise, property['speed'], property['scale'], 0, colorpalette.CloudColors)
        await asyncio.sleep(1 / property['speed'])


@asyn.cancellable
async def oceanNoise(property):
    led_off()
    current_noise = noise.NoiseOptions(max(settings.led_width, settings.led_height))
    while True:
        current_noise = noise.fillNoiseLED(current_noise, property['speed'], property['scale'], 0, colorpalette.OceanColors)
        await asyncio.sleep(1 / property['speed'])


@asyn.cancellable
async def forestNoise(property):
    led_off()
    current_noise = noise.NoiseOptions(max(settings.led_width, settings.led_height))
    while True:
        current_noise = noise.fillNoiseLED(current_noise, property['speed'], property['scale'], 0, colorpalette.ForestColors)
        await asyncio.sleep(1 / property['speed'])


@asyn.cancellable
async def rainbowNoise(property):
    led_off()
    current_noise = noise.NoiseOptions(max(settings.led_width, settings.led_height))
    while True:
        current_noise = noise.fillNoiseLED(current_noise, property['speed'], property['scale'], 1, colorpalette.RainbowColors)
        await asyncio.sleep(1 / property['speed'])


@asyn.cancellable
async def rainbowStripeNoise(property):
    led_off()
    current_noise = noise.NoiseOptions(max(settings.led_width, settings.led_height))
    while True:
        current_noise = noise.fillNoiseLED(current_noise, property['speed'], property['scale'], 1, colorpalette.RainbowStripeColors)
        await asyncio.sleep(1 / property['speed'])
