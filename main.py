#TODO -> ADD Fusion
#TODO -> Attack animations
#TODO -> Shaders

import pygame
import Assets.Scripts.framework as engine
import Assets.Scripts.bg_particles as bg_particles
import Assets.Scripts.grass as g
pygame.init()
screen_w = 800
screen_h = 500

screen = pygame.display.set_mode((screen_w,screen_h))
pygame.display.set_caption("Minoy")
display = pygame.Surface((screen_w//2, screen_h//2))

#Getting image from spirtesheet
def get_image(sheet, frame, width, height, scale, colorkey):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(colorkey)
    return image

def blit_grass(grasses, display, scroll, player):
    for grass in grasses:
        if grass.get_rect().colliderect(player.get_rect()):
            grass.colliding()
        grass.draw(display, scroll)

def draw_text(text, font, text_col, x, y, display):
    img = font.render(text, True, text_col)
    display.blit(img, (x, y))

def palette_swap(surf, old_c, new_c):
    img_copy = pygame.Surface(surf.get_size())
    img_copy.fill(new_c)
    surf.set_colorkey(old_c)
    img_copy.blit(surf, (0,0))
    return img_copy


def make_tile_rects(map, entities, non_touchables):
    y = 0
    tile_rects = []
    tree_locs = []
    btree_locs = []
    grass_locs = []
    bush_locs = []
    for row in map:
        x = 0
        for element in row:
            if element == "b":
                bush_locs.append((x*32,y*32))
            elif element == "g":
                grass_locs.append((x*32,y*32))
            elif element == "x":
                tile_rects.append(engine.Tiles(x*32, y*32, 32, 32, entities["2"], True, False))
            elif element == "t":
                tree_locs.append((x*32,y*32))
            elif element == "y":
                btree_locs.append((x*32, y*32))
            elif element == "c":
                tile_rects.append(engine.Tiles(x*32, y*32, 32, 32, entities[element], True, special_id="c"))
            elif element == "s":
                tile_rects.append(engine.Tiles(x*32, y*32, 32, 32, entities[element], True, special_id="s"))
            elif element == "l":
                tile_rects.append(engine.Tiles(x*32, y*32, 32, 32, entities[element], True, special_id="l"))
            elif element == "m":
                tile_rects.append(engine.Tiles(x*32, y*32, 32, 32, entities[element], True, special_id="m"))
            elif element == "a":
                tile_rects.append(engine.Tiles(x*32, y*32, 32, 32, entities[element], True, special_id="a"))
            elif element != "0":
                if element not in non_touchables:
                    tile_rects.append(engine.Tiles(x*32, y*32, 32, 32, entities[element], True))
                else:
                    tile_rects.append(engine.Tiles(x*32, y*32, 32, 32, entities[element], False))                  
                #display.blit(entities[element], (x*16 - scroll[0], y * 16 - scroll[1]))
            x += 1
        y += 1
    return tile_rects, tree_locs, btree_locs, grass_locs, bush_locs

def draw_tiles(tile_rects, display, scroll):
    for tile in tile_rects:
        tile.draw(display, scroll)

true_scroll = [0,0]
bg_particle_effect = bg_particles.Master()
start = True

#Loading images
tiles = []
for x in range(9):
    current_tile = pygame.image.load("./Assets/Tiles/tile{tile_pos}.png".format(tile_pos = str(x+1))).convert_alpha()
    tile_dup = current_tile.copy()
    tile_dup = pygame.transform.scale(tile_dup, (32,32))
    tiles.append(tile_dup)
btiles = []
for x in range(9):
    current_tile = pygame.image.load("./Assets/Tiles/btile{tile_pos}.png".format(tile_pos = str(x+1))).convert_alpha()
    tile_dup = current_tile.copy()
    tile_dup = pygame.transform.scale(tile_dup, (32,32))
    btiles.append(tile_dup)
miner_img_copy = pygame.image.load("./Assets/Sprites/miner_img.png").convert_alpha()
miner_img = miner_img_copy.copy()
miner_img = pygame.transform.scale(miner_img, (miner_img_copy.get_width()//1.5, miner_img_copy.get_height()//1.5))
miner_img.set_colorkey((255,0,0))
miner_idle_spritesheet = pygame.image.load("./Assets/Sprites/miner_idle.png").convert_alpha()
miner_run_spritesheet = pygame.image.load("./Assets/Sprites/miner_run.png").convert_alpha()
tree_img_copy = pygame.image.load("./Assets/Sprites/tree.png").convert_alpha()
tree_img = tree_img_copy.copy()
tree_img = pygame.transform.scale(tree_img_copy, (tree_img_copy.get_width()*3, tree_img_copy.get_height()*2.5))
tree_img.set_colorkey((0,0,0))
btree_img_copy = pygame.image.load("./Assets/Sprites/btree.png").convert_alpha()
btree_img = btree_img_copy.copy()
btree_img = pygame.transform.scale(btree_img_copy, (btree_img_copy.get_width()*3, btree_img_copy.get_height()*3))
btree_img.set_colorkey((0,0,0))
bush_img_copy = pygame.image.load("./Assets/Sprites/bush.png").convert_alpha()
bush_img = bush_img_copy.copy()
bush_img = pygame.transform.scale(bush_img_copy, (bush_img_copy.get_width()*2, bush_img_copy.get_height()*2))
bush_img.set_colorkey((0,0,0))
element_sprite_sheet = pygame.image.load("./Assets/Entities/minerals.png").convert_alpha()
right_shot_img_copy = pygame.image.load("./Assets/Entities/right_shot.png").convert_alpha()
right_shot = []
for x in range(4):
    right_shot.append(get_image(right_shot_img_copy, x, 11, 23, 2, (0,0,0)))
element_imgs = []
element_logo_imgs = []
for x in range(6):
    element_imgs.append(get_image(element_sprite_sheet, x, 16, 16, 2, (0,0,0)))
    element_logo_imgs.append(get_image(element_sprite_sheet, x, 16, 16, 1, (0,0,0)))
#Quantum
player_idle_animation = []
player_run_animation = []
for x in range(4):
    player_idle_animation.append(get_image(miner_idle_spritesheet, x, 47, 67, 2/3, (255,0,0)))
    player_run_animation.append(get_image(miner_run_spritesheet, x, 47, 67, 2/3, (255,0,0)))
player = engine.Player(50,50,miner_img.get_width(),miner_img.get_height(), miner_img, player_idle_animation, player_run_animation, right_shot)
#Grass
grasses = []
grass_loc = []
grass_spawn = True
grass_last_update = 0
grass_cooldown = 50
#Game Variables
run = True
clock = pygame.time.Clock()

#Reading the map
map = []
f = open("./Assets/Maps/map.txt", "r")
data = f.read()
f.close()
data = data.split("\n")
for row in data:
    map.append(list(row))

#Entities list
entities = {"1" : tiles[0], "2" : tiles[1], "3" : tiles[2], "4" : tiles[3], "5" : tiles[4], "6" : tiles[5], "7" : tiles[6], "8" : tiles[7], "9" : tiles[8], "!" : btiles[0], "¬" : btiles[1], ")" : btiles[2], "$" : btiles[3], "%" : btiles[4] , "^" : btiles[5], "&" : btiles[6], "*" : btiles[7], "(" : btiles[8], "c" : element_imgs[1], "s" : element_imgs[2], "l" : element_imgs[3], "m" : element_imgs[4], "a" : element_imgs[5]}
non_touchable_entities = ["!", "¬", ")", "$", "%", "^", "&", "*", "("]
#Digging
dig_cooldown = 200
dig_last_update = 0
dig_down = False
dig_right = False
dig_left = False
dig_up = False
#Inventory
inventory = [{"c":0}, {"s":0}, {"l":0}, {"m":0}, {"a":0}] #Example -> {"c" : 1} Element : Count
inven_slot = -1
inven_items = {"c":[0, element_logo_imgs[1], "Copper"], "s": [1, element_logo_imgs[2], "Tin (SN) "], "l": [2, element_logo_imgs[3], "Aluminium"], "m": [3, element_logo_imgs[4], "Manganese"], "a":[4, element_logo_imgs[5], "Antimony"]}
mapping = {"0": "c", "1": "s", "2": "l", "3": "m", "4": "a"}
#Fonts
inven_font = pygame.font.Font("./Assets/Fonts/jayce.ttf", 7)
element_font = pygame.font.Font("./Assets/Fonts/jayce.ttf", 17)
tile_rects, tree_locs, btree_locs, grass_loc, bush_locs = make_tile_rects(map, entities, non_touchable_entities)
#Fusion
fusion = [-1, -1]
fusion_dict = {}
fusion_rect = pygame.rect.Rect(350,210,32,32)
grasses = []
for loc in grass_loc:
    x_pos = loc[0]
    while x_pos < loc[0] + 32:
        x_pos += 2.5
        grasses.append(g.grass([x_pos, loc[1]+14], 2, 18))
click = False

while run:
    clock.tick(60)
    time = pygame.time.get_ticks()
    display.fill((0,0,0))

    mouse_pos = list(pygame.mouse.get_pos())
    mouse_pos[0] //= 2
    mouse_pos[1] //= 2

    true_scroll[0] += (player.get_rect().x - true_scroll[0] - 202) / 5
    true_scroll[1] += (player.get_rect().y - true_scroll[1] - 132) / 5
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    draw_tiles(tile_rects, display, scroll)

    #Grass movement
    if time - grass_last_update > grass_cooldown:
        for grass in grasses:
            grass.move()
        grass_last_update = time

    #Tree drawing
    for loc in tree_locs:
        display.blit(tree_img, (loc[0] - scroll[0] - 79, loc[1] - scroll[1] - 145))
    for loc in btree_locs:
        display.blit(btree_img, (loc[0] - scroll[0] - 79, loc[1] - scroll[1] - 149))
    
    player.move(time, tile_rects, dig_down, dig_right, dig_left, dig_up, inventory, inven_items)
    player.draw(display, scroll)

    #Background Particles
    bg_particle_effect.recursive_call(time, display, scroll, 1)

    #Blitting Items After Blitting The Player
    blit_grass(grasses, display, scroll, player)
    #Bush drawing
    for loc in bush_locs:
        display.blit(bush_img, (loc[0] - scroll[0] - 32, loc[1] - scroll[1]))

    #Inventory management
    left = 150
    pygame.draw.line(display, (255,255,255), (left - 10, 250), (left, 220))
    pygame.draw.line(display, (255,255,255), (left, 220), (272, 220))
    pygame.draw.line(display, (255,255,255), (272,220), (282, 250))
    for x in range(len(inventory)):
        if pygame.rect.Rect(left, 225, 20, 20).collidepoint(mouse_pos[0], mouse_pos[1]):
            pygame.draw.rect(display, (0,150,0), pygame.rect.Rect(left, 225, 20, 20), border_radius=5)    
        else:
            pygame.draw.rect(display, (46,94,100), pygame.rect.Rect(left, 225, 20, 20), border_radius=5)
        pygame.draw.rect(display, (0,0,0), pygame.rect.Rect(left + 2, 225 + 2.5, 20 - 2.5, 20 - 2.5), border_radius=4)
        if inventory[x][mapping[str(x)]] > 0:
            display.blit(inven_items[mapping[str(x)]][1], (left + 2.2 , 225 + 2.2))
            draw_text(str(inventory[x][mapping[str(x)]]), inven_font, (255,255,255), left + 9, 242, display)
            if pygame.rect.Rect(left, 225, 20, 20).collidepoint(mouse_pos[0], mouse_pos[1]):
                current_overlay = x
                draw_text(inven_items[mapping[str(x)]][2], element_font, (255,255,255), left - 15, 210, display)
        left += 25

    #Drawing fusion rect
    pygame.draw.rect(display, (0,0,0), fusion_rect, border_radius=7)
    if len(fusion_dict) == 1:
        for key in fusion_dict.keys():
            display.blit(entities[key], (fusion_rect.x, fusion_rect.y))
    elif len(fusion_dict) > 1:
        pass

    if click:
        display.blit(inven_items[mapping[str(fusion[0])]][1], mouse_pos)

    dig_down = False
    dig_right = False
    dig_left = False
    dig_up = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                if time - dig_last_update > dig_cooldown:
                    dig_down = True
                    dig_last_update = time
            if event.key == pygame.K_LEFT:
                if time - dig_last_update > dig_cooldown:
                    dig_left = True
                    dig_last_update = time
            if event.key == pygame.K_RIGHT:
                if time - dig_last_update > dig_cooldown:
                    dig_right = True
                    dig_last_update = time
            if event.key == pygame.K_UP:
                if time - dig_last_update > dig_cooldown:
                    dig_up = True
                    dig_last_update = time
            if event.key == pygame.K_SPACE:
                print(inventory, fusion_dict)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not click:
                    if current_overlay >= 0 and current_overlay <= 4:
                        fusion[0] = current_overlay
                        click = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if click:
                    if fusion_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                        #perfrom the swap 
                        if mapping[str(fusion[0])] in fusion_dict:
                            fusion_dict[mapping[str(fusion[0])]] += 1
                        else:
                            fusion_dict.update({mapping[str(fusion[0])]:1})
                        inventory[fusion[0]][mapping[str(fusion[0])]] -= 1
                    click = False             
    surf = pygame.transform.scale(display, (screen_w, screen_h))
    screen.blit(surf, (0,0))
    pygame.display.flip()