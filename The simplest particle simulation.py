import pygame
import sys
import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

class Particle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = random.choice([RED, GREEN, BLUE])
        self.speed = random.uniform(1, 3)
        self.angle = random.uniform(0, 2 * math.pi)

    def move(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)
        self.speed += 0.1  # Gravity

    def change_color(self):
        self.color = random.choice([RED, GREEN, BLUE])

def handle_particle_collision(p1, p2):
    distance = math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)
    if distance < p1.radius + p2.radius:
        p1.change_color()
        p2.change_color()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle Animation")

clock = pygame.time.Clock()

particles = [Particle(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(5, 20)) for _ in range(50)]

def apply_kinetic_force(particle):
    if particle.y + particle.radius >= HEIGHT:
        particle.speed = -abs(particle.speed)  # Bounce
        particle.change_color()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    for i in range(len(particles)):
        particles[i].move()
        apply_kinetic_force(particles[i])

        for j in range(i + 1, len(particles)):
            handle_particle_collision(particles[i], particles[j])

        if particles[i].x - particles[i].radius < 0 or particles[i].x + particles[i].radius > WIDTH:
            particles[i].angle = math.pi - particles[i].angle  # Bounce off side walls
            particles[i].change_color()

    screen.fill(BLACK)

    for particle in particles:
        pygame.draw.circle(screen, particle.color, (int(particle.x), int(particle.y)), particle.radius)

    pygame.display.flip()

    clock.tick(FPS)
