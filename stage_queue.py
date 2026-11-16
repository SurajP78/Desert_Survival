from random import randint
from collections import deque

class Queue():
    def __init__(self,game):
        self.game = game
        self.stages = []

        self.initial_stages = {
            0:  [1,0,0],
            1:  [3 , 4, 1],
            2 : [5 , 6 , 1],
            3 : [0 , 10 , 0],
            4 : [8 , 6 , 2],
            5 : [5 , 5 , 5],
            6 : [15 , 0 , 0],
            7 : [0 , 0 , 10],
            8 : [8 , 8 , 3],
            9 : [20 , 0 , 7],
            10 : [10,10,10]
        }
        self.stages = list(self.initial_stages.values())

    def add_round(self):   # adds rounds to the game
        # fast_enemy_amount = 1
        # medium_enemy_amount = 0
        # tank_enemy_amount = 0
        # print("ajsiidsfs")
        # print(fast_enemy_amount)
        
        if self.game.round < 10:
            return

        if self.game.round >= 10 and self.game.round < 15:
            fast_enemy_amount = randint(8,15)
            medium_enemy_amount = randint(7,14)
            tank_enemy_amount = randint(3,7)
    
        if self.game.round >= 15:
            fast_enemy_amount = randint(12,20)
            medium_enemy_amount = randint(10,17)
            tank_enemy_amount = randint(5,10)
        
        self.stages.append([fast_enemy_amount,medium_enemy_amount,tank_enemy_amount])
        print(self.stages)


    def remove_round(self):    # removes the round from the game
        self.stages.remove(self.stages[0])

       
        
    
    
    
    
