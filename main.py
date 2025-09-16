# main.py
# Arquivo principal que executa a simulação.

import pygame
import pymunk # type: ignore
import sys
import threading
import random as r
import resource

# Importa os módulos que criamos
from config import WIDTH, HEIGHT, FPS, WALL_THICKNESS
from ball import Ball
from vector import Vector
from environment import create_walls, draw_walls, draw_background
from ui import draw_hud, tk_window

# --- CONFIGURAÇÃO DE RECURSOS ---
try:
    # limite de memória: 500 MB (Funciona em Linux/macOS)
    memory_limit = 500 * 1024 * 1024  
    resource.setrlimit(resource.RLIMIT_AS, (memory_limit, memory_limit))
    
    # limite de CPU: 30 segundos (Funciona em Linux/macOS)
    cpu_limit = 30
    resource.setrlimit(resource.RLIMIT_CPU, (cpu_limit, cpu_limit))
except ImportError:
    print("Módulo 'resource' não disponível neste sistema operacional. Limites não aplicados.")
except ValueError:
    print("Não foi possível definir os limites de recursos.")

# --- INICIALIZAÇÃO ---
pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulação Física - Refatorada")
font = pygame.font.Font(None, 28)
clock = pygame.time.Clock()

space = pymunk.Space()
space.gravity = (0, 0)
space.damping = 0.99 # Um pouco de amortecimento para estabilizar

# --- CRIAÇÃO DOS OBJETOS ---
create_walls(space, WIDTH, HEIGHT, WALL_THICKNESS)

balls = [
    Ball(int(WIDTH/3), HEIGHT/2, 0, 0, 1, space),
    Ball(int(WIDTH/2), HEIGHT/2, 0, 0, 2, space),
    Ball(int(WIDTH/1.5), HEIGHT/2, 0, 0, 3, space),
]
vectors = [Vector(ball.id) for ball in balls]

# --- INICIALIZAÇÃO DA THREAD DO TKINTER ---
t = threading.Thread(target=tk_window, args=(balls,))
t.daemon = True
t.start()

# --- LOOP PRINCIPAL ---
def main_loop():
    run = True
    dragging_ball = None
    
    while run:
        # --- LÓGICA DE EVENTOS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    for ball in balls:
                        ball.body.velocity = (0, 0)
                        ball.body.position = (r.randint(50, WIDTH-50), r.randint(50, HEIGHT-50))
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botão esquerdo
                    mx, my = event.pos
                    for ball in balls:
                        dist_sq = (mx - ball.body.position.x)**2 + (my - ball.body.position.y)**2
                        if dist_sq <= ball.radius**2:
                            dragging_ball = ball
                            break
                
                if event.button == 3:  # Botão direito
                    mx, my = event.pos
                    new_id = (max(b.id for b in balls) + 1) if balls else 1
                    new_ball = Ball(mx, my, 0, 0, new_id, space)
                    balls.append(new_ball)
                    vectors.append(Vector(new_ball.id))

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging_ball = None
            
            if event.type == pygame.MOUSEMOTION and dragging_ball:
                dragging_ball.body.position = event.pos
                dragging_ball.body.velocity = (0,0) # Para o movimento ao arrastar

        # --- ATUALIZAÇÃO DA FÍSICA ---
        space.step(1 / FPS)

        # --- RENDERIZAÇÃO ---
        draw_background(screen, WIDTH, HEIGHT)
        draw_walls(screen, WIDTH, HEIGHT, WALL_THICKNESS)

        for ball in balls:
            ball.draw(screen, font)
            if ball.get_momentum() > 0:
                # Encontra o vetor correspondente
                vector = next((v for v in vectors if v.id == ball.id), None)
                if vector:
                    vector.draw(screen, ball)
        
        draw_hud(screen, balls, font)
        pygame.display.flip()
        
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_loop()