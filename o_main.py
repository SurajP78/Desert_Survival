import random
import pygame
import sys
from settings import *
from entity import *
from projectile import *
from menu import *
from hud import *
import time

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width , screen_height))
        pygame.display.set_caption("Desert Survival")
        self.clock = pygame.time.Clock()
        self.main_menu = Main_menu(self.screen)
        self.game_screen = Game_screen(self.screen)
        self.screen_list = [self.main_menu,self.game_screen,"upgrade_screen"]
        self.current_screen = self.screen_list[0]
        self.running = True


    def run(self):
        while self.running == True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            
        #update



        #draw
        pygame.display.flip()



    pygame.quit()

    def show(self):
        return self.current_screen
    def update(self):
        pass
    def draw(self):
        pass





pygame.init()
clock = pygame.time.Clock()
# setting the screen

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Desert Survival')

main_menu = Main_menu(screen)
game_screen = Game_screen(screen)

current_screen = game_screen




#sets class 
all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
print("HELLLOOOOOOOOOO")
fighter = Player(player_start_x,player_start_y,all_sprites)
small_enemy = Small_enemy(enemy_sprites)
score = Hud()


print(fighter.player_stats["speed"])
print("HELLLOOOOOOOOOO")

#main loop
timer = time.perf_counter()
running = True
while running == True:
    clock.tick(fps)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    current_screen.update()
    current_screen.draw()

    if current_screen == game_screen:
        #current_screen.event_handler()

        if event.type == pygame.MOUSEBUTTONDOWN and fighter.shoot_cooldown == 0:

            fighter.shoot()
            #print("mouse being clicked")
        #updats the all the group sprites and bullets
        all_sprites.update()
        fighter.bullets_group.update()
        enemy_sprites.update()
        score.update()
        if pygame.sprite.spritecollide(small_enemy,fighter.bullets_group,True):
            print("collision theory is correct ")
            small_enemy.take_damage()
        #current_screen.update()
        #current_screen.draw()
        
        # draws the sprites
        all_sprites.draw(screen)
        fighter.bullets_group.draw(screen)
        enemy_sprites.draw(screen)
        score.draw(screen)

        


        pygame.draw.rect(screen, (255, 255, 255), fighter.rect, 1)
        pygame.draw.rect(screen , (0,0,255) , small_enemy.rect , 4)


    pygame.display.flip()
    #print(round(1/(time.perf_counter()-timer)))
    timer = time.perf_counter()



pygame.quit()

