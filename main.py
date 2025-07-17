import pygame, sys
from pygame.locals import *

from flock import *
from boid import *
from global_var import *

class Simulation:
    def __init__(self, num_boids: int=100) -> None:
        print("Initializing the simulation")
        pygame.init()
        pygame.display.set_caption("Boids Simulation")

        self.running = True
        self.surface = pygame.display.set_mode(WINSIZE)
        self.clock = pygame.time.Clock()

        self.flocks = Flock(num_boids)

    def handle_event(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_q):
                self.running = False
                pygame.quit()
                sys.exit()

    def update(self) -> None:
        self.flocks.run()

    def render(self) -> None:
        self.surface.fill(BLACK)
        self.flocks.render(self.surface)
        pygame.display.update()

    def run(self) -> None:
        print("Running the simulation")
        while self.running:
            self.handle_event()
            self.update()
            self.render()
            self.clock.tick(60)
        
def main():
    sim = Simulation(200)
    sim.run()

if __name__ == "__main__":
    main()