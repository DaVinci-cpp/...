import pygame
import math
import random
pygame.init()

sw=800
sh=650
pygame.init()

#učitavanje slike pozadine, slike rakete i slike asteroida
pozadina=pygame.image.load("pozadina.jpg")
Raketa=pygame.image.load("Raketa1.png")
asteroid1=pygame.image.load("Stone1.png")
asteroid2=pygame.image.load("Stone2.png")
asteroid3=pygame.image.load("Stone3.png")
asteroid4=pygame.image.load("Stone4.png")
asteroid5=pygame.image.load("Stone5.png")
asteroid6=pygame.image.load("Stone6.png")

pygame.display.set_caption("Asteroidi")
win=pygame.display.set_mode((sw,sh))

clock=pygame.time.Clock()

kraj=False  #indikator završetka igre
zivoti=3   #broj života
poeni=0   #broj poena

#klasa igrača-rakete
class Player(object):
    
    def __init__(self):
        self.img=Raketa
        #dimenzije rakete
        self.w=self.img.get_width()
        self.h=self.img.get_height()
        #početni položaj rakete - na centru
        self.x=sw//2
        self.y=sh//2
        self.angle=0
        self.rotiraj()

    def rotiraj(self):
        #rotiranje rakete
        self.rotatedSurf=pygame.transform.rotate(self.img, self.angle)

        #get_rect naredba od pygame.Surface, kreira novi pravougaonik
        #iste veličine kao slika sa x, y kordinatama (0, 0).
        #Da bi dali pravougaoniku druge koordinate najčešće se dodeljuju
        #određene vrednosti njegovim koordinatama centra ili gornjeg levog ugla
        self.rotatedRect=self.rotatedSurf.get_rect()
        self.rotatedRect.center=(self.x, self.y)

        #određivanje pravca rakete pomoću trigonometrije
        self.cosine=math.cos(math.radians(self.angle+90))
        self.sine=math.sin(math.radians(self.angle+90))

        #koordinate centra rakete odakle će se ispaljivati meci
        #su iste kao koordinate centra 
        self.head=(self.x, self.y)

    #iscrtavanje rakete
    def crtaj(self,win):
        win.blit(self.rotatedSurf, self.rotatedRect)

    #rotiranje rakete nalevo
    def Levo(self):
        self.angle+=5
        self.rotiraj()

    #rotiranje rakete nadesno
    def Desno(self):
        self.angle-=5
        self.rotiraj()

    #kretanje rakete napred
    def Napred(self):
        #izračunavanje pomeraja po x i y osi
        self.x+=self.cosine*6
        self.y-=self.sine*6
        self.rotiraj()

    #kretanje rakete unazad
    def Nazad(self):
        self.x-=self.cosine*6
        self.y+=self.sine*6
        self.rotiraj()

    #ukoliko raketa izađe iz ekrana pojavljuje se sa druge strane 
    def osveziLokaciju(self):
        if self.x>sw+self.w:
            self.x=0
        elif self.x<0-self.w:
            self.x=sw
        if self.y<-self.h:
            self.y=sh
        elif self.y>sh+self.h:
            self.y=0

#klasa municije
class Municija(object):
    def __init__(self):
        #kordinate metka su koordinate centra rakete
        self.x, self.y = igrac.head
        #dimenzije metka
        self.w=4
        self.h=4
        #određivanje brzine kretanja metka po x i y osi
        self.xv=igrac.cosine*10
        self.yv=igrac.sine*10

    #kretanje metka
    def move(self):
        self.x+=self.xv
        self.y-=self.yv

    #iscrtavanje metka u vidu malog pravouganika
    def crtaj(self, win):
        pygame.draw.rect(win, (255,255,255), (self.x, self.y, self.w, self.h))

    #provera da li je metak van ekrana
    def checkOffScreen(self):
        if self.x<-igrac.w or self.x>sw or self.y>sh or self.y<-igrac.h:
            return True

#klasa asteroida
class Asteroid(object):
    def __init__(self, rang):
        self.rang=rang
        if self.rang==1:
            self.img=asteroid1
        elif self.rang==2:
            self.img=asteroid2
        elif self.rang==3:
            self.img=asteroid3
        elif self.rang==4:
            self.img=asteroid4
        elif self.rang==5:
            self.img=asteroid5
        elif self.rang==6:
            self.img=asteroid6
        #određivanje dimenzija asteroida
        self.w=self.img.get_width()
        self.h=self.img.get_height()
        #određivanje početnih koordinata asteroida
        gore_dole=(random.randrange(0,sw-self.w), random.choice([-1*self.h-5, sh+5]))
        levo_desno=(random.choice([-1*self.w-5,sw+5]), random.randrange(0, sh-self.h))
        self.x, self.y = random.choice([gore_dole, levo_desno])
        #određivanje pravca kretanja asteroida
        if self.x<sw//2:
            self.xdir=1
        else:
            self.xdir=-1
        if self.y<sh//2:
            self.ydir=1
        else:
            self.ydir=-1
        #određivanje brzine asteroida u željenom pravcu
        self.xv=self.xdir*random.randrange(1,3)
        self.yv=self.ydir*random.randrange(1,3)

    def crtaj(self, win):
        win.blit(self.img, (self.x, self.y))
        
# osvežavanje ekrana
def osveziEkran():
    #postavljanje pozadine
    win.blit(pozadina, (0,0))
    #definisanje fontova i teksta za ispis broja života, sk ora i poruke na kraju igre
    font=pygame.font.SysFont("arial",30)
    font1=pygame.font.SysFont("arial",50)
    zivotiTekst=font.render("Životi: " + str(zivoti), True, (255,255,255))
    poeniTekst=font.render("Poeni: " + str(poeni), True, (255,255,255))
    IgrajPonovoTekst=font1.render("Pritisni SPACE da bi ponovo igrao:", True, (255,255,0))
    
    #iscrtavanje rakete, asteroida i municije
    igrac.crtaj(win)
    for a in asteroidi:
        a.crtaj(win)
    for b in igracMunicija:
        b.crtaj(win)

    #ispis teksta ukoliko je igra završena (igraj ponovo)
    if kraj:
        win.blit(IgrajPonovoTekst, (sw//2-IgrajPonovoTekst.get_width()//2, sh//2-IgrajPonovoTekst.get_height()//2))
    #ispis broja preostalih života u gornjem levom uglu ekrana
    win.blit(zivotiTekst, (25,25))
    #ispis postignutog skora u gornjem desnom uglu ekrana
    win.blit(poeniTekst, (sw-poeniTekst.get_width()-25,25))

    pygame.display.update()

igrac=Player()
igracMunicija=[] #lista ispaljenih metaka
asteroidi=[] #lista asteroida
count=0
   
run=True

while run:
    clock.tick(60)
    count+=1
    if not kraj:
        #na svakih 50 učitavanja dodati po jedan asteroid
        if count%50==0:
            #određivanje ranga asteroida (1-najmanji, 6-najveći) na osnovu verovatnoće
            rang=random.choice([1,1,1,1,1,1,2,2,2,3,3,3,4,4,5,5,6])
            asteroidi.append(Asteroid(rang))
            
        #ažuriranje položaja rakete - ukoliko je izašla sa ekrana, pojavljuje se na suprotnoj strani
        igrac.osveziLokaciju()
        
        #pomeranje municije i uklanjanje one koja je napustila ekran 
        for b in igracMunicija:
            b.move()
            if b.checkOffScreen():
                igracMunicija.pop(igracMunicija.index(b))

        #pomeranje asteroida 
        for a in asteroidi:
            a.x+=a.xv
            a.y+=a.yv

            #umanjenje broja života rakete i uklanjanje asteroida u slučaju sudara rakete i asteroida
            if (igrac.x>=a.x and igrac.x<=a.x+a.w) or (igrac.x+igrac.w>=a.x and igrac.x+igrac.w<=a.x+a.w):
                    if (igrac.y>=a.y and igrac.y<=a.y+a.h) or (igrac.y+igrac.h>=a.y and igrac.y+igrac.h<=a.y+a.h):
                        zivoti-=1
                        asteroidi.pop(asteroidi.index(a))
                        break   #prekid jer nećemo proveravati da li je asteroid pogođen jer ga više nema

            #sudar metka i asteroida
            for b in igracMunicija:
                #provera pozicije metka u odnosu na asteroid
                if (b.x>=a.x and b.x<=a.x+a.w) or (b.x+b.w>=a.x and b.x+b.w<=a.x+a.w):
                    if (b.y>=a.y and b.y<=a.y+a.h) or (b.y+b.h>=a.y and b.y+b.h<=a.y+a.h):
                        #ukoliko se pogodi najveći asteroid dobija se 10 poena i od njega nastaju 4 nova najmanja asteroida
                        if a.rang==6:
                            poeni+=10
                            for i in range(4):
                                novi_asteroid=Asteroid(1)
                                novi_asteroid.x=a.x
                                novi_asteroid.y=a.y
                                asteroidi.append(novi_asteroid)
                        #ukoliko se pogode asteroidi veličine 4 ili 5 dobija se po 20 poena i od njih nastaju po 2 nova najmanja asteroida
                        elif a.rang==4 or a.rang==5:
                            poeni+=20
                            for i in range(2):
                                novi_asteroid=Asteroid(1)
                                novi_asteroid.x=a.x
                                novi_asteroid.y=a.y
                                asteroidi.append(novi_asteroid)
                        #ukoliko se pogode asteroidi veličine 2 ili 3 dobija se po 30 poena
                        elif a.rang==3 or a.rang==2:
                            poeni+=30
                        #ukoliko se pogodi najmanji asteroid dobija se po 50 poena
                        elif a.rang==1:
                            poeni+=50
                        #uklanjanje pogodjenog asteroida i metka iz liste
                        asteroidi.pop(asteroidi.index(a))
                        igracMunicija.pop(igracMunicija.index(b))

        #prekid igre ako su svi životi potrošeni    
        if zivoti<=0:
            kraj=True

        #provera koji taster je pritisnut
        keys= pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            igrac.Levo()
        if keys[pygame.K_RIGHT]:
            igrac.Desno()
        if keys[pygame.K_UP]:
            igrac.Napred()
        if keys[pygame.K_DOWN]:
            igrac.Nazad()

        #osvežavanje ekrana   
        osveziEkran()

    #provera da li je korisnik zatvorio ekran
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False

        #na taster SPASE ispaljujemo municije i igramo ispočetka u slučaju da se igra završila
        #(ovo se radi ovde a ne u delu gde se proverava da li su strelice pritisnute
        #da bi moglo istovremeno da bude pritisnuta i neka strelica i SPACE
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                if not kraj:
                    #dodavanje metka u listu municije
                    igracMunicija.append(Municija())
                else:
                    #kada se igrica završi igramo ponovo klikom na SPACE
                    kraj=False
                    zivoti=3
                    poeni=0
                    asteroidi.clear()
                    igracMunicija.clear()
            
#kraj igrice
pygame.quit()
