import pygame
class Scientist():
    def __init__(self, x, y, width, height, idle_animation) -> None:
        self.x = x 
        self.y = y
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.idle_animation = idle_animation
        self.frame = 0
        self.frame_update_cooldown = 200
        self.frame_last_update = 0
        self.collison_type = {}
        self.movement = [0,0]
        self.display_x = 0
        self.display_y = 0
        self.facing_right = True
    
    def draw(self, display, scroll):
        self.display_x = self.rect.x
        self.display_y = self.rect.y
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
        if self.facing_right:
            display.blit(self.idle_animation[self.frame], self.rect)
        else:
            flip = self.idle_animation[self.frame].copy()
            flip = pygame.transform.flip(flip, True, False)
            display.blit(flip, self.rect)
        self.rect.x = self.display_x
        self.rect.y = self.display_y

    def move(self, time, tiles, player_rect):
        self.movement = [0,0]
        self.movement[1] += 10
        if self.rect.x > player_rect.x:
            self.facing_right = False
        else:
            self.facing_right = True
        if time - self.frame_last_update > self.frame_update_cooldown:
            self.frame += 1
            if self.frame >= 4:
                self.frame = 0
            self.frame_last_update = time
        self.collison_type = self.collision_checker(tiles)
    
    def collision_test(self, tiles):
        hitlist = []
        for tile in tiles:
            if tile.touchable:
                if self.rect.colliderect(tile.get_rect()):
                    hitlist.append(tile)
        return hitlist
    
    def collision_checker(self, tiles):
        collision_types = {"top": False, "bottom": False, "right": False, "left": False}
        self.rect.x += self.movement[0]
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if self.movement[0] > 0:
                self.rect.right = tile.get_rect().left
                collision_types["right"] = True
            elif self.movement[0] < 0:
                self.rect.left = tile.get_rect().right
                collision_types["left"] = True
        self.rect.y += self.movement[1]
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if self.movement[1] > 0:
                self.rect.bottom = tile.get_rect().top
                collision_types["bottom"] = True
            if self.movement[1] < 0:
                self.rect.top = tile.get_rect().bottom
                collision_types["top"] = True
        return collision_types

    def get_rect(self):
        return self.rect
