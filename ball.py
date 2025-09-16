# Define a classe Ball e seus comportamentos.

import pygame
import pymunk
import random as r
import math

class Ball:
    def __init__(self, x, y, speed_x, speed_y, id, space):
        mass = r.randint(30, 150)
        radius = mass // 2
        
        self.radius = radius
        self.color = (r.randint(50, 255), r.randint(50, 255), r.randint(50, 255))
        self.mass = mass
        self.id = id
        self.trail = []
        self.space = space # Armazena a referência ao espaço pymunk

        moment = pymunk.moment_for_circle(mass, 0, radius)
        self.body = pymunk.Body(mass, moment)
        self.body.position = (x, y)
        self.body.velocity = (speed_x, speed_y)

        self.shape = pymunk.Circle(self.body, radius)
        self.shape.elasticity = 1
        self.space.add(self.body, self.shape)

    def draw(self, screen, font):
        x, y = self.body.position

        # Registrar pontos da trilha
        if len(self.trail) > 15:
            self.trail.pop(0)
        self.trail.append((x, y))

        # Desenhar trilha fantasma
        for i, (tx, ty) in enumerate(self.trail):
            alpha = max(50, 255 - (len(self.trail) - i) * 20)
            s = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.color, alpha), (self.radius, self.radius), self.radius)
            screen.blit(s, (tx - self.radius, ty - self.radius))

        # Contorno + bola
        pygame.draw.circle(screen, (0, 0, 0), (int(x), int(y)), self.radius + 2)
        pygame.draw.circle(screen, self.color, (int(x), int(y)), self.radius)
        id_text = font.render(str(self.id), True, (0, 0, 0))
        screen.blit(id_text, (int(x) - id_text.get_width() // 2, int(y) - id_text.get_height() // 2))

    def get_momentum(self):
        vx, vy = self.body.velocity
        return self.mass * math.sqrt(vx**2 + vy**2)

    def update_mass(self, new_mass):
        vx, vy = self.body.velocity
        x, y = self.body.position
        
        self.radius = int(new_mass // 2)
        self.space.remove(self.body, self.shape)
        
        self.mass = new_mass
        moment = pymunk.moment_for_circle(self.mass, 0, self.radius)
        self.body = pymunk.Body(self.mass, moment)
        self.body.position = (x, y)
        self.body.velocity = (vx, vy)
        
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.elasticity = 1
        self.space.add(self.body, self.shape)