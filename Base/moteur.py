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
                                                                                                     
PH Blelly & M Dufraisse
A-V0.42

/!\ À ne pas encore trop utiliser, un certain nombre d'accès aux classes va être modifié

/!\ La doc est inexistante!
"""

import pygame
import math
import random
import time
import numpy as np

import matplotlib.pyplot as plt

DEGTORAD = math.pi/180

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)


def import_texture(nom, height=64, width=64):
    """
    Crée une liste de texture à partir d'une seule image qui les regroupe.
    """
    L=[]
    texture= pygame.image.load(nom).convert()
    for i in range (int( texture.get_height() /height)):
        for j in range (int(texture.get_width()/width)):
            L.append(texture.subsurface(j * width,i * height ,width ,height))
    return(L)


def pop(Map):
    """
    Trouve aleatoirement un point de spawn convenable.
    
    :param Map: La carte sur laquelle on cherche un point de spawn
    :type Map: Liste de listes de booléens
    :return: Les coordonnes (X,Y) où l'on doit apparaitre
    :rtype: tuple d'entiers
    """
    X = 0
    Y = 0
    while Map[X][Y] != 0:
        X = random.randrange(1, len(Map))
        Y = random.randrange(1, len(Map[0]))
    return(X, Y)


class Scene():
    """
    Une classe contenant toutes les méthodes d'affichage de la scene en 3D 
    ainsi que toutes les données relatives aux entités à afficher.
    """
    def __init__(self, screen, size, Map, textures, X, Y, Angle,
                 Unit=64.0, FOV=60, player_height=32):
        """
        Initialise l'objet de type Scene.
        
        :param screen: La surface Pygame sur laquelle on affiche
        :param size: Les dimensions de l'affichage (largeur, hauteur)
        :param Map: La carte
        :param textures: Les textures à utiliser
        :param X: Position en X
        :param Y: Position en Y
        :param Angle: Angle de la vue
        :param Unit: Facteur d'echelle
        :param FOV: Champ de vision
        :param player_height: Demander à PH
        :type screen: pygame.Surface
        :type size: tuple d'entier
        :type Map: Liste de listes de booléens
        :type textures: Liste de pygame.Surface
        :type X: float
        :type Y: float
        :type Angle: float
        :type Unit: float
        :type FOV: float
        """
        self.screen = screen
        self.Map = Map
        self.PROJ_WIDTH, self.PROJ_HEIGHT = size
        self.normal = np.zeros((self.PROJ_HEIGHT, self.PROJ_WIDTH, 3))
        self.xyz = np.zeros_like(self.normal)
        self.textures = textures
        self.X_player, self.Y_player = X, Y
        self.Angle = Angle
        self.FOV = FOV
        self.Unit = Unit
        self.player_height = player_height
        self.dist_ecran = (0.5 * self.PROJ_WIDTH)/math.tan(0.5 * self.FOV * DEGTORAD)
        self.RAY_ANGLE = self.FOV / self.PROJ_WIDTH
        self.dist_ec_reelle = self.dist_ecran * self.Unit
        self.XMap = len(self.Map)
        self.YMap = len(self.Map[0])
    
    def raycast(self,angle):
        normalX = [0,0,0]
        normalY = [0,0,0]
        angle = (float(angle%360)*math.pi)/180
        _Angle = self.Angle * math.pi / 180
        epsilon = 10**(-6)
        flag = 0
        pi = math.pi
        tan = math.tan(angle)
        map_width = len(self.Map[0]) * self.Unit
        map_height= len(self.Map) * self.Unit
        # Cas Particuliers
        ###Cas pi/2 
        if abs(angle -pi/2)<= epsilon:
            flag = 1
            Y = int(self.Y_player/self.Unit) - 1
            X = int(self.X_player/self.Unit) 
            while self.Map[Y][X] == 0:
                Y -= 1
            Y += 1
            val = self.Map[Y][X]
            normalX = [0.,1.,0.]
            normalY = normalX

        ## Cas 3*pi/2
        elif abs(angle - 3*pi/2) <= epsilon:
            flag = 1
            Y = int(self.Y_player/self.Unit) + 1
            X = int(self.X_player/self.Unit)
            while self.Map[Y][X] == 0:
                Y += 1
            Y -= 1
            val = self.Map[Y][X]
            normalX = [0.,-1.,0.]
            normalY = normalX

        ###Cas -pi
        elif abs(angle - pi) <= epsilon:
            flag = 1
            Y = int(self.Y_player/self.Unit)
            X = int(self.X_player/self.Unit)
            while self.Map[Y][X] == 0:
                X -= 1
            X += 1
            val = self.Map[Y][X]
            normalX = [1., 0., 0.]
            normalY = normalX

        ##Cas 0
        elif abs(angle) <= epsilon:
            flag = 1
            Y = int(self.Y_player/self.Unit)
            X = int(self.X_player/self.Unit) + 1
            while self.Map[Y][X] == 0:
                X+= 1
            X -= 1
            val = self.Map[Y][X]
            normalX = [-1., 0., 0.]
            normalY = normalX

        if flag == 1:
            dist = math.sqrt((self.X_player - X * self.Unit)**2 + (self.Y_player - Y * self.Unit)**2)
            return (self.dist_ec_reelle/(dist*math.cos(angle-_Angle)), 1, X % self.Unit,val), [0.,0., 0.]
        #Fin Cas particuliers
        
        else:
            ###Detection suivant les X
            if 0 < angle < pi:
                Y = int (self.Y_player / self.Unit)*self.Unit - 1
                Xa = float(self.Unit)/tan
                X = self.X_player +(self.Y_player -Y)/tan
                while 0 < X <  map_width and Y > 0 and self.Map[int(float(Y)/self.Unit)][int(X / self.Unit)] == 0:
                    Y -= self.Unit
                    X = X + Xa
                
                if 0 < X < map_width and map_height > Y > 0:
                    valX = self.Map[int(float(Y)/self.Unit)][int(X / self.Unit)]
                else:
                    valX = 0
                normalX = [0., 1., 0.]
            else:
                Y = int(self.Y_player / self.Unit)*self.Unit + self.Unit
                Xa = -float(self.Unit)/tan
                X = self.X_player +(self.Y_player -Y)/tan
                
                while 0 < X <  map_width and Y < map_height and self.Map[int(float(Y)/self.Unit)][int(X / self.Unit)] == 0:
                    Y += self.Unit
                    X = X + Xa
                
                if 0 < X < map_width and map_height > Y > 0:
                    valX = self.Map[int(float(Y)/self.Unit)][int(X / self.Unit)]
                else:
                    valX = 10
                normalX = [0., -1., 0.]
            Prct_X = X % self.Unit
            distXa = math.sqrt((X - self.X_player)**2+(Y - self.Y_player)**2)
    
        # Detection suivant les Y
        ####A revoir
            if  0 < angle < pi:
                X = int(self.X_player / self.Unit)*self.Unit - 1
                if angle < pi/2:
                    X += self.Unit + 2
                Ya = abs (self.Unit * tan)
                Y = self.Y_player + (self.X_player - X) * tan
    
                while Y > 0 and 0 < X < map_width and self.Map[int(Y/self.Unit)][int(float(X) / self.Unit)] == 0:
                    if angle < pi/2:
                        X += self.Unit 
                        normalY = [-1., 0., 0.]
                    else:
                        X -= self.Unit
                        normalY = [1., 0., 0.]
                    Y -= Ya
                if 0 < X < map_width and map_height >Y > 0:
                    valY = self.Map[int(Y/self.Unit)][int(float(X) / self.Unit)]
                else:
                    valY = 10
            else:
                X = int(self.X_player / self.Unit)*self.Unit - 1
                if angle > 3 * (pi/2):
                    X += self.Unit + 2
                
                Ya = abs (self.Unit * tan)
                ###Modif X - X_plyer
                Y = self.Y_player + (self.X_player - X) * tan

                while 0 < Y < map_height and 0 < X < map_width and self.Map[int(Y/self.Unit)][int(float(X) / self.Unit)] == 0:
                    if angle > 3*(pi/2):
                        X += self.Unit
                        normalY = [-1., 0., 0.]
                    else:
                        X-= self.Unit
                        normalY = [1., 0., 0.]
                    Y += Ya
                if 0 < X < map_width and 0 < Y < map_height:
                    valY = self.Map[int(Y/self.Unit)][int(float(X) / self.Unit)]
                else:
                    valY = 10
    
            # Modi dist
            
            distYa = math.sqrt((X - self.X_player) ** 2 + (Y - self.Y_player) ** 2) 
            Prct_Y = Y % self.Unit
            if distXa < distYa:
                return self.dist_ec_reelle/(distXa*math.cos(angle-_Angle)), 1, Prct_X,valX, normalX
            else:
                return self.dist_ec_reelle/(distYa*math.cos(angle-_Angle)), 0, Prct_Y,valY, normalY


    def update(self):
        """
        Met à jour l'affichage 
        Pour plus de flexibilité le "pygame.display.flip()" est laissé
        à la charge de l'utilisateur
        """
        # Le mapping est a revoir
        dist = map((lambda i:self.raycast(self.Angle + (i- (self.PROJ_WIDTH // 2)) * self.RAY_ANGLE)), range(self.PROJ_WIDTH))
        self.screen.fill(white)
        pygame.draw.rect(self.screen, black, [0, self.PROJ_HEIGHT / 2, self.PROJ_WIDTH, self.PROJ_HEIGHT])
        pygame.draw.rect(self.screen, white, [0, 0, self.PROJ_WIDTH, self.PROJ_HEIGHT / 2])

        self.normal[:self.PROJ_HEIGHT//2,:] = [0.,0.,-1.]
        self.normal[self.PROJ_HEIGHT//2:,:] = [0.,0.,1.]

        for x, i in enumerate(dist):
            y_deb = int((self.PROJ_HEIGHT-i[0])/2)
            y_fin = int((self.PROJ_HEIGHT + i[0])/2)
            #if i[1] == 1:
            if i[3] != 0:
                cropped = self.textures[i[3]].subsurface(i[2], 0, 1, 64)
                cropped = pygame.transform.scale(cropped, (1, y_fin-y_deb))
                self.screen.blit(cropped, (x, y_deb))
                self.normal[y_deb:y_fin-1, x] = i[4]
        if random.random()<0.01:
            np.save("normal.npy", self.normal)
    
#    def getX_player(self):
#        return self.X_player
#    
#    def setX_player(self, value):
#        self.X_player = value
#    
#    X_player = property(getX_player, setX_player)
#    
#    def getAngle(self):
#        return self.Angle
           
            
