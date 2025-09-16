# Define a classe Vector para visualização da velocidade.

import pygame
import math

class Vector:
    def __init__(self, id):
        self.id = id

    def draw(self, screen, ball):
        vx, vy = ball.body.velocity
        # Evita erro de divisão por zero se a velocidade for (0,0)
        if vx == 0 and vy == 0:
            return
            
        angle = math.atan2(vy, vx)
        start_x = ball.body.position.x + ball.radius * math.cos(angle)
        start_y = ball.body.position.y + ball.radius * math.sin(angle)
        end_x = start_x + vx * 0.2
        end_y = start_y + vy * 0.2
        multx = math.cos(angle)
        multy = math.sin(angle)

        pygame.draw.line(screen, ball.color, (start_x, start_y), (end_x, end_y), 3)
        pygame.draw.polygon(screen, ball.color, [
            (end_x + 3 * multx, end_y + 3 * multy),
            (end_x - 10 * multx + 5 * multy, end_y - 10 * multy - 5 * multx),
            (end_x - 10 * multx - 5 * multy, end_y - 10 * multy + 5 * multx)
        ])