import pygame
import random

class Hirvio():
    def __init__(self, kuva, x: int, y):
        self.__kuva          = kuva
        self.__korkeus       = kuva.get_height()
        self.__leveys        = kuva.get_width()
        self.__x             = x
        self.__y             = y
        self.__id            = -(random.randint(1,100))
        self.__tuhottu       = False
        self.__koko       = 50 # 'Törmäyslaatikon' laskemiseen
        self.__rect       = pygame.Rect(self.__x, self.__y, self.__koko , self.__koko)
        

    def paivita(self):
        self.__rect = pygame.Rect(self.__x, self.__y, self.__koko , self.__koko)


    @property
    def tuhottu(self):
        return self.__tuhottu
    

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
    def id(self):
        return self.__id
    
    @property
    def rec(self):
        return self.__rect
    
    
    def muuta_x(self, arvo: int):
        self.__x += arvo

        
    def muuta_y(self, arvo: int):
        self.__y += arvo