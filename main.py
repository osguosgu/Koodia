
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from map import Map
from player import Player
import clobals as c
import sys


class Main(object):
    def __init__(self, map_file):
        '''
        parametri: map_file eli karttatiedoston nimi komentorivilta
        
        konstruktori lataa musiikkia,
        asettaa kursorin nakymattomaksi,
        luo player olion,
        luo PyGamen pohja-Surfacen self.screen jonka paalle kaikki
        graafinen toteutus tulee,
        asettaa pelin tilaksi 'kaynnissa' running = True
        luo clock olion jonka avulla suorituskyky pysyy kurissa,
        luo map olion Map luokasta ja map saa parametreiksi
        map-tiedoston nimen ja pelaaja olion
        '''
        
        pygame.init()
        pygame.mixer.music.load('media/music.mp3')
        pygame.mixer.music.play(100)
        pygame.mouse.set_visible(False)
        self.player = Player()
        self.screen = pygame.display.set_mode((c.WIDTH, c.HEIGHT))
        self.map = Map(map_file, self.player)
        self.running = True
        self.clock = pygame.time.Clock()
        
        
        self.pause = False #Flagi joka maarittelee soiko taustamusiikki va ei
        
    def update(self):
        '''
        paivittaa pelaajan liikkeet kartalla,
        saa parametriksi map-olion
        '''
        self.player.update_actions(self.map)

    def draw(self):
        '''
        paivittaa piirtamisen
        antaa map-olion draw_map() funktiolle parametriksi pohja-surfacen
        piirtamista varten.
        '''
        self.screen.fill((0,0,0))
        self.map.draw_map(self.screen)
        pygame.display.flip() #PyGame: Tarpeellinen jotta kuva lopulta piirtyy
    def mainloop(self):
        '''
        mainloop tarkistaa jos m tai p nappain painettu
        ja toimii sen mukaisesti, eli jos m niin muuttaa
        map olion arvoa niin etta map piirretaan kuvaan tai otetaan siita pois.
        Kutsuu update() ja draw() funktioita joka loopilla
        '''
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == MOUSEBUTTONDOWN:
                    self.player.shoot()
                    print 'LAUKAUS!' #testi joka oli hauska jattaa :)
                if event.type == KEYDOWN and event.key == K_m:
                    if not self.map.minimapbool: #tarkistaa onko minimap nakyvissa vai ei
                        self.map.minimapbool = True
                    else: self.map.minimapbool = False
                if event.type == KEYDOWN and event.key == K_p:
                    if not self.pause: #tarkistaa onko musiikki paalla
                        pygame.mixer.music.pause()
                        self.pause = True
                    else:
                        pygame.mixer.music.unpause()
                        self.pause = False
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()

if __name__ == '__main__':
    map_file = sys.argv[1]
    main = Main(map_file)
    main.mainloop()