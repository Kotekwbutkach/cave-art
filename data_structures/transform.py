class Transform:
    position: float
    velocity: float
    acceleration: float

    def __init__(self, position, velocity, acceleration):
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration

    def __repr__(self):
        return f"({self.position}, {self.velocity}, {self.acceleration})"

    def __add__(self, other: "Transform"):
        position = self.position + other.position
        velocity = self.velocity + other.velocity
        acceleration = self.acceleration + other.acceleration
        return Transform(position, velocity, acceleration)

    def __sub__(self, other: "Transform"):
        position = self.position - other.position
        velocity = self.velocity - other.velocity
        acceleration = self.acceleration - other.acceleration
        return Transform(position, velocity, acceleration)

    def __mul__(self, x: float):
        position = self.position * x
        velocity = self.velocity * x
        acceleration = self.acceleration * x
        return Transform(position, velocity, acceleration)

    def wrap(self, modulo):
        if modulo is not None:
            self.position %= modulo
        return self

    def modulo_combination(self, other, modulo, self_scale, other_scale, stability: float = 1 / 3):
        first_value = self.copy()
        second_value = other.copy()

        if modulo is None:
            return (first_value * self_scale) + (second_value * other_scale)

        if first_value.position > (modulo * (1-stability)) and second_value.position < (modulo * stability):
            second_value.position += modulo  # account for modulo wrap
        elif first_value.position < (modulo * stability) and second_value.position > (modulo * (1-stability)):
            first_value.position += modulo  # account for reverse modulo wrap

        return (first_value * self_scale) + (second_value * other_scale).wrap(modulo)

    def copy(self):
        return Transform(self.position, self.velocity, self.acceleration)
