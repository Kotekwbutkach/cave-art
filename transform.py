class Transform:
    position: float
    velocity: float
    acceleration: float

    def __init__(self, position, velocity, acceleration):
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration

    def __str__(self):
        return f"{str(self.position)}; {str(self.velocity)}; {str(self.acceleration)}"

    def __add__(self, other: "Transform"):
        return Transform(self.position + other.position,
                         self.velocity + other.velocity,
                         self.acceleration + other.acceleration)

    def __mul__(self, scale: float):
        return Transform(scale * self.position, scale * self.velocity, scale * self.acceleration)

    def distance(self, other, modulo: float = None):
        dist = other.position - self.position
        if modulo is not None:
            dist = dist % modulo
        return dist

    def velocity_difference(self, other):
        return self.velocity - other.velocity