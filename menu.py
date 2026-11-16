import pygame
from settings import *
from random import choice

class Screen():  # starts the screen class
    def __init__(self,screen):
        self.screen = screen
        self.dimensions = (1440,900)


    def update(self):
        pass

    def draw(self):
        pass

    


class Main_menu(Screen): # class for the main menu
    def __init__(self,screen):
        super().__init__(screen)
        #main background
        self.image = pygame.transform.scale(pygame.image.load("Images/main_menu_v3.png").convert_alpha(),(self.dimensions))
        self.original_play_button = pygame.image.load("Images/play_button.png").convert_alpha()
        self.play_button = pygame.transform.scale_by(self.original_play_button, 10)
        self.play_button_rect = self.play_button.get_rect(center = (300,700))
        self.how_to_play_button = pygame.transform.scale(pygame.image.load("Images/how_to_play_button.png").convert_alpha(),(500,100))
        self.how_to_play_button_rect = self.how_to_play_button.get_rect(center = (1100,700))

    def draw(self):#draws all the elements on the screen
        self.screen.blit(self.image, (0,0))
        self.screen.blit(self.play_button , self.play_button_rect)
        self.screen.blit(self.how_to_play_button,self.how_to_play_button_rect)
    
    
    def input(self):# takes in the input of the mouse being pressed and reurns the new screen based on which button is pressed
        #by using the the mouse pos at the time of the click
        mx,my = pygame.mouse.get_pos()

        if self.play_button_rect.collidepoint(mx,my) == True:
            #return True
            return "play"

        if self.how_to_play_button_rect.collidepoint(mx,my) == True:
            return "how_to_play"
        

class How_to_play(Screen):
    def __init__(self,screen):
        super().__init__(screen)
        self.image =  pygame.transform.scale(pygame.image.load("Images/how_to_play.png").convert_alpha(),(self.dimensions))
        self.return_button =  pygame.transform.scale(pygame.image.load("Images/return.png").convert_alpha(),(1000,200))
        self.return_button_rect = self.return_button.get_rect(center = (700,730))

    def draw(self):
        self.screen.blit(self.image , (0,0))
        self.screen.blit(self.return_button,self.return_button_rect)
    
    def input(self):
        mx,my = pygame.mouse.get_pos()

        if self.return_button_rect.collidepoint(mx,my) == True:
            return True






class Game_over_screen(Screen):
    def __init__(self,screen,):
        super().__init__(screen)
        self.image = pygame.transform.scale(pygame.image.load("Images/game_over_v3.png").convert_alpha(),(self.dimensions))
        self.play_again_image = pygame.transform.scale(pygame.image.load("Images/play_again_button.png").convert_alpha(),(900,200)) 
        self.play_again_image_rect = self.play_again_image.get_rect(center = (750,600))
        self.font = pygame.font.Font(None,100)
        self.round = 0
        self.show_round = self.font.render(f"You managed to reach round:  {self.round}\n Try again next time",True,(0,255,0))
        self.show_round_rect = self.show_round.get_rect(center = (600,450))

    def draw(self):
        self.update_round()
        self.screen.blit(self.image, (0,0))
        self.screen.blit(self.show_round , self.show_round_rect)

    def update_round(self):
        self.show_round = self.font.render(f"You managed to reach round:  {self.round}",True,(0,255,0))
        self.show_round_rect = self.show_round.get_rect(center = (650,450))

    def get_round(self,round):
        self.round = round

        
        # self.screen.blit(self.play_again_image,self.play_again_image_rect)

    # def input(self):
    #     mx,my = pygame.mouse.get_pos()

    #     if self.play_again_image_rect.colliderect(mx,my) == True:
    #         return True
    
class Upgrades(Screen):
    def __init__(self,screen,player,game):
        super().__init__(screen)
        self.background_image = pygame.transform.scale(pygame.image.load("Images/upgrades_screen.png").convert_alpha(),(self.dimensions))
        self.player = player
        self.game = game
        self.font = pygame.font.Font(None , 40)


        self.pos1 = (300,400)
        self.pos2 = (700,400)
        self.pos3 = (1100 , 400)


        self.upgrades = {
            "fire_rate_lvl": 0,
            "damage_lvl": 0,
            "magazine_size_lvl": 0,
            "reload_speed_lvl" : 0,
            "move_speed_lvl": 0,
            "health_regen_lvl": 0,
            "max_health_lvl": 0,
            "piercing_bullets_lvl": 0,
            "bouncing_bullets_lvl": 0,
            
        }

        self.possible_upgrades = {
            1:["fire_rate_lvl1","fire_ratelvl2","fire_ratelvl3"],
            2:["damage_lvl1","damage_lvl2","damage_lvl3"],
            3:["magazine_size_lvl1","magazine_size_lvl2","magazine_size_lvl3"],
            4:["reload_speed_lvl1","reload_speed_lvl2","reload_speed_lvl3"],
            5:["move_speed_lvl1", "move_speed_lvl2", "move_speed_lvl3"],
            6:["health_regen_lvl1", "health_regen_lvl2", "health_regen_lvl3"],
            7:["max_health_lvl1","max_health_lvl2","max_health_lvl3"],
            8:["piercing_bullets_lvl1","piercing_bullets_lvl2","piercing_bullets_lvl3"],
            9:["bouncing_bullets_lvl1","bouncing_bullets_lvl2","bouncing_bullets_lvl3"]

        
        }
        
        self.fire_rate_1 = pygame.transform.scale(pygame.image.load("Images/fire_rate_1.png"), (300,300))
        self.fire_rate_2 = pygame.transform.scale(pygame.image.load("Images/fire_rate_2.png"), (300,300))
        self.fire_rate_3 = pygame.transform.scale(pygame.image.load("Images/fire_rate_3.png") , (300,300))
        self.damage_1 = pygame.transform.scale(pygame.image.load("Images/damage_1.png"),(300,300))
        self.damage_2 = pygame.transform.scale(pygame.image.load("Images/damage_2.png"),(300,300))
        self.damage_3 = pygame.transform.scale(pygame.image.load("Images/damage_3.png"),(300,300))
        self.magazine_1 = pygame.transform.scale(pygame.image.load("Images/magazine_1.png"),(300,300))
        self.magazine_2 = pygame.transform.scale(pygame.image.load("Images/magazine_2.png"),(300,300))
        self.magazine_3 = pygame.transform.scale(pygame.image.load("Images/magazine_3.png"),(300,300))
        self.reload_1 = pygame.transform.scale(pygame.image.load("Images/reload_1.png"),(300,300))
        self.reload_2 = pygame.transform.scale(pygame.image.load("Images/reload_2.png"),(300,300))
        self.reload_3 = pygame.transform.scale(pygame.image.load("Images/reload_3.png"),(300,300))
        self.move_speed_1 = pygame.transform.scale(pygame.image.load("Images/movespeed_1.png"),(300,300))
        self.move_speed_2 = pygame.transform.scale(pygame.image.load("Images/movespeed_2.png"),(300,300))
        self.move_speed_3 = pygame.transform.scale(pygame.image.load("Images/movespeed_3.png"),(300,300))
        self.health_regen_1 = pygame.transform.scale(pygame.image.load("Images/regen_1.png"),(300,300))
        self.health_regen_2 = pygame.transform.scale(pygame.image.load("Images/regen_2.png"),(300,300))
        self.health_regen_3 = pygame.transform.scale(pygame.image.load("Images/regen_3.png"),(300,300))
        self.max_health_1 = pygame.transform.scale(pygame.image.load("Images/health_1.png"),(300,300))
        self.max_health_2 = pygame.transform.scale(pygame.image.load("Images/health_2.png"),(300,300))
        self.max_health_3 = pygame.transform.scale(pygame.image.load("Images/health_3.png"),(300,300))

        self.max_upgrade = pygame.transform.scale(pygame.image.load("Images/max_upgrade.png"),(300,300))
        self.max_upgrade_rect = self.max_upgrade.get_rect(center = (700,450))


        self.upgrade_images = {
            1:[self.fire_rate_1,self.fire_rate_2,self.fire_rate_3],
            2:[self.damage_1,self.damage_2,self.damage_3],
            3:[self.magazine_1,self.magazine_2,self.magazine_3],
            4:[self.reload_1,self.reload_2,self.reload_3],
            5:[self.move_speed_1,self.move_speed_2,self.move_speed_3],
            6:[self.health_regen_1,self.health_regen_2,self.health_regen_3],
            7:[self.max_health_1,self.max_health_2,self.max_health_3]

            }
        
        self.x_image =self.fire_rate_1 = pygame.transform.scale(pygame.image.load("Images/fire_rate_1.png"), (100,100)) #self.upgrade_images[6][2]
        self.x_rect = self.x_image.get_rect(center = self.pos1)
        self.y_image =self.fire_rate_1 = pygame.transform.scale(pygame.image.load("Images/fire_rate_1.png"), (100,100)) #self.upgrade_images[6][2]
        self.y_rect = self.y_image.get_rect(center = self.pos2)
        self.z_image = self.fire_rate_1 = pygame.transform.scale(pygame.image.load("Images/fire_rate_1.png"), (100,100))#self.upgrade_images[6][2]
        self.z_rect = self.z_image.get_rect(center = self.pos3)

        self.upgrade_descriptions = {
            0: "Max upgrade",
            1: "Increase fire rate",
            2: "Increase damage",
            3: "increase magazine size",
            4 : "Decrease reload time",
            5: "Increase move speed",
            6: "Increase health regen",
            7: "Increase max health",
            "piercing_bullets_lvl":0,
            "bouncing_bullets_lvl":0

        }

        self.x_text = None
        self.x_text_rect = None
        self.y_text = None
        self.y_text_rect = None
        self.z_text = None
        self.z_text_rect = None

        self.upgrade_instruction = self.font.render("Press on the upgrade icon you want" , True,(255,255,255))
        self.upgrade_instruction_rect = self.upgrade_instruction.get_rect(center = (self.pos2[0], self.pos2[1] + 350))



        self.chosen = False
        self.choices = []
        self.original_list = [1,2,3,4,5,6,7]
        self.up_list = self.original_list.copy()
        

    def draw(self):
        self.draw_bg()
        self.get_upgrade_images()
        self.x_rect = self.x_image.get_rect(center = self.pos1)
        self.screen.blit(self.x_image , self.x_rect)
        self.y_rect = self.y_image.get_rect(center = self.pos2)
        self.screen.blit(self.y_image,self.y_rect)
        self.z_rect = self.z_image.get_rect(center = self.pos3)
        self.screen.blit(self.z_image, self.z_rect)
        self.draw_descriptions()

    def draw_bg(self):
         self.screen.blit(self.background_image , (0,0))


    def choose_random_upgrade(self):
        self.up_list = self.original_list.copy()
        while len(self.up_list) < 3:
            self.up_list.append(0)
       
        x = choice(self.up_list)
        self.up_list.remove(x)
        y = choice(self.up_list)
        self.up_list.remove(y)
        z = choice(self.up_list)
        self.up_list.remove(z)
        self.choices = [x,y,z]
       

        for letter in self.choices:
            if letter == 0:
                continue
            else:  
                 if len(self.possible_upgrades[letter]) == 0:
                    self.original_list.remove(letter)
                    
                    return self.choose_random_upgrade()
            
        self.choices = [x,y,z]

        return
    
    def get_upgrade_images(self):
        if self.chosen == False:
            self.choose_random_upgrade()
            #print(f"x = {x} y = {y} z = {z}")
            #self.choices = [x,y,z]
            #print(f"final one{x,y,z}")
           
            upgrade_options = [self.x_image , self.y_image , self.z_image]
            i = 0

            for letter in self.choices:
                if letter == 0:
                    upgrade_options[i] = self.max_upgrade
                else:
                    if letter == 1:
                        key = self.upgrades["fire_rate_lvl"]
                    elif letter == 2:
                        key = self.upgrades["damage_lvl"]
                    elif letter == 3:
                        key = self.upgrades["magazine_size_lvl"]
                    elif letter == 4:
                        key = self.upgrades["reload_speed_lvl"]
                    elif letter == 5:
                        key = self.upgrades["move_speed_lvl"]
                    elif letter == 6:
                        key = self.upgrades["health_regen_lvl"]
                    elif letter == 7:
                        key = self.upgrades["max_health_lvl"]
                    #print(letter)
                    #print(key)
                    upgrade_options[i] = self.upgrade_images[letter][key]

                # else:
                #     upgrade_options[i] = self.max_upgrade
                #     self.choices[i] = 0
                
                i += 1 
            self.x_image = upgrade_options[0]
            self.y_image = upgrade_options[1]
            self.z_image = upgrade_options[2]
            self.get_descriptions()

            self.chosen = True
        
    def event_handler(self):
        mx,my = pygame.mouse.get_pos()
        if self.x_rect.collidepoint(mx,my) == True:
            value = self.choices[0]
            if value == 1:
                self.fire_rate_increase()
                self.upgrades["fire_rate_lvl"] += 1
            elif value == 2:
                self.damage_increase()
                self.upgrades["damage_lvl"] += 1
            elif value == 3:
                self.magazine_size_increase()
                self.upgrades["magazine_size_lvl"] += 1
            elif value == 4:
                self.reload_speed_decrease()
                self.upgrades["reload_speed_lvl"] += 1
            elif value == 5:
                self.move_speed_increase()
                self.upgrades["move_speed_lvl"] += 1
            elif value == 6:
                self.health_regen_increase()
                self.upgrades["health_regen_lvl"] += 1
            elif value == 7:
                self.max_health_increase()
                self.upgrades["max_health_lvl"] += 1
            
            if value != 0:
                del(self.possible_upgrades[value][0])
            self.chosen = False
            self.player.bullet_count = self.player.gun_stats["magazine"]
            return True
        
        if self.y_rect.collidepoint(mx,my) == True:
            value = self.choices[1]
            if value == 1:
                self.fire_rate_increase()
                self.upgrades["fire_rate_lvl"] += 1
            elif value == 2:
                self.damage_increase()
                self.upgrades["damage_lvl"] += 1
            elif value == 3:
                self.magazine_size_increase()
                self.upgrades["magazine_size_lvl"] += 1
            elif value == 4:
                self.reload_speed_decrease()
                self.upgrades["reload_speed_lvl"] += 1
            elif value == 5:
                self.move_speed_increase()
                self.upgrades["move_speed_lvl"] += 1
            elif value == 6:
                self.health_regen_increase()
                self.upgrades["health_regen_lvl"] += 1
            elif value == 7:
                self.max_health_increase()
                self.upgrades["max_health_lvl"] += 1
            if value != 0:
                del(self.possible_upgrades[value][0])
            self.chosen = False
            self.player.bullet_count = self.player.gun_stats["magazine"]
            return True
              
        if self.z_rect.collidepoint(mx,my) == True:
            value = self.choices[2]
            if value == 1:
                self.fire_rate_increase()
                self.upgrades["fire_rate_lvl"] += 1
            elif value == 2:
                self.damage_increase()
                self.upgrades["damage_lvl"] += 1
            elif value == 3:
                self.magazine_size_increase()
                self.upgrades["magazine_size_lvl"] += 1
            elif value == 4:
                self.reload_speed_decrease()
                self.upgrades["reload_speed_lvl"] += 1
            elif value == 5:
                self.move_speed_increase()
                self.upgrades["move_speed_lvl"] += 1
            elif value == 6:
                self.health_regen_increase()
                self.upgrades["health_regen_lvl"] += 1
            elif value == 7:
                self.max_health_increase()
                self.upgrades["max_health_lvl"] += 1
            if value != 0:
                del(self.possible_upgrades[value][0])
            self.chosen = False
            self.player.bullet_count = self.player.gun_stats["magazine"]
            return True
 

        


    def fire_rate_increase(self): 
        self.player.gun_stats["shoot_cooldown"] -= 100
    
    def damage_increase(self):
        self.player.gun_stats["damage"] += 10
    
    def magazine_size_increase(self):
        self.player.gun_stats["magazine"] += 10
    
    def reload_speed_decrease(self):
        self.player.gun_stats["reload_speed"] -= 500
    
    def move_speed_increase(self):
        self.player.player_stats["speed"] += 30
    
    def health_regen_increase(self):
        self.player.player_stats["regen"] = True
        self.player.player_stats["regen_amount"] += 5
    
    def max_health_increase(self):
        diff = self.player.player_stats["max_health"] - self.player.player_stats["current_health"]
        self.player.player_stats["max_health"] += 20
        self.player.player_stats["current_health"] = self.player.player_stats["max_health"] - diff

    def get_descriptions(self):  # gets description of the three upgrades that are going to be displayed
        self.x_text = self.font.render(self.upgrade_descriptions[self.choices[0]] , True , (255,255,255))
        self.x_text_rect = self.x_text.get_rect(center = (self.pos1[0],self.pos1[1] + 200))
        self.y_text = self.font.render(self.upgrade_descriptions[self.choices[1]] , True , (255,255,255))
        self.y_text_rect = self.y_text.get_rect(center = (self.pos2[0],self.pos2[1] + 200))
        self.z_text = self.font.render(self.upgrade_descriptions[self.choices[2]] , True , (255,255,255))
        self.z_text_rect = self.z_text.get_rect(center = (self.pos3[0],self.pos3[1] + 200))
    
        

            
    def draw_descriptions(self): # draws the descriptions of the upgrades on screen and a instruction
       
        self.screen.blit(self.x_text, self.x_text_rect)
        self.screen.blit(self.y_text , self.y_text_rect)
        self.screen.blit(self.z_text , self.z_text_rect)
        self.screen.blit(self.upgrade_instruction , self.upgrade_instruction_rect)



                
            
        
                
        
            
            


