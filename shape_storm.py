"""
Abheek Tuladhar
Period 4 HCP
HCP Final Project : ShapeStorm
Description: A game where you shoot down enemy shapes that fall from the sky while collecting power ups to survive and make it back to your home planet.
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
POWERUPS1 = [ammo_regen] #1:0:0:0:0
POWERUPS2 = [ammo_regen, ammo_regen, ammo_regen, shield, shield, heart, heart, slowtime, slowtime, slowtime] #3:2:2:3:0
POWERUPS3 = [ammo_regen, ammo_regen, shield, shield, heart, heart, heart, slowtime, slowtime, slowtime, slowtime, plague] #2:2:3:4:1
POWERUPS4 = [ammo_regen, shield, heart, slowtime, plague, plague] #1:1:1:1:2
POWERUPS5 = [ammo_regen, shield, heart, heart, heart, slowtime, slowtime, plague, plague, plague, plague] #1:1:3:2:5

#There actual names for if statements because POWERUPS#is a image, not a string.
PNAMES1 = ['ammo_regen'] #Should be impossible to get powerups on level 1 with the 99 second wait, but just in case
PNAMES2 = ['ammo_regen', 'ammo_regen', 'ammo_regen', 'shield', 'shield', 'heart', 'heart', 'slowtime', 'slowtime', 'slowtime']
PNAMES3 = ['ammo_regen', 'ammo_regen', 'shield', 'shield', 'heart', 'heart', 'heart', 'slowtime', 'slowtime', 'slowtime', 'slowtime', 'plague']
PNAMES4 = ['ammo_regen', 'shield', 'heart', 'slowtime', 'plague', 'plague']
PNAMES5 = ['ammo_regen', 'shield', 'heart', 'heart', 'heart', 'slowtime', 'slowtime', 'plague', 'plague', 'plague', 'plague']

#Possible enemies per level
LEVEL1ENEMIES = ['easy', 'medium'] #Only easy and medium enemies
LEVEL2ENEMIES = ['easy', 'medium', 'medium', 'hard'] #Medium is more common. Hard is introduced
LEVEL3ENEMIES = ['medium', 'hard', 'hard', 'insane'] #Hard is more common. Insane is introduced
LEVEL4ENEMIES = ['medium', 'hard', 'hard', 'insane', 'insane', 'insane'] #Insane is more common
LEVEL5ENEMIES = ['hard', 'insane', 'insane', 'insane', 'insane', 'insane'] #Insane mostly

#The stats per level in a list of dictionaries
LEVELED_INFO = ['PLACEHOLDER SO INDECIES ARE CORRECT. THIS IS NONFUNCTIONAL INDEX 0',
                {'enemy_cooldown' : 4.0, 'player_speed' : 15, 'bullet_cooldown' : 1.0, 'powerup_cooldown' : 99, 'powerups' : POWERUPS1, 'powerup_names' : PNAMES1, 'enemy_choice' : LEVEL1ENEMIES},
                {'enemy_cooldown' : 3.0, 'player_speed' : 17, 'bullet_cooldown' : 0.9, 'powerup_cooldown' : 20, 'powerups' : POWERUPS2, 'powerup_names' : PNAMES2, 'enemy_choice' : LEVEL2ENEMIES},
                {'enemy_cooldown' : 3.5, 'player_speed' : 19, 'bullet_cooldown' : 0.8, 'powerup_cooldown' : 15, 'powerups' : POWERUPS3, 'powerup_names' : PNAMES3, 'enemy_choice' : LEVEL3ENEMIES},
                {'enemy_cooldown' : 2.0, 'player_speed' : 21, 'bullet_cooldown' : 0.7, 'powerup_cooldown' : 10, 'powerups' : POWERUPS4, 'powerup_names' : PNAMES4, 'enemy_choice' : LEVEL4ENEMIES},
                {'enemy_cooldown' : 1.5, 'player_speed' : 23, 'bullet_cooldown' : 0.6, 'powerup_cooldown' :  5, 'powerups' : POWERUPS5, 'powerup_names' : PNAMES5, 'enemy_choice' : LEVEL5ENEMIES}
                ]

powerups = LEVELED_INFO[1]['powerups']
powerup_names = LEVELED_INFO[1]['powerup_names']

#Sound Loading
MUSIC = pygame.mixer.Sound('Audio/music.mp3')
SHOT = pygame.mixer.Sound('Audio/shot.wav')
NO_AMMO = pygame.mixer.Sound('Audio/no_ammo.mp3')
GUN_COCK = pygame.mixer.Sound('Audio/gun_cock.wav')
LOSE = pygame.mixer.Sound('Audio/lose.mp3')
VICTORY = pygame.mixer.Sound('Audio/victory.mp3')
ENEMY_DEATH = pygame.mixer.Sound('Audio/Pop.mp3')
PAUSED = pygame.mixer.Sound('Audio/Paused.mp3')
COLLECT_POWERUP = pygame.mixer.Sound('Audio/Collect_powerups.mp3')
USE_POWERUP = pygame.mixer.Sound('Audio/Use_powerup.mp3')

#Background music plays on repeat
MUSIC.play(-1)

clock = pygame.time.Clock()


def powerup_effect(powerup_name, bullet_reload_time, enemies, lives, kills, dying_enemies, current_time, shield_active):
    """
    Applies the effect of the powerup to the player

    Parameters:
    -----------
    powerup_name : str
        The name of the powerup (e.g., 'ammo_regen')
    bullet_reload_time : float
        The player's normal, original bullet reload time
    enemies : list
        A list of enemy dictionaries filled with their stats.
    lives : int
        The number of lives the player has
    kills : int
        The number of enemies the player has killed
    dying_enemies : list
        A list of enemy dictionaries that are currently in their death animation.
    current_time : int
        The current game time in milliseconds, for timing the death animation.
    shield_active : bool
        Whether the shield powerup is currently active.

    Returns:
    --------
    bullet_reload_time : float
        The updated bullet_reload_time
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
    dying_enemies : list
        The updated list of dying_enemies.
    """

    win = False
    paused = False

    if powerup_name == 'plague':
        original_enemy_count = len(enemies)
        enemies_to_remove = []

        for enemy in enemies:
            if enemy['y'] >= HEIGHT // 2 - 3 * XU: #Below half way line including touching the half way line
                dying_enemies.append({'enemy_data': enemy, 'animation_start_time': current_time}) #Add to animation list
                enemies_to_remove.append(enemy)

        for enemy in enemies_to_remove:
            enemies.remove(enemy)

        num_killed_by_plague = original_enemy_count - len(enemies)
        kills += num_killed_by_plague

        if kills >= 60: #Check win condition after updating kills
            win = True
            MUSIC.stop()
            VICTORY.play(-1)
            paused = True

    elif powerup_name == 'shield':
        shield_active = True #This will be used to make a barrier of shield Images (Needs to be checked and drawn every frame so it's in main/drawing_functions.py)

    elif powerup_name == 'slowtime':
        for enemy in enemies:
            enemy['speed'] /= 2

    elif powerup_name == 'ammo_regen':
        bullet_reload_time /= 2

    elif powerup_name == 'heart':
        lives += 1

    return bullet_reload_time, enemies, shield_active, lives, kills, win, paused, dying_enemies


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


def pause_play_logic(PAUSE_BUTTON_HITBOX, mouse_pos, win, lose, PLAY_BUTTON_HITBOX, paused, last_shot_time, last_enemy_spawn_time, last_powerup_spawn_time, ammo_regen_time_end, slowtime_end, shield_time_end, time_at_pause_start):
    """
    Handles the logic for pausing and unpausing the game.

    Parameters:
    -----------
    PAUSE_BUTTON_HITBOX : pygame.Rect
        The hitbox for the pause button.
    mouse_pos : tuple
        The current (x, y) coordinates of the mouse.
    win : bool
        Whether the player has won the game.
    lose : bool
        Whether the player has lost the game.
    PLAY_BUTTON_HITBOX : pygame.Rect
        The hitbox for the play button (visible when paused).
    paused : bool
        The current pause state of the game.
    last_shot_time : int
        The timestamp of the last shot fired.
    last_enemy_spawn_time : int
        The timestamp of the last enemy spawn.
    last_powerup_spawn_time : int
        The timestamp of the last powerup spawn.
    ammo_regen_time_end : int
        The timestamp when the ammo regeneration powerup ends.
    slowtime_end : int
        The timestamp when the slow time powerup ends.
    shield_time_end : int
        The timestamp when the shield powerup ends.
    time_at_pause_start : int
        The timestamp when the game was paused.

    Returns:
    --------
    paused : bool
        The updated pause state of the game.
    last_enemy_spawn_time : int
        The updated timestamp of the last enemy spawn.
    last_shot_time : int
        The updated timestamp of the last shot fired.
    last_powerup_spawn_time : int
        The updated timestamp of the last powerup spawn.
    ammo_regen_time_end : int
        The updated timestamp for ammo regeneration end.
    slowtime_end : int
        The updated timestamp for slow time end.
    shield_time_end : int
        The updated timestamp for shield end.
    time_at_pause_start : int
        The updated timestamp for when the game was paused (0 if unpaused).
    """

    if not paused: #If game is running, check for pause click
        if PAUSE_BUTTON_HITBOX.collidepoint(mouse_pos) and not win: #If the user did hit the pause button
            paused = True
            MUSIC.stop()
            PAUSED.play(-1)
            time_at_pause_start = pygame.time.get_ticks() #Record time when pausing
    else: #If game is paused, check for the user hitting the play button
        if not lose and not win and PLAY_BUTTON_HITBOX.collidepoint(mouse_pos): #Only unpause if game isn't over
            paused = False
            PAUSED.stop()
            MUSIC.play(-1)
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

    return paused, last_enemy_spawn_time, last_shot_time, last_powerup_spawn_time, ammo_regen_time_end, slowtime_end, shield_time_end, time_at_pause_start


def shoot_logic(bullet_cooldown_time, player_x, BULLET_WIDTH, BULLET_HEIGHT, BULLET_SPEED, bullets, last_shot_time, cock_done):
    """
    Handles the logic for player shooting.

    Parameters:
    -----------
    bullet_cooldown_time : float
        The time (in seconds) required between shots.
    player_x : int
        The x-coordinate of the player.
    BULLET_WIDTH : int
        The width of the bullets.
    BULLET_HEIGHT : int
        The height of the bullets.
    BULLET_SPEED : int
        The speed of the bullets.
    bullets : list
        A list of active bullet dictionaries.
    last_shot_time : int
        The timestamp of the last shot fired.
    cock_done : bool
        Whether the gun cocking sound has played since the last shot.

    Returns:
    --------
    cock_done : bool
        The updated status of the gun cocking sound.
    last_shot_time : int
        The updated timestamp of the last shot fired.
    bullets : list
        The updated list of active bullet dictionaries.
    """

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

    return cock_done, last_shot_time, bullets


def powerup_logic(event, collected_powerups, AMMO_REGEN_EXPIRATION, SHIELD_EXPIRATION, SLOWTIME_EXPIRATION, bullet_cooldown_time, enemies, shield_active, lives, kills, win, paused, ammo_regen_time_end, slowtime_end, shield_time_end, dying_enemies, current_time):
    """
    Handles the activation of collected powerups based on key presses.

    Parameters:
    -----------
    event : pygame.event.Event
        The Pygame event object (specifically for key presses).
    collected_powerups : list
        A list of powerup dictionaries that the player has collected.
    AMMO_REGEN_EXPIRATION : int
        The duration (in milliseconds) of the ammo regeneration powerup.
    SHIELD_EXPIRATION : int
        The duration (in milliseconds) of the shield powerup.
    SLOWTIME_EXPIRATION : int
        The duration (in milliseconds) of the slow time powerup.
    bullet_cooldown_time : float
        The current bullet reload time.
    enemies : list
        A list of enemy dictionaries.
    shield_active : bool
        Whether the shield powerup is currently active.
    lives : int
        The player's current number of lives.
    kills : int
        The player's current number of kills.
    win : bool
        Whether the player has won the game.
    paused : bool
        Whether the game is currently paused.
    ammo_regen_time_end : int
        The timestamp when the ammo regeneration powerup ends.
    slowtime_end : int
        The timestamp when the slow time powerup ends.
    shield_time_end : int
        The timestamp when the shield powerup ends.
    dying_enemies : list
        A list of enemy dictionaries that are currently in their death animation.
    current_time : int
        The current game time in milliseconds.

    Returns:
    --------
    bullet_cooldown_time : float
        The updated bullet reload time.
    enemies : list
        The updated list of enemy dictionaries.
    shield_active : bool
        The updated status of the shield powerup.
    lives : int
        The updated number of lives the player has.
    kills : int
        The updated number of kills the player has.
    win : bool
        The updated status of the win condition.
    paused : bool
        The updated status of the pause state.
    ammo_regen_time_end : int
        The updated timestamp for ammo regeneration end.
    shield_time_end : int
        The updated timestamp for shield end.
    dying_enemies : list
        The updated list of dying_enemies.
    """

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
        USE_POWERUP.play()
        bullet_cooldown_time, enemies, shield_active, lives, kills, win, paused, dying_enemies = powerup_effect(powerup_name, bullet_cooldown_time, enemies, lives, kills, dying_enemies, current_time, shield_active)

        #Timed powerups for expiration
        if powerup_name == 'ammo_regen':
            ammo_regen_time_end = pygame.time.get_ticks() + AMMO_REGEN_EXPIRATION
        elif powerup_name == 'shield':
            shield_time_end = pygame.time.get_ticks() + SHIELD_EXPIRATION
        elif powerup_name == 'slowtime':
            slowtime_end = pygame.time.get_ticks() + SLOWTIME_EXPIRATION

        #Remove the powerup from the collected powerups list
        collected_powerups.pop(powerup_remove_idx)

    return bullet_cooldown_time, enemies, shield_active, lives, kills, win, paused, ammo_regen_time_end, slowtime_end, shield_time_end, dying_enemies


def powerup_spawning_logic(current_time, powerup_cooldown, powerup_list, last_powerup_spawn_time, level):
    """
    Handles the spawning of new powerups on the screen.

    Parameters:
    -----------
    current_time : int
        The current game time in milliseconds.
    powerup_cooldown : float
        The time (in seconds) between powerup spawns.
    powerup_list : list
        A list of active powerup dictionaries currently on screen.
    last_powerup_spawn_time : int
        The timestamp of the last powerup spawn.
    level : int
        The current game level.

    Returns:
    --------
    last_powerup_spawn_time : int
        The updated timestamp of the last powerup spawn.
    powerup_list : list
        The updated list of active powerup dictionaries.
    """

    if current_time - last_powerup_spawn_time > powerup_cooldown * 1000: #If the powerup_cooldown allows us to spawn a new powerup
        #Random coords within the range of below the half way line and in the arena
        powerup_x = random.randint(int(WIDTH // 3 + 40), int(WIDTH - 2 * XU - (2 * XU)))
        powerup_y = random.randint(int(HEIGHT // 2), int(HEIGHT - 13 * YU - (2 * XU)))

        powerups = LEVELED_INFO[level]['powerups']
        powerup_index = random.randint(0, len(powerups) - 1)
        powerup = pygame.transform.scale(powerups[powerup_index], (2 * XU, 2 * XU))
        powerup_name = LEVELED_INFO[level]['powerup_names'][powerup_index]

        powerup_list.append({'image': powerup, 'x': powerup_x, 'y': powerup_y, 'name': powerup_name})
        last_powerup_spawn_time = current_time #Update last_powerup_spawn_time

    return last_powerup_spawn_time, powerup_list


def move_bullets_logic(bullets):
    """
    Moves all active bullets up the screen and removes those that go off-screen.

    Parameters:
    -----------
    bullets : list
        A list of active bullet dictionaries.

    Returns:
    --------
    bullets : list
        The updated list of active bullet dictionaries.
    """

    active_bullets = []
    for bullet in bullets:
        bullet['y'] -= bullet['speed'] #Move the bullet up
        if bullet['y'] + bullet['height'] > 0: #If bullet is still on screen
            active_bullets.append(bullet)
    bullets = active_bullets #Removes unnecessary bullets that are off screen

    return bullets


def powerup_expiration_logic(current_time, level, enemies, ammo_regen_time_end, slowtime_end, shield_time_end, bullet_cooldown_time, shield_active):
    """
    Checks for and handles the expiration of active timed powerups.

    Parameters:
    -----------
    current_time : int
        The current game time in milliseconds.
    level : int
        The current game level.
    enemies : list
        A list of active enemy dictionaries.
    ammo_regen_time_end : int
        The timestamp when the ammo regeneration powerup ends.
    slowtime_end : int
        The timestamp when the slow time powerup ends.
    shield_time_end : int
        The timestamp when the shield powerup ends.
    bullet_cooldown_time : float
        The current bullet reload time.
    shield_active : bool
        Whether the shield powerup is currently active.

    Returns:
    --------
    bullet_cooldown_time : float
        The updated bullet reload time.
    shield_active : bool
        The updated status of the shield powerup.
    enemies : list of dicts
        The updated list of active enemy dictionaries.
    ammo_regen_time_end : int
        The updated timestamp for ammo regeneration end.
    slowtime_end : int
        The updated timestamp for slowtime end
    shield_time_end : int
        The updated timestamp for shield end.
    """

    #ammo_regen
    if ammo_regen_time_end > 0 and current_time >= ammo_regen_time_end:
        bullet_cooldown_time = LEVELED_INFO[level]['bullet_cooldown'] #Revert to normal
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

    return bullet_cooldown_time, shield_active, enemies, ammo_regen_time_end, slowtime_end, shield_time_end


def bullet_powerup_collisions(powerup_list, bullets, collected_powerups):
    """
    Checks for collisions between bullets and on-screen powerups.
    If a collision occurs, the powerup is collected (if space available) and both bullet and powerup are removed.

    Parameters:
    -----------
    powerup_list : list
        A list of powerup dictionaries currently on screen.
    bullets : list
        A list of active bullet dictionaries.
    collected_powerups : list
        A list of powerup dictionaries that the player has collected.

    Returns:
    --------
    bullets : list
        The updated list of active bullet dictionaries.
    collected_powerups : list
        The updated list of collected powerup dictionaries.
    powerup_list : list
        The updated list of on-screen powerup dictionaries.
    """

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
                COLLECT_POWERUP.play()
                bullets.remove(bullet)
                powerup_list.remove(powerup_data)

    return bullets, collected_powerups, powerup_list


def enemy_spawning(paused, current_time, enemy_cooldown, possible_x_pos, enemy_choice, enemy_speed, slowtime_end, enemies, last_enemy_spawn_time):
    """
    Spawns the enemies when the cooldown is over

    Parameters:
    -----------
    paused : bool
        If the game is paused or not
    current_time : int
        The current time in milliseconds
    enemy_cooldown : float
        The cooldown for enemy spawning
    possible_x_pos : list
        List of all the possible x positions the enemy can come from (The dispensers)
    enemy_choice : list
        A list showing which enemies can spawn from the level
    enemy_speed : int
        The speed of the enemy
    slowtime_end : float
        slowtime powerup ending times
    enemies : list of dicts
        Information on all the enemies on the screen
    last_enemy_spawn_time : float
        The last time an enemy was spawned

    Returns:
    --------
    enemies : list of dicts
        Updated information on the enemies
    last_enemy_spawn_time : float
        The updated time since the last enemy spawned
    """

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
                'health' : enemy_health(enemy_type)
                }

        enemies.append(enemy)
        last_enemy_spawn_time = current_time

    return enemies, last_enemy_spawn_time


def enemy_bullet_collisions(bullets, dying_enemies, current_time, LEVEL_REQUIREMENTS, enemies, kills, win, paused, level):
    """
    Removes bullets that hit enemies, removes enemies that have died, and updataes level

    Parameters:
    -----------
    bullets : list of dicts
        Information on all the bullets on the screen
    dying_enemies : list of dicts
        Information on all the dying enemies
    current_time : int
        The current time in milliseconds
    LEVEL_REQUIREMENTS : dict
        The required amount of kills to move to each level
    enemies : list of dicts
        Information on all the enemies on the screen
    kills : int
        The amount of kills the player has
    win : bool
        If the user has won or not
    paused : bool
        If the game is paused or not
    level : int
        The current level of the game

    Returns:
    --------
    enemies : list of dicts
        The updated information on all the enemies on the screen
    dying_enemies : list of dicts
        The updated information on all the dying enemies
    bullets : list of dicts
        The updated information on all the bullets on the screen
    win : bool
        Updated win boolean
    paused : bool
        Updated paused boolean
    level : int
        Updated level
    kills : int
        Updated amount of kills
    """

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
                    ENEMY_DEATH.play()

                    if kills >= 60:
                        win = True
                        MUSIC.stop()
                        PAUSED.stop()
                        VICTORY.play(-1)
                        paused = True

                    #Level Update (should happen when enemy is confirmed killed)
                    for lvl, requirement in LEVEL_REQUIREMENTS.items():
                        if kills >= requirement:
                            level = lvl

        if enemy['health'] > 0: #If enemy is still alive after bullet checks
            enemies_to_keep.append(enemy)
    enemies = enemies_to_keep

    return enemies, dying_enemies, bullets, win, paused, level, kills


def enemy_death_animations(current_time, DEATH_ANIMATION_DURATION, dying_enemies):
    """
    Useful for the enemy death animations (fireworks) in draw_functions.py

    Parameters:
    -----------
    current_time : int
        The current time in milliseconds
    DEATH_ANIMATION_DURATION : int
        The duration of the death animation in milliseconds
    dying_enemies : list of dicts
        Information on all the dying enemies

    Returns:
    --------
    dying_enemies : list of dicts
        The updated information on all the dying enemies
    """

    active_dying_enemies = []
    for dying_enemy_info in dying_enemies:
        if current_time - dying_enemy_info['animation_start_time'] <= DEATH_ANIMATION_DURATION: #If we should be animating the death
            active_dying_enemies.append(dying_enemy_info)
    dying_enemies = active_dying_enemies

    return dying_enemies


def removing_lives_logic(enemies, lives, lose, paused):
    """
    Removes lives from the player if an enemy reaches the other side of the arena

    Parameters:
    -----------
    enemies : list of dicts
        Information on all the enemies on the screen
    lives : int
        The amount of lives the player has
    lose : bool
        If the user has lost or not
    paused : bool
        If the game is paused or not

    Returns:
    --------
    enemies : list of dicts
        The updated information on all the enemies on the screen
    lives : int
        The updated amount of lives the player has
    lose : bool
        Updated user losing boolean
    paused : bool
        Updated because when player dies, game pauses
    """

    enemies_still_on_screen = []
    for enemy in enemies:
        if enemy['y'] >= HEIGHT: #If the enemy made it to the other end of the screen
            lives -= 1
            if lives <= 0: #If the player died
                lose = True
                MUSIC.stop()
                LOSE.play()
                paused = True
        #Removes it
        else:
            enemies_still_on_screen.append(enemy)
    enemies = enemies_still_on_screen

    return enemies, lives, lose, paused


def level_checks(level, ammo_regen_time_end, bullet_cooldown_time):
    """
    Updates level variables based on the current level and power-up status.

    Parameters:
    -----------
    level : int
        The current level of the game.
    ammo_regen_time_end : int
        The time (in milliseconds) when the ammo regen effect ends.
    bullet_cooldown_time : float
        The current cooldown time between player bullets.

    Returns:
    --------
    enemy_cooldown : float
        The cooldown time between enemy actions for the current level.
    player_speed : float
        The player's movement speed for the current level.
    bullet_cooldown_time : float
        The updated cooldown time between player bullets, adjusted for power-ups.
    powerup_cooldown : float
        The cooldown time between power-up spawns for the current level.
    enemy_choice : list
        The list of enemy types available for the current level.
    """

    enemy_cooldown = LEVELED_INFO[level]['enemy_cooldown']
    player_speed = LEVELED_INFO[level]['player_speed']

    #Update base cooldown and apply ammo_regen if active
    new_cooldown = LEVELED_INFO[level]['bullet_cooldown']
    if bullet_cooldown_time is not new_cooldown:
        bullet_cooldown_time = new_cooldown #Update cooldown

    #Set the actual bullet_cooldown_time based on ammo_regen status and current base
    current_time_for_level_check = pygame.time.get_ticks()
    if ammo_regen_time_end > 0 and current_time_for_level_check < ammo_regen_time_end: #ammo_regen is active
        bullet_cooldown_time /= 2
    else: #ammo_regen is not active or has just expired
        bullet_cooldown_time = LEVELED_INFO[level]['bullet_cooldown']

    powerup_cooldown = LEVELED_INFO[level]['powerup_cooldown']
    enemy_choice = LEVELED_INFO[level]['enemy_choice']

    return enemy_cooldown, player_speed, bullet_cooldown_time, powerup_cooldown, enemy_choice


def player_movement(keys, LEFTWALL, RIGHTWALL, player_speed, player_x):
    """
    Moves the player across the x axis

    Parameters:
    -----------
    keys : pygame.key.get_pressed()
        All the keys being pressed at that moment
    LEFTWALL : int
        The left wall of the arena
    RIGHTWALL : int
        The right wall of the arena
    player_speed : int
        The player's speed according to the level
    player_x : int
        The player's x position

    Returns:
    --------
    player_x : int
        The updated player's x position
    """

    if (keys[pygame.K_a] or keys[pygame.K_LEFT]):
        player_x = max(LEFTWALL, player_x - player_speed)

    elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
        player_x = min(RIGHTWALL, player_x + player_speed)

    return player_x


def game_variables():
    """
    Sets all the game variables

    Parameters:
    -----------
    None

    Returns:
    --------
    All of the game variables (there's too many for me to list)
    """

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

    #Powerup Variables
    powerup_list = []
    collected_powerups = []
    powerup_cooldown = 5
    last_powerup_spawn_time = 0
    ammo_regen_time_end = 0
    slowtime_end = 0
    shield_time_end = 0
    shield_active = False
    AMMO_REGEN_EXPIRATION = 5000 #5 seconds
    SLOWTIME_EXPIRATION = 5000 #5 seconds
    SHIELD_EXPIRATION = 3000 #3 seconds
    DEATH_ANIMATION_DURATION = 500 #0.5 seconds

    #Pause/Play Variables
    PAUSE_BUTTON_HITBOX = pygame.Rect(58.5 * XU, 0, 4 * XU, 4 * XU)
    PLAY_BUTTON_HITBOX = pygame.Rect(37 * XU, 24 * YU, 10 * XU, 10 * XU)
    #I didn't copy code from Gemini AI, however, I was stuck on how to adjust the current_time with the pausing
    #It gave me the idea of tracking how much time was spent in pause mode
    time_at_pause_start = 0
    current_time = 0

    #Level Variable
    LEVEL_REQUIREMENTS = {1: 0,
                          2: 5,
                          3: 15,
                          4: 30,
                          5: 50} #Kills needed for each level

    return player_x, player_speed, lives, kills, level, lose, win, LEFTWALL, RIGHTWALL, paused, last_enemy_spawn_time, enemy_speed, enemies, \
        dying_enemies, enemy_cooldown, enemy_choice, possible_x_pos, bullets, last_shot_time, cock_done, BULLET_WIDTH, \
        BULLET_HEIGHT, BULLET_SPEED, bullet_cooldown_time, powerup_list, collected_powerups, powerup_cooldown, \
        last_powerup_spawn_time, ammo_regen_time_end, slowtime_end, shield_time_end, shield_active, AMMO_REGEN_EXPIRATION, \
        SLOWTIME_EXPIRATION, SHIELD_EXPIRATION, DEATH_ANIMATION_DURATION, PLAY_BUTTON_HITBOX, PAUSE_BUTTON_HITBOX, time_at_pause_start, \
        current_time, LEVEL_REQUIREMENTS


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
    player_x, player_speed, lives, kills, level, lose, win, LEFTWALL, RIGHTWALL, paused, last_enemy_spawn_time, enemy_speed, enemies, dying_enemies, \
    enemy_cooldown, enemy_choice, possible_x_pos, bullets, last_shot_time, cock_done, BULLET_WIDTH, BULLET_HEIGHT, BULLET_SPEED, bullet_cooldown_time, \
    powerup_list, collected_powerups, powerup_cooldown, last_powerup_spawn_time, ammo_regen_time_end, slowtime_end, shield_time_end, shield_active, \
    AMMO_REGEN_EXPIRATION, SLOWTIME_EXPIRATION, SHIELD_EXPIRATION, DEATH_ANIMATION_DURATION, PLAY_BUTTON_HITBOX, PAUSE_BUTTON_HITBOX, time_at_pause_start, \
    current_time, LEVEL_REQUIREMENTS = game_variables()


    #Initial sound state for a fresh game (starts paused)
    MUSIC.stop()
    PAUSED.play(-1)

    #Game Loop!
    while True:
        mouse_pos = pygame.mouse.get_pos() #Mouse position for pausing/playing

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r: #Restart the game
                #Stop all potentially looping sounds before resetting variables
                MUSIC.stop()
                PAUSED.stop()
                VICTORY.stop()
                #LOSE.stop() #LOSE sound is short, not looped

                #Game Variables
                player_x, player_speed, lives, kills, level, lose, win, LEFTWALL, RIGHTWALL, paused, last_enemy_spawn_time, enemy_speed, enemies, dying_enemies, \
                enemy_cooldown, enemy_choice, possible_x_pos, bullets, last_shot_time, cock_done, BULLET_WIDTH, BULLET_HEIGHT, BULLET_SPEED, bullet_cooldown_time, \
                powerup_list, collected_powerups, powerup_cooldown, last_powerup_spawn_time, ammo_regen_time_end, slowtime_end, shield_time_end, shield_active, \
                AMMO_REGEN_EXPIRATION, SLOWTIME_EXPIRATION, SHIELD_EXPIRATION, DEATH_ANIMATION_DURATION, PLAY_BUTTON_HITBOX, PAUSE_BUTTON_HITBOX, time_at_pause_start, \
                current_time, LEVEL_REQUIREMENTS = game_variables()

                #Set sound for the new paused state (game restarts paused)
                PAUSED.play(-1)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                paused, last_enemy_spawn_time, last_shot_time, last_powerup_spawn_time, ammo_regen_time_end, slowtime_end, shield_time_end, time_at_pause_start = pause_play_logic(PAUSE_BUTTON_HITBOX, mouse_pos, win, lose, PLAY_BUTTON_HITBOX, paused, last_shot_time, last_enemy_spawn_time, last_powerup_spawn_time, ammo_regen_time_end, slowtime_end, shield_time_end, time_at_pause_start)

            #If not paused, continue as normal
            if not paused:
                if event.type == pygame.KEYDOWN: #If there's pretty much any input from user
                    if event.key == pygame.K_SPACE: #Shoot
                        cock_done, last_shot_time, bullets = shoot_logic(bullet_cooldown_time, player_x, BULLET_WIDTH, BULLET_HEIGHT, BULLET_SPEED, bullets, last_shot_time, cock_done)

                    #Powerups
                    bullet_cooldown_time, enemies, shield_active, lives, kills, win, paused, ammo_regen_time_end, slowtime_end, shield_time_end, dying_enemies = powerup_logic(event, collected_powerups, AMMO_REGEN_EXPIRATION, SHIELD_EXPIRATION, SLOWTIME_EXPIRATION, bullet_cooldown_time, enemies, shield_active, lives, kills, win, paused, ammo_regen_time_end, slowtime_end, shield_time_end, dying_enemies, current_time)

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
            player_x = player_movement(keys, LEFTWALL, RIGHTWALL, player_speed, player_x)

            #Powerup Spawning
            last_powerup_spawn_time, powerup_list = powerup_spawning_logic(current_time, powerup_cooldown, powerup_list, last_powerup_spawn_time, level)

            #Move bullets
            bullets = move_bullets_logic(bullets)

            #Check if powerup effects should expire
            bullet_cooldown_time, shield_active, enemies, ammo_regen_time_end, slowtime_end, shield_time_end = powerup_expiration_logic(current_time, level, enemies, ammo_regen_time_end, slowtime_end, shield_time_end, bullet_cooldown_time, shield_active)

            #Bullet - Powerup Collisions
            bullets, collected_powerups, powerup_list = bullet_powerup_collisions(powerup_list, bullets, collected_powerups)

        #Enemies
        enemies, last_enemy_spawn_time = enemy_spawning(paused, current_time, enemy_cooldown, possible_x_pos, enemy_choice, enemy_speed, slowtime_end, enemies, last_enemy_spawn_time)

        #Enemy - Bullet Collisions & Player Death/Win
        enemies, dying_enemies, bullets, win, paused, level, kills = enemy_bullet_collisions(bullets, dying_enemies, current_time, LEVEL_REQUIREMENTS, enemies, kills, win, paused, level)

        #Enemy_death animations
        dying_enemies = enemy_death_animations(current_time, DEATH_ANIMATION_DURATION, dying_enemies)

        #Removing Lives
        enemies, lives, lose, paused = removing_lives_logic(enemies, lives, lose, paused)

        #Level checks
        enemy_cooldown, player_speed, bullet_cooldown_time, powerup_cooldown, enemy_choice = level_checks(level, ammo_regen_time_end, bullet_cooldown_time)

        SURFACE.fill(BLUE) #Refill the screen for the next frame
        drawing_functions.draw_screen(player_x, bullets, powerup_list, collected_powerups, enemies, dying_enemies, paused, shield_active, lose, lives, level, kills, win) #Draws next frame

        pygame.display.update()
        clock.tick(20)

main()
