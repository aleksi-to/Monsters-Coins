import random
import pygame

class Kolikko():
    # Erilaisten kolikoiden arvot
    # TODO kolikon koko vaihtuu arvon mukaan
    arvot =  [5,10,20]

    def __init__(self, kuva,  xy: tuple, arvo: int):
        self.__kuva       = kuva
        self.__x          = xy[0]
        self.__y          = xy[1]
        self.__arvo       = self.arvot[arvo]
        self.__id         = random.randint(1000,10000000)
        self.__leveys     = kuva.get_width()
        self.__korkeus    = kuva.get_height()
        self.__keskikohta = ((self.__x + self.__leveys / 2), (self.__y + self.__korkeus) / 2)
        self.__tuhottu    = False
        self.__koko       = 50 # 'Törmäyslaatikon' laskemiseen
        self.__rect       = pygame.Rect(self.__x, self.__y, self.__koko , self.__koko)
        


    def paivita(self):
        self.__rect = pygame.Rect(self.__x, self.__y, self.__koko, self.__koko)


    @property
    def rec(self):
        return self.__rect
    

    @property
    def tuhottu(self):
        return self.__tuhottu


    def tuhotaan(self):
        self.__tuhottu = True


    @property
    def kuva(self):
        return self.__kuva
    

    @property
    def x(self):
        return self.__x
    
    
    @property
    def y(self):
        return self.__y
    
    @property
    def keskikohta(self):
        return self.__keskikohta
    
    @property
    def id(self):
        return self.__id
