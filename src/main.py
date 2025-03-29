import pygame as py
import random
from hirvio  import *
from kolikko import *
from robotti import *
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog

skaalaus       = 1.5
nLeveys        = int(640 * skaalaus)
nKorkeus       = int(480 * skaalaus)


# TODO Erilaisia arvokkaampia kolikkoja
# TODO Hirviön väri muuttuu
# TODO Vaikeusasteet
# TODO Paremmat taustavärit
# TODO Aikaraja ja kello
# TODO Möröt hulluja -valinta
# TODO tekstille varjot
# Kolikot antaa pisteitä OK!
# Liikkuminen sulavaa OK!
# Lisää mörköjä OK!
# Kentän reunat OK!
# Hirviö saa pelaajan kiinni OK!
# Aloitusnäkymä OK!
# Lopetusnäkymä  OK!
# Kentän väri vaihtuu satunnaisesti uuden pelin alkaessa OK!


debug = False # Tulostaa erilaisia arvoja debuggausta varten pelin ollessa käynnissä

class Peli():
    # Alustetaan pelissä tarvittavia arvoja, kuvia yms.
    def __init__(self):
        py.init()
        
        self.colors         = [(55, 55, 55),(236, 236, 236),(208, 208, 208), (82, 82, 82), (173, 173, 173), (143, 143, 143)]
        self.color          = self.colors[random.randint(1,len(self.colors)-1)]
        self.ekaKierros     = True
        self.suunnat        = {'vasen': False, 'oikea': False, 'alas': False, 'ylös': False}

        self.naytto         = py.display.set_mode((nLeveys,nKorkeus))
        self.kello          = py.time.Clock()
        self.peli_kaynnissa = True
        self.nopeus         = 1
        self.fontti         = py.font.SysFont("Arial", 24)

        self.hirvioKuva       = py.image.load('hirvio.png')
        self.__pisteet  = 0

        self.roboKuva         = py.image.load('robo.png')
        self.korkeusRobo      = self.roboKuva.get_height()
        self.leveysRobo       = self.roboKuva.get_width()

        self.kolikkoKuva      = py.image.load('kolikko.png')
        self.korkeusKolikko   = self.kolikkoKuva.get_height()
        self.leveysKolikko    = self.kolikkoKuva.get_width()

        self.uusiPeli()

    def uusiPeli(self):
        # Kysellään käyttäjältä nimi, haluttu hirviöiden määrä ja aikaraja (joka ei toimi vielä)
        self.aloitusIkkunat()
        
        self.nopeus         = 1
        self.peliobjektit   = []
        self.robo       = Robotti(self.roboKuva, nLeveys / 2, nKorkeus / 2 - 50)

        self.hirviot    = []
        hirvioXY = [(nLeveys - 100, 50),(100, 50), (nLeveys / 2, nKorkeus - 100)]
        for i in range(self.hirvioMaara):
            self.hirviot.append(Hirvio(self.hirvioKuva, hirvioXY[i][0], hirvioXY[i][1]))
        
        self.peliobjektit.append(self.robo)
        for hirvio in self.hirviot:
            self.peliobjektit.append(hirvio)

        self.silmukka()

    def silmukka(self):
        while self.peli_kaynnissa:
            self.tapahtumat()                               # Liikkuminen ja nappien painelut
            self.robo.liiku(self.suunnat)
            self.piirra_naytto()                            # Piirretään näyttö ja tekstit
            self.kolikoita()                                # Luodaan kolikoita näytölle
            self.piirra()                                   # Piirretään objektit näytölle
            self.monsteri_seuraa(self.robo, self.hirviot)    # Hirviö(t) seuraa pelaajaa
            self.tarkasta_tormaykset(self.peliobjektit[0], self.hirviot)  # Tarkastetaan kolikoiden, pelaajan ja hirviön törmäykset
            self.peli_loppuu()                              # Tarkastetaan loppuuko peli
            py.display.flip()
            if debug:
                self.debug()
            self.kello.tick(60)

    def aloitusIkkunat(self):
        root = Tk()
        root.withdraw()
        self.pelaajaNimi = simpledialog.askstring("Input", "Pelaajan nimi:")
        if not (self.pelaajaNimi):
            self.pelaajaNimi = 'Pelaaja' # Oletusarvo

        self.hirvioMaara = int(simpledialog.askstring("Input", "Hirviöiden määrä (1-2): "))
        if(self.hirvioMaara < 1 or self.hirvioMaara > 3):
            self.hirvioMaara = 1    # # Oletusarvo

        self.aikaraja = int(simpledialog.askstring("Input", "Aikaraja sekunneissa (0 = ei aikarajaa, maksimi 120): "))
        if(self.aikaraja < 1 or self.aikaraja > 120):
            self.aikaraja = 0   # # Oletusarvo
        

    def debug(self):
        print(f"Robo: {self.robo}")
        print(f"Hirviot: {self.hirviot}")
        for item in self.peliobjektit:
            print(f"ID:  {item.id}")
        print(f"Peliobjektit: {self.peliobjektit}")

    # Tarkastetaan päättyykö peli
    # - Monsteri sai pelaajan kiinni
    # - Aika loppui (ei toimi vielä)
    # - Joku muu?
    def peli_loppuu(self):
        if(self.peli_kaynnissa == False):
            root = Tk()
            root.withdraw()
            input = simpledialog.askstring("Input", "Uusi peli? (k/e)")
            if(input.lower() in ['k', 'kyllä', 'kyl', 'ky', 'joo', 'yes']):
                self.peli_kaynnissa = True
                self.uusiPeli()
            else:
                exit()

        self.peli_kaynnissa = True


    # Piirretään peliobjektit
    def piirra(self):
        for olio in self.peliobjektit:
            if not(olio.tuhottu):
                self.naytto.blit(olio.kuva, (olio.x, olio.y))


    def piirra_naytto(self):
        
        marginaali_yla = 5
        self.naytto.fill((self.color))
        fontti = py.font.SysFont("Arial", 24)

        py.draw.rect(self.naytto, (0, 0, 0), (0, 0, nLeveys,nKorkeus), 40) # Reunat

        vari = (255, 58, 19)
        varjoVari = (173, 37, 10)

        teksti = self.fontti.render(f"Pisteet: {self.__pisteet}", True, (vari))
        self.naytto.blit(teksti, (nLeveys - 110, marginaali_yla))

        teksti = self.fontti.render(f"Pelaaja: {self.pelaajaNimi}", True, (vari))
        self.naytto.blit(teksti, (nLeveys - 260, marginaali_yla))

        teksti = self.fontti.render("F2 = uusi peli", True, (vari))
        self.naytto.blit(teksti, (30, marginaali_yla))

        teksti = self.fontti.render("Esc = sulje peli", True, (vari))
        self.naytto.blit(teksti, (170, marginaali_yla))
        
        py.display.flip()


    def liikuRobo(self, arvo: int):
        self.robo.liiku(arvo)


    # Hirviö seuraa robottia
    def monsteri_seuraa(self, robo: Robotti, hirviot: list[Hirvio]):
        roboX = robo.x
        roboY = robo.y
        for hirvio in hirviot:
            hirvioX = hirvio.x
            hirvioY = hirvio.y

            if hirvioX < roboX:
                hirvio.muuta_x(self.nopeus)
            else:
                hirvio.muuta_x(-self.nopeus)
            if hirvioY < roboY:
                hirvio.muuta_y(self.nopeus)
            else:
                hirvio.muuta_y(-self.nopeus)

        # Hirviö liikkuu nopeammin ja nopeammin
            self.nopeus *= 1.0005

    def kolikoita(self):
        # n. 2 % mahdollisuus luoda kolikko joka syklillä
        # Tarkistetaan myös, ettei kolikoita ole liikaa ruudulla
        if( (random.randint(1,100) > 98) and (len(self.peliobjektit) <= 50) ):
            coin = Kolikko(self.kolikkoKuva, self.arvo_xy(), 0)
            self.peliobjektit.append(coin)


    def arvo_xy(self):
        marginaali = 80 # Jotta kolikot eivät ilmesty reuna-alueelle
        x = random.randint(marginaali, nLeveys - marginaali)
        y = random.randint(marginaali, nKorkeus - marginaali)
        return (x,y)
    

    def lisaaPiste(self):
        self.__pisteet += 1


    def display(self):
        # Näytä pisteet, elämät, aika yms.
        pass

    def tarkasta_tormaykset(self, robo: Robotti, hirviot: list):
        # Pelaaja/hirviö -törmäystarkistus
        for hirvio in hirviot:
            if debug:
                print("Tarkastetaan pelaaja/hirviö törmays")
            self.tormays_pelaaja_hirvio(robo, hirvio)

        # Pelaaja/kolikko -törmäystarkistus
        for objekti in self.peliobjektit:
            if(objekti.id > 100):
                self.tormays_kolikko_pelaaja(robo, objekti)
                if debug:
                    print("Objekti.id > 100, tarkistetaan kolikko/pelaaja törmäys")


    # Pelaajan ja hirviön törmäyksen tarkistaminen
    def tormays_pelaaja_hirvio(self, robo: Robotti, hirvio: Hirvio):
        if debug:
            print("Tarkistetaan robo/hirviö törmäys")
            print(f"Pelaaja: {robo} hirviö: {hirvio}")
        robo.paivita()
        hirvio.paivita()
        collide = robo.rec.colliderect(hirvio.rec)
        if debug:
            print("Ollaan tormays_pelaaja_hirvio-metodissa")

        if(collide):
            self.peli_kaynnissa = False
            print("MÖRKÖ SÖI!") # Debuggausta varten


    # Kolikoiden ja pelaajan törmäysten tarkistaminen
    def tormays_kolikko_pelaaja(self, robo: Robotti, coin: Kolikko):
        robo.paivita()
        coin.paivita()
        collide = robo.rec.colliderect(coin.rec)

        if (collide):
            self.lisaaPiste()
            self.tuhoaKolikko(coin.id)
            print("Kolikko talteen!")


    # Luodaan uusi lista ilman 'tuhottua' kolikkoa
    def tuhoaKolikko(self, id: int):
        self.peliobjektit = [alkio for alkio in self.peliobjektit if(alkio.id != id)]


    # Tarkastetaan näppäimiin liittyviä tapahtumia
    def tapahtumat(self):
        for tapahtuma in py.event.get():
            if tapahtuma.type == py.KEYDOWN:
                if tapahtuma.key == py.K_LEFT:
                    self.suunnat['vasen'] = True

                if tapahtuma.key == py.K_RIGHT:
                    self.suunnat['oikea'] = True

                if tapahtuma.key == py.K_DOWN:
                    self.suunnat['alas'] = True

                if tapahtuma.key == py.K_UP:
                    self.suunnat['ylös'] = True

                if tapahtuma.key == py.K_ESCAPE:
                    exit()

                if tapahtuma.key == py.K_F1:
                    pass # TODO uusi peli tms.

            if tapahtuma == py.QUIT:
                exit()

            if tapahtuma.type == py.KEYUP:
                if tapahtuma.key == py.K_LEFT:
                    self.suunnat['vasen'] = False
                if tapahtuma.key == py.K_RIGHT:
                    self.suunnat['oikea'] = False
                if tapahtuma.key == py.K_UP:
                    self.suunnat['ylös'] = False
                if tapahtuma.key == py.K_DOWN:
                    self.suunnat['alas'] = False

if __name__ == "__main__":
    Peli()