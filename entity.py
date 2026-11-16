from os import pwrite
import pygame
import math
from settings import *
from projectile import *



class Entities(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.player_stats = {
            "current_health": 100,
            "max_health": 100,
            "speed": 10,
            

            }




class Player(pygame.sprite.Sprite):
    def __init__(self,x,y, groups , collision_tile_group , enemy_sprites , collision_sprites,game):
        super().__init__(groups)      
        
        #images
        self.original_image = pygame.transform.rotozoom(pygame.image.load("Images/fighter.png").convert_alpha() , 0 ,3 )
        self.image = self.original_image.copy()
        self.rotated_image = self.image.copy()

        self.pos = pygame.math.Vector2(x,y)
        self.direction = pygame.Vector2(1,0)

        #hitbox
        self.rect = self.image.get_frect(center = (x , y ))
        self.hitbox_rect = self.rect.copy()
        self.hitbox_rect.center = self.rect.center
        self.last_rect = self.rect.copy()   # the rect of the frame before

        #measurements
        self.width = 64
        self.height = self.image.get_width()
        self.width = self.image.get_height()
        self.x_velocity = 0
        self.y_velocity = 0

        #player stats
        self.player_stats = {
                "max_health": 100,
                "speed": 200,
                "regen": True,
                "regen_amount": 0,
        }
        self.player_stats["current_health"] = self.player_stats["max_health"]
        self.regen_cooldown = 3000
        

        #gun stats
        self.gun_stats = {
            "damage": 10,
            "magazine": 10,
            "reload_speed": 2500,
            "shoot_cooldown": 700,

        }

        #gun controller
        self.shoot_time = 0
        self.can_shoot = False
        self.bullet_count = self.gun_stats["magazine"]
        self.reload_start_time = 0
        self.reloading = False



        
        
        self.can_take_damage = False
        #collecting groups
        self.bullets_group = pygame.sprite.Group()
        self.collision_tiles = collision_tile_group 
        self.enemy_sprites = enemy_sprites
        self.collision_sprites = collision_sprites
        self.game = game

        self.rotations = [pygame.transform.rotate(self.image, i) for i in range(-180,180)]




    def update(self , dt , bullet_sprites , screen):  #update methods
        self.last_rect = self.hitbox_rect.copy()
        self.input(bullet_sprites , dt)
        self.move(dt)
        self.shoot_timer()
        self.empty_magazine()
        self.reload()
        self.rotate()

       
    def input(self , bullet_sprites , dt):    #takes in all player inputs during the game
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        
        if keys[pygame.K_r]:
            if self.bullet_count != self.gun_stats["magazine"]:
                if self.reloading == False :
                    self.reloading = True
                    self.reload_start_time = pygame.time.get_ticks()

            

        if pygame.mouse.get_pressed()[0] and self.can_shoot == True and self.reloading == False: # used for shooting
            self.shoot(bullet_sprites , dt )
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            

    def show_shooter(self):
        print("can_shoot  = ", self.can_shoot)
   
   
    def move(self , dt ):
        speed = self.player_stats["speed"]   # gets the speed
        if self.direction.length() != 0:
            self.direction = self.direction.normalize()
       
        #updates rect and checks for collision
        self.hitbox_rect.x += self.direction.x * speed * dt
        self.collision_wall("horizontal")
       
        self.hitbox_rect.y += self.direction.y * speed * dt
        self.collision_wall("vertical")

        self.rect.center = self.hitbox_rect.center

    def collision_wall(self , direction):   # handles the collisions between the player and the wall
        for sprite in self.collision_tiles:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == "horizontal":
                    if self.direction.x > 0:
                        self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.hitbox_rect.left = sprite.rect.right
                if direction == "vertical":
                    if self.direction.y > 0:
                        self.hitbox_rect.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.hitbox_rect.top = sprite.rect.bottom
        
    
    def movement2(self , dt): #movement of the player 
        x_move = 0
        y_move = 0
        speed = self.player_stats["speed"]
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            y_move = -1
        if keys[pygame.K_s]:
            y_move = 1
        if keys[pygame.K_d]:
            x_move = 1
        if keys[pygame.K_a]:
            x_move = -1
        
        if x_move != 0 and y_move != 0:
            magnitude = math.sqrt(x_move**2 + y_move**2)
            x_move /= magnitude
            y_move /= magnitude
        
        self.hitbox_rect.x += x_move * speed * dt

        if self.hitbox_rect.left < 64:
            self.hitbox_rect.x -= x_move * speed * dt
            self.rect.left = 94
        elif self.hitbox_rect.right > 1392:
            self.hitbox_rect.x -= x_move * speed * dt
            self.rect.right = 1382

        self.hitbox_rect.y += y_move * speed * dt

        if self.hitbox_rect.bottom > 777:
            self.hitbox_rect.y -= y_move * speed * dt
            self.rect.bottom = 757
        elif self.rect.top < 75:
            self.hitbox_rect.y -= y_move * speed * dt
            self.rect.top = 95

        self.rect.x = self.hitbox_rect.x
        self.rect.y = self.hitbox_rect.y
    
    
    def show_rect(self):
        return self.rect

    def get_pos(self):
        return self.pos
        

    def rotate(self):   #rotates the player so it is facing the mouse
        angle = self.get_mouse_angle()
        self.image = self.rotations[round(angle)]
        self.rect = self.image.get_frect(center = self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)


    def shoot(self,bullet_sprites, dt):  # performs the action of shooting
        angle = math.radians(self.get_mouse_angle())
        offset_x = math.cos(angle) * 40
        offset_y = math.sin(angle) * -20
        bullet_start_pos = (self.rect.centerx + offset_x, self.rect.centery + offset_y ) 
        bullet = Projectile(bullet_start_pos[0],bullet_start_pos[1], self.get_mouse_angle() , dt)
        bullet_sprites.add(bullet)
        self.bullet_count -= 1


    def shoot_timer(self): #adds a cooldown to being able to shoot
        if self.can_shoot == False:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.gun_stats["shoot_cooldown"]:
                
                self.can_shoot = True
            
    def empty_magazine(self): # checks if the  players ammo = 0 so they cant shoot
        if self.bullet_count <= 0:
            self.can_shoot = False
            
        
    
    def reload(self): # carries out the reload
        if self.reloading == True:
            current_time = pygame.time.get_ticks()
        
            if current_time - self.reload_start_time >= self.gun_stats["reload_speed"]:
                self.reloading = False
                self.bullet_count = self.gun_stats["magazine"]
        

    def get_mouse_angle(self):   # gets the mouse angle from the mouse position
        mx,my = pygame.mouse.get_pos()
        change_x = mx - self.rect.centerx
        change_y = my - self.rect.centery
        angle = math.degrees(math.atan2(-change_y , change_x))
        return angle

         
    def take_damage(self,damage): # changes the players health based on what enemy their attacked by
        self.player_stats["current_health"] -= damage
        self.death()
    
    
    def death(self): # kills the player if the health is below 0
        if self.player_stats["current_health"] <= 0:
            self.kill()
            self.game.current_screen = self.game.menus[3]




class Enemy(pygame.sprite.Sprite):
    def __init__(self,groups,x,y,player,dt,enemy_sprites,collision_sprites):
        super().__init__(groups)
        self.original_image = pygame.image.load("Images/small_enemy.png")
        self.image = pygame.transform.scale_by(self.original_image , 5)
        self.pos = pygame.Vector2 (x,y)
        self.player = player


        self.enemy_sprites = enemy_sprites
        self.collision_sprites = collision_sprites
        
        #creates rects
        self.rect = self.image.get_frect(center = self.pos)
        self.hitbox_rect = self.rect.copy()
        self.last_rect = self.rect.copy()
        self.mask = pygame.mask.from_surface(self.image)

        self.direction = pygame.Vector2()
       #stats of each enemy
        self.stats = {"max_health" : 100,
                       "speed" : 200,
                       "damage" : 10,
                       }
        self.stats["current_health"] = self.stats["max_health"]
        self.attack_cooldown_a = 1000
        self.attack_time = 0
        self.can_attack = True


        self.font = pygame.font.Font(None, 40)
        


    def update(self,dt,screen):  #update methods
        self.last_rect = self.rect.copy()
        self.move(dt)
        self.death()
        self.draw_health(screen)
        
    def death(self):#kills enemy if health below 0 
        if self.stats["current_health"] <= 0:
            self.kill()
            

    def take_damage(self):  #allows the enemy to take damage if it gets hit
            self.stats["current_health"] -= self.player.gun_stats["damage"]
            #print(f"enemy current haelth : {self.stats["current_health"]}")


    def attack_cooldown(self):  # controls the coolddown on how frequent the enemy can attack
        if self.can_attack == False:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_time >= self.attack_cooldown_a:
                self.can_attack = True
        


    def move(self , dt):  #movement for the enemy
        player_pos = pygame.Vector2(self.player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center)

        if (player_pos - enemy_pos).length() != 0:
            self.direction = (player_pos - enemy_pos).normalize()

        else:
            self.direction = pygame.Vector2(0,0)

        self.hitbox_rect.x += self.direction.x * self.stats["speed"] * dt
        #self.collision_player('horizontal')
        self.col_player("horizontal")
        self.collision_enemy("horizontal")
        self.hitbox_rect.y += self.direction.y * self.stats["speed"] * dt
        #self.collision_player('vertical')
        self.col_player("vertical")
        self.collision_enemy("vertical")

        self.rect.x = self.hitbox_rect.x
        self.rect.y = self.hitbox_rect.y 

    def col_player(self,direction):   #used for chwcking for collision between an emeny and the player
        if self.player.hitbox_rect.colliderect(self.hitbox_rect): # checks to see if reccts are overlapping
            if direction == "horizontal":
                if self.hitbox_rect.right >= self.player.hitbox_rect.left and self.last_rect.right <= self.player.last_rect.left:
                    self.hitbox_rect.right = self.player.hitbox_rect.left
                elif self.hitbox_rect.left <= self.player.hitbox_rect.right and self.last_rect.left >= self.player.last_rect.right:
                    self.hitbox_rect.left = self.player.hitbox_rect.right
                    
            if direction == "vertical": # compares rect with last rect to see if its still the same after moving
                if self.hitbox_rect.top <= self.player.hitbox_rect.bottom and self.last_rect.top  >= self.player.last_rect.bottom:
                    self.hitbox_rect.top = self.player.hitbox_rect.bottom
                    
                elif self.hitbox_rect.bottom  >= self.player.hitbox_rect.top and self.last_rect.bottom <= self.player.last_rect.top:
                    self.hitbox_rect.bottom = self.player.hitbox_rect.top
                    
            self.deal_damage() #deals damage to player
            self.attack_cooldown() # cooldown to prevent continous attacking

    def collision_enemy(self , direction): #used for checking for collisions between the enemies using the enemy sprite group
        for sprite in self.enemy_sprites:
            if sprite == self:
                continue
            else: 
                if sprite.rect.colliderect(self.hitbox_rect): # checks to see if the rects overlap
                    if direction == "horizontal":
                        if self.hitbox_rect.right >= sprite.hitbox_rect.left and self.last_rect.right <= sprite.last_rect.left:#checks between recent and last rect
                            self.hitbox_rect.right = sprite.rect.left
                        elif self.hitbox_rect.left <= sprite.hitbox_rect.right and self.last_rect.left >= sprite.last_rect.right:
                            self.hitbox_rect.left = sprite.rect.right
                    if direction == "vertical":
                        if self.hitbox_rect.top <= sprite.hitbox_rect.bottom and self.last_rect.top  >= sprite.last_rect.bottom:
                            self.hitbox_rect.top = sprite.rect.bottom
                        if self.hitbox_rect.bottom  >= sprite.hitbox_rect.top and self.last_rect.bottom <= sprite.last_rect.top:
                            self.hitbox_rect.bottom = sprite.rect.top
    
        
    def deal_damage(self): #if an enemy hits the player , the player takes damage
        if self.can_attack == True:
            self.attack_time = pygame.time.get_ticks()
            self.player.take_damage(self.stats["damage"])
            self.can_attack = False


    def draw_health(self,screen): # used to display the enemy health on the screen
        for sprite in self.enemy_sprites:
            health_text = self.font.render(str(sprite.stats["current_health"]),False,(255,255,255))
            health_text_rect = health_text.get_rect(topleft = (sprite.rect.centerx,sprite.rect.top - 10))
            screen.blit(health_text , health_text_rect)



                
    


        


        

        
        

class Fast_enemy(Enemy):   #creates the fast enemy and adjust the stats
    def __init__(self,groups,x,y , player, dt , enemy_sprites , collision_sprites):
        super().__init__(groups , x ,y , player, dt , enemy_sprites , collision_sprites)
    
        self.original_image = pygame.image.load("Images/small_enemy.png").convert_alpha()
        self.image = pygame.transform.scale_by(self.original_image , 5).convert_alpha()
        self.rect = self.image.get_frect(center = (self.pos))
        self.hitbox_rect = self.rect.copy()
        self.mask = pygame.mask.from_surface(self.image)
        self.stats = {"max_health" : 10,
                       "speed" : 200,
                       "damage" : 5
                       }
        self.stats["current_health"] = self.stats["max_health"]

class Normal_enemy(Enemy):   #creates the normal enemy and adjusts the stats
    def __init__(self,groups,x,y , player, dt , enemy_sprites , collision_sprites):
        super().__init__(groups , x ,y , player, dt , enemy_sprites , collision_sprites)
    
        self.original_image = pygame.image.load("Images/normal_enemy.png").convert_alpha()
        self.image = pygame.transform.scale_by(self.original_image , 5).convert_alpha()

        self.rect = self.image.get_frect(center = (self.pos))
        self.hitbox_rect = self.rect.copy()
        self.mask = pygame.mask.from_surface(self.image)

        self.stats = {"max_health" : 30,
                       "speed" : 150,
                       "damage" : 20}
        self.stats["current_health"] = self.stats["max_health"]

class Tank_enemy(Enemy):  #creates the tank enemy and adjusts the stats
    def __init__(self,groups,x,y , player, dt , enemy_sprites , collision_sprites):
        super().__init__(groups , x ,y , player, dt , enemy_sprites , collision_sprites)
    
        self.original_image = pygame.image.load("Images/tank_enemy.png").convert_alpha()
        self.image = pygame.transform.scale_by(self.original_image , 5).convert_alpha()
        
        self.rect = self.image.get_frect(center = (self.pos))
        self.hitbox_rect = self.rect.copy()
        self.mask = pygame.mask.from_surface(self.image)

        self.stats = {"max_health" : 100,
                       "speed" : 100,
                       "damage" : 40}
        self.stats["current_health"] = self.stats["max_health"]

    
        


        

    
            

            

        