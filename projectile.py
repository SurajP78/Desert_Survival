import pygame
import math
from settings import *
from entity import *



class Projectile(pygame.sprite.Sprite):
    def __init__(self,x,y,angle , dt):
        super().__init__()
        self.image = pygame.image.load("Images/bullet.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image , 0 , 0.05 )
        self.speed = 500
        self.rect = self.image.get_frect(center = (x,y))
        self.angle = angle
        self.x_velocity = math.cos(math.radians(self.angle)) * self.speed 
        self.y_velocity = math.sin(math.radians(self.angle)) * -self.speed
        self.range = 700 #in pixels
        

    

    def move(self, dt):    # moves the bullet rect 

        self.rect.x += self.x_velocity * dt
        self.rect.y += self.y_velocity * dt

    def update(self , dt): #updates
        self.move(dt)

        

        #if self.rect.x < 0 or self.rect.x > 1440 or self.rect.y < 0 or self.rect.y < 900:
            #self.kill()

        # if math.sqrt((self.rect.x ** 2 ) + (self.rect.y ** 2)) > self.range:
        #     self.kill()
        #     print("bullet died")



    





        