""" 
Abheek Tuladhar
Period 4 HCP
HCP Final Project : ShapeStorm
Description: A game where you shoot down enemy shapes that fall from the sky
with numerous abilities and shapes while collecting power ups to survive and make it back to your home planet.
"""

"""
MILESTONE LIST:
1. Create the directions screen ✅
2. Create the background with the dispensers, player, and play button ✅
3. Make the player move left and right ✅
4. Make the player shoot bullets ✅
5. Make the bullets move up the screen ✅
6. Add unfunctional powerups to the screen every VARIABLE seconds ✅
7. Make bullets disappear when they hit a powerup ✅
8. Make it so that powerup goes into the powerups section of the directions screen ✅
9. Make it so hitting 1, 2, 3, or 4 deletes the powerup from the directions screen ✅
10. Make the pause and play button functional ✅
11. Make functional powerup for the ammo regen - DUE DATE 5/12 (Gotta study for those keystones) ✅
12. Make random enemies spawn and move down the screen from the dispensers - DUE DATE 5/14
13. Make the plague, shield, and slowtime powerups functional since enemies exist now - DUE DATE 5/15
14. Make it so that the player can shoot the enemies and they disappear based on their color for lives - DUE DATE 5/16
15. Make it so that there are levels based on how many enemies the user has killed - DUE DATE 5/17
16. (OPTIONAL???) Make it so that the enemies come out of the dispensers at an angle and bounce off of the walls and other enemies - DUE DATE 5/20
17. Make it so that easier enemies spawn more often at lower levels and harder enemies spawn more often at higher levels - DUE DATE 5/21
18. Add random powerups to the enemies based on their color - 5/23 (Use the weekend to study for your finals. Good luck from your past self from 5/12)
"""

import pygame, sys, random
import drawingFunctions #This has all the drawing functions for the game. It got too long and I only was working with main and powerup stuff

pygame.init()
pygame.mixer.init()

WIDTH=1000
HEIGHT=WIDTH*2/3

size=(WIDTH, HEIGHT)
surface = pygame.display.set_mode(size)

pygame.display.set_caption("ShapeStorm")

#Colors
BLACK    = (0, 0, 0)
BROWN    = (145, 113, 76)
WHITE    = (255, 255, 255)
GOLD     = (255, 215, 0)
GREEN    = (0, 200, 0)
YELLOW   = (200, 200, 0)
RED      = (200, 0, 0)
PURPLE   = (200, 0, 200)
BLUE     = (173, 216, 230)

#Split screen into a 60 by 60 grid
xu = WIDTH//60
yu = HEIGHT//60

#Load and Scale Images
plague = pygame.image.load("images/Plague.png").convert_alpha()
slowtime  = pygame.image.load("images/slowtime.png").convert_alpha()
shield = pygame.image.load("images/shield.png").convert_alpha()
ammoregen = pygame.image.load("images/ammoregen.png").convert_alpha()
heart = pygame.image.load("images/heart.png").convert_alpha()
heart = pygame.transform.scale(heart, (xu, xu))
dodger = pygame.image.load("images/dodger.png").convert_alpha()
dash = pygame.image.load("images/dash.png").convert_alpha()
rotation = pygame.image.load("images/rotation.png").convert_alpha()
bumper = pygame.image.load("images/bumper.png").convert_alpha()
teleport = pygame.image.load("images/teleport.png").convert_alpha()
player = pygame.image.load("images/Player.png").convert_alpha()
player_x_scale = 80
player = pygame.transform.scale(player, (player_x_scale, player_x_scale*1.25))

#Powerup images and their names (for the powerup effect function)
POWERUPS = [plague, shield, shield, slowtime, slowtime, slowtime, ammoregen, ammoregen, ammoregen, ammoregen] #Certain powerups are more common then others
POWERUP_NAMES = ['plague', 'shield', 'shield', 'slowtime', 'slowtime', 'slowtime', 'ammoregen', 'ammoregen', 'ammoregen', 'ammoregen']

#Sound Loading
music = pygame.mixer.Sound("Audio/Music.mp3")
shot = pygame.mixer.Sound("Audio/shot.wav")
no_ammo = pygame.mixer.Sound("Audio/no_ammo.mp3")
gun_cock = pygame.mixer.Sound("Audio/gun_cock.wav")

#Background music plays on repeat
music.play(-1)

def powerup_effect(powerup_name, current_bullet_reload_time, bullet_reload_time):
    """
    Applies the effect of the powerup to the player.
    For ammoregen, it returns the halved cooldown based on the base reload time.

    Parameters:
    -----------
    powerup_name : str
        The name of the powerup (e.g., 'ammoregen').
    current_bullet_reload_time : float
        The current bullet reload time.
    bullet_reload_time : float
        The player's normal, original bullet reload time.

    Returns:
    --------
    bullet_reload_time_updated : float
        The new bullet_reload_time.
    """

    bullet_reload_time_updated = current_bullet_reload_time

    if powerup_name == 'plague':
        pass #TODO: Implement plague effect
    elif powerup_name == 'shield':
        pass #TODO: Implement shield effect
    elif powerup_name == 'slowtime':
        pass #TODO: Implement slowtime effect
    elif powerup_name == 'ammoregen':
        bullet_reload_time_updated = bullet_reload_time / 2 #Half the original cooldown

    return bullet_reload_time_updated


def main():
    """
    Where all the action happens

    Parameters:
    -----------
    None

    Returns:
    --------
    None
    """

    #Game Variables
    x = 40*xu
    leftwall = (WIDTH//3)
    rightwall = WIDTH - player.get_width()
    bullets = []
    last_shot_time = 0
    cock_done = False
    speed = 15
    powerup_list = []
    paused = False
    collected_powerups = []

    powerup_cooldown = 5
    last_powerup_spawn_time = 0

    #I didn't copy code from Gemini AI, however, I was stuck on how to adjust the current_time with the pausing
    #It gave me the idea of tracking how much time was spent in pause mode
    time_at_pause_start = 0 #To store timestamp when pause begins so pausing doesn't continue the ticks

    #Hitboxes... again
    pause_button_hitbox = pygame.Rect(58.5*xu, 0, 4*xu, 4*xu)
    play_button_hitbox = pygame.Rect(37*xu, 24*yu, 10*xu, 10*xu)

    #Bullet constants
    BULLET_WIDTH = 10
    BULLET_HEIGHT = 20
    BULLET_SPEED = 20

    bullet_cooldown_time = 0.8
    copy_bullet_cooldown_time = bullet_cooldown_time #Store the normal cooldown so we can edit and save it
    ammoregen_time_end = 0 #Timestamp when ammoregen effect ends and is 0 if not active

    #Game Loop!
    while True:
        mouse_pos = pygame.mouse.get_pos() #mouse position for pausing

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not paused: #If game is running, check for pause click
                    if pause_button_hitbox.collidepoint(mouse_pos):
                        paused = True
                        time_at_pause_start = pygame.time.get_ticks() #Record time when pausing
                else: #If game is paused, check for the user hitting the play button
                    if play_button_hitbox.collidepoint(mouse_pos):
                        paused = False
                        #Adjust all the timing variables to account for the time spent paused
                        pause_duration = pygame.time.get_ticks() - time_at_pause_start
                        last_shot_time += pause_duration
                        last_powerup_spawn_time += pause_duration

                        time_at_pause_start = 0 #Reset for the next pause

            #If not paused, continue as normal
            if not paused:
                if event.type == pygame.KEYDOWN: #If there's pretty much any input from user
                    if event.key == pygame.K_SPACE: #Shoot
                        current_time = pygame.time.get_ticks() #Get current_time
                        if current_time - last_shot_time > bullet_cooldown_time * 1000: #If the cooldown is over and you shoot
                            shot.play()
                            cock_done = False

                            #Create a new bullet originating from the player's cannon
                            #x is the top left of the player, so adding with the width and dividing by 2 is middle
                            #Minus the bullet_width//2 because otherwise top left of bullet is in the middle
                            bullet_x = x + player.get_width() // 2 - BULLET_WIDTH // 2
                            bullet_y = HEIGHT - 8*yu

                            #Attribute idea with dictionaries was given to me by a friend
                            new_bullet = {
                                'x': bullet_x,
                                'y': bullet_y,
                                'width': BULLET_WIDTH,
                                'height': BULLET_HEIGHT,
                                'speed': BULLET_SPEED,
                                'color': YELLOW
                            }

                            bullets.append(new_bullet)
                            last_shot_time = current_time #update last shot time
                        else:
                            no_ammo.play()

                    #POWERUPS
                    powerup_name = None
                    powerup_remove_idx = -1

                    if event.key == pygame.K_1 and len(collected_powerups) >= 1:
                        powerup_name = collected_powerups[0]['name']
                        powerup_remove_idx = 0
                    elif event.key == pygame.K_2 and len(collected_powerups) >= 2:
                        powerup_name = collected_powerups[1]['name']
                        powerup_remove_idx = 1
                    elif event.key == pygame.K_3 and len(collected_powerups) >= 3:
                        powerup_name = collected_powerups[2]['name']
                        powerup_remove_idx = 2
                    elif event.key == pygame.K_4 and len(collected_powerups) >= 4:
                        powerup_name = collected_powerups[3]['name']
                        powerup_remove_idx = 3

                    if powerup_name != None:
                        bullet_cooldown_time = powerup_effect(powerup_name, bullet_cooldown_time, copy_bullet_cooldown_time)

                        if powerup_name == 'ammoregen':
                            ammoregen_time_end = pygame.time.get_ticks() + 10000 #the expiration time
                        elif powerup_name == 'shield':
                            pass
                        elif powerup_name == 'plague':
                            pass
                        elif powerup_name == 'slowtime':
                            pass

                        #Remove the powerup from the collected powerups list
                        collected_powerups.pop(powerup_remove_idx)

        #Game logic updates only if not paused
        if not paused:
            keys = pygame.key.get_pressed() #For continuous input like movement
            current_time = pygame.time.get_ticks() #For time-based logic

            if current_time - last_shot_time > bullet_cooldown_time * 1000 and not cock_done:
                gun_cock.play()
                cock_done = True

            #Movement- max min idea credit to Friend
            if (keys[pygame.K_a] or keys[pygame.K_LEFT]):
                x = max(leftwall, x - speed)

            elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
                x = min(rightwall, x + speed)

            #Powerup Spawning
            if current_time - last_powerup_spawn_time > powerup_cooldown * 1000:
                powerup_x = random.randint(int(WIDTH//3 + 40), int(WIDTH - 2*xu - (2*xu)))
                powerup_y = random.randint(int(HEIGHT//2), int(HEIGHT - 13*yu - (2*xu)))

                powerup_index = random.randint(0, len(POWERUPS) - 1)
                powerup = pygame.transform.scale(POWERUPS[powerup_index], (2*xu, 2*xu))

                powerup_list.append({'image': powerup, 'x': powerup_x, 'y': powerup_y, 'name': POWERUP_NAMES[powerup_index]})
                last_powerup_spawn_time = current_time

            #Move bullets
            active_bullets = []
            for bullet in bullets:
                bullet['y'] -= bullet['speed'] #Move the bullet up
                if bullet['y'] + bullet['height'] > 0: #If bullet on screen
                    active_bullets.append(bullet)
            bullets = active_bullets

            #Check if ammoregen effect should expire
            if ammoregen_time_end > 0 and current_time >= ammoregen_time_end:
                bullet_cooldown_time = copy_bullet_cooldown_time #Revert to normal
                ammoregen_time_end = 0 #Mark as inactive

            #Bullet-Powerup Collisions
            powerups_to_keep = []
            bullets_after_collision = list(bullets) #Modifyable copy

            for powerup_data in powerup_list:
                powerup_hit_by_bullet = False
                for bullet in bullets:
                    #Create proper rects for collision
                    powerup_rect = pygame.Rect(powerup_data['x'], powerup_data['y'], 2*xu, 2*xu) #Powerups are 2*xu by 2*xu
                    bullet_rect = pygame.Rect(bullet['x'], bullet['y'], bullet['width'], bullet['height'])

                    if powerup_rect.colliderect(bullet_rect):
                        if len(collected_powerups) < 4: #Make sure user doesn't have more than 4 powerups ever
                            collected_powerups.append(powerup_data) #Add the actual powerup dict
                        else:
                            collected_powerups[random.randint(0, len(collected_powerups) - 1)] = powerup_data

                        if bullet in bullets_after_collision: #Bullet is consumed
                            bullets_after_collision.remove(bullet)
                        powerup_hit_by_bullet = True
                        break #Bullet hits one powerup, powerup is collected

                if not powerup_hit_by_bullet:
                    powerups_to_keep.append(powerup_data)

            powerup_list = powerups_to_keep
            bullets = bullets_after_collision

        surface.fill(BLUE)
        drawingFunctions.drawScreen(x, bullets, powerup_list, collected_powerups)

        if paused:
            drawingFunctions.drawPlay()

        pygame.display.update()

main()
