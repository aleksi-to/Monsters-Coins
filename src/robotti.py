import pygame

skaalaus       = 1.5
nLeveys        = int(640 * skaalaus)
nKorkeus       = int(480 * skaalaus)

class Robotti():
    def __init__(self, kuva, x: int, y: int):
        self.__x             = x #100
        self.__y             = y # nKorkeus-100 TODO todellinen keskikohta x:lle ja y:lle
        self.__kuva          = kuva
        self.__nopeusKerroin = 35
        self.__id            = 1
        self.__tuhottu       = False
        self.__leveys        = kuva.get_width()
        self.__korkeus       = kuva.get_height()
        self.__keskikohta    = ((self.__x + self.__leveys) / 2,
                                (self.__y + self.__korkeus) / 2)
        self.__koko          = 50
        self.__rect          = pygame.Rect(self.__x, self.__y, self.__koko, self.__koko)


    def paivita(self):
        self.__rect          = pygame.Rect(self.__x, self.__y, self.__koko, self.__koko)


    @property
    def rec(self):
        return self.__rect

    @property
    def tuhottu(self):
        return self.__tuhottu

    def liiku(self, suunnat: dict):
        nopeus = 5
        if suunnat['vasen'] and self.__x >= 30:
            self.__x -= nopeus

        if suunnat['oikea'] and self.__x <= nLeveys - 80:
            self.__x += nopeus

        if suunnat['ylös'] and self.__y >= 0 + 10:
            self.__y -= nopeus

        if suunnat['alas'] and self.__y <= (nKorkeus - 130):
            self.__y += nopeus


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
