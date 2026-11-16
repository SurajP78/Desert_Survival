import pygame



class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, tile_size):
        super().__init__()
        self.image = pygame.transform.scale(image , (tile_size , tile_size))
        self.rect = self.image.get_rect(topleft = (x, y)) 



class Map:
    def __init__(self,tile_group , collision_tiles):
        self.tile_size = 64
        self.tilemap = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]


        self.tile_list = []
        sand_img = pygame.image.load("Images/desert_images/PNG/land_0.png").convert_alpha()
        mud_wall_img = pygame.image.load("Images/desert_images/PNG/land_17.png").convert_alpha()

        # row_count = 0
        # for row in self.tilemap:
        #     col_count = 0
        #     for tile in row:
        #         if tile == 0:
        #             img = pygame.transform.scale_by(sand_img , 0.25)
        #             img_rect = img.get_rect()
        #             img_rect.x = col_count * self.tile_size
        #             img_rect.y = row_count * self.tile_size
        #             tile = (img , img_rect)
        #             self.tile_list.append(tile)
        #         if tile == 1:
        #             img = pygame.transform.scale_by(mud_wall_img , 0.25)
        #             img_rect = img.get_rect()
        #             img_rect.x = col_count * self.tile_size
        #             img_rect.y = row_count * self.tile_size
        #             tile = (img , img_rect)
        #             self.tile_list.append(tile)
        #         col_count += 1
        #     row_count += 1

        row_count = 0
        for row in self.tilemap:
            col_count = 0
            for tile in row:
                if tile == 0:
                    tile_sprite = Tile(sand_img , col_count * self.tile_size , row_count * self.tile_size , self.tile_size )
                    tile_group.add(tile_sprite)
                if tile == 1:
                    tile_sprite = Tile(mud_wall_img , col_count * self.tile_size , row_count * self.tile_size , self.tile_size )
                    tile_group.add(tile_sprite)
                    collision_tiles.add(tile_sprite)
                col_count += 1
            row_count += 1
    
    def draw(self,screen,groups):
        # for tile in self.tile_list:
        #     screen.blit(tile[0] , tile[1])
        #     pygame.draw.rect(screen ,(0,100,200), tile[1], 1)

        groups.draw(screen)