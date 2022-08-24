
def rgb_to_hex(rgb):
    hex_dict = {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9",
           10: "a", 11: "b", 12: "c", 13: "d", 14: "e", 15: "f"}
    hex_string = "#"
    for col in rgb:
        hex_string = hex_string + hex_dict[col // 16] + hex_dict[col % 16]
    return hex_string


def arcpoint(angle: float) -> float:
    angle = angle % 360
    if angle <= 60 or angle >= 300:
        return 1
    elif 120 <= angle <= 240:
        return 0
    elif angle < 120:
        return 2 - (angle / 60)
    else:
        return (angle / 60) - 4


# color gen using an adaptation of the sunflower seeds algorithm
def from_id(c: int, sat: float = 1):

    phi = (1 + 5 ** 0.5) / 2
    theta = 360 * c/(phi ** 2) % 360
    radius = 10 * phi * c ** 0.5 % 100
    red = int((radius + (255-radius) * arcpoint(theta)) * sat)
    green = int((radius + (255-radius) * arcpoint(theta + 120)) * sat)
    blue = int((radius + (255-radius) * arcpoint(theta + 240)) * sat)
    return rgb_to_hex((red, green, blue))


def focus(c: int, sat: float = 1):
    if c == 0:
        return rgb_to_hex((int(255 * sat), int(63 * sat), 0))
    else:
        saturation = int(200 * sat)
        return rgb_to_hex((saturation, saturation, saturation))

