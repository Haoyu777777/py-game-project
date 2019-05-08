# Haoyu Li hl6de
# Rickey Guo rg7cz
# We acknowledge Luther Tychonievich for his gamebox code.


import pygame
import gamebox
import random


camera = gamebox.Camera(400, 600)
# the below are characters, done
number_of_frame_character = 3
sheet = gamebox.load_sprite_sheet("img/jet.png", 8, number_of_frame_character)
frame_character = 0
frame_right = 3
frame_left = 12
character = gamebox.from_image(200, 300, sheet[frame_character])
cannon = gamebox.from_color(character.x, character.y, "white", 10, 10)
bullet = []  # empty list for appending bullets to be shot
background = [gamebox.from_image(200, 300, "img/background.jpg"),
              gamebox.from_image(200, -300, "img/background.jpg")]


# the boundary of the screen, do not change (done)
boundary = [gamebox.from_color(200, 0, "black", 400, 10), gamebox.from_color(200, 600, "black", 400, 10),
            gamebox.from_color(0, 300, "black", 10, 600), gamebox.from_color(400, 300, "black", 10, 600)]


# rules and instructions
game_name = "Air Supremacy"
creator_names = "Created by Haoyu Li and Rickey Guo"
controls1 = "w = move up        s = move down"
controls2 = "a = move left      d = move right"
controls3 = "space = shoot"
goal = "Shoot down the enemies and stay alive!"
press_to_start = "Press space to start"
tip = "Collecting hearts will restore to your health."


# enemy movement is done
enemy_0 = []
enemy_1 = []
enemy_bullet0 = []
enemy_bullet1 = []
frame_enemy_1 = 0
frame_enemy_0 = 0
number_of_frame_enemy_1 = 4
number_of_frame_enemy_0 = 6
enemy_1_sheet = gamebox.load_sprite_sheet(
    "img/enemy1.png", 4, number_of_frame_enemy_1)
enemy_0_sheet = gamebox.load_sprite_sheet(
    "img/enemy0.png", 6, number_of_frame_enemy_0)


# the below are some systems and upgrades, aka global variables
level = 1
score = 0
health = 1
count = 0
count_self = 0
game_on = False


health_port = []  # done
number_of_frame_heart = 2
heart_sheet = gamebox.load_sprite_sheet("img/heart.png", 1, number_of_frame_heart)


# explosion
frame_of_explosion = 0
exploding_sheet = gamebox.load_sprite_sheet("img/explosion.png", 4, 4)
exploding = gamebox.from_image(
    character.x, character.y, exploding_sheet[frame_of_explosion])

# no timer, no saving point, no multiplayers, no inter-session progress


def back_ground():
    camera.clear("white")
    for i in background:
        i.y += 2
        if i.y >= 900:
            i.y = -300
        camera.draw(i)


def start_screen(keys):  # the beginning screen, can include everything needed before game start
    global game_on
    camera.clear("white")  # color subject to change
    camera.draw(gamebox.from_text(200, 100, game_name, 40, "green"))
    camera.draw(gamebox.from_text(200, 130, creator_names, 25, "blue"))
    camera.draw(gamebox.from_text(200, 200, controls1, 25, "black"))
    camera.draw(gamebox.from_text(200, 220, controls2, 25, "black"))
    camera.draw(gamebox.from_text(200, 240, controls3, 25, "black"))
    camera.draw(gamebox.from_text(200, 300, goal, 25, "red"))
    camera.draw(gamebox.from_text(200, 330, tip, 25, "red"))
    # rules written here
    camera.draw(gamebox.from_text(200, 550, press_to_start, 25, "red"))
    camera.display()
    if pygame.K_SPACE in keys:  # not sure if space is a good choice as it is also the firing key
        game_on = True  # needs set the condition for the game to start


# w, s, a, d + space to control the movement/attack of the character
def character_control(keys):
    global count_self, frame_character, frame_right, frame_left
    frame_character += 1
    if frame_character == number_of_frame_character:
        frame_character = 0
    if count % 1 == 0:
        character.image = sheet[frame_character]
    cannon.center = character.center
    if pygame.K_w in keys:
        character.y -= 6
    if pygame.K_s in keys:
        character.y += 6
    if pygame.K_a in keys:
        frame_left += 1
        if frame_left == number_of_frame_character + 12:
            frame_left = 12
        if count % 1 == 0:
            character.image = sheet[frame_left]
        character.x -= 4
    if pygame.K_d in keys:
        frame_right += 1
        if frame_right == number_of_frame_character + 3:
            frame_right = 3
        if count % 1 == 0:
            character.image = sheet[frame_right]
        character.x += 4
    if pygame.K_SPACE in keys:
        count_self += 1
        if count_self % 10 == 0:
            bullet.append(gamebox.from_image(
                cannon.x, cannon.y, "img/missile.png"))  # bullet is
            # subject to change
    for i in bullet:
        i.y -= 7
        if i.y < -20:
            bullet.remove(i)
        camera.draw(i)
    camera.draw(character)


def enemy_movement():  # enemy coming randomly from left or right and the number and
    # shooting frequency are based on level
    global count, frame_enemy_0, frame_enemy_1
    count += 1
    frame_enemy_0 += 1
    frame_enemy_1 += 1
    if frame_enemy_1 == number_of_frame_enemy_1 + 3:
        frame_enemy_1 = 0
    if frame_enemy_0 == number_of_frame_enemy_0*6:
        frame_enemy_0 = 0
    if count % (180 // level) == 0:
        direction = random.randint(0, 1)
        if direction == 0:
            enemy_0.append(gamebox.from_image(
                450, 0, enemy_0_sheet[frame_enemy_0]))
        if direction == 1:
            enemy_1.append(gamebox.from_image(-50, 0,
                                              enemy_1_sheet[frame_enemy_1]))
    for unit0 in enemy_0:
        if count % 1 == 0:
            unit0.image = enemy_0_sheet[frame_enemy_0]
        unit0.move(-3, 2 * random.random())
        if unit0.x < -500:
            enemy_0.remove(unit0)
        if count % (90 // level) == random.randint(0, 18):
            enemy_bullet0.append(gamebox.from_image(
                unit0.x, unit0.y, "img/enemy missile.png"))
        camera.draw(unit0)
    for i in enemy_bullet0:
        i.y += 5
        if i.y > 700:
            enemy_bullet0.remove(i)
        camera.draw(i)
    for unit1 in enemy_1:
        if count % 1 == 0:
            unit1.image = enemy_1_sheet[frame_enemy_1]
        unit1.move(3, 2 * random.random())
        if unit1.x > 900:
            enemy_1.remove(unit1)
        if count % (90 // level) == random.randint(0, 18):
            enemy_bullet1.append(gamebox.from_image(
                unit1.x, unit1.y, "img/enemy missile.png"))
        camera.draw(unit1)
    for i in enemy_bullet1:
        i.y += 5
        if i.y > 700:
            enemy_bullet1.remove(i)
        camera.draw(i)


def boundary_condition():  # to prevent the character to move over the screen, by stopping it
    for wall in boundary:
        if character.touches(wall):
            character.move_to_stop_overlapping(wall)


def collision_control():
    global health, score
    for i in enemy_bullet0:  # receive damage from the enemy
        if i.touches(character):
            health -= 1
            enemy_bullet0.remove(i)
    for j in enemy_bullet1:
        if j.touches(character):
            health -= 1
            enemy_bullet1.remove(j)
    for i in bullet:  # to kill the enemy
        for enemy in enemy_0:
            if i.touches(enemy):
                enemy_0.remove(enemy)
                score += 1
                bullet.remove(i)
    for i in bullet:
        for enemy in enemy_1:
            if i.touches(enemy):
                # when killing an enemy, its bullet disappears,
                enemy_1.remove(enemy)
                # dk how to keep them
                score += 1
                bullet.remove(i)
    camera.draw(gamebox.from_text(50, 40, "score: " + str(score), 20, "black"))


def game_end():
    global frame_of_explosion
    if health <= 0:
        frame_of_explosion += 1
        if count % 1 == 0:
            exploding.center = character.center
            exploding.image = exploding_sheet[frame_of_explosion]
        if frame_of_explosion == 15:
            gamebox.pause()
            camera.draw(gamebox.from_text(
                200, 300, "Your final score is " + str(score) + " !", 30, "black"))
        camera.draw(exploding)


def health_portion():
    global health
    if count % (600*level) == 0:  # the timing is based on level
        health_port.append(gamebox.from_image(random.randint(100, 300), random.randint(200, 500),
                                              "img/heart.png"))  # the healt port can change in shape
    for i in health_port:
        camera.draw(i)
        if character.touches(i):
            health_port.remove(i)
            health += 1
    camera.draw(gamebox.from_text(50, 55, "health: " +
                                  str(health), 20, "black"))  # the location, size
    #  or shape are subject to change


def level_control():
    global level  # level changes based on scores
    if score == 10:
        level = 2
    if score == 20:
        level = 3
    if score == 30:
        level = 4
    if score > 50:
        level = 5
    camera.draw(gamebox.from_text(50, 25, "lvl: " + str(level), 20, "black"))


def tick(keys):
    start_screen(keys)
    if game_on:
        back_ground()
        level_control()
        character_control(keys)
        enemy_movement()
        boundary_condition()
        collision_control()
        health_portion()
        game_end()
        camera.display()


tick_per_second = 30
gamebox.timer_loop(tick_per_second, tick)
