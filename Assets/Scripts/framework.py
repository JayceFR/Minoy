import pygame

class Player():
    def __init__(self, x ,y, width, height, img, idle_animation, run_animation, right_shot, right_mine_animation, up_mine_animation) -> None:
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.movement = [0,0]
        self.display_x = 0
        self.display_y = 0
        self.moving_left = False
        self.moving_right = False
        self.collision_type = {}
        self.speed = 4
        self.idle_animation = idle_animation
        self.run_animation = run_animation
        self.frame = 0
        self.frame_last_update = 0
        self.frame_cooldown = 200
        self.facing_right = True
        self.facing_left = False
        self.img = img
        self.show_cooldown = 600
        self.show_last_update = 0
        self.show_right = False
        self.show_left = False
        self.show_up = False
        self.right_shot = right_shot
        self.jump = False
        self.jump_last_update = 0
        self.jump_cooldown = 600
        self.jump_up_spped = 9
        self.air_timer = 0
        self.right_mine_animation = right_mine_animation
        self.up_mine_animation = up_mine_animation

    def draw(self, display, scroll):
        self.display_x = self.rect.x
        self.display_y = self.rect.y
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
        #pygame.draw.rect(display, (255,0,0), self.rect)
        if self.show_right:
            display.blit(self.right_mine_animation[self.frame], self.rect)
        elif self.show_left:
            flip = self.right_mine_animation[self.frame].copy()
            flip = pygame.transform.flip(flip, True, False)
            display.blit(flip, self.rect)
        elif self.show_up:
            display.blit(self.up_mine_animation[self.frame], (self.rect.x, self.rect.y - 12))
        else:
            if self.moving_right:
                display.blit(self.run_animation[self.frame], self.rect)
            elif self.moving_left:
                flip = self.run_animation[self.frame].copy()
                flip = pygame.transform.flip(flip, True, False)
                display.blit(flip, self.rect)
            else:
                if self.facing_right:
                    display.blit(self.idle_animation[self.frame], self.rect)
                else:
                    flip = self.idle_animation[self.frame].copy()
                    flip = pygame.transform.flip(flip, True, False)
                    display.blit(flip, self.rect)
        
        self.rect.x = self.display_x
        self.rect.y = self.display_y
    
    def move(self, time,  tiles, dig_down, dig_right, dig_left, dig_up, inventory, inven_items):
        self.movement = [0, 0]

        if self.moving_right:
            self.facing_right = True
            self.facing_left = False
            self.movement[0] += self.speed
            self.moving_right = False
        if self.moving_left:
            self.facing_left = True
            self.facing_right = False
            self.movement[0] -= self.speed
            self.moving_left = False
        if self.jump:
            if self.air_timer < 40:
                self.air_timer += 1
                self.movement[1] -= self.jump_up_spped
                self.jump_up_spped -= 0.5
            else:
                self.air_timer = 0
                self.jump = False
                self.jump_up_spped = 9
        

        if self.show_right:
            if time - self.show_last_update > self.show_cooldown:
                self.show_last_update = time
                self.show_right = False
        elif self.show_left:
            if time - self.show_last_update > self.show_cooldown:
                self.show_last_update = time
                self.show_left = False
        elif self.show_up:
            if time - self.show_last_update > self.show_cooldown:
                self.show_last_update = time
                self.show_up = False
        
        if not self.jump:
            self.movement[1] += 10

        self.collision_type = self.collision_checker(tiles)

        if dig_down:
            for tile in self.collision_type["bottom"][1]:
                if tile.breakable:
                    tile.health -= 20
                if tile.health <= 0:
                    if tile.special_id != "n":
                        self.add_to_inventory(inventory, inven_items, tile.special_id)
                    tiles.remove(tile)
        if dig_right:
            self.show_right = True
            self.show_last_update = time
            for tile in self.collision_type["right"][1]:
                if tile.breakable:
                    tile.health -= 20
                if tile.health <= 0:
                    if tile.special_id != "n":
                        self.add_to_inventory(inventory, inven_items, tile.special_id)
                    tiles.remove(tile)
        if dig_left:
            self.show_left = True
            self.show_last_update = time
            for tile in self.collision_type["left"][1]:
                if tile.breakable:
                    tile.health -= 20
                if tile.health <= 0:
                    if tile.special_id != "n":
                        self.add_to_inventory(inventory, inven_items, tile.special_id)
                    tiles.remove(tile)
        if dig_up:
            self.show_up = True
            self.show_last_update = time
            for tile in self.collision_type["top"][1]:
                if tile.breakable:
                    tile.health -= 20
                if tile.health <= 0:
                    if tile.special_id != "n":
                        self.add_to_inventory(inventory, inven_items, tile.special_id)
                    tiles.remove(tile)

        key = pygame.key.get_pressed()
        if  key[pygame.K_a]:
            self.moving_left = True
        if key[pygame.K_d]:
            self.moving_right = True
        if key[pygame.K_SPACE] or key[pygame.K_w]:
            if not self.jump and self.collision_type['bottom'][0]:
                if time - self.jump_last_update > self.jump_cooldown:
                    #self.music.play()
                    self.jump = True
                    self.jump_last_update = time
        
        if time - self.frame_last_update > self.frame_cooldown:
            self.frame += 1
            if self.frame >= 4:
                self.frame = 0
            self.frame_last_update = time
    
    def collision_test(self, tiles):
        hitlist = []
        for tile in tiles:
            if tile.touchable:
                if self.rect.colliderect(tile.get_rect()):
                    hitlist.append(tile)
        return hitlist
    
    def add_to_inventory(self, inventory, inven_items, id):
        inventory[inven_items[id][0]][id] += 1
            
    
    def collision_checker(self, tiles):
        collision_types = {"top": [False, []], "bottom": [False, []], "right": [False, []], "left": [False, []]}
        self.rect.x += self.movement[0]
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if self.movement[0] > 0:
                self.rect.right = tile.get_rect().left
                collision_types["right"][0] = True
                collision_types["right"][1].append(tile)
            elif self.movement[0] < 0:
                self.rect.left = tile.get_rect().right
                collision_types["left"][0] = True
                collision_types["left"][1].append(tile)
        self.rect.y += self.movement[1]
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if self.movement[1] > 0:
                self.rect.bottom = tile.get_rect().top
                collision_types["bottom"][0] = True
                collision_types["bottom"][1].append(tile)
            if self.movement[1] < 0:
                self.rect.top = tile.get_rect().bottom
                collision_types["top"][0] = True
                collision_types['top'][1].append(tile)
        return collision_types

    def get_rect(self):
        return self.rect

class Tiles():
    def __init__(self, x, y, width, height, img, touchable, breakable = True, special_id = "n") -> None:
        self.img = img
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.touchable = touchable
        self.health = 60
        self.breakable = breakable
        self.special_id = special_id
    
    def draw(self, display, scroll):
        display.blit(self.img, (self.rect.x - scroll[0], self.rect.y - scroll[1]) )
    
    def get_rect(self):
        return self.rect