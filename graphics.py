import pygame
import math
from road import Road
from data_structures import Transform
from typing import Callable


# color gen using an adaptation of the sunflower seeds algorithm
def get_color(c: int):
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


class VisibleRoad:
    road: Road
    screen_width: int
    screen_height: int
    road_width: int
    sps: float
    screen: pygame.Surface
    debug_function: Callable

    def __init__(self,
                 road: Road,
                 screen_width=300,
                 screen_height=500,
                 road_width=10,
                 sps=1,
                 debug_function=None):
        self.road = road
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.road_width = road_width
        self.sps = sps
        self.screen = pygame.display.set_mode([screen_width, screen_height])
        self.debug_function = debug_function

    def draw_car(self, transform: Transform, color):
        y_position = transform.position / self.road.length * self.screen_height
        position = (self.screen_width//2, y_position)
        car_length = 2000 * transform.length / self.road.length * self.screen_height
        car_width = car_length/2
        rect = pygame.Rect([position[0] - car_width/2,
                            position[1] - car_length,
                            car_width,
                            car_length])
        pygame.draw.rect(self.screen, color, rect)

    def draw_road(self):
        pygame.draw.rect(self.screen, (100, 100, 100),
                         (self.screen_width // 2 - self.road_width // 2, 0,
                          self.road_width, self.screen_height))
        for i, vehicle in enumerate(self.road.vehicles):
            self.draw_car(vehicle.physics.transform, get_color(i))

    def simulate(self, delta_time: float, time_steps: int, autosave: int = 0):
        running = True
        finished = False
        clock = pygame.time.Clock()
        pygame.init()
        t = 0
        fps = int(self.sps // delta_time)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if t < time_steps:
                self.screen.fill((255, 255, 255))
                self.road.simulate_step(delta_time)
                self.draw_road()
                pygame.display.flip()
                if autosave > 0 and t % autosave == 0:
                    self.road.data.save_to_csv()
                clock.tick(fps)
                t += 1
            else:
                finished = True
            if not finished and self.debug_function is not None:
                self.debug_function(self.road, delta_time)
        pygame.quit()
        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])


class VisibleCircleRoad(VisibleRoad):
    radius: float
    ring_width: float

    def __init__(self,
                 road: Road,
                 screen_width=300,
                 screen_height=500,
                 road_width=10,
                 sps=1,
                 radius=None,
                 debug_function=None):
        super(VisibleCircleRoad, self).__init__(road, screen_width, screen_height, road_width, sps, debug_function)

        if radius is None:
            self.radius = min(self.screen_width * 0.4, self.screen_height * 0.4)
        else:
            self.radius = radius

        ring_length = 2 * math.pi * self.radius
        self.ring_width = self.road_width * self.road.length/ring_length

    def draw_car(self, transform: Transform, color):
        angle = 2 * transform.position/self.road.length * math.pi
        car_width = self.road_width * 1.2
        car_length = transform.length + car_width

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
        for i, vehicle in enumerate(self.road.vehicles):
            self.draw_car(vehicle.physics.transform, get_color(vehicle.id))
