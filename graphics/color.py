
# color gen using an adaptation of the sunflower seeds algorithm
def from_id(c: int):
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
    phi = (1 + 5 ** 0.5) / 2
    theta = 360 * c/(phi ** 2) % 360
    radius = 10 * phi * c ** 0.5 % 100
    red = radius + (255-radius) * arcpoint(theta)
    green = radius + (255-radius) * arcpoint(theta + 120)
    blue = radius + (255-radius) * arcpoint(theta + 240)
    return red, green, blue
