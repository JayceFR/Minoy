import pygame
import random
import math
import time as t
import Assets.Scripts.framework as engine
import Assets.Scripts.bg_particles as bg_particles
import Assets.Scripts.grass as g
import Assets.Scripts.sparks as spark
import Assets.Scripts.typewriter as typewriter
import Assets.Scripts.scientist as science
import Assets.Scripts.shader as shader
pygame.init()
from pygame.locals import *
screen_w = 800
screen_h = 500

window = pygame.display.set_mode((screen_w, screen_h), pygame.OPENGL | pygame.DOUBLEBUF)
screen = pygame.Surface((screen_w,screen_h))
display = pygame.Surface((screen_w//2, screen_h//2))
ui_display = pygame.Surface((screen_w//2, screen_h//2), pygame.SRCALPHA)
pygame.display.set_caption("Minoy")


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



def make_tile_rects(map, entities, non_touchables):
    y = 0
    tile_rects = []
    tree_locs = []
    btree_locs = []
    grass_locs = []
    bush_locs = []
    scientist_loc = []
    player_loc = []
    for row in map:
        x = 0
        for element in row:
            if element == "p":
                player_loc = [x*32, y*32]
            elif element == "b":
                bush_locs.append((x*32,y*32))
            elif element == "v":
                scientist_loc.append((x*32,y*32))
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
    return tile_rects, tree_locs, btree_locs, grass_locs, bush_locs, scientist_loc, player_loc

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
tick_img = pygame.image.load("./Assets/Entities/tick.png").convert_alpha()
tick_img.set_colorkey((0,0,0))
list_img = pygame.image.load("./Assets/Entities/list.png").convert_alpha()
list_img_logo = list_img.copy()
list_img_logo = pygame.transform.scale(list_img, (40, 40))
list_img_logo.set_colorkey((0,0,0))
list_img.set_colorkey((0,0,0))
element_sprite_sheet = pygame.image.load("./Assets/Entities/minerals.png").convert_alpha()
right_shot_img_copy = pygame.image.load("./Assets/Entities/right_shot.png").convert_alpha()
alloy_sprite_sheet = pygame.image.load("./Assets/Entities/fake_minerals.png").convert_alpha()
correct_alloys = pygame.image.load("./Assets/Entities/alloy_imgs.png").convert_alpha()
right_mine_sprite_sheet = pygame.image.load("./Assets/Sprites/right_mine.png").convert_alpha()
up_mine_sprite_sheet = pygame.image.load("./Assets/Sprites/up_mine.png").convert_alpha()
down_mine_sprite_sheet = pygame.image.load("./Assets/Sprites/down_mine.png").convert_alpha()
scientist_idle_sprite_sheet = pygame.image.load("./Assets/Sprites/scientist_idle.png").convert_alpha()
scientist_head = pygame.image.load("./Assets/Sprites/head.png").convert_alpha()
background_img = pygame.image.load("./Assets/Entities/background.png").convert_alpha()
background_img = pygame.transform.scale(background_img, (background_img.get_width()*2, background_img.get_height()*2))
background_img.set_colorkey((0,0,0))
scientist_head.set_colorkey((255,0,0))
game_over_screen = pygame.image.load("./Assets/Entities/end_screen.png").convert_alpha()
wasd_img = pygame.image.load("./Assets/Entities/wasd.png").convert_alpha()
wasd_img.set_colorkey((255,255,255))
showel_img = pygame.image.load("./Assets/entities/showel.png").convert_alpha()
showel_img.set_colorkey((0,0,0))
showel_display_img = showel_img.copy()
showel_display_img = pygame.transform.flip(showel_display_img, True, False)
showel_display_img.set_colorkey((0,0,0))
arrow_img = pygame.image.load("./Assets/Entities/arrow.png").convert_alpha()
arrow_img.set_colorkey((255,255,255))
down = pygame.image.load("./Assets/Entities/down.png").convert_alpha()
down = pygame.transform.scale(down, (down.get_width()*2, down.get_height()*2))
down.set_colorkey((0,0,0))
right_shot = []
sparks = []
for x in range(4):
    right_shot.append(get_image(right_shot_img_copy, x, 11, 23, 2, (0,0,0)))
element_imgs = []
element_logo_imgs = []
for x in range(6):
    element_imgs.append(get_image(element_sprite_sheet, x, 16, 16, 2, (0,0,0)))
    element_logo_imgs.append(get_image(element_sprite_sheet, x, 16, 16, 1, (0,0,0)))
alloy_imgs = []
for x in range(6):
    alloy_imgs.append(get_image(alloy_sprite_sheet, x, 16,16, 2, (0,0,0)))
correct_alloy_imgs = []
for x in range(3):
    correct_alloy_imgs.append(get_image(correct_alloys, x, 25,25, 4, (0,0,0)))
right_mine_animation = []
for x in range(4):
    right_mine_animation.append(get_image(right_mine_sprite_sheet, x, 65, 65, 2/3, (255,0,0)))
up_mine_animation = []
for x in range(4):
    up_mine_animation.append(get_image(up_mine_sprite_sheet, x, 62, 81, 2/3, (255,0,0)))
down_mine_animation = []
for x in range(4):
    down_mine_animation.append(get_image(down_mine_sprite_sheet, x, 64, 67, 2/3, (255,0,0)))
sceintist_idle_animation = []
for x in range(4):
    sceintist_idle_animation.append(get_image(scientist_idle_sprite_sheet, x, 32, 32, 2, (0,0,0)))
#Quantum
player_idle_animation = []
player_run_animation = []
for x in range(4):
    player_idle_animation.append(get_image(miner_idle_spritesheet, x, 47, 67, 2/3, (255,0,0)))
    player_run_animation.append(get_image(miner_run_spritesheet, x, 47, 67, 2/3, (255,0,0)))

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
f = open("./Assets/Maps/world.txt", "r")
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
#Sounds 
fusion_sound = pygame.mixer.Sound("./Assets/Music/fusion.wav")
jump_sound = pygame.mixer.Sound("./Assets/Music/jump.wav")
jump_sound.set_volume(0.1)
mining_sound = pygame.mixer.Sound("./Assets/Music/mining.wav")
mining_sound.set_volume(0.1)
#Fonts
inven_font = pygame.font.Font("./Assets/Fonts/jayce.ttf", 7)
element_font = pygame.font.Font("./Assets/Fonts/jayce.ttf", 17)
tile_rects, tree_locs, btree_locs, grass_loc, bush_locs, scientist_loc, player_loc = make_tile_rects(map, entities, non_touchable_entities)
#Player
player = engine.Player(player_loc[0],player_loc[1],miner_img.get_width(),miner_img.get_height(), miner_img, player_idle_animation, player_run_animation, right_shot, right_mine_animation, up_mine_animation, down_mine_animation, mining_sound, jump_sound)
#Fusion
fusion = [-1, -1]
fusion_dict = {}
fusion_rect = pygame.rect.Rect(345,205,40,40)
around_fusion_rect = pygame.rect.Rect(340, 200, 50, 50)
fusion_display_tile = alloy_imgs[0]
fusion_animation = False
fusion_animation_cooldown = 400
fusion_animation_last_update = 0
fusion_radius = 5
#Scientist
scientist = science.Scientist(scientist_loc[0][0], scientist_loc[0][1], sceintist_idle_animation[0].get_width(), sceintist_idle_animation[1].get_height(), sceintist_idle_animation)
grasses = []
current_overlay = -1
for loc in grass_loc:
    x_pos = loc[0]
    while x_pos < loc[0] + 32:
        x_pos += 2.5
        grasses.append(g.grass([x_pos, loc[1]+14], 2, 18))
click = False
typer = typewriter.TypeWriter(element_font, (255,255,255), 90, 10, 400, 9)
typer.write(['Hi! My name is minstein', 'I need alloys to save the world, miner', 'As you can only control the environment...', 'by mining the tiles that are free of vegetation', 'Please Help Me', 'Mine the indiviual elements...', 'And Fuse Them!', 'Here is my list of alloys' ])
done_typing = False
display_list = False
list_rect = pygame.rect.Rect(15, 200, 50, 50)
list_black_rect = pygame.rect.Rect(19, 203, 44, 44)
levels = [[{"c": 2, "s": 1}, "0", False], [{"l": 4, "c" : 2, "m" : 1}, "1", False], [{"s": 5, "a" : 1, "c": 1}, "2", False]]
made_alloy = [False, -1]
made_alloy_last_update = 0
made_alloy_cooldown = 1200
made_alloy_rect = pygame.rect.Rect(200, 40, 100, 100)
scientist_talk = False
colliding_with_scientist = False
sceintist_speech_done = False
#Shader stuff
shader_obj = shader.Shader(True, "./Assets/Shader/vertex.vert", "./Assets/Shader/fragment.frag")
noise_img = pygame.image.load("./Assets/Shader/pnoise.png").convert_alpha()
start_time = t.time()
game_ended = False
collected_mineral = False

down_cooldown = 5000
down_last_update = 0

list_down_update = 0

pygame.mixer.music.load("./Assets/Music/bg_song.wav")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

tutorial_cooldown = 5000
tutorial_last_update = 0

pygame.mouse.set_visible(False)


while run:
    clock.tick(60)
    time = pygame.time.get_ticks()
    display.fill((0,0,0))
    ui_display.fill((0,0,0,0))

    colliding_with_scientist = False

    if not collected_mineral:
        for x in inventory:
            for key, value in x.items():
                if value != 0:
                    collected_mineral = True
                    down_last_update = time

    current_overlay = -1
    mouse_pos = list(pygame.mouse.get_pos())
    mouse_pos[0] //= 2
    mouse_pos[1] //= 2

    true_scroll[0] += (player.get_rect().x - true_scroll[0] - 202) 
    true_scroll[1] += (player.get_rect().y - true_scroll[1] - 132) 
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    display.blit(background_img, (-100 - scroll[0], -100 - scroll[1]))

    draw_tiles(tile_rects, display, scroll)

    #Checking if game has ended
    game_ended = True
    for alloy in levels:
        if alloy[2] == False:
            game_ended = False

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
    
    #Scientist
    scientist.move(time, tile_rects, player.get_rect())
    scientist.draw(display, scroll)

    if not game_ended:
        if not scientist_talk:
            player.move(time, tile_rects, dig_down, dig_right, dig_left, dig_up, inventory, inven_items, scroll)
    player.draw(display, scroll)

    #Background Particles
    bg_particle_effect.recursive_call(time, display, scroll, 1)
    #Typing Effect
    if scientist_talk:
        if not done_typing:
            pygame.draw.rect(ui_display, (0,0,0), pygame.rect.Rect(0, 0, 400, 120))
            ui_display.blit(scientist_head, (0,0))
            done_typing = typer.update(time, ui_display)
        else:
            scientist_talk = False
            sceintist_speech_done = True
            list_down_update = time
    
    #Scientist talk settings
    if player.get_rect().colliderect(scientist.get_rect()):
        draw_text("E", element_font, (255,255,255), player.get_rect().x + 14 - scroll[0], player.get_rect().y - 40 - scroll[1], ui_display)
        colliding_with_scientist = True
    if not game_ended:
        #Blitting Items After Blitting The Player
        blit_grass(grasses, display, scroll, player)
        #Bush drawing
        for loc in bush_locs:
            display.blit(bush_img, (loc[0] - scroll[0] - 32, loc[1] - scroll[1]))

        #Inventory management
        left = 150
        pygame.draw.line(ui_display, (255,255,255), (left - 10, 250), (left, 220))
        pygame.draw.line(ui_display, (255,255,255), (left, 220), (272, 220))
        pygame.draw.line(ui_display, (255,255,255), (272,220), (282, 250))
        for x in range(len(inventory)):
            if pygame.rect.Rect(left, 225, 20, 20).collidepoint(mouse_pos[0], mouse_pos[1]):
                pygame.draw.rect(ui_display, (0,150,0), pygame.rect.Rect(left, 225, 20, 20), border_radius=5)    
            else:
                pygame.draw.rect(ui_display, (46,94,100), pygame.rect.Rect(left, 225, 20, 20), border_radius=5)
            pygame.draw.rect(ui_display, (0,0,0), pygame.rect.Rect(left + 2, 225 + 2.5, 20 - 2.5, 20 - 2.5), border_radius=4)
            if inventory[x][mapping[str(x)]] > 0:
                ui_display.blit(inven_items[mapping[str(x)]][1], (left + 2.2 , 225 + 2.2))
                draw_text(str(inventory[x][mapping[str(x)]]), inven_font, (255,255,255), left + 9, 242, ui_display)
                if pygame.rect.Rect(left, 225, 20, 20).collidepoint(mouse_pos[0], mouse_pos[1]):
                    current_overlay = x
                    draw_text(inven_items[mapping[str(x)]][2], element_font, (255,255,255), left - 15, 210, ui_display)
            left += 25

        #Drawing fusion rect
        if around_fusion_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            pygame.draw.rect(ui_display, (0,150,0), around_fusion_rect, border_radius=9)
        else:
            pygame.draw.rect(ui_display, (255,201,14), around_fusion_rect, border_radius=9)
        pygame.draw.rect(ui_display, (0,0,0), fusion_rect, border_radius=7)
        if len(fusion_dict) == 1:
            for key in fusion_dict.keys():
                ui_display.blit(entities[key], (fusion_rect.x + 4, fusion_rect.y + 5))
        elif len(fusion_dict) > 1:
            ui_display.blit(fusion_display_tile, (fusion_rect.x + 4, fusion_rect.y + 5))

        if click:
            ui_display.blit(inven_items[mapping[str(fusion[0])]][1], mouse_pos)
        
        for s in sparks:
            s.move(1)
            s.draw(display)
        
        if fusion_animation:
            if time - fusion_animation_last_update > fusion_animation_cooldown//2:
                fusion_rect.x -= 7
                fusion_rect.y += 5
            else:
                fusion_rect.x += 2.5
                fusion_rect.y -= 5
            if time - fusion_animation_last_update > fusion_animation_cooldown:
                fusion_animation = False
                fusion_rect.width = 40
                fusion_rect.height = 40
                fusion_rect.x = 345
                fusion_rect.y = 205
            pygame.draw.circle(ui_display, (255,255,255), (370, 230), fusion_radius, 9)
            fusion_radius += 20
        
        #Cycling the map
        if player.rect.y > 1000:
            player.rect.y = -50

        if sceintist_speech_done:
            if list_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                current_overlay = 5
                pygame.draw.rect(ui_display, (0,150,0), list_rect, border_radius=9)
            else:
                pygame.draw.rect(ui_display, (255,201,14), list_rect, border_radius=9)
            pygame.draw.rect(ui_display, (0,0,0), list_black_rect, border_radius=4)
            ui_display.blit(list_img_logo, (20, 205))
            if time - list_down_update < down_cooldown:
                draw_text("Click Me!", element_font, (255,255,255), 10, 150, ui_display)
                ui_display.blit(down, (25, 170 + math.sin(time) * 2))

    #Displaying list
    if not game_ended:
        if display_list:
            ui_display.blit(list_img, (100, 50))
            y = 0
            for pos, alloy in enumerate(levels):
                y += 40
                if alloy[2] == True:
                    ui_display.blit(tick_img, (120, 50 + y))
    
        #Checking if required alloy is fused
        for pos, alloy in enumerate(levels):
            equal = True
            if alloy[2] == False:
                if len(alloy[0]) == len(fusion_dict):
                    for key, value in alloy[0].items():
                        if fusion_dict.get(key) != value:
                            equal = False
                    if equal:
                        fusion_dict = {}
                        alloy[2] = True
                        made_alloy[0] = True
                        made_alloy[1] = pos
                        made_alloy_last_update = time
        
        if made_alloy[0] == True:
            flip = correct_alloy_imgs[made_alloy[1]].copy()
            flip = pygame.transform.scale(flip, (made_alloy_rect.width, made_alloy_rect.height))
            ui_display.blit(flip, made_alloy_rect)
            if time - made_alloy_last_update > made_alloy_cooldown:
                made_alloy[0] = False
                made_alloy[1] = -1
                made_alloy_rect = pygame.rect.Rect(200, 40, 100, 100)
            made_alloy_rect.x -= 5
            made_alloy_rect.y += 5
            if made_alloy_rect.width > 5 and made_alloy_rect.height > 5:
                made_alloy_rect.width -= 2.5
                made_alloy_rect.height -= 2.5
    
    if game_ended:
        display.blit(game_over_screen, (0,0))
    
    if collected_mineral:
        if time - down_last_update < down_cooldown:
            draw_text("Drag To Fuse", element_font, (255,255,255), 300, 150, ui_display)
            ui_display.blit(down, (350, 170 + math.sin(time) * 2))

    if time - tutorial_last_update < tutorial_cooldown:
        ui_display.blit(wasd_img, (player.get_rect().x - scroll[0] - 20 , player.get_rect().y - scroll[1] - 30))
        ui_display.blit(arrow_img, (player.get_rect().x - scroll[0] + 15, player.get_rect().y - scroll[1] - 30 ))
        ui_display.blit(showel_display_img, (player.get_rect().x - scroll[0] + 35, player.get_rect().y - scroll[1] - 30 ) )
    ui_display.blit(showel_img, (mouse_pos[0], mouse_pos[1]))

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
            if event.key == pygame.K_i:
                if display_list:
                    display_list = False
                else:
                    display_list = True
            if event.key == pygame.K_e:
                if colliding_with_scientist:
                    scientist_talk = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not click:
                    if display_list:
                        display_list = False
                    if current_overlay >= 0 and current_overlay <= 4:
                        fusion[0] = current_overlay
                        click = True
                    if current_overlay == 5:
                        if not display_list:
                            display_list = True
                
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
                        fusion_display_tile = alloy_imgs[random.randint(0, len(alloy_imgs)-1)]
                        for x in range(50):
                            sparks.append(spark.Spark([fusion_rect.x + 15 ,fusion_rect.y + 15], math.radians(random.randint(0,360)), random.randint(2,5), (random.randint(0,255),random.randint(0,255),random.randint(0,255)), 2, 1))
                        fusion_animation = True
                        fusion_sound.play()
                        fusion_animation_last_update = time
                        fusion_radius = 0
                    
                    click = False             
    surf = pygame.transform.scale(display, (screen_w, screen_h))
    screen.blit(surf, (0,0))
    #"time" : t.time() - start_time,
    shader_obj.draw({"tex" : screen, "noise_tex1": noise_img, "ui_tex" : ui_display}, { "itime": int((t.time() - start_time) * 100) })
    pygame.display.flip()