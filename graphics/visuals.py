from simulation.road import Road
from data_structures.vehicle_data import Transform
from .color import from_id
import pygame


class RoadVisual:
    road: Road
    screen_width: int
    screen_height: int
    road_width: int
    speed: float
    screen: pygame.Surface

    def __init__(self,
                 road: Road,
                 screen_width=300,
                 screen_height=500,
                 road_width=10,
                 speed=1.,
                 vehicle_size=1):
        self.road = road
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.road_width = road_width
        self.speed = speed
        self.screen = pygame.display.set_mode([screen_width, screen_height])
        self.car_size = vehicle_size

    def draw_car(self, transform: Transform, color):
        y_position = transform.position / self.road.data.length * self.screen_height
        position = (self.screen_width//2, y_position)
        car_length = self.car_size * transform.length / self.road.data.length * self.screen_height
        car_width = car_length/2
        rect = pygame.Rect([position[0] - car_width/2,
                            position[1] - car_length,
                            car_width,
                            car_length])
        pygame.draw.rect(self.screen, color, rect)

    def draw_frame(self, n):
        pygame.draw.rect(self.screen, (100, 100, 100),
                         (self.screen_width // 2 - self.road_width // 2, 0,
                          self.road_width, self.screen_height))
        for i, transform_data in enumerate(self.road.data.vehicles_data):
            self.draw_car(transform_data.get_at(n), from_id(i))

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
