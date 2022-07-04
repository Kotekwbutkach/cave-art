from simulation.road import Road
from data_structures.vehicle_data import Transform
from .color import from_id
import pygame
import math


class RoadVisual:
    road: Road
    screen_width: int
    screen_height: int
    road_width: int
    speed: float
    vehicle_size: float
    screen: pygame.Surface

    def __init__(self,
                 road: Road,
                 screen_width: int = 300,
                 screen_height: int = 500,
                 road_width: int = 10,
                 speed: float = 1.,
                 vehicle_size: float = 1.):
        self.road = road
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.road_width = road_width
        self.speed = speed
        self.vehicle_size = vehicle_size
        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])

    def draw_car(self, transform: Transform, color):
        y_position = transform.position / self.road.data.road_length * self.screen_height
        position = (self.screen_width//2, y_position)
        car_width = self.vehicle_size * self.road_width * 1.1
        car_length = car_width * 2

        border = pygame.Rect([position[0] - (car_width / 2) * 1.15,
                             position[1] - car_length * 1.15,
                             car_width * 1.3,
                             car_length * 1.3])
        rect = pygame.Rect([position[0] - car_width/2,
                            position[1] - car_length,
                            car_width,
                            car_length])
        pygame.draw.rect(self.screen, (0, 0, 0), border)
        pygame.draw.rect(self.screen, color, rect)

    def draw_road(self):
        pygame.draw.rect(self.screen, (100, 100, 100),
                         (self.screen_width // 2 - self.road_width // 2, 0,
                          self.road_width, self.screen_height))

    def draw_frame(self, n):
        self.draw_road()
        for vehicle_data in self.road.data.vehicles_data:
            self.draw_car(vehicle_data.get_at(n), from_id(vehicle_data.vehicle_id))

    def show(self):

        running = True
        clock = pygame.time.Clock()
        pygame.init()
        n = 0
        fps = int(30 * self.speed)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if n < self.road.data.age:
                self.screen.fill((255, 255, 255))
                self.draw_frame(n)
                pygame.display.flip()
                clock.tick(fps)
                n += 1
        pygame.quit()


class CircularRoadVisual(RoadVisual):
    radius: float
    ring_width: float

    def __init__(self,
                 road: Road,
                 screen_width=300,
                 screen_height=500,
                 road_width=10,
                 speed=1.,
                 vehicle_size=1,
                 radius: int = None):
        super().__init__(road, screen_width, screen_height, road_width, speed, vehicle_size)

        if radius is None:
            self.radius = min(self.screen_width * 0.4, self.screen_height * 0.4)
        else:
            self.radius = radius

        ring_length = 2 * math.pi * self.radius
        self.ring_width = self.road_width * self.road.data.road_length/ring_length

    def draw_car(self, transform: Transform, color):
        angle = 2 * transform.position/self.road.data.road_length * math.pi
        car_width = self.vehicle_size * self.road_width * 1.1
        car_length = car_width * 2

        center_x = self.screen_width // 2 + self.radius * math.cos(angle)
        center_y = self.screen_height // 2 + self.radius * math.sin(angle)

        width_diff_x, width_diff_y = car_width/2 * math.cos(angle), car_width/2 * math.sin(angle)
        length_diff_x, length_diff_y = car_length/2 * math.sin(angle), - car_length/2 * math.cos(angle)

        border = [[center_x + a * width_diff_x + b * length_diff_x, center_y + a * width_diff_y + b * length_diff_y]
                  for a, b in [(1.25, 1.15), (1.25, -1.15), (-1.25, -1.15), (-1.25, 1.15)]]
        corners = [[center_x + a * width_diff_x + b * length_diff_x, center_y + a * width_diff_y + b * length_diff_y]
                   for a, b in [(1, 1), (1, -1), (-1, -1), (-1, 1)]]
        pygame.draw.polygon(self.screen, (0, 0, 0), border)
        pygame.draw.polygon(self.screen, color, corners)

    def draw_road(self):
        pygame.draw.circle(self.screen, (100, 100, 100), (self.screen_width // 2, self.screen_height // 2),
                           self.radius + self.road_width/2, self.road_width)
