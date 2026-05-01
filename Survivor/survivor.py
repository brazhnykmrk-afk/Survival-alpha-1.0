import pygame
import sys
import random

pygame.init()

#Music
pygame.mixer.music.load('sound/musik.ogg')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

#Wood sound
wood_sound = pygame.mixer.Sound('sound/wood.ogg')

#Step on Grass sound
step_sound = pygame.mixer.Sound('sound/walking.ogg')
step_sound.set_volume(0.1)

# Score
score = 0
score2 = 0

# Colors
white = (255, 255, 255)
yellow = (255, 255, 0)
red = (255, 0, 0)

# Base
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Survivor")
clock = pygame.time.Clock()

# Place
player_x = 0
player_y = 380
player_speed = 7

# Inventory
logs = 0
stone_block = 0
grass = 0

# Img
background = pygame.image.load("img/bg.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

tree_img = pygame.image.load("img/tree.png")
tree_img = pygame.transform.scale(tree_img, (450, 450))

stone_img = pygame.image.load("img/stone.jpg")
stone_img = pygame.transform.scale(stone_img, (60, 60))

log_img = pygame.image.load("img/log.jpg")
log_img = pygame.transform.scale(log_img, (60, 60))

grass_img = pygame.image.load("img/grass.jpg")
grass_img = pygame.transform.scale(grass_img, (60, 60))

rock_img = pygame.image.load("img/rock.png")
rock_img = pygame.transform.scale(rock_img, (260, 260))


stones = []
stones.append({"x": 700, "y": 340, "hits": 8})
# Trees with a 'hits' property set to 5
trees = []
trees.append({"x": 0, "y": 88, "hits": 5})
trees.append({"x": 450, "y": 88, "hits": 5})

# Animation Setup
PLAYER_SIZE = (100, 140)

walk_right = [
    pygame.transform.scale(pygame.image.load("anim/pos1.png").convert_alpha(), PLAYER_SIZE),
    pygame.transform.scale(pygame.image.load("anim/pos2.png").convert_alpha(), PLAYER_SIZE),
    pygame.transform.scale(pygame.image.load("anim/pos3.png").convert_alpha(), PLAYER_SIZE),
    pygame.transform.scale(pygame.image.load("anim/pos4.png").convert_alpha(), PLAYER_SIZE)
]

hand_img = pygame.transform.scale(pygame.image.load("anim/hand_anim.png").convert_alpha(), PLAYER_SIZE)

direction = "right"
frame = 0
frame_count = 0
animation_speed = 10
image = walk_right[0]

# To prevent one key press counting as 60 hits per second,
# we track if the key was already down
f_key_pressed = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(background, (0, 0))

    keys = pygame.key.get_pressed()
    moving = False
    hitting = False



    # Random trees + stones placement
    if player_x > 1080:
        player_x = 0

        min_distance = 120  # расстояние между деревьями

        random_x = random.randint(0, WIDTH - 100)

        random_x2 = random.randint(0, WIDTH - 100)
        while abs(random_x - random_x2) < min_distance:
            random_x2 = random.randint(0, WIDTH - 100)

        # TREESd
        trees.append({"x": random_x, "y": 88, "hits": 5})
        trees.append({"x": random_x2, "y": 88, "hits": 5})

        # STONES (гармонично рядом, но не на том же месте)
        stone_offset = random.randint(-80, 80)

        stones.append({
            "x": max(0, random_x + stone_offset),
            "y": 340,
            "hits": 8
        })

        stones.append({
            "x": max(0, random_x2 - stone_offset),
            "y": 340,
            "hits": 8
        })

        # лимит объектов (баланс игры)
        if len(trees) > 6:
            trees.pop(0)
            trees.pop(0)

        if len(stones) > 6:
            stones.pop(0)
            stones.pop(0)

    # Movement
    if keys[pygame.K_a]:
        player_x -= player_speed
        direction = "left"
        moving = True
        step_sound.play()
    if keys[pygame.K_d]:
        player_x += player_speed
        direction = "right"
        moving = True
        step_sound.play()

    # Mining Logic (requires individual clicks)
    if keys[pygame.K_f]:
        hitting = True
        if not f_key_pressed:  # Trigger only on the initial press
            player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE[0], PLAYER_SIZE[1])

            for tree in trees[:]:
                # Tree hitbox centered on the trunk
                tree_rect = pygame.Rect(tree["x"] + 180, tree["y"] + 300, 80, 150)

                if player_rect.colliderect(tree_rect):
                    tree["hits"] -= 1
                    if tree["hits"] <= 0:
                        trees.remove(tree)
                        logs += 6
                        wood_sound.play()


            #Stone Logic
            for stone in stones[:]:
                # Tree hitbox centered on the trunk
                stone_rect = pygame.Rect(stone["x"], stone["y"], 260, 260)

                if player_rect.colliderect(stone_rect):
                    stone["hits"] -= 1
                    if stone["hits"] <= 0:
                        stones.remove(stone)
                        stone_block += 3
                        wood_sound.play()



            f_key_pressed = True
    else:
        f_key_pressed = False

    # Borders
    if player_x < -40: player_x = -40
    if player_x > WIDTH - PLAYER_SIZE[0]: player_x = WIDTH - PLAYER_SIZE[0]

    # Draw Trees
    for tree in trees:
        screen.blit(tree_img, (tree["x"], tree["y"]))

    # Draw rocks
    for stone in stones:
        screen.blit(rock_img, (stone["x"], stone["y"]))

    # Animation Logic
    if moving:
        frame_count += 1
        if frame_count >= animation_speed:
            frame += 1
            frame_count = 0
    else:
        frame = 0

    # Select Sprite
    if hitting:
        image = hand_img
    else:
        image = walk_right[frame % len(walk_right)]

    if direction == "left":
        image = pygame.transform.flip(image, True, False)


    # Draw Player
    screen.blit(image, (player_x, player_y))

    # UI Elements
    screen.blit(stone_img, (20, 20))
    screen.blit(log_img, (120, 20))
    screen.blit(grass_img, (220, 20))

    font = pygame.font.Font(None, 40)
    screen.blit(font.render(f"{stone_block}", True, red), (85, 35))
    screen.blit(font.render(f"{logs}", True, red), (185, 35))
    screen.blit(font.render(f"{grass}", True, red), (285, 35))

    pygame.display.flip()
    clock.tick(60)