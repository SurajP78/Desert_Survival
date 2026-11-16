import pygame
from settings import *






class Hud():
    def __init__(self,screen,player,enemy_group):
        self.screen = screen
        self.player = player
        self.font = pygame.font.Font(None , 40)
        self.current_time = pygame.time.get_ticks() // 100
        self.enemy_sprites = enemy_group

        #round
        self.round = 0
        self.round_surf = self.font.render(f"round:{self.round}", True , (255,255,255))
        self.round_rect = self.round_surf.get_rect(center = (100,40))

        #ammo
        self.ammo_pos = (20,770)
        self.ammo_y = 760
        self.ammo_icon = pygame.transform.scale(pygame.image.load("Images/ammo_icon.png"),(100,50))
        self.ammo_text = self.font.render(str(self.player.bullet_count) , False ,(255,255,255))
        self.ammo_text_rect = self.ammo_text.get_rect(center = (130,760))
        self.magazine_text = self.font.render(f"/{str(self.player.gun_stats["magazine"])}" , False , (255,255,255))
        self.magazine_text_rect = self.magazine_text.get_rect(center = (160,760))

        #player health
        self.health_pos = (550,775)
        self.health_bar_image = pygame.transform.scale(pygame.image.load("Images/health_bar.png"),(400,50))
        self.current_health_text = self.font.render(str(self.player.player_stats["current_health"]),False , (0,0,0))
        self.current_health_text_rect = self.current_health_text.get_rect(center = (self.health_pos[0] , self.health_pos[1]))
        self.max_health = self.font.render(str(self.player.player_stats["max_health"]),False, (0,0,0))
        self.max_health_rect = self.max_health.get_rect(center = (self.health_pos[0] + 200 , self.health_pos[1]))

        #enemy health
        self.enemy_healths = {}



    def draw(self):
        self.screen.blit(self.round_surf , self.round_rect)
        self.screen.blit(self.ammo_icon,self.ammo_pos)
        self.screen.blit(self.ammo_text , self.ammo_text_rect)
        self.screen.blit(self.magazine_text,self.magazine_text_rect)

        self.screen.blit(self.health_bar_image,self.health_pos)
        self.screen.blit(self.current_health_text , self.current_health_text_rect)
        self.screen.blit(self.max_health,self.max_health_rect)
    
    def update(self):

        #ammo
        self.ammo_text = self.font.render(str(self.player.bullet_count) , False ,(255,255,255))
        self.ammo_text_rect = self.ammo_text.get_rect(center = (150,800))
        self.magazine_text = self.font.render(f"/{str(self.player.gun_stats["magazine"])}" , False , (255,255,255))
        self.magazine_text_rect = self.magazine_text.get_rect(center = (185,800))

        #health
        self.current_health_text = self.font.render(str(self.player.player_stats["current_health"]),False , (0,0,0))
        self.current_health_text_rect = self.current_health_text.get_rect(center = (self.health_pos[0]  + 70, self.health_pos[1]+ 30))
        self.max_health = self.font.render(str(self.player.player_stats["max_health"]),False, (0,0,0))
        self.max_health_rect = self.max_health.get_rect(center = (self.health_pos[0]+ 300 , self.health_pos[1]+30))
        

    def update_round(self,round):
        self.round = round
        self.round_surf = self.font.render(f"round:{self.round}", True , (255,255,255))
        self.round_rect = self.round_surf.get_rect(center = (100,40))

    def draw_health(self):
        for sprite in self.enemy_sprites:
            health_text = self.font.render(str(sprite.stats["current_health"]),False,(50,255,50))
            health_text_rect = health_text.get_rect(topleft = (sprite.rect.centerx,sprite.rect.top - 25))
            self.screen.blit(health_text , health_text_rect)

    # def update_enemy_health(self):
    #     self.enemy_health_text.clear()
    #     for enemy in self.enemy_group:
    #         enemy_health_text = self.font.render(str(enemy.stats["current_health"]),False , (0,0,0) ,(255,0,0))
    #         enemy_health_text_rect = self.enemy_health_text.get_rect(center = (enemy.rect.center))
    
    # def draw_enemy(self):
    #     self.screen.blit(self.enemy_health_text, self.enemy_health_text_rect)
        
        

class Score():
    def __init__(self):
        self.font = pygame.font.Font(None , 40)
        self.current_time = pygame.time.get_ticks() // 1000
        self.text_surf = self.font.render(str(self.current_time) , True, (0,255,0))
        self.text_rect = self.text_surf.get_rect(midbottom = (screen_width / 2 , screen_height - 100 ))

