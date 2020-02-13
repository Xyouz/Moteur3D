#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Genere des cartes labyrinthiques.
"""

import random

class Cell:
    ##val = valeur de la cellule
    ##Definition de l'état des murs de la cellule (Nord/Sud/Est/ouest)
    ##Si ==0 ->cellule isolée, Sinon cellule reliée
    def __init__(self,v):
        self.n = 0
        self.s = 0
        self.e = 0
        self.o = 0
        self.val = v


def generation(HEIGHT,WIDTH):
    boucle = 0
    def initialisation(height,width):
        ###Génère la grille sous forme de ligne
        L=[Cell(i) for i in range(height*width)]
        return(L)

    def convertion(x):
        nonlocal WIDTH
        ###Converti ligne -->tableau
        return(int(x/WIDTH),x%WIDTH)

    def reconvertion(x,y):
        nonlocal WIDTH
        ###Converti tableau --> ligne
        return(y * WIDTH + x)

    def voisins(x):
        nonlocal WIDTH
        ###Renvoie une liste des cellules voisines de la cellule (Haut,bas,gauche,droite) si le mur qui les sépare n'existe plus
        L=[]
        if x > 0:
            L.append(x - WIDTH)

        if x < HEIGHT:
            L.append(x + WIDTH)

        if x % WIDTH != 0:
            L.append(x - 1)
        if x % WIDTH != WIDTH - 1:
            L.append(x + 1)
        return(L)

    def voisins_lies(x):
        nonlocal HEIGHT, WIDTH, Lab
        ###Renvoie une liste des cellules voisines de la cellule (Haut,bas,gauche,droite)
        L=[]
        if x > 0 and Lab[x].n == 1:
            L.append(x - WIDTH)
        if x + WIDTH  < HEIGHT * WIDTH and Lab[x].s == 1:
            L.append(x + WIDTH)

        if x % WIDTH != 0 and Lab[x].o == 1:
            L.append(x - 1)

        if x % WIDTH != WIDTH - 1 and Lab[x].e == 1:
            L.append(x + 1)
        return(L)
    def liste_murs(x):
        '''Renvoie une liste de murs disponibles de la cellule si la cellule
        adjascente possède une valeur différente'''
        nonlocal WIDTH, Lab
        L=[]
        if Lab[x].n == 0:
            L.append('n')
        if Lab[x].s == 0:
            L.append('s')
        if Lab[x].e == 0:
            L.append('e')
        if Lab[x].o == 0:
            L.append('o')

        ###Exclusion des murs reliant 2 cellules de même valeur
        if x > WIDTH and Lab[x-WIDTH].val ==Lab[x].val:
            L=[i for i in L if i!='n']

        if x +WIDTH < HEIGHT * WIDTH and Lab[x + WIDTH].val ==Lab[x].val:
            L=[i for i in L if i!='s']

        if x % WIDTH != 0 and Lab[x-1].val ==Lab[x].val:
            L=[i for i in L if i!='o']

        if x % WIDTH != WIDTH - 1 and Lab[x+1].val ==Lab[x].val:
            L=[i for i in L if i!='e']

        return(L)

    def briser_cloison(x,mur):
        nonlocal WIDTH, Lab
        if mur == 'n':
            Lab[x].n = 1
            Lab[x - WIDTH].s = 1
        elif mur == 's':
            Lab[x].s = 1
            Lab[x + WIDTH].n = 1
        elif mur == 'e':
            Lab[x].e = 1
            Lab[x + 1].o = 1
        elif mur == 'o':
            Lab[x].o = 1
            Lab[x - 1].e = 1
        flood([x])

    def flood(liste):
        """
        Unification des valeurs de la zone
        """
        nonlocal Lab
        if len(liste) != 0:
            L=[]
            for i in liste:
                vois = voisins_lies(i)
                for j in vois:
                    if Lab[j].val != Lab[i].val:
                        L.append(j)
                        Lab[j].val = Lab[i].val
            flood(L)



    def liste_cell(x):
        '''
        Crée une
        liste des cellules possédant une valeur différente de x
        '''
        nonlocal Lab
        X = Lab[x].val
        return( [j for j in range(len(Lab)) if Lab[j].val != X])

    def affich_rogue():
        nonlocal HEIGHT, WIDTH, Lab
        res = []
        for i in range (HEIGHT * 2 +1):
            L=[]
            for j in range( WIDTH * 2 + 1):
                L.append(1)
            res.append(L)
        for i in range (HEIGHT*WIDTH):
            i2=convertion(i)
            res[i2[0] * 2 +1][i2[1] * 2 +1]=0
            if Lab[i].n == 1:
                res[i2[0] * 2 ][i2[1] * 2 + 1]=0
            if Lab[i].s == 1:
                res[i2[0] * 2 + 2][i2[1] * 2 + 1]=0

            if Lab[i].e == 1:
                res[i2[0]*2 + 1][i2[1]*2 + 2]=0

            if Lab[i].o == 1:
                res[i2[0]*2 + 1][i2[1]*2]=0
        return res

    Lab = initialisation(HEIGHT,WIDTH)
    liste_c=liste_cell(0)

    for i in range (WIDTH*HEIGHT -1 ):
        ##Sélectionne une cellule qui possède des murs
        ###Sa valeur doit être différente de la précédente
        cell = random.choice(liste_c)
        murs=[]
        ###A revoir
        while len(murs) == 0:
            #print(cell)
            liste_c =liste_cell(cell)
            murs = liste_murs(cell)
            if cell < WIDTH :
                murs = [i for i in murs if i!='n']

            if (cell + WIDTH) > HEIGHT * WIDTH - 1:
                murs = [i for i in murs if i!='s']

            if cell % WIDTH == 0 :
                murs=[i for i in murs if i!='o']

            if cell % WIDTH == WIDTH -1 :
                murs=[i for i in murs if i!='e']

            if len(murs) == 0:
                cell = random.choice(liste_c)
            else:
                clois = random.choice(murs)

        briser_cloison(cell,clois)
        boucle += 1
    res = affich_rogue()
    return res



if __name__ == '__main__':
    boucle =0
    HEIGHT = 10
    WIDTH = 10
    a = generation(10,10)

