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
12. Make random enemies spawn and move down the screen from the dispensers - DUE DATE 5/14 ✅
13. Make the plague, shield, and slowtime powerups functional since enemies exist now - DUE DATE 5/15 ✅
14. Make it so that the player can shoot the enemies and they disappear based on their color for lives - DUE DATE 5/16 ✅
15. Make it so you can die and restart the game - DUE DATE 5/16 ✅
16. Make a life powerup that gives you an extra life - DUE DATE 5/16 ✅
17. Make it so that there are levels based on how many enemies the user has killed. Lower levels = easier enemies and less powerups and vice versa - DUE DATE 5/17 ✅
18. Make it so that easier enemies spawn more often at lower levels and harder enemies spawn more often at higher levels - DUE DATE 5/17 ✅
19. Add a way to win - DUE DATE 5/17 ✅
20. Add enemy death animation - DUE DATE 5/18 ✅
21. Refine details and make sure code is up to PEP standards - DUE DATE 5/23 ✅
22. Make main() more function based than code based - DUE DATE 5/23
"""

try:
    import pygame
    import sys
    import random
    import drawing_functions
except ImportError:
    print('Please install the requirements.txt')
    exit()

pygame.init()
pygame.mixer.init()

WIDTH = 1000
HEIGHT = WIDTH * 2 / 3

SIZE = (WIDTH, HEIGHT)
SURFACE = pygame.display.set_mode(SIZE)

pygame.display.set_caption('ShapeStorm')

#Colors
BLACK = (0, 0, 0)
BROWN = (145, 113, 76)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
GREEN = (0, 200, 0)
YELLOW = (200, 200, 0)
RED = (200, 0, 0)
PURPLE = (200, 0, 200)
BLUE = (173, 216, 230)

#Split screen into a 60 by 60 grid
XU = WIDTH // 60
YU = HEIGHT // 60

#Load and Scale Images
plague = pygame.image.load('Images/Plague.png').convert_alpha()
slowtime = pygame.image.load('Images/slowtime.png').convert_alpha()
shield = pygame.image.load('Images/shield.png').convert_alpha()
ammo_regen = pygame.image.load('Images/ammo_regen.png').convert_alpha()
heart = pygame.image.load('Images/heart.png').convert_alpha()
heart = pygame.transform.scale(heart, (XU, XU))
player = pygame.image.load('Images/Player.png').convert_alpha()
PLAYER_X_SCALE = 80
player = pygame.transform.scale(player, (PLAYER_X_SCALE, PLAYER_X_SCALE * 1.25))

#These determine what powerups spawn and their ratio of them spawning by the level
POWERUPS1 = [ammo_regen]
POWERUPS2 = [ammo_regen, ammo_regen, ammo_regen, shield, shield, heart, heart, slowtime, slowtime, slowtime] #3:2:2:3:0
POWERUPS3 = [ammo_regen, ammo_regen, shield, shield, heart, heart, heart, slowtime, slowtime, slowtime, slowtime, plague] #2:2:3:4:1
POWERUPS4 = [ammo_regen, shield, heart, slowtime, plague, plague] #1:1:1:1:2
POWERUPS5 = [ammo_regen, shield, heart, heart, heart, slowtime, slowtime, plague, plague, plague, plague] #1:1:3:2:5

PNAMES1 = ['ammo_regen'] #Should be impossible to get powerups on level 1 with the 99 second wait, but just in case
PNAMES2 = ['ammo_regen', 'ammo_regen', 'ammo_regen', 'shield', 'shield', 'heart', 'heart', 'slowtime', 'slowtime', 'slowtime']
PNAMES3 = ['ammo_regen', 'ammo_regen', 'shield', 'shield', 'heart', 'heart', 'heart', 'slowtime', 'slowtime', 'slowtime', 'slowtime', 'plague']
PNAMES4 = ['ammo_regen', 'shield', 'heart', 'slowtime', 'plague', 'plague']
PNAMES5 = ['ammo_regen', 'shield', 'heart', 'heart', 'heart', 'slowtime', 'slowtime', 'plague', 'plague', 'plague', 'plague']

LEVEL1ENEMIES = ['easy', 'medium'] #Only easy and medium enemies
LEVEL2ENEMIES = ['easy', 'medium', 'medium', 'hard'] #Medium is more common. Hard is introduced
LEVEL3ENEMIES = ['medium', 'hard', 'hard', 'insane'] #Hard is more common. Insane is introduced
LEVEL4ENEMIES = ['medium', 'hard', 'hard', 'insane', 'insane', 'insane'] #Insane is more common
LEVEL5ENEMIES = ['hard', 'insane', 'insane', 'insane', 'insane', 'insane'] #Insane mostly

#The stats per level in a list of dictionaries
LEVELED_INFO = ['PLACEHOLDER SO INDECIES ARE CORRECT. THIS IS NONFUNCTIONAL INDEX 0',
                {'enemy_cooldown' : 4.0, 'player_speed' : 15, 'bullet_cooldown' : 1.0, 'powerup_cooldown' : 99, 'powerups' : POWERUPS1, 'powerup_names' : PNAMES1, 'enemy_choice' : LEVEL1ENEMIES},
                {'enemy_cooldown' : 3.5, 'player_speed' : 17, 'bullet_cooldown' : 0.9, 'powerup_cooldown' : 20, 'powerups' : POWERUPS2, 'powerup_names' : PNAMES2, 'enemy_choice' : LEVEL2ENEMIES},
                {'enemy_cooldown' : 3.0, 'player_speed' : 19, 'bullet_cooldown' : 0.8, 'powerup_cooldown' : 15, 'powerups' : POWERUPS3, 'powerup_names' : PNAMES3, 'enemy_choice' : LEVEL3ENEMIES},
                {'enemy_cooldown' : 2.5, 'player_speed' : 21, 'bullet_cooldown' : 0.7, 'powerup_cooldown' : 10, 'powerups' : POWERUPS4, 'powerup_names' : PNAMES4, 'enemy_choice' : LEVEL4ENEMIES},
                {'enemy_cooldown' : 2.0, 'player_speed' : 23, 'bullet_cooldown' : 0.6, 'powerup_cooldown' :  5, 'powerups' : POWERUPS5, 'powerup_names' : PNAMES5, 'enemy_choice' : LEVEL5ENEMIES}]

powerups = LEVELED_INFO[1]['powerups']
powerup_names = LEVELED_INFO[1]['powerup_names']

#Sound Loading
MUSIC = pygame.mixer.Sound('Audio/music.mp3')
SHOT = pygame.mixer.Sound('Audio/shot.wav')
NO_AMMO = pygame.mixer.Sound('Audio/no_ammo.mp3')
GUN_COCK = pygame.mixer.Sound('Audio/gun_cock.wav')

#Background music plays on repeat
MUSIC.play(-1)

clock = pygame.time.Clock()


def powerup_effect(powerup_name, current_bullet_reload_time, bullet_reload_time, enemies, lives, kills):
    """
    Applies the effect of the powerup to the player

    Parameters:
    -----------
    powerup_name : str
        The name of the powerup (e.g., 'ammo_regen')
    current_bullet_reload_time : float
        The current bullet reload time
    bullet_reload_time : float
        The player's normal, original bullet reload time
    enemies : list
        A list of enemy dictionaries filled with their stats.
    lives : int
        The number of lives the player has
    kills : int
        The number of enemies the player has killed

    Returns:
    --------
    bullet_reload_time_updated : float
        The new bullet_reload_time
    enemies : list
        The updated list of enemies
    shield_active : bool
        Whether the shield is active or not
    lives : int
        The updated number of lives the player has
    kills : int
        The updated number of kills the player has
    win : bool
        Whether the player has won or not
    paused : bool
        Whether the game is paused or not
    """

    bullet_reload_time_updated = current_bullet_reload_time
    shield_active = False
    win = False
    paused = False

    if powerup_name == 'plague':
        original_enemy_count = len(enemies)
        enemies_to_remove = []

        for enemy in enemies:
            if enemy['y'] >= HEIGHT // 2 - 3 * XU:
                enemies_to_remove.append(enemy)

        for enemy in enemies_to_remove:
            enemies.remove(enemy)

        num_killed_by_plague = original_enemy_count - len(enemies)
        kills += num_killed_by_plague

        if kills >= 60: #Check win condition after updating kills
            win = True
            paused = True

    elif powerup_name == 'shield':
        shield_active = True #This will be used to make a barrier of shield Images (Needs to be checked every frame so it's in main)

    elif powerup_name == 'slowtime':
        for enemy in enemies:
            enemy['speed'] = enemy['speed'] / 2

    elif powerup_name == 'ammo_regen':
        bullet_reload_time_updated = bullet_reload_time / 2 #Half the original cooldown

    elif powerup_name == 'heart':
        lives += 1

    return bullet_reload_time_updated, enemies, shield_active, lives, kills, win, paused


def enemy_health(enemy_type):
    """
    Returns the health of the enemy based on its type

    Parameters:
    -----------
    enemy_type : str
        The type of the enemy (e.g., 'easy', 'medium', 'hard', 'insane')

    Returns:
    --------
    int
        The health of the enemy
    """

    if enemy_type == 'easy':
        return 1
    elif enemy_type == 'medium':
        return 2
    elif enemy_type == 'hard':
        return 3
    elif enemy_type == 'insane':
        return 4


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

    #Player Variables
    player_x = 40 * XU
    player_speed = 3
    lives = 5
    kills = 0
    level = 1 #Initialize level
    lose = False
    win = False
    LEFTWALL = (WIDTH // 3)
    RIGHTWALL = WIDTH - player.get_width()
    paused = True

    #Enemy Variables
    last_enemy_spawn_time = 0
    enemy_speed = 4
    enemies = []
    dying_enemies = [] #List to store enemies undergoing death animation
    enemy_cooldown = 3
    enemy_choice = ['easy', 'medium', 'hard', 'insane']
    possible_x_pos = [24.5 * XU, 33.5 * XU, 42.5 * XU, 51.5 * XU]
    enemies = []

    #Bullet Variables
    bullets = []
    last_shot_time = 0
    cock_done = False
    BULLET_WIDTH = 10
    BULLET_HEIGHT = 20
    BULLET_SPEED = 20
    bullet_cooldown_time = 0.8
    copy_bullet_cooldown_time = bullet_cooldown_time

    #Powerup Variables
    powerup_list = []
    collected_powerups = []
    powerup_cooldown = 5
    last_powerup_spawn_time = 0
    ammo_regen_time_end = 0
    slowtime_end = 0
    shield_time_end = 0
    shield_active = False
    AMMO_REGEN_EXPIRATION = 10000 #10 seconds
    SLOWTIME_EXPIRATION = 5000 #5 seconds
    SHIELD_EXPIRATION = 3000 #3 seconds
    DEATH_ANIMATION_DURATION = 500 #0.5 seconds

    #Pause/Play Variables
    PAUSE_BUTTON_HITBOX = pygame.Rect(58.5 * XU, 0, 4 * XU, 4 * XU)
    PLAY_BUUTTON_HITBOX = pygame.Rect(37 * XU, 24 * YU, 10 * XU, 10 * XU)
    #I didn't copy code from Gemini AI, however, I was stuck on how to adjust the current_time with the pausing
    #It gave me the idea of tracking how much time was spent in pause mode
    time_at_pause_start = 0 #To store timestamp when pause begins so pausing doesn't continue the ticks

    #Level Variable
    LEVEL_REQUIREMENTS = {1: 0,
                          2: 5,
                          3: 15,
                          4: 30,
                          5: 50} #Kills needed for each level

    #Game Loop!
    while True:
        mouse_pos = pygame.mouse.get_pos() #Mouse position for pausing/playing

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r: #Restart the game
                #Game Variables
                #Player Variables
                player_x = 40 * XU
                player_speed = 3
                lives = 5
                kills = 0
                win = False
                level = 1  #Initialize level
                lose = False
                LEFTWALL = (WIDTH // 3)
                RIGHTWALL = WIDTH - player.get_width()
                paused = True

                #Enemy Variables
                last_enemy_spawn_time = 0
                enemy_speed = 5
                enemy_cooldown = 3
                dying_enemies = []
                enemy_choice = ['easy', 'medium', 'hard', 'insane']
                possible_x_pos = [24.5 * XU, 33.5 * XU, 42.5 * XU, 51.5 * XU]
                enemies = []

                #Bullet Variables
                bullets = []
                last_shot_time = 0
                cock_done = False
                BULLET_WIDTH = 10
                BULLET_HEIGHT = 20
                BULLET_SPEED = 20
                bullet_cooldown_time = 0.8
                copy_bullet_cooldown_time = bullet_cooldown_time

                #Powerup Variables
                powerup_list = []
                collected_powerups = []
                powerup_cooldown = 5
                last_powerup_spawn_time = 0
                ammo_regen_time_end = 0
                slowtime_end = 0
                shield_time_end = 0
                shield_active = False
                AMMO_REGEN_EXPIRATION = 10000 #10 seconds
                SLOWTIME_EXPIRATION = 5000 #5 seconds
                SHIELD_EXPIRATION = 3000 #3 seconds

                #Pause / Play Variables
                PAUSE_BUTTON_HITBOX = pygame.Rect(58.5 * XU, 0, 4 * XU, 4 * XU)
                PLAY_BUUTTON_HITBOX = pygame.Rect(37 * XU, 24 * YU, 10 * XU, 10 * XU)
                #I didn't copy code from Gemini AI, however, I was stuck on how to adjust the current_time with the pausing
                #It gave me the idea of tracking how much time was spent in pause mode
                time_at_pause_start = 0 #To store timestamp when pause begins so pausing doesn't continue the ticks

                #Level Variable
                LEVEL_REQUIREMENTS = {1: 0, 2: 5, 3: 15, 4: 30, 5: 50}  #Kills needed for each level

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not paused: #If game is running, check for pause click
                    if PAUSE_BUTTON_HITBOX.collidepoint(mouse_pos): #If the user did hit the pause button
                        paused = True
                        time_at_pause_start = pygame.time.get_ticks() #Record time when pausing
                else: #If game is paused, check for the user hitting the play button
                    if not lose and PLAY_BUUTTON_HITBOX.collidepoint(mouse_pos): #Only unpause if game isn't over
                        paused = False
                        #Adjust all the timing variables to account for the time spent paused, that way there isn't a pause and wait for powerups to spawn strategy
                        pause_duration = pygame.time.get_ticks() - time_at_pause_start #Amount of time spent paused
                        #Update time variables
                        last_shot_time += pause_duration
                        last_powerup_spawn_time += pause_duration
                        last_enemy_spawn_time += pause_duration #Adjust enemy spawn timer

                        #Adjust active powerup timers
                        if ammo_regen_time_end > 0:
                            ammo_regen_time_end += pause_duration
                        if slowtime_end > 0:
                            slowtime_end += pause_duration
                        if shield_time_end > 0:
                            shield_time_end += pause_duration

                        time_at_pause_start = 0 #Reset for the next pause

            #If not paused, continue as normal
            if not paused:
                if event.type == pygame.KEYDOWN: #If there's pretty much any input from user
                    if event.key == pygame.K_SPACE: #Shoot
                        current_time = pygame.time.get_ticks() #Get current_time
                        if current_time - last_shot_time > bullet_cooldown_time * 1000: #If the cooldown is over and you shoot
                            SHOT.play()
                            cock_done = False

                            #Create a new bullet originating from the player's cannon
                            #x is the top left of the player, so adding with the width and dividing by 2 is middle
                            #Minus the bullet_width // 2 because otherwise top left of bullet is in the middle
                            bullet_x = player_x + player.get_width() // 2 - BULLET_WIDTH // 2
                            bullet_y = HEIGHT - 8 * YU

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
                            NO_AMMO.play()

                    #Powerups
                    powerup_name = None
                    powerup_remove_idx = None

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

                    if powerup_name is not None: #If a powerup actually got used, then call powerup_effect()
                        bullet_cooldown_time, enemies, shield_active, lives, kills, win, paused = powerup_effect(powerup_name, bullet_cooldown_time, copy_bullet_cooldown_time, enemies, lives, kills)

                        #Timed powerups for expiration
                        if powerup_name == 'ammo_regen':
                            ammo_regen_time_end = pygame.time.get_ticks() + AMMO_REGEN_EXPIRATION
                        elif powerup_name == 'shield':
                            shield_time_end = pygame.time.get_ticks() + SHIELD_EXPIRATION
                        elif powerup_name == 'slowtime':
                            slowtime_end = pygame.time.get_ticks() + SLOWTIME_EXPIRATION

                        #Remove the powerup from the collected powerups list
                        collected_powerups.pop(powerup_remove_idx)

        #This isn't inside of powerup_effect because it needs to be checked every frame, unlike the others
        if shield_active:
            for enemy in enemies:
                if enemy['y'] >= HEIGHT - 15 * YU - enemy['size'] * XU:
                    enemy['y'] = HEIGHT - 15 * YU - enemy['size'] * XU

        #Game logic updates only if not paused
        if not paused:
            keys = pygame.key.get_pressed() #For continuous input like movement
            current_time = pygame.time.get_ticks() #For time - based logic

            if current_time - last_shot_time > bullet_cooldown_time * 1000 and not cock_done:
                GUN_COCK.play()
                cock_done = True

            #Movement -  max min idea credit to a friend
            if (keys[pygame.K_a] or keys[pygame.K_LEFT]):
                player_x = max(LEFTWALL, player_x - player_speed)

            elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
                player_x = min(RIGHTWALL, player_x + player_speed)

            #Powerup Spawning
            if current_time - last_powerup_spawn_time > powerup_cooldown * 1000: #If the powerup_cooldown allows us to spawn a new powerup
                #Random coords within the range of below the half way line and in the arena
                powerup_x = random.randint(int(WIDTH // 3 + 40), int(WIDTH - 2 * XU - (2 * XU)))
                powerup_y = random.randint(int(HEIGHT // 2), int(HEIGHT - 13 * YU - (2 * XU)))

                powerup_index = random.randint(0, len(powerups) - 1)
                powerup = pygame.transform.scale(powerups[powerup_index], (2 * XU, 2 * XU))
                powerup_name = powerup_names[powerup_index]

                powerup_list.append({'image': powerup, 'x': powerup_x, 'y': powerup_y, 'name': powerup_name})
                last_powerup_spawn_time = current_time #Update last_powerup_spawn_time

            #Move bullets
            active_bullets = []
            for bullet in bullets:
                bullet['y'] -= bullet['speed'] #Move the bullet up
                if bullet['y'] + bullet['height'] > 0: #If bullet is still on screen
                    active_bullets.append(bullet)
            bullets = active_bullets #Removes unnecessary bullets that are off screen

            #Check if powerup effects should expire
            #ammo_regen
            if ammo_regen_time_end > 0 and current_time >= ammo_regen_time_end:
                bullet_cooldown_time = copy_bullet_cooldown_time #Revert to normal
                ammo_regen_time_end = 0 #Mark as inactive

            #Slowtime
            if slowtime_end > 0 and current_time >= slowtime_end:
                for enemy in enemies:
                    enemy['speed'] = enemy['speed'] * 2
                slowtime_end = 0 #Mark as inactive

            #Shield
            if shield_time_end > 0 and current_time >= shield_time_end:
                shield_active = False
                shield_time_end = 0 #Mark as inactive

            #Bullet - Powerup Collisions
            for powerup_data in powerup_list:
                for bullet in bullets:
                    #Create rects for collision
                    powerup_rect = pygame.Rect(powerup_data['x'], powerup_data['y'], 2 * XU, 2 * XU) #powerups are 2 * xu by 2 * xu
                    bullet_rect = pygame.Rect(bullet['x'], bullet['y'], bullet['width'], bullet['height'])

                    if powerup_rect.colliderect(bullet_rect):
                        if len(collected_powerups) < 4: #Make sure user doesn't have more than 4 powerups ever
                            collected_powerups.append(powerup_data) #Add the actual powerup dict
                        else: #If all the spots are filled, fill the new powerup in a random spot
                            collected_powerups[random.randint(0, 3)] = powerup_data
                        #Remove the bullet and powerup
                        bullets.remove(bullet)
                        powerup_list.remove(powerup_data)

        #Enemies
        if not paused and current_time - last_enemy_spawn_time > enemy_cooldown * 1000: #If it's time to spawn a new enemy
            enemy_x = random.choice(possible_x_pos) #Randomly choose x position from the dispensers
            enemy_type = random.choice(enemy_choice)

            current_spawn_speed = enemy_speed #Default speed
            if slowtime_end > 0 and current_time < slowtime_end:
                current_spawn_speed = enemy_speed / 2

            enemy = {'x' : enemy_x,
                     'y' : 8 * YU,
                     'type' : enemy_type,
                     'size' : 3,
                     'speed' : current_spawn_speed,
                     'health' : enemy_health(enemy_type)}

            enemies.append(enemy)
            last_enemy_spawn_time = current_time

        #Enemy - Bullet Collisions & Player Death
        enemies_to_keep = []
        for enemy in enemies:
            for bullet in bullets:
                #Create proper rects for collision
                enemy_rect = pygame.Rect(enemy['x'], enemy['y'], enemy['size'] * XU, enemy['size'] * XU)
                bullet_rect = pygame.Rect(bullet['x'], bullet['y'], bullet['width'], bullet['height'])

                if bullet_rect.colliderect(enemy_rect):
                    enemy['health'] -= 1
                    bullets.remove(bullet)
                    if enemy['health'] <= 0: #If the enemy died
                        kills += 1  #Increment kill count
                        #Add to dying_enemies list instead of removing from enemies directly
                        dying_enemies.append({'enemy_data': enemy, 'animation_start_time': current_time})

                        if kills >= 60:
                            win = True
                            paused = True

                        #Level Update (should happen when enemy is confirmed killed)
                        for lvl, requirement in LEVEL_REQUIREMENTS.items():
                            if kills >= requirement:
                                level = lvl

            if enemy['health'] > 0: #If enemy is still alive after bullet checks
                enemies_to_keep.append(enemy)
        enemies = enemies_to_keep

        #Enemy_death animations
        active_dying_enemies = []
        for dying_enemy_info in dying_enemies:
            if current_time - dying_enemy_info['animation_start_time'] <= DEATH_ANIMATION_DURATION: #If we should be animating the death
                active_dying_enemies.append(dying_enemy_info)
        dying_enemies = active_dying_enemies

        #For making sure that if one enemy reaches the bottom, you don't lose infinite health
        enemies_still_on_screen = []
        for enemy in enemies:
            if enemy['y'] >= HEIGHT: #If the enemy made it to the other end of the screen
                lives -= 1
                if lives <= 0: #If the player died
                    lose = True
                    paused = True
                #Removes it
            else:
                enemies_still_on_screen.append(enemy)
        enemies = enemies_still_on_screen

        #Level checks
        enemy_cooldown = LEVELED_INFO[level]['enemy_cooldown']
        player_speed = LEVELED_INFO[level]['player_speed']

        #Update base cooldown and apply ammo_regen if active
        new_base_cooldown = LEVELED_INFO[level]['bullet_cooldown']
        if copy_bullet_cooldown_time is not new_base_cooldown:
            copy_bullet_cooldown_time = new_base_cooldown #Update cooldown

        #Set the actual bullet_cooldown_time based on ammo_regen status and current base
        current_time_for_level_check = pygame.time.get_ticks()
        if ammo_regen_time_end > 0 and current_time_for_level_check < ammo_regen_time_end: #ammo_regen is active
            bullet_cooldown_time = copy_bullet_cooldown_time / 2
        else: #ammo_regen is not active or has just expired
            bullet_cooldown_time = copy_bullet_cooldown_time

        powerup_cooldown = LEVELED_INFO[level]['powerup_cooldown']
        powerups = LEVELED_INFO[level]['powerups']
        powerup_names = LEVELED_INFO[level]['powerup_names']
        enemy_choice = LEVELED_INFO[level]['enemy_choice']

        SURFACE.fill(BLUE) #Refill the screen for the next frame
        drawing_functions.draw_screen(player_x, bullets, powerup_list, collected_powerups, enemies, dying_enemies, paused, shield_active, lose, lives, level, kills, win) #Draws next frame

        pygame.display.update()
        clock.tick(60)

main()
