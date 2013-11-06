
# -*- coding: utf-8 -*-

from math import *
import pygame
import clobals as c


class Player():
    def __init__(self):
        '''
        konstruktori pitaa sisallaan hyodyllista tietoa pelaajan
        hetkellisista ominaisuuksista.
        paikka kartalla, katselukulma,etenemis-suunta, nopeus ja muutama flagi
        joita hyodynnetaan etenkin maailman piirtamissa pelaajan perspektiivista.
        ''' 
        self.x = self.y = 1.1
        self.angle = 0.0
        self.direction = 0
        self.speed = 0.02
        self.floor = None
        self.fire = False #aseen piirtämistä varten, eli ampuuko vai ei
        self.drawfire = False #suuliekin piirtämistä varten
        self.shot = pygame.mixer.Sound('media/gun.wav') #ääniefekti ammuttaessa
        

    def update_actions(self, map):
        keyboard = pygame.key.get_pressed()
        self.direction = 0 #0: paikoillaan 1: eteenpäin -1:taaksepäin
        self.speed = 0.02
        
        if keyboard[pygame.K_w]:
            self.direction = 1
            
        elif keyboard[pygame.K_s]:
            self.direction = -1
            
        if keyboard[pygame.K_RSHIFT] or keyboard[pygame.K_LSHIFT]:
            self.speed = 0.04
            
        if keyboard[pygame.K_LEFT]:
            
            self.angle += 0.05
        
        elif keyboard[pygame.K_RIGHT]:
            
            self.angle -= 0.05
            
        if keyboard[pygame.K_a]:
            #tarkistaa ensin onko liikkumavaraa ja liikuttaa pelaajaa jos 
            tryX = self.x + sin(self.angle + pi/2) * 0.1
            tryY = self.y + cos(self.angle + pi/2) * 0.1
            if map.map[int(tryX)][int(self.y)] == 0:
                self.x += sin(self.angle + pi/2) * self.speed
            if map.map[int(self.x)][int(tryY)] == 0:
                self.y += cos(self.angle + pi/2) * self.speed

        elif keyboard[pygame.K_d]:
            tryX = self.x + sin(self.angle - pi/2) * 0.1
            tryY = self.y + cos(self.angle - pi/2) * 0.1
            if map.map[int(tryX)][int(self.y)] == 0:
                self.x += sin(self.angle - pi/2) * self.speed
                self.sideways = -1

            if map.map[int(self.x)][int(tryY)] == 0:
                self.y += cos(self.angle - pi/2) * self.speed
                self.sideways = -1

        if self.direction != 0:
            
            tryX = self.x + self.direction * sin(self.angle) * 0.4
            tryY = self.y + self.direction * cos(self.angle) * 0.4
            dirX = dirY = -1
            if sin(self.angle) > 0:
                dirX = 1
            if cos(self.angle) > 0:
                dirY = 1
            
            if map.map[int(tryX)][int(self.y)] == 0:
                self.x += self.direction * sin(self.angle) * self.speed
            if map.map[int(self.x)][int(tryY)] == 0:
                self.y += self.direction * cos(self.angle) * self.speed
        
        #pitaa huolen siita etta kun ammutaan niin tulee vain yksi suuliekki ja yksi nykays aseella
        if pygame.mouse.get_pressed()[0] or keyboard[pygame.K_UP]:
            if not self.fire:
                self.drawfire = 5
            self.fire = True
        else: self.fire = False
        

        #kaantaa kuvakulmaa jos hiirta liikutetaan ja palauttaa hiiren keskelle
        self.angle -= (pygame.mouse.get_pos()[0] - c.WIDTH/2) * 0.01
        pygame.mouse.set_pos([c.WIDTH/2,c.HEIGHT/2])

            
        if keyboard[pygame.K_ESCAPE]:
            pygame.quit()
        
    def shoot(self):
        '''
        soittaa aaniefektin kun ammutaan
        '''
        pygame.mixer.Sound(self.shot).play()
       