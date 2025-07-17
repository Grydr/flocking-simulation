from typing import Optional
import pygame, random, math

from global_var import *

class Boid:
    def __init__(self, pos: Optional[pygame.Vector2] = None, vel: Optional[pygame.Vector2] = None, acc: Optional[pygame.Vector2] = None) -> None:
        self.max_force = 0.3
        self.max_speed = 10

        angle = random.uniform(0, 2*math.pi)

        self.position = pos or pygame.Vector2(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        self.velocity = vel or pygame.Vector2(math.cos(angle), math.sin(angle))
        self.acceleration = acc or pygame.Vector2(0, 0)

    def edges(self) -> None:
        if self.position.x > WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = WIDTH

        if self.position.y > HEIGHT:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = HEIGHT

    def boids_in_radius(self, boids: list["Boid"], radius: float) -> list["Boid"]:
        boids_in_radius = []

        for other in boids:
            if other == self:
                continue

            if self.position.distance_to(other.position) < radius:
                boids_in_radius.append(other)
        
        return boids_in_radius

    def alignment(self, boids: list["Boid"]) -> pygame.Vector2:
        avg_vel = pygame.Vector2(0, 0)
        steer = pygame.Vector2(0, 0)
        boids_in_view: list[Boid] = self.boids_in_radius(boids, ALIGNMENT_PERCEPTION)

        if boids_in_view:
            # get the avg velocity vector of local flock
            for other_boid in boids_in_view:
                avg_vel += other_boid.velocity
            avg_vel /= len(boids_in_view)

        if avg_vel.length() > 0:
            # scale to speed
            avg_vel = avg_vel.normalize() * self.max_speed

            # Implement Reynolds: Steering = Desired - Velocity
            steer = avg_vel - self.velocity
            steer = steer.clamp_magnitude(self.max_force) if steer.length() > 0 else steer
            
        return steer

    def cohesion(self, boids: list["Boid"]) -> pygame.Vector2:
        avg_pos = pygame.Vector2(0, 0)
        steer = pygame.Vector2(0, 0)
        boids_in_view: list[Boid] = self.boids_in_radius(boids, COHESION_PERCEPTION)

        if boids_in_view:
            # get avg position of local flock
            for other_boid in boids_in_view:
                avg_pos += other_boid.position
            avg_pos /= len(boids_in_view)

        # STEER = DESIRED MINUS VELOCITY
        desired = avg_pos - self.position

        if desired.length() > 0:
            desired = desired.normalize() * self.max_speed

            steer = desired - self.velocity
            steer = steer.clamp_magnitude(self.max_force) if steer.length() > 0 else steer
        
        return steer

    def separation(self, boids: list["Boid"]) -> pygame.Vector2:
        separation_threshold: float = 50.0
        steer = pygame.Vector2(0, 0)
        boids_in_view: list[Boid] = self.boids_in_radius(boids, SEPARATION_PERCEPTION)

        if boids_in_view:
            for other_boid in boids_in_view:
                dist = self.position.distance_to(other_boid.position)

                if dist > 0 and dist < separation_threshold:
                    # Calculate vector pointing away from neighbor
                    diff = self.position - other_boid.position
                    if diff.length() > 0:
                        diff = diff.normalize() / dist
                        steer += diff
        
            steer /= len(boids_in_view)

            if steer.magnitude() > 0:
                # Implement Reynolds: Steering = Desired - Velocity
                steer = steer.normalize() * self.max_speed
                steer -= self.velocity
                steer = steer.clamp_magnitude(self.max_force);
    
        return steer

    def flock(self, boids: list["Boid"]) -> None:
        cohesion = self.cohesion(boids)
        alignment = self.alignment(boids)
        separation = self.separation(boids)

        cohesion *= COHESION_FACTOR
        alignment *= ALIGNMENT_FACTOR
        separation *= SEPARATION_FACTOR

        self.acceleration += cohesion
        self.acceleration += alignment
        self.acceleration += separation

    def update(self) -> None:
        self.position += self.velocity
        self.velocity += self.acceleration
        self.velocity = self.velocity.clamp_magnitude(self.max_speed)
        self.acceleration *= 0

    def draw(self, surface: pygame.Surface, color: pygame.Color = WHITE) -> None:
        pygame.draw.circle(surface, color, self.position, 6)

if __name__ == '__main__':
    print("this is boid class module file")
