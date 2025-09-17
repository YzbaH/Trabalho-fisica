# ui.py
# Contém as funções da interface do usuário (HUD e painel Tkinter).

import pygame
import tkinter as tk

def draw_hud(screen, balls, font):
    if not balls: # Não desenha se não houver bolas
        return
        
    hud_height = 10 + 30 * len(balls)
    hud = pygame.Surface((300, hud_height), pygame.SRCALPHA)
    hud.fill((30, 30, 30, 180))
    y = 10
    for b in balls:
        vx, vy = b.body.velocity
        text = font.render(f"Bola {b.id} | M:{b.mass} | V:({int(vx)},{int(vy)})", True, (255, 255, 255))
        hud.blit(text, (10, y))
        y += 30
    screen.blit(hud, (10, 10))


def tk_window(balls):
    root = tk.Tk()
    root.title("Painel das Bolas")
    root.configure(bg="#1e1e1e")
    
    # Dicionários para guardar os widgets de cada bola pelo ID
    widgets = {}

    def aplicar(ball_id):
        try:
            # Encontra a bola correta na lista
            target_ball = next((b for b in balls if b.id == ball_id), None)
            if not target_ball:
                return

            vx = float(widgets[ball_id]['vel_x'].get())
            vy = float(widgets[ball_id]['vel_y'].get())
            mass = float(widgets[ball_id]['mass'].get())
            
            target_ball.body.velocity = (vx, vy)
            target_ball.update_mass(mass)
        except (ValueError, KeyError):
            pass

    def update_ui():
        # Verifica bolas novas ou removidas
        current_ids = {b.id for b in balls}
        widget_ids = set(widgets.keys())

        # Adiciona widgets para novas bolas
        for b in balls:
            if b.id not in widget_ids:
                i = len(widgets) # Para posicionar na grid
                widgets[b.id] = {}
                
                lbl = tk.Label(root, text=f"Bola {b.id}", bg="#1e1e1e", fg="white", font=("Arial", 11, "bold"))
                lbl.grid(row=i*3, column=0, columnspan=4, pady=5)
                widgets[b.id]['label'] = lbl

                tk.Label(root, text="Vel X", bg="#1e1e1e", fg="white").grid(row=i*3+1, column=0)
                ex = tk.Entry(root, width=6)
                ex.grid(row=i*3+1, column=1)
                widgets[b.id]['vel_x'] = ex

                tk.Label(root, text="Vel Y", bg="#1e1e1e", fg="white").grid(row=i*3+1, column=2)
                ey = tk.Entry(root, width=6)
                ey.grid(row=i*3+1, column=3)
                widgets[b.id]['vel_y'] = ey

                tk.Label(root, text="Massa", bg="#1e1e1e", fg="white").grid(row=i*3+2, column=0)
                em = tk.Entry(root, width=6)
                em.grid(row=i*3+2, column=1)
                widgets[b.id]['mass'] = em

                btn = tk.Button(root, text="Aplicar", command=lambda id=b.id: aplicar(id), bg="#444", fg="white")
                btn.grid(row=i*3+2, column=2, columnspan=2, pady=3)

        # Atualiza os valores
# Atualiza os valores
        widget_com_foco = root.focus_get() # Pega o widget que está atualmente em foco

        for b in balls:
            if b.id in widgets:
                vx, vy = b.body.velocity
                # O label sempre atualiza, pois não é editável
                widgets[b.id]['label']["text"] = f"Bola {b.id} | Massa: {b.mass} | Vel: ({vx:.1f},{vy:.1f})"

                # --- Lógica de atualização condicional ---
                # SÓ atualiza o campo de Entry se ele NÃO for o que o usuário está editando
                
                campo_vx = widgets[b.id]['vel_x']
                if campo_vx != widget_com_foco:
                    campo_vx.delete(0, tk.END)
                    campo_vx.insert(0, f"{vx:.1f}")

                campo_vy = widgets[b.id]['vel_y']
                if campo_vy != widget_com_foco:
                    campo_vy.delete(0, tk.END)
                    campo_vy.insert(0, f"{vy:.1f}")

                campo_massa = widgets[b.id]['mass']
                if campo_massa != widget_com_foco:
                    campo_massa.delete(0, tk.END)
                    campo_massa.insert(0, f"{b.mass}")
        root.after(500, update_ui)

    update_ui()
    root.mainloop()