import pygame
import math
from typing import Tuple
from road import Road


def get_color(c: int):
    red = (c * 112) % 256
    green = (64 + c * 144) % 256
    blue = (128 + c * 48) % 256
    return red, green, blue


class VisibleRoad:
    screen_width: int
    screen_height: int
    road_width: int
    car_width: int
    car_length: int
    sps: float
    screen: pygame.Surface

    def __init__(self,
                 road: Road,
                 screen_width=300,
                 screen_height=500,
                 road_width=20,
                 car_width=10,
                 car_length=20,
                 sps=1):
        self.road = road
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.road_width = road_width
        self.car_width = car_width
        self.car_length = car_length
        self.sps = sps
        self.screen = pygame.display.set_mode([screen_width, screen_height])

    def draw_car(self, position: Tuple[float, float], color):
        size = self.car_width, self.car_length
        rect = pygame.Rect([position[0] - size[0] / 2,
                            position[1] - size[1] / 2,
                            size[0],
                            size[1]])
        pygame.draw.rect(self.screen, color, rect)

    def draw_road(self):
        pygame.draw.rect(self.screen, (100, 100, 100),
                         (self.screen_width // 2 - self.road_width // 2, 0,
                          self.road_width, self.screen_height))
        for i, vehicle in enumerate(self.road.vehicles):
            y_position = vehicle.transform.position/self.road.length * self.screen_height
            self.draw_car((self.screen_width//2, self.screen_height - y_position), get_color(i))

    def simulate(self, delta_time: float, time_steps: int):
        running = True
        clock = pygame.time.Clock()
        pygame.init()
        t = 0
        fps = self.sps / delta_time
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if t < time_steps:
                self.screen.fill((255, 255, 255))
                self.road.simulate_step(delta_time)
                self.draw_road()
                pygame.display.flip()
                clock.tick()
                t += 1
        pygame.quit()
        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])


class VisibleRoundRoad(VisibleRoad):
    def draw_car(self, position: Tuple[float, float], color):
        radius = position[0]
        angle = position[1]
        center_x = self.screen_width // 2 + radius * math.cos(angle)
        center_y = self.screen_height // 2 + radius * math.sin(angle)
        width_diff_x, width_diff_y = self.car_width/2 * math.cos(angle), self.car_width/2 * math.sin(angle)
        length_diff_x, length_diff_y = self.car_length/2 * math.sin(angle), - self.car_length/2 * math.cos(angle)
        corners = [[center_x + a * width_diff_x + b * length_diff_x, center_y + a * width_diff_y + b * length_diff_y]
                   for a, b in [(1, 1), (1, -1), (-1, -1), (-1, 1)]]
        pygame.draw.polygon(self.screen, color, corners)

    def draw_road(self):
        radius = 3.5*self.road_width
        pygame.draw.circle(self.screen, (100, 100, 100), (self.screen_width // 2, self.screen_height // 2),
                           radius + self.road_width/2, self.road_width)
        for i, vehicle in enumerate(self.road.vehicles):
            angle = 2 * vehicle.transform.position/self.road.length * math.pi
            self.draw_car((radius, angle), get_color(i))


