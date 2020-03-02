# -*- coding: utf-8 -*-
"""
Pour la A-V0.42
"""

import pygame
import moteur
import math
import time
import labyrinthe


Unit = float(64)
Player_height = 32
Map=[[1, 1, 1, 1, 1, 1],[2, 0, 0, 0, 0, 3],[2, 0, 0, 0, 0, 3],[2, 0, 0, 0, 0, 3],[4, 4, 4, 4, 4, 4]]
#Map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1], [1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1], [1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1], [1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1], [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1], [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1], [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1], [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1], [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1], [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1], [1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
#Map = generation()
PROJ_HEIGHT = 240
PROJ_WIDTH = 320



X, Y = moteur.pop(Map)
X, Y = X * Unit + 32, Y * Unit + 32

pygame.init()
size = [PROJ_WIDTH, PROJ_HEIGHT]
screen = pygame.display.set_mode(size)  # ,pygame.FULLSCREEN)
pygame.display.set_caption("Moteur 3D")


textures = moteur.import_texture("Texture_tot.bmp")

clock = pygame.time.Clock()

done = False

sc = moteur.Scene(screen, size, Map, textures, X, Y, 42)

vit = 0  # Vitesse
vit_l = 0  # Vitesse latérale 
acc = 0  # Accéleration
acc_l = 0 # Acceleration latérale
vit_rad = 0
sensi = 40 ###Zone sans mouvement de souris
vitesse_souris = 50

tt = 0
t = 0
fps = 42

green = (0, 255, 0)

font = pygame.font.SysFont('Consolas', 18, True, False)


while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            # Figure out if it was an arrow key. If so
            # adjust speed.
            if event.key == pygame.K_LEFT:
                acc_l = 1
            elif event.key == pygame.K_RIGHT:
                acc_l = -1
            elif event.key == pygame.K_UP:
                acc = 1
            elif event.key == pygame.K_DOWN:
                acc = -1
            
            elif event.key == pygame.K_q:
                acc_l = 1
            elif event.key == pygame.K_d:
                acc_l = -1
            elif event.key == pygame.K_z:
                acc = 1
            elif event.key == pygame.K_s:
                acc = -1
            ###Pour quitter plus facilement le moteur
            if event.key == pygame.K_ESCAPE:
                done = True
            

        # User let up on a key
        elif event.type == pygame.KEYUP:
            # If it is an arrow key, reset vector back to zero
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_q or event.key == pygame.K_d:
                vit_l = 0
                acc_l = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_s or event.key == pygame.K_z:
                vit = 0
                acc = 0

        ##test souris
        pos = pygame.mouse.get_pos()[0]

        diff = pos - (PROJ_WIDTH //2 )
        if abs(diff) < sensi:
            vit_rad = 0
        else:
            vit_rad = diff /vitesse_souris

    # Modification de l'angle
    sc.Angle = (sc.Angle + vit_rad) % 360

    vit = vit + acc*(-7 <= vit <= 7)
    vit_l = vit_l + acc_l*(-4 <= vit_l <= 4)
    # Modification de la position
    X_player_new = sc.X_player + math.cos(sc.Angle * math.pi / 180) * vit + math.cos((sc.Angle+90) * math.pi / 180) * vit_l
    Y_player_new = sc.Y_player - math.sin(sc.Angle * math.pi / 180) * vit - math.sin((sc.Angle+90) * math.pi / 180) * vit_l
    if Map[int(Y_player_new / Unit)][int(X_player_new / Unit)] == 0:
        sc.X_player = X_player_new
        sc.Y_player = Y_player_new
    elif Map[int(Y_player_new / Unit)][int(sc.X_player / Unit)] == 0:
        sc.Y_player = Y_player_new
    elif Map[int(sc.Y_player / Unit)][int(X_player_new / Unit)] == 0:
        sc.X_player = X_player_new

    sc.update()
    fps_t = font.render("Fps: {:.0f}".format(fps), False, green)
    screen.blit(fps_t, [0, PROJ_HEIGHT - 20])

    
    pygame.display.flip()
    tt = time.time()
    fps = 1/(tt - t)
    t= time.time()


    # Le nombres de fps max
    clock.tick(2000)

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
