# -*- coding: utf-8 -*-

import pygame

from math import *
import clobals as c

class Map(object):
    def __init__(self, map_file_name, player):
        '''
        Mapin konstruktori saa parametreiksi map tiedoston nimen ja player olion.
        
        konstruktorissa ladataan ja piirretaan kuvia valmiiksi,
        ennen ohjelman varsinaista kaynnistysta.
        '''
        self.shade = 1  #saadellaan alueen valaistusta eli varjostuksia samalla (luvuilla n 1-2)
        self.player = player
        self.floor = self.draw_floor()
        self.map = self.create_map(map_file_name)
        self.sky = pygame.image.load('media/starry_sky.png').convert()
        self.sky_position = None
        self.minimapbool = False
        self.minimap = self.draw_mini_map()
        pygame.transform.scale(self.sky, (c.WIDTH/640 * self.sky.get_width(), c.WIDTH/640 * self.sky.get_height()))
        self.sight = pygame.transform.scale(pygame.image.load('media/tahtain2.png'), (c.WIDTH/11, c.WIDTH/11))
        self.gunfire = pygame.transform.scale(pygame.image.load('media/fire.png'),(c.WIDTH/4, c.WIDTH/4))
        self.gun = pygame.transform.scale(pygame.image.load('media/gun.png'), (c.WIDTH/3, c.WIDTH/3))
        
        
    def create_map(self, file_name):
        f = open('maps/'+file_name)
        map = []
        while 1:
            line = f.readline()
            list = []
            for a in line:
                if a in ['0','1','2','3','4','5','6','7','8','9']:
                    list.append(int(a))
            if len(list) > 1:
                map.append(list)
            if not line: break
        return map
    
    def draw_map(self, screen):
        '''
        pitaa huolen että kaikki piirretaan kuvaan mita on tarkoituskin
        ottaa parametrikseen pohja surfacen
        ei palauta mitaan
        '''
        #ensin piirretaan lattia ja taivas jotta ne jaavat seinien alle
        self.draw_sky(screen) #piirtaa taivaan
        
        screen.blit(self.floor,(0, c.HEIGHT/2)) # piirtaa lattian

        for i in range(c.WIDTH): # käydaan jokainen pikselipylvas x-akselilta lapi
            
            angle = (i*(c.FOV/c.WIDTH) - c.FOV/2) #kulma lähtien näkymän vasemmasta laidasta
            self.draw_walls(i, angle, screen) # piirtaa seinant
            
        screen.blit(self.sight,(c.WIDTH/2-c.WIDTH/22,c.HEIGHT/2-c.HEIGHT/17)) #piirtaa tahtaimen kaiken paalle
        self.shoot(screen) #piirtaa aseen kaiken paalle
        
        if self.minimapbool:
            screen.blit(self.minimap,(c.WIDTH/15,c.HEIGHT/15))
        
    def shoot(self,screen):
        '''
        piirtaa kuvaan aseen ja hypayttaa sita hieman ammuttaessa
        tarvitsee parametrikseen pohja surfacen johon piirtaa
        ei palauta mitaan
        '''
        
        if self.player.drawfire > 0:
            self.player.drawfire -= 1
            screen.blit(self.gunfire,(c.WIDTH/2-c.WIDTH/50,c.HEIGHT-int(c.HEIGHT/3)))
            
        if self.player.drawfire:
            screen.blit(self.gun,(c.WIDTH/2+c.WIDTH/37,c.HEIGHT-int(c.HEIGHT/2.3)))
            
            pygame.draw.circle(screen, screen.get_at((c.WIDTH/2-2,c.HEIGHT/2-2)), (c.WIDTH/2+int(c.WIDTH/3.7),c.HEIGHT-int(c.HEIGHT/7)), 17)
        else:
            screen.blit(self.gun,(c.WIDTH/2+c.WIDTH/37,c.HEIGHT-int(c.HEIGHT/2.35)))
            #pygame.draw.ellipse(screen, screen.get_at((c.WIDTH/2-2,c.HEIGHT/2-2)), (c.WIDTH/2,c.HEIGHT),5,5)
            pygame.draw.circle(screen, screen.get_at((c.WIDTH/2-2,c.HEIGHT/2-2)), (c.WIDTH/2+int(c.WIDTH/3.7),c.HEIGHT-int(c.HEIGHT/7.5)), 17)

    def draw_floor(self):
        '''
        piirtaa lattian pythagoraan lauseen avulla pixeli pixeliltäja palauttaa sen
        '''
        floor = pygame.Surface((c.WIDTH,c.HEIGHT/2))
        floor.fill((100,100,100))
        #käy jokaisen pikselin läpi ja tarkistaa sen etäisyyden kuvan ala-keskikohdasta
        #jolloin syntyy puolikaaren muotoinen varjostunut skaala
        for i in range(c.WIDTH):
            for a in range(c.HEIGHT/2):
                #paljon suhteuttamiseen tarkoitettuja juttuja ja kertoimia joilla varjostumisen sai onnistumaan
                dist = sqrt(((c.WIDTH/ 2-i)*0.7)**2 + ((self.shade*250 + c.HEIGHT/2) - a)**2)
                shade =  110*self.shade - dist*0.21

                if shade < 0:
                    shade = 0
                floor.set_at((i,a),(shade, shade, shade))
        return floor
        
    def draw_walls(self,i,angle,screen):
        '''
        Piirtaa yhen pikelipylvaan seinaa varten.
        saa parametreina i eli mihin kohtaan kuvakulmaa piirretaan,
        angle, eli sateen kulma
        screen eli pohja-surface
        '''
        
        #Tassa mennyt pieleen X ja Y ainakin, eli tasta lahden korjaamaan peilikuvaongelmaa
        #laskee pelaajan kulmasta ja säteen kulmasta kuvakulmassa säteelle kaksi vektoria jotka kuvaavat siis säteen suuntaa.
        dirX = sin(self.player.angle)*cos(angle) - cos(self.player.angle)*sin(angle)
        dirY = sin(self.player.angle)*sin(angle) + cos(self.player.angle)*cos(angle)
        
        
        color , dist = self.raycastWall(dirX,dirY)
        shade = 0.3/dist * self.shade * 400 # varjostuskikkailua
        dist =(c.HEIGHT/2)/(dist * cos(angle)) #(c.HEIGHT/2) on suhdeutukseen
        if shade < 0: shade = 0 #pidetään huoli ettei seinän tummuus/varjostus mene värimaailmojen yli eli värit voivat olla 0-255 arvoltaan
        elif shade > 150: shade = 150
        # tarkistetaan minkä värinen viiva on piirrettävä
        if color == 1:
            pygame.draw.line(screen, (shade,0,0), (i, (c.HEIGHT/2) - dist), (i, (c.HEIGHT/2) + dist))
        elif color == 2:
            pygame.draw.line(screen, (0,shade,0), (i, (c.HEIGHT/2) - dist), (i, (c.HEIGHT/2) + dist))
        elif color == 3:
            pygame.draw.line(screen, (0,0,shade), (i, (c.HEIGHT/2) - dist), (i, (c.HEIGHT/2) + dist))
        elif color == 4:
            pygame.draw.line(screen, (shade,shade ,0), (i, (c.HEIGHT/2) - dist), (i, (c.HEIGHT/2) + dist))
        elif color == 5:
            pygame.draw.line(screen, (shade,0,shade), (i, (c.HEIGHT/2) - dist), (i, (c.HEIGHT/2) + dist))
        elif color == 6:
            pygame.draw.line(screen, (shade,shade,0), (i, (c.HEIGHT/2) - dist), (i, (c.HEIGHT/2) + dist))
        elif color == 7:
            pygame.draw.line(screen, (shade,shade,shade), (i, (c.HEIGHT/2) - dist), (i, (c.HEIGHT/2) + dist))
        
        
                
    def draw_sky(self, screen):
        '''
        piirtaa taivaan ja liikuttaa sita pelaajan katselukulman mukaan
        '''
        
        angle = self.player.angle
        #laskee kuvan aloituspistetta
        #kuva on siis kolme kertaa peräkkäin tiedostossa ja aina kun kuva on mennyt yhden
        #leveytensä verran jompaan kumpaan suuntaan asetetaan se takas keskellä.
        self.sky_position = -self.sky.get_width()/3+ (self.sky.get_width()/3)*(angle/(pi*2) % 1)
        screen.blit(self.sky, (self.sky_position,0))
        
    def draw_mini_map(self):
        '''
        piirtaa minimapin
        ja palauttaa sen
        '''
        width = len(self.map[0])
        height = len(self.map)
        tile = c.HEIGHT/96
        minimap = pygame.Surface((tile*(width), tile*(height)))
        minimap.set_alpha(140)
        #kay jokaisen ruudun läpi kartta tiedostossa ja piirtää oikeaan kohtaa minimappia ruudun jos seinä loutui
        for y in range(height):
            for x in range(width):
                if self.map[y][x] != 0:
                    minimap.fill((100,100,100), ((x*tile, y*tile), (tile, tile)))
        minimap = pygame.transform.flip(minimap, False, True)
        return minimap

        
    def raycastWall(self, DirX,DirY):
        '''
        Pelin tarkein funktio, joka tunnistaa seinat ja laskee etäisyyden kuhunkin pisteeseen.
        Saa parametrinä säteen suunnan x ja y suuntaisin vektoreina DirX ja DirY
        
        Paluttaa: minkä väriseen seinään säde törmäsi (1-7) ja tarkan etäisyyden tähän kohtaan
        '''
        
        PosX = self.player.x    #tarkka x koordinaatti
        PosY = self.player.y    #tarkka y koordinaatti
        X = int(PosX)   # x koordinaatti kokonaisina ruutuina
        Y = int(PosY)   # y koordinaatti kokonaisina ruutuina
        deltaDX = deltaDY = 0.0   # x koordinaatin muutos kun liikutaan y-suunnassa yksi ruutu(ja toisinpäin y:lle)
        side = 0 #kumpi seinäma
        stepX = stepY = 0 # kokonaisluku -1 tai 1, hyppii ruutuja yksi kerrallaan eteenpain
        sideDX = sideDY = 0 # etaisyys lähtöpisteesta ensimmaiseen ruudun reunaan
        if (DirX != 0): #tarkistus ettei osoittajaan tule nollaa
            deltaDX = sqrt(1+(DirY**2) / (DirX**2)) #lasketaan matka x ruutuseinaminen valinen sateen kulkema matka
        if (DirY != 0):
            deltaDY = sqrt( 1+(DirX**2) / (DirY**2))
        if (DirX < 0): # katsotaan mihin suuntaan säde kulkee
                stepX = -1 # asetetaan askel oikean merkkiseksi 
                sideDX = (PosX - X) * deltaDX # lasketaan matka katsojan sijainnista ensimmaiseen ruudun x seinaan
        else:
                stepX = 1
                sideDX = (1.0 + X - PosX) * deltaDX
        if (DirY < 0):
                stepY = -1
                sideDY = (PosY - Y) * deltaDY
        else:
                stepY = 1
                sideDY = (-PosY + 1.0 + Y) * deltaDY
        while 1:
            if (sideDX < sideDY): #tarkistetaan kumpi seinä on seuraavaksi edessa
                sideDX += deltaDX #lisätaan aina yksi vali lisaa jotta paastaan seuraavalle seinalle
                X += stepX #jotta tiedetaan missä ruudussa mennaa kartassa ruutukartassa
                side = 0
            else:
                sideDY += deltaDY #sama kuin ylempänä mutta toisille sivuille
                Y += stepY
                side = 1
            if (self.map[X][Y] != 0): #jos ollaan seinässa
                if DirX == 0: #ettei jaeta nollalla
                    DirX = 0.0001
                if DirY == 0:
                    DirY = 0.0001
                if side == 0:
                    #tekstuureja varten:
                    #position_on_wall = PosY + ((X - PosX + (1 - stepX) / 2) / DirX) * DirY
                    return self.map[X][Y], abs((X - PosX + (1 - stepX) / 2) / DirX) #lasketaan etäisyys seinään
                #position_on_wall = PosX + ((Y - PosY + (1 - stepY) / 2) / DirY) * DirX
                return self.map[X][Y], abs((Y - PosY + (1 - stepY) / 2) / DirY)
        
        
        
        
        
        
        
        
        
        
        
        
            