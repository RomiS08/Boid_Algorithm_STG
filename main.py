import pygame
import random
import math

# Define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Boid parameters
NUM_BOIDS = 50
MAX_SPEED = 5
PERCEPTION_RADIUS = 50
SEPARATION_RADIUS = 20
COHESION_RADIUS = 50


class Boid:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def update(self, flock):
        # Apply rules
        separation = self.separation(flock)
        alignment = self.alignment(flock)
        cohesion = self.cohesion(flock)

        # Update velocity
        self.dx += separation[0] + alignment[0] + cohesion[0]
        self.dy += separation[1] + alignment[1] + cohesion[1]

        # Limit speed
        speed = math.sqrt(self.dx ** 2 + self.dy ** 2)
        if speed > MAX_SPEED:
            ratio = MAX_SPEED / speed
            self.dx *= ratio
            self.dy *= ratio

        # Update position
        self.x += self.dx
        self.y += self.dy

        # Wrap around screen edges
        if self.x < 0:
            self.x = SCREEN_WIDTH
        elif self.x > SCREEN_WIDTH:
            self.x = 0
        if self.y < 0:
            self.y = SCREEN_HEIGHT
        elif self.y > SCREEN_HEIGHT:
            self.y = 0

    def separation(self, flock):
        steer = [0, 0]
        count = 0
        for boid in flock:
            if boid != self:
                dist = math.sqrt((self.x - boid.x) ** 2 + (self.y - boid.y) ** 2)
                if dist < SEPARATION_RADIUS:
                    steer[0] += self.x - boid.x
                    steer[1] += self.y - boid.y
                    count += 1
        if count > 0:
            steer[0] /= count
            steer[1] /= count
            steer_mag = math.sqrt(steer[0] ** 2 + steer[1] ** 2)
            steer[0] /= steer_mag
            steer[1] /= steer_mag
        return steer

    def alignment(self, flock):
        avg_dx = 0
        avg_dy = 0
        count = 0
        for boid in flock:
            if boid != self:
                dist = math.sqrt((self.x - boid.x) ** 2 + (self.y - boid.y) ** 2)
                if dist < PERCEPTION_RADIUS:
                    avg_dx += boid.dx
                    avg_dy += boid.dy
                    count += 1
        if count > 0:
            avg_dx /= count
            avg_dy /= count
            avg_mag = math.sqrt(avg_dx ** 2 + avg_dy ** 2)
            avg_dx /= avg_mag
            avg_dy /= avg_mag
        return [avg_dx, avg_dy]

    def cohesion(self, flock):
        center = [0, 0]
        count = 0
        for boid in flock:
            if boid != self:
                dist = math.sqrt((self.x - boid.x) ** 2 + (self.y - boid.y) ** 2)
                if dist < COHESION_RADIUS:
                    center[0] += boid.x
                    center[1] += boid.y
                    count += 1
        if count > 0:
            center[0] /= count
            center[1] /= count
            dir_x = center[0] - self.x
            dir_y = center[1] - self.y
            dir_mag = math.sqrt(dir_x ** 2 + dir_y ** 2)
            dir_x /= dir_mag
            dir_y /= dir_mag
        else:
            dir_x = 0
            dir_y = 0
        return [dir_x, dir_y]


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Boid Flocking Simulation")
    clock = pygame.time.Clock()

    # Create boids
    flock = []
    for _ in range(NUM_BOIDS):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        dx = random.uniform(-1, 1)
        dy = random.uniform(-1, 1)
        boid = Boid(x, y, dx, dy)
        flock.append(boid)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)

        # Update and draw boids
        for boid in flock:
            boid.update(flock)
            pygame.draw.circle(screen, WHITE, (int(boid.x), int(boid.y)), 3)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
