# Funções para criar e desenhar o ambiente (paredes, fundo).

import pygame
import pymunk # type: ignore

def draw_walls(screen, width, height, thickness):
    cor = (180, 180, 180)
    pygame.draw.line(screen, cor, (0, 0), (0, height), thickness)
    pygame.draw.line(screen, cor, (width, 0), (width, height), thickness)
    pygame.draw.line(screen, cor, (0, height), (width, height), thickness)
    pygame.draw.line(screen, cor, (0, 0), (width, 0), thickness)

def create_walls(space, width, height, thickness):
    walls = [
        pymunk.Segment(space.static_body, (0, 0), (0, height), thickness),
        pymunk.Segment(space.static_body, (width, 0), (width, height), thickness),
        pymunk.Segment(space.static_body, (0, height), (width, height), thickness),
        pymunk.Segment(space.static_body, (0, 0), (width, 0), thickness)
    ]
    for wall in walls:
        wall.elasticity = 1
        space.add(wall)

def draw_background(screen, width, height):
    for y in range(height):
        cor = (0, int(40 + 100 * y / height), int(80 + 150 * y / height))
        pygame.draw.line(screen, cor, (0, y), (width, y))