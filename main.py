import pygame
import Assets.Scripts.framework as engine
import Assets.Scripts.bg_particles as bg_particles

screen_w = 1000
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

def make_tile_rects(map, entities, non_touchables):
    y = 0
    tile_rects = []
    for row in map:
        x = 0
        for element in row:
            if element != "0":
                if element not in non_touchables:
                    tile_rects.append(engine.Tiles(x*24, y*24, 24, 24, entities[element], True))
                else:
                    tile_rects.append(engine.Tiles(x*24, y*24, 24, 24, entities[element], False))                  
                #display.blit(entities[element], (x*16 - scroll[0], y * 16 - scroll[1]))
            x += 1
        y += 1
    return tile_rects

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
    tile_dup = pygame.transform.scale(tile_dup, (24,24))
    tiles.append(tile_dup)
btiles = []
for x in range(9):
    current_tile = pygame.image.load("./Assets/Tiles/btile{tile_pos}.png".format(tile_pos = str(x+1))).convert_alpha()
    tile_dup = current_tile.copy()
    tile_dup = pygame.transform.scale(tile_dup, (24,24))
    btiles.append(tile_dup)
miner_img_copy = pygame.image.load("./Assets/Sprites/miner_img.png").convert_alpha()
miner_img = miner_img_copy.copy()
miner_img = pygame.transform.scale(miner_img, (miner_img_copy.get_width()//1.5, miner_img_copy.get_height()//1.5))
miner_img.set_colorkey((255,0,0))
miner_idle_spritesheet = pygame.image.load("./Assets/Sprites/miner_idle.png").convert_alpha()
miner_run_spritesheet = pygame.image.load("./Assets/Sprites/miner_run.png").convert_alpha()
#Quantum
player_idle_animation = []
player_run_animation = []
for x in range(4):
    player_idle_animation.append(get_image(miner_idle_spritesheet, x, 47, 67, 2/3, (255,0,0)))
    player_run_animation.append(get_image(miner_run_spritesheet, x, 47, 67, 2/3, (255,0,0)))
player = engine.Player(50,50,miner_img.get_width(),miner_img.get_height(), miner_img, player_idle_animation, player_run_animation)

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
entities = {"1" : tiles[0], "2" : tiles[1], "3" : tiles[2], "4" : tiles[3], "5" : tiles[4], "6" : tiles[5], "7" : tiles[6], "8" : tiles[7], "9" : tiles[8], "!" : btiles[0], "¬" : btiles[1], ")" : btiles[2], "$" : btiles[3], "%" : btiles[4] , "^" : btiles[5], "&" : btiles[6], "*" : btiles[7], "(" : btiles[8]}
non_touchable_entities = ["!", "¬", ")", "$", "%", "^", "&", "*", "("]
#Digging
dig_cooldown = 200
dig_last_update = 0
dig_down = False
dig_right = False
dig_left = False
dig_up = False

tile_rects = make_tile_rects(map, entities, non_touchable_entities)

while run:
    clock.tick(60)
    time = pygame.time.get_ticks()
    display.fill((0,0,0))

    true_scroll[0] += (player.get_rect().x - true_scroll[0] - 242) / 5
    true_scroll[1] += (player.get_rect().y - true_scroll[1] - 172) / 5
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    draw_tiles(tile_rects, display, scroll)

    player.move(time, tile_rects, dig_down, dig_right, dig_left, dig_up)
    player.draw(display, scroll)

    #Background Particles
    bg_particle_effect.recursive_call(time, display, scroll, 1)

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
    surf = pygame.transform.scale(display, (screen_w, screen_h))
    screen.blit(surf, (0,0))
    pygame.display.flip()