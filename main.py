import pygame
from settings import *
from menu import *
from hud import *
from map import Map
from entity import *
from random import randint
#from stage import Stage
from stage_queue import Queue


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width , screen_height),pygame.RESIZABLE)

        pygame.display.set_caption("Desert Survival")
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
        self.running = True
        self.round_started = False
        
        #groups
        self.all_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.tiles_group = pygame.sprite.Group()
        self.collision_tiles = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()



        #classes
        self.map = Map(self.tiles_group,self.collision_tiles)
        self.fighter = Player(player_start_x,player_start_y,(self.all_sprites,self.collision_sprites),self.collision_tiles , self.enemy_sprites , self.collision_sprites , self)
        self.hud = Hud(self.screen,self.fighter,self.enemy_sprites)
        self.stage_queue = Queue(self)

        #stage
        self.round = 0
        #self.stage = self.stage1.stage
        


        #menus

        self.main_menu = Main_menu(self.screen)
        self.game_over_screen = Game_over_screen(self.screen)
        self.upgrades_screen = Upgrades(self.screen,self.fighter,self)
        self.how_to_play_screen = How_to_play(self.screen)
        #self.game_screen = Game_screen(self.screen)
        self.menus = (self.main_menu,"game_screen","upgrades","game_over","how_to_play")
        self.current_screen = self.menus[0]
        
    
        
        #creates events for enemy spawns

        self.fast_enemy_event = pygame.event.custom_type()
        self.normal_enemy_event = pygame.event.custom_type()
        self.tank_enemy_event = pygame.event.custom_type()

        self.health_regen_event = pygame.event.custom_type()
        self.regen_timer_active = False
      

    def run(self):
        
        while self.running == True:
            if self.current_screen == self.menus[0]: # drawing main_menu
                game.draw_mainmenu()
            
            if self.current_screen == self.menus[4]: #drawing instructions page
                game.draw_how_to_play_screen()

            if self.current_screen == self.menus[3]: # drawing game _over
                game.draw_game_over_screen()
            
            if self.current_screen == self.menus[2]: #drawing the upgrade screen
                self.round_started = False 
                self.upgrades_screen.get_upgrade_images
                dt = self.clock.tick(120) / 1000
                for event in pygame.event.get():    # used to close the game

                    if event.type == pygame.QUIT:
                        self.running = False
                        pygame.quit()
                        return
                
                    if event.type == pygame.MOUSEBUTTONDOWN: # detects when mouse is pressed for upgrade to happen
                        
                        if self.upgrades_screen.event_handler():
                            self.current_screen = self.menus[1]
                            self.round += 1
                            self.stage_queue.add_round()
                            self.hud.update_round(self.round)
                            self.enemy_timers()



                self.upgrades_screen.draw()
               


                pygame.display.update()
                
                

            if self.current_screen == self.menus[1]: # the main game loop 
                dt = self.clock.tick(fps) / 1000
                self.regen_timer()
                #print(self.clock.get_fps())
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False

                    if event.type in [self.fast_enemy_event,self.normal_enemy_event,self.tank_enemy_event]:#checks if the round has started
                        self.round_started = True

                    if event.type == self.fast_enemy_event: # creating all of the different type of enemies
                        x,y = self.choose_random_enemy_coords()
                        Fast_enemy((self.enemy_sprites , self.collision_sprites) , x , y , self.fighter , dt, self.enemy_sprites,self.collision_sprites)
                    if event.type == self.normal_enemy_event:
                        x,y = self.choose_random_enemy_coords()
                        Normal_enemy((self.enemy_sprites , self.collision_sprites) , x , y , self.fighter , dt , self.enemy_sprites,self.collision_sprites)
                    if event.type == self.tank_enemy_event:
                        x,y = self.choose_random_enemy_coords()
                        Tank_enemy((self.enemy_sprites , self.collision_sprites) , x , y , self.fighter , dt,self.enemy_sprites,self.collision_sprites )

                    #used for health regen upgrade, once eplayer unlocks level 1 upgrade this timer begins    
                    if event.type == self.health_regen_event:
                        if self.fighter.player_stats["current_health"] < self.fighter.player_stats["max_health"]:
                            new_health = self.fighter.player_stats["current_health"] + self.fighter.player_stats["regen_amount"]
                            if new_health >= self.fighter.player_stats["max_health"]:
                                self.fighter.player_stats["current_health"] = self.fighter.player_stats["max_health"]
                            else:
                                self.fighter.player_stats["current_health"] = new_health
                            
            

                
                #update
                self.tiles_group.update()
                self.all_sprites.update(dt , self.bullet_sprites , self.screen)
                self.bullet_sprites.update(dt)
                self.enemy_sprites.update(dt,self.screen)
                self.bullet_collisions()
                self.hud.update()

            

                if self.round_started == True: # check to see if all enemies are dead then moves onto upgrade screen
                    if len(self.enemy_sprites) == 0:
                        #self.round += 1
                        self.stage_queue.remove_round()
                        self.current_screen = self.menus[2]
                        continue



                #draw
                self.screen.fill("black")
                self.tiles_group.draw(self.screen)
                # for sprite in self.collision_tiles:
                #     pygame.draw.rect(self.screen , ( 0,30,0), sprite.rect , 2)
                # for sprite in self.enemy_sprites:
                #     pygame.draw.rect(self.screen , ( 0,255,0), sprite.rect , 2)
                # pygame.draw.rect(self.screen , (255,0,0) , self.fighter.rect , 2)
                # pygame.draw.rect(self.screen , (0,0,255) , self.fighter.hitbox_rect , 2)
                self.all_sprites.draw(self.screen)
                self.enemy_sprites.draw(self.screen)
                self.bullet_sprites.draw(self.screen)
                self.hud.draw()
                self.hud.draw_health()

                pygame.display.update()



        pygame.quit()
   
   
    def choose_random_enemy_coords(self): # gets random cooridnate for an enemy to spawn in
        coord_choice = randint(0,1)
        if coord_choice == 1:
            choicex_list= []
            choice_x = randint(0,1)
            x_left  = randint(0,64)
            x_right = randint(1390 , 1440)
            choicex_list.append(x_left)
            choicex_list.append(x_right)
            x = choicex_list[choice_x]
            y = randint(0,900)
            return x,y
        
        if coord_choice == 0:
            choicey_list= []
            choice_y = randint(0,1)
            y_top  = randint(0,64)
            y_bottom = randint(840, 900)
            choicey_list.append(y_top)
            choicey_list.append(y_bottom)
            x = randint(0,1440)
            y = choicey_list[choice_y]
            return x,y

    

    def bullet_enemy_collisions(self): #detects collision between enemy and bullet and the enemy takes damage
        collisions = pygame.sprite.groupcollide(self.enemy_sprites , self.bullet_sprites , False , True)
        for enemy in collisions:
            for bullet in collisions[enemy]:
                enemy.take_damage()
    
    def bullet_walll_collisions(self):# kills a bullet if it hits the wall
        pygame.sprite.groupcollide(self.collision_tiles , self.bullet_sprites , False , True)
    
    def bullet_collisions(self):
        self.bullet_enemy_collisions()
        self.bullet_walll_collisions()
    
    def draw_mainmenu(self): #used to handle the main menu
        next_menu = False
        dt = self.clock.tick(120) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                return
            
            if event.type == pygame.MOUSEBUTTONDOWN: #detects if a button was pressed 
                if self.main_menu.input() == "play":
                    #next_menu = True
                    self.current_screen = self.menus[1]
                    self.enemy_timers()
                    return None
                if self.main_menu.input() == "how_to_play":
                    self.current_screen = self.menus[4]
                    return None
            
        # if next_menu == True:
        #     self.current_screen = self.menus[1]
        #     self.enemy_timers()
        #     return None

        self.main_menu.draw()
        pygame.display.update()
        
    def draw_game_over_screen(self): #used to handle game over screen
            dt = self.clock.tick(120) / 1000
            self.game_over_screen.get_round(self.round)
            #print(self.round)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    return
                
            self.game_over_screen.draw()
            pygame.display.update()

    def draw_how_to_play_screen(self): #used to handle hwo to play screen
        next_menu = False
        dt = self.clock.tick(120) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                return
            
            if event.type == pygame.MOUSEBUTTONDOWN:  #detects mouse pressed and detecs collision with button
                if self.how_to_play_screen.input() == True:
                    next_menu = True
            
        if next_menu == True:    #swaps to next screen
            self.current_screen = self.menus[0]
            return None

        self.how_to_play_screen.draw()
        pygame.display.update()

    def enemy_timers(self):   #controls the enemy timers so they spawn at the start of every round
        current_stage = self.stage_queue.stages
        #print(current_stage)
        if current_stage[0][0] > 0:
            pygame.time.set_timer(self.fast_enemy_event , 500 , current_stage[0][0])
        if current_stage[0][1] > 0:
            pygame.time.set_timer(self.normal_enemy_event , 1000 , current_stage[0][1])
        if current_stage[0][2] > 0:
            pygame.time.set_timer(self.tank_enemy_event , 1500 , current_stage[0][2])
        
    def regen_timer(self): #is a timer for the regen , once it is activated , it doesnt run again as the timer stay on from then
        if self.fighter.player_stats["regen"] and not self.regen_timer_active:
            pygame.time.set_timer(self.health_regen_event,5000,)
            self.regen_timer_active = True
            #print("active")

            
    def check_end_round(self):  # checks to see if all enemies are dead
        if not self.enemy_sprites.sprites():
            self.current_screen = self.menus[2]
    
    def get_round(self):
        return self.round


if __name__ == "__main__":  # starts the game
    game = Game()
    # if game.current_screen == game.main_menu:
    #     game.draw_menu()
    # if game.current_screen == "work":
    #     print("Hurray")
    game.run()
    

