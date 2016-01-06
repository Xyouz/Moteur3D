# -*- coding: utf-8 -*-
"""
__/\\\\____________/\\\\______________________________________________________________________________________/\\\\\\\\\\___/\\\\\\\\\\\\____        
 _\/\\\\\\________/\\\\\\____________________________________________________________________________________/\\\///////\\\_\/\\\////////\\\__       
  _\/\\\//\\\____/\\\//\\\___________________/\\\____________________________________________________________\///______/\\\__\/\\\______\//\\\_      
   _\/\\\\///\\\/\\\/_\/\\\_____/\\\\\_____/\\\\\\\\\\\_____/\\\\\\\\___/\\\____/\\\__/\\/\\\\\\\____________________/\\\//___\/\\\_______\/\\\_     
    _\/\\\__\///\\\/___\/\\\___/\\\///\\\__\////\\\////____/\\\/////\\\_\/\\\___\/\\\_\/\\\/////\\\__________________\////\\\__\/\\\_______\/\\\_    
     _\/\\\____\///_____\/\\\__/\\\__\//\\\____\/\\\_______/\\\\\\\\\\\__\/\\\___\/\\\_\/\\\___\///______________________\//\\\_\/\\\_______\/\\\_   
      _\/\\\_____________\/\\\_\//\\\__/\\\_____\/\\\_/\\__\//\\///////___\/\\\___\/\\\_\/\\\____________________/\\\______/\\\__\/\\\_______/\\\__  
       _\/\\\_____________\/\\\__\///\\\\\/______\//\\\\\____\//\\\\\\\\\\_\//\\\\\\\\\__\/\\\___________________\///\\\\\\\\\/___\/\\\\\\\\\\\\/___ 
        _\///______________\///_____\/////_________\/////______\//////////___\/////////___\///______________________\/////////_____\////////////_____


Moteur 3D de l'enfer.
PH Blelly & M Dufraisse

La fonction d'import des textures est prête.
La doc est inexistante :P
"""

import pygame
import math
import random
import time
import Labyrinthe

try:
    import psutil  # Fournit des infos sur la charge du CPU
    psutil_enabled = True
except ImportError:
    psutil_enabled = False
# Var
Unit = float(64)
Player_height = 32
boucle = 0
HEIGHT = 10
WIDTH = 10
#Map = Labyrinthe.generation(HEIGHT, WIDTH)

Map=[[1, 1, 1, 1, 1, 1],[2, 0, 0, 0, 0, 3],[2, 0, 0, 0, 0, 3],[2, 0, 0, 0, 0, 3],[4, 4, 4, 4, 4, 4]]
#Map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1], [1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1], [1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1], [1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1], [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1], [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1], [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1], [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1], [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1], [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1], [1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

PROJ_HEIGHT = 480
PROJ_WIDTH = 640


def pop():
    X = 0
    Y = 0
    while Map[X][Y] == 1:
        X = random.randrange(1, len(Map))
        Y = random.randrange(1, len(Map))
    return((X, Y))

coord = pop()
X_player = float(coord[0]*Unit + 32)
Y_player = float(coord[1]*Unit + 32)
FOV = 60
Angle = 90
dist_ecran = (float(PROJ_WIDTH)/2)/math.tan((float(FOV)/2)*math.pi / 180)
RAY_ANGLE = float(FOV)/PROJ_WIDTH
vit_rad = 0
vit = 0
murs = []


black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# Fonctions 3d


def ray_cast(angle, X_player, Y_player, Map):

    angle = (float(angle%360)*math.pi)/180
    _Angle =Angle*math.pi/180
    epsilon = 10**(-6)
    flag = 0
    pi =math.pi
    tan= math.tan(angle)
    map_width = len(Map[0]) * Unit
    map_height= len(Map) * Unit
    # Cas Particuliers
    ###Cas pi/2 
    if abs(angle -pi/2)<= epsilon:
        flag = 1
        Y = int(Y_player/Unit) - 1
        X = int(X_player/Unit) 
        while Map[Y][X] == 0:
            Y -= 1
        Y += 1
        val = Map[Y][X]
    
    ## Cas 3*pi/2
    elif abs(angle - 3*pi/2) <= epsilon:
        flag = 1
        Y = int(Y_player/Unit) + 1
        X = int(X_player/Unit)
        while Map[Y][X] == 0:
            Y += 1
        Y -= 1
        val = Map[Y][X]
    
    ###Cas -pi
    elif abs(angle - pi) <= epsilon:
        flag = 1
        Y = int(Y_player/Unit)
        X = int(X_player/Unit)
        while Map[Y][X] == 0:
            X -= 1
        X += 1
        val = Map[Y][X]
        
    ##Cas 0
    elif angle <= epsilon:
        flag = 1
        Y = int(Y_player/Unit)
        X = int(X_player/Unit) + 1
        while Map[Y][X] == 0:
            X+= 1
        X -= 1
        val = Map[Y][X]
        
    if flag == 1:
        dist = math.sqrt((X_player - X * Unit)**2 + (Y_player - Y * Unit)**2)
        return(dist_ecran * Unit/(dist*math.cos(angle-_Angle)), 1, X % Unit,val)
    #Fin Cas particuliers
    
    else:
        ###Detection suivant les X
        if 0 < angle < pi:
            Y = int (Y_player / Unit)*Unit - 1
            Xa = float(Unit)/tan
            X = X_player +(Y_player -Y)/tan
            while 0 < X <  map_width and Y > 0 and Map[int(float(Y)/Unit)][int(X / Unit)] == 0:
                Y -= Unit
                X = X + Xa
            
            if 0 < X < map_width and map_height > Y > 0:
                valX = Map[int(float(Y)/Unit)][int(X / Unit)]
            else:
                valX = 0
        else:
            Y = int(Y_player / Unit)*Unit + Unit
            Xa = -float(Unit)/tan
            X = X_player +(Y_player -Y)/tan
            
            while 0 < X <  map_width and Y < map_height and Map[int(float(Y)/Unit)][int(X / Unit)] == 0:
                Y += Unit
                X = X + Xa
            
            if 0 < X < map_width and map_height > Y > 0:
                valX = Map[int(float(Y)/Unit)][int(X / Unit)]
            else:
                valX = 10
        Prct_X = X % Unit
        distXa = math.sqrt((X - X_player)**2+(Y - Y_player)**2)

    # Detection suivant les Y
    ####A revoir
        if  0 < angle < pi:
            X = int(X_player / Unit)*Unit - 1
            if angle < pi/2:
                X += Unit + 2
            Ya = abs (Unit * tan)
            Y = Y_player + (X_player - X) * tan

            while Y > 0 and 0 < X < map_width and Map[int(Y/Unit)][int(float(X) / Unit)] == 0:
                if angle < pi/2:
                    X += Unit 
                else:
                    X -= Unit
                Y -= Ya
            if 0 < X < map_width and map_height >Y > 0:
                valY = Map[int(Y/Unit)][int(float(X) / Unit)]
            else:
                valY = 10
        else:
            X = int(X_player / Unit)*Unit - 1
            if angle > 3 * (pi/2):
                X += Unit + 2
            
            Ya = abs (Unit * tan)
            ###Modif X - X_plyer
            Y = Y_player + (X_player - X) * tan
            
            while 0 < Y < map_height and 0 < X < map_width and Map[int(Y/Unit)][int(float(X) / Unit)] == 0:
                if angle > 3*(pi/2):
                    X += Unit
                else:
                    X-= Unit
                Y += Ya
            if 0 < X < map_width and 0 < Y < map_height:
                valY = Map[int(Y/Unit)][int(float(X) / Unit)]
            else:
                valY = 10

        ###Modi dist
        
        distYa = math.sqrt((X - X_player) ** 2 + (Y - Y_player) ** 2) 
        Prct_Y = Y % Unit
        if distXa < distYa:
            return(dist_ecran * Unit/(distXa*math.cos(angle-_Angle)), 1, Prct_X,valX)
        else:
            return(dist_ecran * Unit/(distYa*math.cos(angle-_Angle)), 0, Prct_Y,valY)





def draw_murs(liste):
    x = 0
    for i in liste:
        y_deb = int((PROJ_HEIGHT-i[0])/2)
        y_fin = int((PROJ_HEIGHT + i[0])/2)
        if i[1] == 0:
            pygame.draw.line(screen, blue, [x, y_deb], [x, y_fin], 1)
        else:
            pygame.draw.line(screen, green, [x, y_deb], [x, y_fin], 1)
        x = x + 1


def draw_textures(liste):
    x = 0
    for i in liste:
        y_deb = int((PROJ_HEIGHT-i[0])/2)
        y_fin = int((PROJ_HEIGHT + i[0])/2)
        #if i[1] == 1:
        if i[3] != 0:
            cropped = Texture[i[3]].subsurface(i[2], 0, 1, 64)
            cropped = pygame.transform.scale(cropped, (1, y_fin-y_deb))
            screen.blit(cropped, (x, y_deb))
        #else:
            #cropped = Texture2.subsurface(i[2], 0, 1, 64)
            #cropped = pygame.transform.scale(cropped, (1, y_fin-y_deb))
            #screen.blit(cropped, (x, y_deb))
        x = x + 1


def run(X_player, Y_player, Angle, Map, PROJ_WIDTH, RAY_ANGLE):
    murs = []
    for i in range(PROJ_WIDTH // 2, -PROJ_WIDTH // 2 - 1, -1):
        murs.append(ray_cast(Angle + i * RAY_ANGLE, X_player, Y_player, Map))
    return murs

def import_texture(nom):
    ##Crée une liste de texture à partir d'une seule image
    text_height = 64
    
    text_width=64
    L=[]
    texture= pygame.image.load(nom).convert()
    for i in range (int( texture.get_height() /text_height)):
        for j in range (int(texture.get_width()/text_width)):
            L.append(texture.subsurface(j * text_width,i * text_height ,text_width ,text_height))
    return(L)
    
# Pygame


pygame.init()

# Set the height and width of the screen
size = [PROJ_WIDTH, PROJ_HEIGHT]
#screen = pygame.display.set_mode(size)
screen = pygame.display.set_mode(size)  # ,pygame.FULLSCREEN)
pygame.display.set_caption("Moteur 3D")

# Load texture
Texture = import_texture('Texture_tot.bmp')

font = pygame.font.SysFont('Consolas', 18, True, False)

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Variables 
t = 0  # Temps
tt = 0  # Temps
fps = 42  # Nombre d'images par secondes
vit = 0  # Vitesse
vit_l = 0  # Vitesse latérale 
acc = 0  # Accéleration
acc_l = 0 # Acceleration latérale
vit_rad = 0 # Vitesse angulaire

done = False
disp_inf = False
c = 10

#pos = pygame.mouse.get_pos()
#xSouris_p = pos[0]
###On place la souris au centre
pygame.mouse.set_pos((PROJ_WIDTH//2,PROJ_HEIGHT//2))
sensi = 40 ###Zone sans mouvement de souris
vitesse_souris = 50
# -------- Main Program Loop -----------
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

        diff = (PROJ_WIDTH //2 ) - pos
        if abs(diff) < sensi:
            vit_rad = 0
        else:
            vit_rad = diff /vitesse_souris
        
        ####fin test souris
        #if pygame.mouse.get_pressed()[0]==True:
            #pos = pygame.mouse.get_pos()
            #x = pos[0]
            #diff = xSouris_p - x
            #if -200 < diff < 200:
                #vit_rad = diff/5
            #else:
                #vit_rad = 0
            #xSouris_p = x
        #else:
            #vit_rad = 0
    # Modification de l'angle
    Angle += vit_rad
    Angle = Angle % 360

    vit = vit + acc*(-7 <= vit <= 7)
    vit_l = vit_l + acc_l*(-4 <= vit_l <= 4)
    # Modification de la position
    X_player_new = X_player + math.cos(Angle * math.pi / 180) * vit + math.cos((Angle+90) * math.pi / 180) * vit_l
    Y_player_new = Y_player - math.sin(Angle * math.pi / 180) * vit - math.sin((Angle+90) * math.pi / 180) * vit_l
    if Map[int(Y_player_new / Unit)][int(X_player_new / Unit)] == 0:
        X_player = X_player_new
        Y_player = Y_player_new
    elif Map[int(Y_player_new / Unit)][int(X_player / Unit)] == 0:
        Y_player = Y_player_new
    elif Map[int(Y_player / Unit)][int(X_player_new / Unit)] == 0:
        X_player = X_player_new
    # Set the screen background
    screen.fill(white)
    pygame.draw.rect(screen, black, [0, PROJ_HEIGHT / 2, PROJ_WIDTH, PROJ_HEIGHT])
    pygame.draw.rect(screen, white, [0, 0, PROJ_WIDTH, PROJ_HEIGHT / 2])
    murs = run(X_player, Y_player, Angle, Map, PROJ_WIDTH, RAY_ANGLE)
    #draw_murs(murs)
    draw_textures(murs)
    
    if disp_inf and c >= 10:
        # Render the text. "True" means anti - aliased text.
        # Black is the color. This creates an image of the
        # letters, but does not put it on the screen
        fps_t = font.render("Fps: {:.0f}".format(fps), True, green)
        angle_t = font.render("Angle: {:.1f}".format(Angle), True, green)
        pos_t = font.render("(x, y): ({0:.1f},{1:.1f})".format(X_player, Y_player), True, green)
        # Put the image of the text on the screen at 250x250
        screen.blit(fps_t, [0, PROJ_HEIGHT - 60])
        screen.blit(angle_t, [0, PROJ_HEIGHT - 40])
        screen.blit(pos_t, [0, PROJ_HEIGHT - 20])
        if psutil_enabled:
            memory = psutil.virtual_memory()[2]            #Convert first element to floating number and put in temp
            processeur = 100-psutil.cpu_times_percent()[2]
            mem_t = font.render("RAM: {:.1f}%".format(memory), True, green)
            proc_t = font.render("CPU: {:.1f}%".format(processeur), True, green)
            posM_t = font.render("Map(x, y): ({0},{1})".format(int(X_player/ Unit), int(Y_player/ Unit)), True, red)
            type_t = font.render("Etat case: {0}".format(Map[int(X_player / Unit)][int(Y_player / Unit)]), True, red)
            screen.blit(mem_t, [PROJ_WIDTH-110, PROJ_HEIGHT - 20])
            screen.blit(proc_t, [PROJ_WIDTH-110, PROJ_HEIGHT - 40]) 
        c = 0
    elif disp_inf:
        screen.blit(fps_t, [0, PROJ_HEIGHT - 60])
        screen.blit(angle_t, [0, PROJ_HEIGHT - 40])
        screen.blit(pos_t, [0, PROJ_HEIGHT - 20])
        if psutil_enabled:
            screen.blit(mem_t, [PROJ_WIDTH-110, PROJ_HEIGHT - 20])
            screen.blit(proc_t, [PROJ_WIDTH-110, PROJ_HEIGHT - 40]) 
        c += 1
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second
    tt = time.time()
    fps = 1/(tt - t)
    t= time.time()

    # Le nombres de fps max
    clock.tick(20)

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
