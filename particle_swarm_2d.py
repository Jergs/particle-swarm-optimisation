import math
import random

import pygame

# Initialize Pygame
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set the dimensions of the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

# Define some variables for the particle swarm optimization algorithm
NUM_PARTICLES = 50
MAX_ITERATIONS = 10000
C1 = 1.0
C2 = 1.0
W = 0.5
epsilon = 1e-2
optimisation_stop_flag = False
iterations_per_cycle = []

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the title of the window
pygame.display.set_caption("Particle Swarm Optimization Demo")


###########################################################################################


# Define a class for the particles
class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), 5)


class Particle(Point2D):
    def __init__(self):
        x = random.uniform(0, SCREEN_WIDTH)
        y = random.uniform(0, SCREEN_HEIGHT)
        Point2D.__init__(self, x, y)

        self.vel_x = random.uniform(-1, 1)
        self.vel_y = random.uniform(-1, 1)
        self.best_x = self.x
        self.best_y = self.y
        self.fitness = self.calculate_fitness()

    def calculate_fitness(self):
        return math.sqrt((self.x - target.x) ** 2 + (self.y - target.y) ** 2)

    def update_position(self):
        # Update the particle position based on its velocity
        self.x += self.vel_x
        self.y += self.vel_y

        # If the particle goes out of the screen, bounce back in the opposite direction
        if self.x < 0 or self.x > SCREEN_WIDTH:
            self.vel_x = -self.vel_x
            self.x += self.vel_x  # Move the particle back inside the screen
        if self.y < 0 or self.y > SCREEN_HEIGHT:
            self.vel_y = -self.vel_y
            self.y += self.vel_y  # Move the particle back inside the screen

        self.fitness = self.calculate_fitness()

        if self.fitness < count_p2p_distance(Point2D(self.best_x, self.best_y), target):
            self.best_x = self.x
            self.best_y = self.y

    def update_velocity(self):
        r1 = random.uniform(0, 1)
        r2 = random.uniform(0, 1)
        self.vel_x = W * self.vel_x + C1 * r1 * (self.best_x - self.x) + C2 * r2 * (target.x - self.x)
        self.vel_y = W * self.vel_y + C1 * r1 * (self.best_y - self.y) + C2 * r2 * (target.y - self.y)

    def draw(self):
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), 5)

        # Draw arrow indicating velocity
        angle = math.atan2(self.vel_y, self.vel_x)
        end_x = self.x + 5 * math.cos(angle)
        end_y = self.y + 5 * math.sin(angle)
        pygame.draw.line(screen, RED, (int(self.x), int(self.y)), (int(end_x), int(end_y)), 1)


class Target(Point2D):
    def __init__(self):
        x = 100
        y = 400
        Point2D.__init__(self, x, y)

    def draw(self):
        pygame.draw.circle(screen, BLUE, (int(self.x), int(self.y)), 7)

    def update_position(self):
        global optimisation_stop_flag
        global iteration_per_cycle
        global iterations_per_cycle

        if optimisation_stop_flag:
            self.x = random.uniform(0, SCREEN_WIDTH)
            self.y = random.uniform(0, SCREEN_HEIGHT)

            optimisation_stop_flag = False
            iterations_per_cycle.append(iteration_per_cycle)
            iteration_per_cycle = 0


def count_p2p_distance(point_a, point_b):
    return math.sqrt((point_a.x - point_b.x) ** 2 + (point_a.y - point_b.y) ** 2)


###########################################################################################


# Initialize the particles
target = Target()
particles = []
for i in range(NUM_PARTICLES):
    particles.append(Particle())

# Initialize the global best
global_best_x = particles[0].x
global_best_y = particles[0].y
global_best_point_2d = Point2D(global_best_x, global_best_y)

for particle in particles:
    if particle.fitness < count_p2p_distance(global_best_point_2d, target):
        global_best_x = particle.x
        global_best_y = particle.y

###########################################################################################

# Start the game
running = True
iteration = 0
iteration_per_cycle = 0
while running:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    target.update_position()

    # Update the particles
    for particle in particles:
        particle.update_position()
        if particle.fitness < count_p2p_distance(global_best_point_2d, target):
            global_best_point_2d.x = particle.x
            global_best_point_2d.y = particle.y

    for particle in particles:
        particle.update_velocity()

    if count_p2p_distance(global_best_point_2d, target) < epsilon:
        optimisation_stop_flag = True

    screen.fill(WHITE)
    for particle in particles:
        particle.draw()

    target.draw()

    # Update the display
    pygame.display.update()

    # Check if we've reached the maximum number of iterations
    iteration += 1
    iteration_per_cycle += 1
    if iteration >= MAX_ITERATIONS:
        running = False

    # Add a delay to give Pygame time to draw the particles
    pygame.time.wait(30)

pygame.quit()

print("Average: ", sum(iterations_per_cycle)/len(iterations_per_cycle))
