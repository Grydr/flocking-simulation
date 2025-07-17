import pygame, sys
from pygame.locals import * 
import pygame_gui

from flock import *
from boid import *
from global_var import *
import global_var

class Simulation:
    def __init__(self, num_boids: int=100) -> None:
        print("Initializing the simulation")
        pygame.init()
        pygame.display.set_caption("Boids Simulation")

        self.running = True
        self.surface = pygame.display.set_mode(WINSIZE)
        self.clock = pygame.time.Clock()

        self.flocks = Flock(num_boids)

        self.manager = pygame_gui.UIManager(WINSIZE)

        # Create reset button
        reset_button_str = "Reset Value"
        self.reset_button = pygame_gui.elements.UIButton(
            relative_rect=(20, 20),
            text=" " + reset_button_str + " ",
            manager=self.manager,
        )

        # Create slider
        self.cohesion_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(START_X, START_Y, SLIDER_WIDTH, SLIDER_HEIGHT),
            start_value=COHESION_FACTOR,
            value_range=(0.0, 5.0),
            manager=self.manager,
        )

        self.alignment_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(START_X + 1 * (SLIDER_WIDTH + SLIDER_SPACING), START_Y, SLIDER_WIDTH, SLIDER_HEIGHT),
            start_value=ALIGNMENT_FACTOR,
            value_range=(0.0, 5.0),
            manager=self.manager,
        )

        self.separation_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(START_X + 2 * (SLIDER_WIDTH + SLIDER_SPACING), START_Y, SLIDER_WIDTH, SLIDER_HEIGHT),
            start_value=SEPARATION_FACTOR,
            value_range=(0.0, 5.0),
            manager=self.manager,
        )

        # Create label above slider
        self.cohesion_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(START_X, LABEL_Y, SLIDER_WIDTH, SLIDER_HEIGHT),  # position below the third slider
            text=f"Cohesion: {COHESION_FACTOR}",
            manager=self.manager
        )

        self.alignment_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(START_X + 1 * (SLIDER_WIDTH + SLIDER_SPACING), LABEL_Y, SLIDER_WIDTH, SLIDER_HEIGHT),  # position below the third slider
            text=f"Alignment: {ALIGNMENT_FACTOR}",
            manager=self.manager
        )

        self.separation_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(START_X + 2 * (SLIDER_WIDTH + SLIDER_SPACING), LABEL_Y, SLIDER_WIDTH, SLIDER_HEIGHT),  # position below the third slider
            text=f"Separation: {SEPARATION_FACTOR}",
            manager=self.manager
        )

    def handle_event(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_q):
                self.running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.reset_button:
                    global_var.COHESION_FACTOR = 1.0
                    self.cohesion_slider.set_current_value(global_var.COHESION_FACTOR)

                    global_var.ALIGNMENT_FACTOR = 1.0
                    self.alignment_slider.set_current_value(global_var.ALIGNMENT_FACTOR)

                    global_var.SEPARATION_FACTOR = 1.5
                    self.separation_slider.set_current_value(global_var.SEPARATION_FACTOR)

            self.manager.process_events(event)

    def update(self) -> None:
        self.flocks.run()
        self.manager.update(self.time_delta)

    def render(self) -> None:
        self.surface.fill(BLACK)
        self.flocks.render(self.surface)
        self.manager.draw_ui(self.surface)
        pygame.display.update()

    def run(self) -> None:
        print("Running the simulation")
        while self.running:
            self.time_delta = self.clock.tick(60)/1000.0
            self.handle_event()

            global_var.COHESION_FACTOR = self.cohesion_slider.get_current_value()
            self.cohesion_label.set_text(f"Cohesion: {global_var.COHESION_FACTOR:.2f}")
            global_var.ALIGNMENT_FACTOR = self.alignment_slider.get_current_value()
            self.alignment_label.set_text(f"Alignment: {global_var.ALIGNMENT_FACTOR:.2f}")
            global_var.SEPARATION_FACTOR = self.separation_slider.get_current_value()
            self.separation_label.set_text(f"Separation: {global_var.SEPARATION_FACTOR:.2f}")

            self.update()
            self.render()

def main():
    sim = Simulation(200)
    sim.run()

if __name__ == "__main__":
    main()