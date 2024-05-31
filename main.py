
import pygame
from pygame.locals import *                                                   # * =importované symboly z pygame (např. QUIT, K_UP,...)
import random

pygame.init()


vyska = 500
sirka = 500
velikost_obrazovky = (vyska, sirka)                                           #parametry hracího okna
obrazovka = pygame.display.set_mode(velikost_obrazovky)
pygame.display.set_caption("Mostní Šílenství: Závod s Osudem")


seda = (100, 100, 80)
bila = (255, 245, 255)
modra = (56, 108, 206)                                                         #palety použitých barev ve hře
zluta = (205, 202, 15)
cervena = (200, 0, 0)


sirka_cesty = 305
sirka_znacky = 9
vyska_znacky = 60
prostrední_pruh = 250
levy_pruh = 150                                                                #parametry pro grafiku hry
pravy_pruh = 350
lajny = [prostrední_pruh, levy_pruh, pravy_pruh]
cesta = (100, 0, sirka_cesty, vyska)
leve_ohraniceni = (95, 0, sirka_znacky, vyska)
prave_ohraniceni = (395, 0, sirka_znacky, vyska)


x_zacatek = 250                                                                 #počáteční pozice pro spawn hráče
y_zacatek = 415
rychlost = 2                                                                    #rychlost jízdy (postupně zvyšující se)
lane_marker_move_y = 5
skore = 0                                                                       #započítané skore (předjeté auto= +1)
gameover = False


clock = pygame.time.Clock()

fps = 90                                                                         #nastavení snímku za sekundu


vozidla_obr = [ "pickup_truck.png", "semi_trailer.png", "taxi.png", "van.png","car.png"]
obrazky_vozidel = [pygame.image.load("Obrazky/" + filename) for filename in vozidla_obr]     #nahrátí obrazků použitých vozidel


bourani = pygame.image.load("Obrazky/boom.png")
bourani_load = bourani.get_rect()                                                 #nahrátí obrázku při narážce do dalšího vozidla

class Vozidlo(pygame.sprite.Sprite):
    def __init__(self, obraz, osa_x, osa_y):
        pygame.sprite.Sprite.__init__(self)                                       
        meritko_obrazku = 57 / obraz.get_rect().width
        vyska_2 = obraz.get_rect().height * meritko_obrazku
        sirka_2 = obraz.get_rect().width * meritko_obrazku
        self.image = pygame.transform.scale(obraz, (sirka_2, vyska_2))
        self.rect = self.image.get_rect()
        self.rect.center = [osa_x, osa_y]

class Hrac(Vozidlo):
    def __init__(self, obrazek, vosa_x, vosa_y):
        super().__init__(obrazek, vosa_x, vosa_y)

def textik(text, font, barva, povrch, x, y):
    textobj = font.render(text, True, barva)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    povrch.blit(textobj, textrect)

def hlavni_menu():
    zvolene_auto = 0
    font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    zvolene_auto = (zvolene_auto - 1) % len(obrazky_vozidel)
                if event.key == K_RIGHT:
                    zvolene_auto = (zvolene_auto + 1) % len(obrazky_vozidel)
                if event.key == K_RETURN:
                    return obrazky_vozidel[zvolene_auto]

        obrazovka.fill(cervena)
        textik("VYBERTE SI VOZIDLO", font, bila, obrazovka, 120, 50)
        
        auto_obr = obrazky_vozidel[zvolene_auto]
        auto_rect = auto_obr.get_rect(center=(sirka // 2, vyska // 2))
        obrazovka.blit(auto_obr, auto_rect.topleft)
        
        textik("Pro výběr použijte šipky: <- ->", font, bila, obrazovka, 70, 370)
        textik("Pro potvrzení stiskněte ENTER", font, bila, obrazovka, 63, 450)

        pygame.display.update()
        clock.tick(fps)

def reset_hry():
    global rychlost, skore, gameover
    rychlost = 2
    skore = 0
    gameover = False
    vozidlo_group.empty()
    ovladac.rect.center = [x_zacatek, y_zacatek]


ovladac_group = pygame.sprite.Group()
vozidlo_group = pygame.sprite.Group()


zvolene_auto = hlavni_menu()
ovladac = Hrac(zvolene_auto, x_zacatek, y_zacatek)
ovladac_group.add(ovladac)


beh_hry = True                                      
while beh_hry:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == QUIT:
            beh_hry = False
        if event.type == KEYDOWN:
            if event.key == K_LEFT and ovladac.rect.center[0] > levy_pruh:
                ovladac.rect.x -= 100
            elif event.key == K_RIGHT and ovladac.rect.center[0] < pravy_pruh:
                ovladac.rect.x += 100
            for vehicle in vozidlo_group:
                if pygame.sprite.collide_rect(ovladac, vehicle):
                    gameover = True
                    if event.key == K_LEFT:
                        ovladac.rect.left = vehicle.rect.right
                        bourani_load.center = [ovladac.rect.left, (ovladac.rect.center[1] + vehicle.rect.center[1]) / 2]
                    elif event.key == K_RIGHT:
                        ovladac.rect.right = vehicle.rect.left
                        bourani_load.center = [ovladac.rect.right, (ovladac.rect.center[1] + vehicle.rect.center[1]) / 2]

    
    obrazovka.fill(modra)
    pygame.draw.rect(obrazovka, seda, cesta)                                              #vykreslení obrazovky
    pygame.draw.rect(obrazovka, zluta, leve_ohraniceni)
    pygame.draw.rect(obrazovka, zluta, prave_ohraniceni)

    lane_marker_move_y += rychlost * 2
    if lane_marker_move_y >= vyska_znacky * 2:
        lane_marker_move_y = 0
    for y in range(vyska_znacky * -2, vyska, vyska_znacky * 2):
        pygame.draw.rect(obrazovka, bila, (levy_pruh + 45, y + lane_marker_move_y, sirka_znacky, vyska_znacky))
        pygame.draw.rect(obrazovka, bila, (prostrední_pruh + 45, y + lane_marker_move_y, sirka_znacky, vyska_znacky))

    ovladac_group.draw(obrazovka)

    if len(vozidlo_group) < 2:
        add_vehicle = True
        for vehicle in vozidlo_group:
            if vehicle.rect.top < vehicle.rect.height * 1.5:
                add_vehicle = False
        if add_vehicle:
            lane = random.choice(lajny)
            image = random.choice(obrazky_vozidel)
            vehicle = Vozidlo(image, lane, vyska / -2)
            vozidlo_group.add(vehicle)

    for vehicle in vozidlo_group:
        vehicle.rect.y += rychlost
        if vehicle.rect.top >= vyska:
            vehicle.kill()
            skore += 1
            if skore > 0 and skore % 5 == 0:
                rychlost += 1

    vozidlo_group.draw(obrazovka)

    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render("Skóre: " + str(skore), True, bila)
    text_rect = text.get_rect()
    text_rect.center = (50, 400)
    obrazovka.blit(text, text_rect)

    if pygame.sprite.spritecollide(ovladac, vozidlo_group, True):
        gameover = True
        bourani_load.center = [ovladac.rect.center[0], ovladac.rect.top]

    if gameover:
        obrazovka.blit(bourani, bourani_load)
        pygame.draw.rect(obrazovka, cervena, (0, 50, sirka, 100))
        text = font.render("KONEC HRY. Chcete hrát znovu? (A nebo N)", True, bila)
        text_rect = text.get_rect()
        text_rect.center = (sirka / 2, 100)
        obrazovka.blit(text, text_rect)

    pygame.display.update()

    while gameover:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == QUIT:
                gameover = False
                beh_hry = False
            if event.type == KEYDOWN:
                if event.key == K_a:
                    reset_hry()
                elif event.key == K_n:
                    gameover = False
                    beh_hry = False

pygame.quit()
