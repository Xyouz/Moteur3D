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

import shader

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
        self.Map = np.array(Map)
        self.PROJ_WIDTH, self.PROJ_HEIGHT = size
        self.normal = np.zeros((self.PROJ_HEIGHT, self.PROJ_WIDTH, 3))
        self.texture = np.zeros((self.PROJ_HEIGHT, self.PROJ_WIDTH, 3))
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

        # Shader properties
        self.material = shader.BlinnPhong([0.80,0.42,0.42],5) + shader.Lambert([0.42,0.42,0.42],2)
        self.light = shader.LightSource([-1, 0, 1.5],
                                        [1, 0.4,0.1], 0.6)

    
    def raycast(self,angle):
        _Angle = self.Angle * DEGTORAD

        angle = angle * DEGTORAD

        sins = np.sin(angle) >= 0
        coss = np.cos(angle) >= 0
        # Remplacer tan par sin/cos
        tan = np.tan(angle)        


        ray_c = - self.X_player * tan + self.Y_player

        mindist = np.inf
        minval = 0
        minx = 0
        miny = 0
        minnorm = None

        for i,j in np.ndindex(*self.Map.shape):
            val = self.Map[i,j]
            if val == 0:
                continue
            # corners = np.array([[self.Unit*i, self.Unit*j],
            #            [self.Unit*(i+1), self.Unit*j],
            #            [self.Unit*i, self.Unit*(j+1)],
            #            [self.Unit*(i+1), self.Unit*(j+1)]])
            # vectc = corners - [self.X_player, self.Y_player]
            # cosc = vectc[:,0] / np.linalg.norm(vectc, axis=1)
            # anglc = np.sign(vectc[:,1]) * np.arccos(cosc) /DEGTORAD

            # if angle < min(anglc) or angle > max(anglc):
            #     continue
            
            dist = np.inf

            # Left side
            x = j * self.Unit
            y = tan * x + ray_c
            
            # print(j * self.Unit, y, (j+1)*self.Unit)
            if i * self.Unit <= y <= (i+1) * self.Unit:
                dx, dy = x - self.X_player, y - self.Y_player
                if (dx >= 0) == coss and (dy >= 0) == sins: 
                    dist = np.hypot(dx, dy)
                    normal = [-1, 0, 0]
            
            # Right side
            x = (j + 1) * self.Unit
            y = tan * x + ray_c

            if i * self.Unit <= y <= (i+1) * self.Unit:
                dx, dy = x - self.X_player, y - self.Y_player
                if (dx >= 0) == coss and (dy >= 0) == sins: 

                    dist_c = np.hypot(dx, dy)

                    if dist_c < dist :
                        dist = dist_c
                        normal = [1, 0, 0]
            
            # Top side
            y = (i + 1) * self.Unit
            x = (y - ray_c) / tan

            if j * self.Unit <= x <= (j+1) * self.Unit:
                dx, dy = x - self.X_player, y - self.Y_player

                if (dx >= 0) == coss and (dy >= 0) == sins: 
                    dist_c = np.hypot(dx, dy)
                    
                    if dist_c < dist:
                        dist = dist_c
                        normal = [0, 1, 0]
            
            
            # Bottom side
            y = i * self.Unit
            x = (y - ray_c) / tan

            if j * self.Unit <= x <= (j+1) * self.Unit:
                dx, dy = x - self.X_player, y - self.Y_player

                if (dx >= 0) == coss and (dy >= 0) == sins: 
                    dist_c = np.hypot(dx, dy)
                    
                    if dist_c < dist:
                        dist = dist_c
                        normal = [0, -1, 0]
            
            if mindist > dist:
                mindist = dist
                minx, miny = x,y
                minnorm = normal
                minval = val

        # Abs rajouté artificiellement
        dispDist = self.dist_ec_reelle/(mindist*math.cos(angle-_Angle))
        #dispDist = self.dist_ec_reelle/mindist
        
        return dispDist,1 ,2 , minval, minnorm, minx, miny


    def update(self):
        """
        Met à jour l'affichage 
        Pour plus de flexibilité le "pygame.display.flip()" est laissé
        à la charge de l'utilisateur
        """
        # Le mapping est a revoir
        dist = map((lambda i:self.raycast(self.Angle + (i- (self.PROJ_WIDTH // 2)) * self.RAY_ANGLE)), range(self.PROJ_WIDTH))
        #self.screen.fill(white)
        #pygame.draw.rect(self.screen, black, [0, self.PROJ_HEIGHT / 2, self.PROJ_WIDTH, self.PROJ_HEIGHT])
        #pygame.draw.rect(self.screen, white, [0, 0, self.PROJ_WIDTH, self.PROJ_HEIGHT / 2])

        self.texture[:self.PROJ_HEIGHT//2,:] = white
        self.texture[self.PROJ_HEIGHT//2:,:] = black

        self.normal[:self.PROJ_HEIGHT//2,:] = [0.,0.,-1.]
        self.normal[self.PROJ_HEIGHT//2:,:] = [0.,0.,1.]

        self.xyz[:,:,0] = np.linspace(-1,1,self.PROJ_WIDTH).reshape(1,-1)
        self.xyz[:self.PROJ_HEIGHT//2,:,1] = np.linspace(self.dist_ecran,1000,self.PROJ_HEIGHT//2).reshape(-1,1)
        self.xyz[self.PROJ_HEIGHT//2:,:,1] = np.linspace(1000, self.dist_ecran, self.PROJ_HEIGHT//2).reshape(-1,1)
        self.xyz[:self.PROJ_HEIGHT//2,:,2] = 64
        self.xyz[self.PROJ_HEIGHT//2:,:,2] = 0

        for x, i in enumerate(dist):
            y_deb = int((self.PROJ_HEIGHT-i[0])/2)
            y_fin = int((self.PROJ_HEIGHT + i[0])/2)
            #if i[1] == 1:
            if i[3] != 0:
                #cropped = self.textures[i[3]].subsurface(i[2], 0, 1, 64)
                #cropped = pygame.transform.scale(cropped, (1, y_fin-y_deb))
                #self.screen.blit(cropped, (x, y_deb))
                y_deb = max(0,min(y_deb, self.PROJ_HEIGHT-1))
                y_fin = max(0,min(y_fin, self.PROJ_HEIGHT-1))
                self.normal[y_deb:y_fin-1, x] = i[4]
                self.xyz[y_deb:y_fin-1, x, :2] = [i[5], i[6]]
                self.xyz[y_deb:y_fin-1, x, 2] = np.linspace(64, 0, y_fin-y_deb- 1)
                #self.texture[y_deb:y_fin-1, x] = cropped 
        
        self.xyz = self.xyz / 64
        #shaded = shader.shade(self.normal, self.material, [self.light])
        Z = shader.clip_render(self.xyz[:,:,2])

        surf = pygame.surfarray.make_surface(Z.T)#.transpose(1,0,2))
        self.screen.blit(surf, (0, 0))


    def get_position(self):
        return self.X_player, self.Y_player
    
    def set_position(self, pos):
        x, y = pos
        if self.Map[int(y / self.Unit)][int(x / self.Unit)] == 0:
            self.X_player = x
            self.Y_player = y
        elif self.Map[int(y / self.Unit)][int(self.X_player / self.Unit)] == 0:
            self.Y_player = y
        elif self.Map[int(self.Y_player / self.Unit)][int(x / self.Unit)] == 0:
            self.X_player = x
        # self.light.set_position([0, 0, 0.5])

    position = property(get_position, set_position)
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
           
            
