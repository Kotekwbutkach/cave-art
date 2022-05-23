import pygame
import math
from road import Road
from data_structures import Transform


def get_color(c: int):
    red = (c * 112) % 256
    green = (64 + c * 144) % 256
    blue = (128 + c * 48) % 256
    return red, green, blue


class VisibleRoad:
    screen_width: int
    screen_height: int
    road_width: int
    sps: float
    screen: pygame.Surface

    def __init__(self,
                 road: Road,
                 screen_width=300,
                 screen_height=500,
                 road_width=10,
                 sps=1):
        self.road = road
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.road_width = road_width
        self.sps = sps
        self.screen = pygame.display.set_mode([screen_width, screen_height])

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
                n = len(self.road.vehicles) - 1
                for i in range(self.road.vehicles[0].view.awareness):
                    print(f"Vehicle {i+1}/{0}: {self.road.vehicles[0].view.get_information(delta_time)[i+1]}")
                for i in range(self.road.vehicles[n].view.awareness):
                    print(f"Vehicle {i+1}/{n}: {self.road.vehicles[n].view.get_information(delta_time)[i+1]}")
                if autosave > 0 and t % autosave == 0:
                    self.road.data.save_to_csv()

                clock.tick(fps)
                t += 1
        pygame.quit()
        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])


class VisibleCircleRoad(VisibleRoad):
    radius: float

    def __init__(self,
                 road: Road,
                 screen_width=300,
                 screen_height=500,
                 road_width=10,
                 sps=1,
                 radius=None):
        super(VisibleCircleRoad, self).__init__(road, screen_width, screen_height, road_width, sps)

        if radius is None:
            self.radius = self.road.length/self.road_width
        else:
            self.radius = radius

    def draw_car(self, transform: Transform, color):
        angle = 2 * transform.position/self.road.length * math.pi
        car_length = 2000 * transform.length/self.road.length
        car_width = car_length/2
        center_x = self.screen_width // 2 + self.radius * math.cos(angle)
        center_y = self.screen_height // 2 + self.radius * math.sin(angle)
        width_diff_x, width_diff_y = car_width/2 * math.cos(angle), car_width/2 * math.sin(angle)
        length_diff_x, length_diff_y = car_length/2 * math.sin(angle), - car_length/2 * math.cos(angle)
        corners = [[center_x + a * width_diff_x + b * length_diff_x, center_y + a * width_diff_y + b * length_diff_y]
                   for a, b in [(1, 1), (1, -1), (-1, -1), (-1, 1)]]
        pygame.draw.polygon(self.screen, color, corners)

    def draw_road(self):
        pygame.draw.circle(self.screen, (100, 100, 100), (self.screen_width // 2, self.screen_height // 2),
                           self.radius + self.road_width/2, self.road_width)
        for i, vehicle in enumerate(self.road.vehicles):
            self.draw_car(vehicle.physics.transform, get_color(i))
