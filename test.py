import pygame, sys, random

TILESIZE = 20
MAPH = 20
MAPW = 20
BERRIECOUNT = 2

def add_berrie(berries, worm):
    berry = [random.randint(0,MAPW-1), random.randint(0, MAPH-1)]
    while berry in worm or berry in berries:
        berry = [random.randint(0,MAPW-1), random.randint(0, MAPH-1)]
    berries.append(berry)
def init_worm(berries, worm):
    del berries[:]
    del worm[:]
    for i in range(5):
        worm.append([2,2])
    for i in range(BERRIECOUNT):
        add_berrie(berries, worm)

pygame.init()
screen = pygame.display.set_mode((TILESIZE * MAPW, TILESIZE * MAPH))
pygame.display.set_caption("Oskun super matopeli")

counter = 0
running = True
timer = pygame.time.Clock()
berries = []
worm = []
init_worm(berries, worm)
print berries, worm
direction = 2
points = 0
hiscore = 0
fontti = pygame.font.Font(pygame.font.get_default_font(), 16)
while running:
    for a in pygame.event.get():
        if a.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and direction != 1:
        direction = 3
    if keys[pygame.K_RIGHT] and direction != 3:
        direction = 1
    if keys[pygame.K_DOWN] and direction != 0:
        direction = 2
    if keys[pygame.K_UP] and direction != 2:
        direction = 0
    
    counter += 1
    if counter % 5 == 0:
        counter = 0
        new = [(worm[0][0] + [0,1,0,-1][direction])%MAPW, (worm[0][1] + [-1,0,1,0][direction])%MAPH]
        if new in worm or new[0] < 0 or new[1] < 0 or new[0] >= MAPW or new[1] >= MAPH:
            print "CRASH!"
            init_worm(berries, worm)
            direction = 2
            points = 0
        else:
            worm.insert(0,new)
        if new in berries:
            points += 1
            if points > hiscore:
                hiscore = points
            print "ATE BERRY!"
            berries.remove(new)
            add_berrie(berries, worm)
        else:
            worm.pop()

    screen.fill((255,0,0))
    for i in worm:
        pygame.draw.rect(screen, (0,255,0), (TILESIZE*i[0], TILESIZE*i[1], TILESIZE, TILESIZE))
    for i in berries:
        pygame.draw.rect(screen, (0,0,255), (TILESIZE*i[0], TILESIZE*i[1], TILESIZE, TILESIZE))
    screen.blit(fontti.render("Points: " + str(points) + " Hiscore: " + str(hiscore), True, (0,0,0)), (0,0))
        
    pygame.display.flip()
    timer.tick(60)

pygame.quit()