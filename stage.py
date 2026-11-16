from random import randint
from collections import deque

class Stage():
    def __init__(self):
        self.stage = {
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
        
      
    

    def add_round(self):   # adds rounds to the game

        # length = len(self.stage)
        # self.stage[length ] =[1,0,0]

        fast_enemy_amount = randint(8,20)
        medium_enemy_amount = randint(7,15)
        tank_enemy_amount = randint(3,10)
        length = len(self.stage)
        self.stage[length ] = [fast_enemy_amount,medium_enemy_amount,tank_enemy_amount]
        
    
    
    
    
