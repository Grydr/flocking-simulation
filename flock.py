import pygame
from pygame.locals import *

from boid import *

class Flock:
    def __init__(self, num_boids: int) -> None:
        self.flock = self.__create_boids(num_boids)

    def render(self, surface: pygame.Surface) -> None:
        for boid in self.flock:
            boid.draw(surface)

    def run(self) -> None:
        for boid in self.flock:
            boid.edges()
            boid.flock(self.flock)
            boid.update()

    def __create_boids(self, num_boids: int) -> list[Boid]:
        return [Boid() for _ in range(num_boids)]

if __name__ == '__main__':
    print("this is flock class module file")