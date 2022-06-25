class Transform:
    position: float
    velocity: float
    acceleration: float
    length: float

    def __init__(self, position, velocity, acceleration, length=0.):
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.length = length

    def __str__(self):
        return f"{str(self.position)}; {str(self.velocity)}; {str(self.acceleration)}"

    def __add__(self, other: "Transform"):
        return Transform(self.position + other.position,
                         self.velocity + other.velocity,
                         self.acceleration + other.acceleration,
                         self.length)

    def __sub__(self, other: "Transform"):
        return Transform(self.position - other.position,
                         self.velocity - other.velocity,
                         self.acceleration - other.acceleration,
                         self.length)

    def __mul__(self, scale: float):
        return Transform(scale * self.position, scale * self.velocity, scale * self.acceleration, self.length)

    def distance(self, other, modulo: float = None):
        dist = other.position - other.length - self.position
        if modulo is not None:
            dist = dist % modulo
        return dist

    def velocity_difference(self, other):
        return self.velocity - other.velocity
