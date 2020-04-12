import led_init
import settings
import colorpalette

Phash = (151, 160, 137, 91, 90, 15, 131, 13, 201, 95, 96, 53, 194, 233, 7, 225, 140, 36, 103, 30, 69, 142, 8, 99, 37,
         240, 21, 10, 23, 190, 6, 148, 247, 120, 234, 75, 0, 26, 197, 62, 94, 252, 219, 203, 117, 35, 11, 32, 57, 177,
         33, 88, 237, 149, 56, 87, 174, 20, 125, 136, 171, 168, 68, 175, 74, 165, 71, 134, 139, 48, 27, 166, 77, 146,
         158, 231, 83, 111, 229, 122, 60, 211, 133, 230, 220, 105, 92, 41, 55, 46, 245, 40, 244, 102, 143, 54, 65, 25,
         63, 161, 1, 216, 80, 73, 209, 76, 132, 187, 208, 89, 18, 169, 200, 196, 135, 130, 116, 188, 159, 86, 164, 100,
         109, 198, 173, 186, 3, 64, 52, 217, 226, 250, 124, 123, 5, 202, 38, 147, 118, 126, 255, 82, 85, 212, 207, 206,
         59, 227, 47, 16, 58, 17, 182, 189, 28, 42, 223, 183, 170, 213, 119, 248, 152, 2, 44, 154, 163, 70, 221, 153,
         101, 155, 167, 43, 172, 9, 129, 22, 39, 253, 19, 98, 108, 110, 79, 113, 224, 232, 178, 185, 112, 104, 218,
         246, 97, 228, 251, 34, 242, 193, 238, 210, 144, 12, 191, 179, 162, 241, 81, 51, 145, 235, 249, 14, 239, 107,
         49, 192, 214, 31, 181, 199, 106, 157, 184, 84, 204, 176, 115, 121, 50, 45, 127, 4, 150, 254, 138, 236, 205,
         93, 222, 114, 67, 29, 24, 72, 243, 141, 128, 195, 78, 66, 215, 61, 156, 180, 151)

# max_dimension = max(settings.led_width, settings.led_height)
# noise = []
# x, y, z = 0, 0, 0
# ihue = 0


class NoiseOptions():
    def __init__(self, size):
        self.matrix = [[0] * size for _ in range(size)]
        self.x = 0
        self.y = 0
        self.z = 0
        self.ihue = 0


# def prepare():
#     global noise, x, y, z, ihue
#     noise = [[0] * max_dimension for _ in range(max_dimension)]
#     x, y, z = 0, 0, 0
#     ihue = 0


def ease8InOutQuad(i):
    j = i
    if j & 0x80:
        j = 255 - j
    jj = (j * j) >> 8
    jj2 = jj << 1
    if i & 0x80:
        jj2 = 255 - jj2
    return jj2


def FADE(x):
    return (x * x) >> 16


def avg7(i, j):
    return ((i + j) >> 1) + (i & 0x1)


def grad8(hash, x, y=None, z=None):
    if z is None:
        if y is None:
            if hash & 8:
                u, v = x, x
            elif hash & 4:
                u, v = 1, x
            else:
                u, v = x, 1
        else:
            if hash & 4:
                u, v = y, x
            else:
                u, v = x, y
    else:
        hash &= 0xF
        if hash & 8:
            u = y
        else:
            u = x
        if hash < 4:
            v = y
        elif hash == 12 or hash == 14:
            v = x
        else:
            v = z
    if hash & 1:
        u = -u
    if hash & 2:
        v = -v
    return avg7(u, v)


def lerp7by8(a, b, frac):
    if b > a:
        return a + (((b - a) * frac) >> 8)
    return a - (((a - b) * frac) >> 8)


def inoise8(x, y=None, z=None):
    if z is None:
        if y is None:
            return min(128 + 2 * inoise8_raw(x), 255)
        else:
            return min(128 + 2 * inoise8_raw(x, y), 255)
    return min(128 + 2 * inoise8_raw(x, y, z), 255)


def inoise8_raw(x, y=None, z=None):
    X = x >> 8
    u = x
    xx = (x >> 1) & 0x7F
    N = 0x80
    u = ease8InOutQuad(u)
    if z is None:
        if y is None:
            A = Phash[X]
            AA = Phash[A]
            B = Phash[X + 1]
            BA = Phash[B]
            return lerp7by8(grad8(Phash[AA], xx), grad8(Phash[BA], xx - N), u)
        else:
            Y = y >> 8
            A = Phash[X] + Y
            AA = Phash[A]
            AB = Phash[A + 1]
            B = Phash[X + 1] + Y
            BA = Phash[B]
            BB = Phash[B + 1]
            v = y
            yy = (y >> 1) & 0x7F
            v = ease8InOutQuad(v)
            X1 = lerp7by8(grad8(Phash[AA], xx, yy), grad8(Phash[BA], xx - N, yy), u)
            X2 = lerp7by8(grad8(Phash[AB], xx, yy - N), grad8(Phash[BB], xx - N, yy - N), u)
            return lerp7by8(X1, X2, v)
    Y = y >> 8
    Z = z >> 8
    A = min(Phash[X] + Y, 255)
    AA = min(Phash[A] + Z, 255)
    AB = min(Phash[A + 1] + Z, 255)
    B = min(Phash[X + 1] + Y, 255)
    BA = min(Phash[B] + Z, 255)
    BB = min(Phash[B + 1] + Z, 255)
    v, w = y, z
    yy, zz = (y >> 1) & 0x7F, (z >> 1) & 0x7F
    v, w = ease8InOutQuad(v), ease8InOutQuad(w)
    X1 = lerp7by8(grad8(Phash[AA], xx, yy, zz), grad8(Phash[BA], xx - N, yy, zz), u)
    X2 = lerp7by8(grad8(Phash[AB], xx, yy - N, zz), grad8(Phash[BB], xx - N, yy - N, zz), u)
    X3 = lerp7by8(grad8(Phash[AA + 1], xx, yy, zz - N), grad8(Phash[BA + 1], xx - N, yy, zz - N), u)
    X4 = lerp7by8(grad8(Phash[AB + 1], xx, yy - N, zz - N), grad8(Phash[BB + 1], xx - N, yy - N, zz - N), u)
    Y1, Y2 = lerp7by8(X1, X2, v), lerp7by8(X3, X4, v)
    return lerp7by8(Y1, Y2, w)


def ColorFromPalette(palette, index, brightness=0, blendType=False):
    hi4 = index >> 4
    lo4 = index & 0x0F
    red1, green1, blue1 = palette[hi4]

    if lo4 and blendType:
        hi4 = (hi4 + 1) % 16
        f2 = lo4 << 4
        f1 = 255 - f2
        red2, green2, blue2 = palette[hi4]
        red1 = (red1 * f1) >> 8
        red2 = (red2 * f2) >> 8
        red1 += red2
        green1 = (green1 * f1) >> 8
        green2 = (green2 * f2) >> 8
        green1 += green2
        blue1 = (blue1 * f1) >> 8
        blue2 = (blue2 * f2) >> 8
        blue1 += blue2

    if 0 < brightness <= 255:
        brightness += 1
        if red1:
            red1 = (red1 * brightness) >> 8
            red1 += 1
        if green1:
            green1 = (green1 * brightness) >> 8
            green1 += 1
        if blue1:
            blue1 = (blue1 * brightness) >> 8
            blue1 += 1
    else:
        return (0, 0, 0)
    return (red1, green1, blue1)


def fillNoiseLED(noise, speed, scale, colorLoop, currentPalette):
    # global noise, x, y, z, ihue
    dataSmoothing = 0
    if speed < 50:
        dataSmoothing = 200 - (speed * 4)
    for i in range(len(noise.matrix)):
        ioffset = scale * i
        for j in range(len(noise.matrix)):
            joffset = scale * j
            data = inoise8(noise.x + ioffset, noise.y + joffset, noise.z)
            data = max(data - 16, 0)
            data = min(data + ((data * 39) >> 8), 255)
            if dataSmoothing:
                data = ((noise.matrix[i][j] * dataSmoothing) >> 8) + ((data * (256 - dataSmoothing)) >> 8)
            noise.matrix[i][j] = data
    noise.z += speed
    noise.x += int(speed / settings.led_height)
    noise.y -= int(speed / settings.led_width)

    for i in range(settings.led_width):
        for j in range(settings.led_height):
            index = noise.matrix[j][i]
            bri = noise.matrix[i][j]
            if colorLoop:
                index += noise.ihue
            if bri > 127:
                bri = 255
            else:
                bri = (bri * bri) >> 6
            color = ColorFromPalette(currentPalette, index % 256, bri)
            led_init.setColorXY(i, j, color)
    led_init.pixels.write()
    noise.ihue += 1
    return noise
