"""
Abheek Tuladhar
Period 4 HCP
HCP Final Project : ShapeStorm
Description: All of the drawing code and functions
"""

try:
    import pygame
except ImportError:
    print('Please install the requirements.txt')
    exit()

pygame.init()
pygame.mixer.init()

WIDTH = 1000
HEIGHT = WIDTH * 2 / 3

size=(WIDTH, HEIGHT)
surface = pygame.display.set_mode(size)

pygame.display.set_caption('ShapeStorm')

BLACK = (0, 0, 0)
BROWN = (145, 113, 76)
GOLD = (255, 215, 0)
GREEN = (0, 200, 0)
YELLOW = (200, 200, 0)
RED = (200, 0, 0)
PURPLE = (200, 0, 200)
BLUE = (173, 216, 230)

XU = WIDTH // 60
YU = HEIGHT // 60

plague = pygame.image.load('Images/Plague.png').convert_alpha()
slowtime  = pygame.image.load('Images/slowtime.png').convert_alpha()
shield = pygame.image.load('Images/shield.png').convert_alpha()
ammo_regen = pygame.image.load('Images/ammo_regen.png').convert_alpha()
heart = pygame.image.load('Images/heart.png').convert_alpha()
heart = pygame.transform.scale(heart, (XU, XU))
player = pygame.image.load('Images/Player.png').convert_alpha()
player_x_scale = 80
player = pygame.transform.scale(player, (player_x_scale, player_x_scale * 1.25))

def draw_play():
    """
    Draws the play button

    Parameters:
    -----------
    None

    Returns:
    --------
    play_rect : pygame.Rect
        The rectangle representing the play button.
    """

    play_rect = pygame.Rect(37 * XU, 24 * YU, 10 * XU, 10 * XU)

    pygame.draw.rect(surface, BROWN, play_rect, 0)
    pygame.draw.polygon(surface, GOLD, [(39 * XU, 26 * YU), (39 * XU, 37 * YU), (46 * XU, 31 * YU)]) #The golden triangle

    return play_rect


def draw_enemy(x, y, level, size):
    """
    Draws the enemies on the left side of the screen

    Parameters:
    -----------
    x : int
        The x - coordinate of the top left of the enemy.
    y : int
        The y - coordinate of the top left of the enemy.
    level : str
        The level of the enemy.
    size : float
        The size of the enemy

    Returns:
    --------
    None
    """

    if level == 'easy':
        pygame.draw.rect(surface, GREEN, (x, y, size * XU, size * XU), 0)

        #Eyes
        pygame.draw.line(surface, BLACK, (x + (size * (0.5 / 1.5)) * XU, y + (size * (0.3 / 1.5)) * YU), (x + (size * (0.5 / 1.5)) * XU, y + (size * (1.0 / 1.5)) * YU), 1)
        pygame.draw.line(surface, BLACK, (x + (size * (1.1 / 1.5)) * XU, y + (size * (0.3 / 1.5)) * YU), (x + (size * (1.1 / 1.5)) * XU, y + (size * (1.0 / 1.5)) * YU), 1)

        #Draw Smile
        pygame.draw.arc(surface, BLACK, (x + (size * 0.3 / 1.5) * XU, y + (size * 0.5 / 1.5) * YU, (size * XU * (1 / 1.5)), (size * XU * (1 / 1.5))), 3.28,  - 0.14, 1)

    elif level == 'medium':
        pygame.draw.rect(surface, YELLOW, (x, y, size * XU, size * XU), 0)

        #Eyes
        pygame.draw.line(surface, BLACK, (x + (size * 0.5 / 1.5) * XU, y + (size * 0.3 / 1.5) * YU), (x + (size * 0.5 / 1.5) * XU, y + (size * 1.0 / 1.5) * YU), 1)
        pygame.draw.line(surface, BLACK, (x + (size * 1.1 / 1.5) * XU, y + (size * 0.3 / 1.5) * YU), (x + (size * 1.1 / 1.5) * XU, y + (size * 1.0 / 1.5) * YU), 1)

        #Draw Smile
        pygame.draw.line(surface, BLACK, (x + (size * 0.5 / 1.5) * XU, y + (size * 1.5 / 1.5) * YU), (x + (size * 1.1 / 1.5) * XU, y + (size * 1.5 / 1.5) * YU), 1)

        #Draw Eye brows
        pygame.draw.line(surface, BLACK, (x + (size * 0.3 / 1.5) * XU, y + (size * 0.2 / 1.5) * YU), (x + (size * 0.7 / 1.5) * XU, y + (size * 0.2 / 1.5) * YU), 1)
        pygame.draw.line(surface, BLACK, (x + (size * 0.9 / 1.5) * XU, y + (size * 0.2 / 1.5) * YU), (x + (size * 1.3 / 1.5) * XU, y + (size * 0.2 / 1.5) * YU), 1)

    elif level == 'hard':
        pygame.draw.rect(surface, RED, (x, y, size * XU, size * XU), 0)

        #Eyes
        pygame.draw.line(surface, BLACK, (x + (size * 0.5 / 1.5) * XU, y + (size * 0.5 / 1.5) * YU), (x + (size * 0.5 / 1.5) * XU, y + (size * 1.3 / 1.5) * YU), 1)
        pygame.draw.line(surface, BLACK, (x + (size * 1.1 / 1.5) * XU, y + (size * 0.5 / 1.5) * YU), (x + (size * 1.1 / 1.5) * XU, y + (size * 1.3 / 1.5) * YU), 1)

        #Draw Smile
        pygame.draw.arc(surface, BLACK, (x + (size * 0.3 / 1.5) * XU, y + (size * 0.5 / 1.5) * YU, (size * XU * (1 / 1.5)), (size * XU * (1 / 1.5))), 3.28,  - 0.14, 1)

        #Draw Angry Eye brows
        pygame.draw.line(surface, BLACK, (x + (size * 0.8 / 1.5) * XU, y + (size * 0.5 / 1.5) * YU), (x + (size * 0.2 / 1.5) * XU, y + (size * 0.1 / 1.5) * YU), 1)
        pygame.draw.line(surface, BLACK, (x + (size * 0.8 / 1.5) * XU, y + (size * 0.5 / 1.5) * YU), (x + (size * 1.2 / 1.5) * XU, y + (size * 0.1 / 1.5) * YU), 1)

    elif level == 'insane':
        pygame.draw.rect(surface, PURPLE, (x, y, size * XU, size * XU), 0)

        #Eyes
        pygame.draw.line(surface, BLACK, (x + (size * 0.5 / 1.5) * XU, y + (size * 0.5 / 1.5) * YU), (x + (size * 0.5 / 1.5) * XU, y + (size * 1.3 / 1.5) * YU), 1)
        pygame.draw.line(surface, BLACK, (x + (size * 1.1 / 1.5) * XU, y + (size * 0.5 / 1.5) * YU), (x + (size * 1.1 / 1.5) * XU, y + (size * 1.3 / 1.5) * YU), 1)

        #Draw Smile
        pygame.draw.line(surface, BLACK, (x + (size * 0.5 / 1.5) * XU, y + (size * 1.6 / 1.5) * YU), (x + (size * 1.1 / 1.5) * XU, y + (size * 1.5 / 1.5) * YU), 1)
        pygame.draw.arc(surface, BLACK, (x + (size * 0.5 / 1.5) * XU, y + (size * 0.6 / 1.5) * YU, (size * XU * (0.8 / 1.5)), (size * XU * (1 / 1.5))), 3.28,  - 0.14, 1)

        #Draw Angry Eye brows
        pygame.draw.line(surface, BLACK, (x + (size * 0.8 / 1.5) * XU, y + (size * 0.5 / 1.5) * YU), (x + (size * 0.2 / 1.5) * XU, y + (size * 0.1 / 1.5) * YU), 1)
        pygame.draw.line(surface, BLACK, (x + (size * 0.8 / 1.5) * XU, y + (size * 0.5 / 1.5) * YU), (x + (size * 1.2 / 1.5) * XU, y + (size * 0.1 / 1.5) * YU), 1)


def draw_direction_line(y, horz = True, length = None):
    """
    Draws the lines on the left side of the screen

    Parameters:
    -----------
    y : int
        The y - coordinate of the line.
    horz : bool, optional
        Whether the line is horizontal or vertical. Defaults to True.
    length : int, optional
        The length of the line. Defaults to None.

    Returns:
    --------
    None
    """

    if horz:
        pygame.draw.line(surface, GOLD, [0, y], [1 / 3 * WIDTH, y], 5)
    else:
        pygame.draw.line(surface, GOLD, [WIDTH * 1 / 6, y], [WIDTH * 1 / 6, y + length], 5)

def draw_direction_heart(x, y, amount):
    """
    Draws the hearts on the left side of the screen

    Parameters:
    -----------
    x : int
        The x - coordinate of the top left of the heart.
    y : int
        The y - coordinate of the top left of the heart.
    amount : int
        The number of hearts to draw.

    Returns:
    --------
    None
    """

    for i in range(amount):
        surface.blit(heart, (x + i * XU, y))


def draw_directions(level, kills):
    """
    Draws the directions on the left side of the screen

    Parameters:
    -----------
    None

    Returns:
    --------
    None
    """

    #Directions
    pygame.draw.rect(surface, BROWN, (0, 0, WIDTH * 1 / 3, HEIGHT))
    pygame.draw.line(surface, GOLD, (WIDTH * 1 / 3, HEIGHT // 2), (WIDTH, HEIGHT // 2), 5)
    draw_direction_line(4 * YU)

    show_message('Directions:', 'Consolas', 30, 10 * XU, 2 *  YU, GOLD)
    show_message('<----> : Movement', 'Consolas', 20, 10 * XU, 6 * YU, GOLD)
    show_message(' A   D  : Movement', 'Consolas', 20, 10 * XU, 8 * YU, GOLD)
    show_message('Space  : Shoot', 'Consolas', 20, 9.2 * XU, 10 * YU, GOLD) #9.2 to allign the :
    show_message('1, 2, 3, 4 : Powerups', 'Consolas', 20, 8.8 * XU, 11.7 * YU, GOLD)

    draw_direction_line(13 * YU)

    surface.blit(pygame.transform.scale(plague, (30, 30)), (0, 13 * YU)) #draw plague image
    show_message('Kill all enemies below half way line', 'Consolas', 10, 9 * XU, 14.5 * YU, GOLD)

    surface.blit(pygame.transform.scale(slowtime, (30, 30)), (0, 15 * YU)) #draw slowtime image
    show_message('Slow down the enemies for 3 seconds by 50%', 'Consolas', 10, 10 * XU, 16.5 * YU, GOLD)

    surface.blit(pygame.transform.scale(shield, (30, 30)), (0, 17.5 * YU)) #draw shield image
    show_message('Shield for 5 seconds', 'Consolas', 10, 6 * XU, 19 * YU, GOLD)

    surface.blit(pygame.transform.scale(ammo_regen, (30, 30)), (0, 20 * YU)) #draw ammo_regen image
    show_message('Reload cooldown reduced by 50% for 5 seconds', 'Consolas', 10, 10.7 * XU, 21.5 * YU, GOLD)

    surface.blit(pygame.transform.scale(heart, (30, 30)), (0, 22.3 * YU)) #draw heart image
    show_message('Gain +1 life', 'Consolas', 10, 4.5 * XU, 23.5 * YU, GOLD)

    show_message('Shoot powerups to collect', 'Consolas', 20, 10 * XU, 35 * YU, GOLD)
    show_message(f'Level: 0{level}', 'Consolas', 30, 11 * XU, 38 * YU, GOLD)

    if kills < 10:
        show_message(f'Kills: 0{kills}', 'Consolas', 30, 11 * XU, 41 * YU, GOLD)
    else:
        show_message(f'Kills: {kills}', 'Consolas', 30, 11 * XU, 41 * YU, GOLD)
    show_message('Goal: 60 Kills', 'Consolas', 30, 11 * XU, 44 * YU, GOLD)

    draw_direction_line(25 * YU)
    draw_direction_line(25 * YU, False, 8 * YU)
    draw_direction_line(29 * YU)
    draw_direction_line(33 * YU)

    draw_enemy(5, 26 * YU, 'easy', 1.5)
    draw_enemy(5, 30 * YU, 'medium', 1.5)
    draw_enemy(10.8 * XU, 26 * YU, 'hard', 1.5)
    draw_enemy(10.8 * XU, 30 * YU, 'insane', 1.5)

    show_message('Easy', 'Consolas', 15, 4 * XU, 27 * YU, GOLD)
    show_message('Medium', 'Consolas', 15, 4 * XU, 31 * YU, GOLD)
    show_message('Hard', 'Consolas', 15, 14 * XU, 27 * YU, GOLD)
    show_message('Insane', 'Consolas', 15, 14 * XU, 31 * YU, GOLD)

    draw_direction_heart(6 * XU, 26.3 * YU, 1)
    draw_direction_heart(6 * XU, 30.5 * YU, 2)
    draw_direction_heart(16 * XU, 26.3 * YU, 3)
    draw_direction_heart(16 * XU, 30.5 * YU, 4)

    #Powerups:
    draw_direction_line(47 * YU)
    show_message('Powerups:', 'Consolas', 40, 10 * XU, 49 * YU, GOLD)
    draw_direction_line(51 * YU)
    draw_direction_line(51 * YU, False, 11 * YU)
    draw_direction_line(56 * YU)

    show_message('1', 'Consolas', 30, 9.5 * XU, 52.5 * YU, GOLD)
    show_message('2', 'Consolas', 30, 20 * XU, 52.5 * YU, GOLD)
    show_message('3', 'Consolas', 30, 9.5 * XU, 57.5 * YU, GOLD)
    show_message('4', 'Consolas', 30, 20 * XU, 57.5 * YU, GOLD)


def draw_dispensers(x):
    """
    Draws the dispensers on the screen

    Parameters:
    -----------
    x : int
        The x - coordinate of the top left of the dispenser.

    Returns:
    --------
    None
    """

    pygame.draw.rect(surface, BLACK, (x, 0, XU, 2 * YU))
    pygame.draw.rect(surface, BLACK, (x - XU, 2 * YU, 3 * XU, 2 * YU), 0)
    pygame.draw.rect(surface, BLACK, (x - 2 * XU, 4 * YU, 5 * XU, 4 * YU), 0)

def draw_powerups(powerup_list):
    """
    Draws all powerups currently in the powerup_list onto the surface.

    Parameters:
    -----------
    powerup_list : list
        The list of powerups to be drawn.

    Returns:
    --------
    None
    """

    for powerup_data in powerup_list:
        surface.blit(powerup_data['image'], (powerup_data['x'], powerup_data['y']))

def enemy_death_animation(enemy):
    """
    Draws the enemy death animation (Like a firework)

    Parameters:
    -----------
    enemy : list of dict
        The enemy data containing its position, type, and other attributes.

    Returns:
    --------
    None
    """

    enemy_x = enemy['x']
    enemy_y = enemy['y']
    enemy_type = enemy['type']

    if enemy_type == 'easy':
        color = GREEN
    elif enemy_type == 'medium':
        color = YELLOW
    elif enemy_type == 'hard':
        color = RED
    elif enemy_type == 'insane':
        color = PURPLE

    pygame.draw.rect(surface, color, (enemy_x + 1.5 * XU, enemy_y - 1.5 * YU, 0.5 * YU, 1.5 * YU), 0) #Top Firework
    pygame.draw.rect(surface, color, (enemy_x + 1.5 * XU, enemy_y + 3 * XU, 0.5 * YU, 1.5 * YU), 0) #Bottom Firework
    pygame.draw.rect(surface, color, (enemy_x - 1.5 * XU, enemy_y + 1.5 * YU, 1.5 * XU, 0.5 * YU), 0) #Left Firework
    pygame.draw.rect(surface, color, (enemy_x + 3 * XU, enemy_y + 1.5 * YU, 1.5 * XU, 0.5 * YU), 0) #Right Firework


def draw_screen(shield_wall_x, current_bullets, powerup_list, collected_powerup_list, enemies, dying_enemies_list, paused, shield_active, lose, lives, level, kills, win):
    """
    Draws the screen with all the elements

    Parameters:
    -----------
    x : int
        The x - coordinate of the player
    current_bullets : list
        The list of current bullets on the screen
    powerup_list : list
        The list of active powerups on the screen.
    collected_powerup_list : list
        The list of collected powerups.
    enemies : list
        The list of enemies on the screen.
    dying_enemies_list : list
        The list of enemies currently undergoing death animation.
    paused : bool
        Whether the game is paused or not.
    shield_active : bool
        Whether the shield powerup is active or not.
    lose : bool
        Whether the player has lost or not.

    Returns:
    --------
    None
    """

    draw_directions(level, kills)

    #Draw Pause Button
    pause = pygame.Rect(58.5 * XU, 0, 4 * XU, 4 * XU)
    pygame.draw.rect(surface, BROWN, pause, 0)
    pygame.draw.rect(surface, GOLD, [59 * XU, 0.7 * YU, XU, 3 * XU], 0)
    pygame.draw.rect(surface, GOLD, [61 * XU, 0.7 * YU, XU, 3 * XU], 0)

    #Draw Dispensers at the top
    draw_dispensers(25 * XU)
    draw_dispensers(34 * XU)
    draw_dispensers(43 * XU)
    draw_dispensers(52 * XU)

    #Draw Player:
    surface.blit(player, (shield_wall_x, HEIGHT - 10 * YU)) #draw player image

    #Draw Player Health:
    surface.blit(pygame.transform.scale(heart, (2 * XU, 2 * XU)), (shield_wall_x, HEIGHT - 4.5 * YU))
    show_message(f'x{lives}', 'Consolas', 40, shield_wall_x + 3.5 * XU, HEIGHT - 3 * YU, GOLD)

    #Draw Bullets:
    for bullet in current_bullets:
        pygame.draw.rect(surface, bullet['color'], (bullet['x'], bullet['y'], bullet['width'], bullet['height']))

    #Draw Powerups:
    draw_powerups(powerup_list)

    #Draw the collected powerups
    for powerup in collected_powerup_list:
        powerup['image'] = pygame.transform.scale(powerup['image'], (3 * XU, 3 * XU))

        if collected_powerup_list.index(powerup) == 0:
            surface.blit(powerup['image'], (3.5 * XU, HEIGHT - 9.5 * YU))
        elif collected_powerup_list.index(powerup) == 1:
            surface.blit(powerup['image'], (14 * XU, HEIGHT - 9.5 * YU))
        elif collected_powerup_list.index(powerup) == 2:
            surface.blit(powerup['image'], (3.5 * XU, HEIGHT - 4.5 * YU))
        elif collected_powerup_list.index(powerup) == 3:
            surface.blit(powerup['image'], (14 * XU, HEIGHT - 4.5 * YU))

    #Draw enemies
    for enemy in enemies:
        draw_enemy(enemy['x'], enemy['y'], enemy['type'], enemy['size'])
        if not paused: #If game isn't paused, move enemy
            enemy['y'] += enemy['speed']

    #Draw enemy death animations
    for dying_enemy_info in dying_enemies_list:
        enemy_death_animation(dying_enemy_info['enemy_data']) #Pass the actual enemy data

    if shield_active: #If shield active, draw the shield wall
        shield_wall_x = WIDTH // 3
        for _ in range(45): #Draw 45 shields for the wall
            surface.blit(pygame.transform.scale(shield, (XU, XU)), (shield_wall_x, HEIGHT - 15 * YU))
            shield_wall_x += XU

    if lose:
        show_message('Game Over', 'Consolas', 60, 2 * WIDTH // 3, HEIGHT // 2, RED, BLACK)
        show_message('Press R to Restart', 'Consolas', 30, 2 * WIDTH // 3, HEIGHT // 2 + 35, RED, BLACK)

    if win:
        show_message('You Won!', 'Consolas', 60, 2 * WIDTH // 3, HEIGHT // 2, GREEN, BLACK)
        show_message('Press R to Restart', 'Consolas', 30, 2 * WIDTH // 3, HEIGHT // 2 + 35, GREEN, BLACK)

    if paused and not lose and not win: #Only draw play button if paused  * and not game over *
        draw_play()


def show_message(words, font_name, size, x, y, color, bg=None, hover=False):
    """
    Credit to programming mentor, Valerie Klosky

    Parameters:
    -----------
    words : str
        The text to be displayed.
    font_name : str
        The name of the font to use.
    size : int
        The size of the font.
    x : int
        The x - coordinate of the center of the text.
    y : int
        The y - coordinate of the center of the text.
    color : tuple
        The RGB color of the text.
    bg : tuple, optional
        The RGB background color of the text. Defaults to None.
    hover : bool, optional
        Whether to change the text color on hover. Defaults to False.

    Returns:
    --------
    text_bounds : Rect
        The bounding box of the text.
    """

    font = pygame.font.SysFont(font_name, size, True, False)
    text_image = font.render(words, True, color, bg)
    text_bounds = text_image.get_rect()  #bounding box of the text image
    text_bounds.center = (x, y)  #center text within the bounding box

    #find position of mouse pointer
    mouse_pos = pygame.mouse.get_pos()  #returns (x,y) of mouse location

    if text_bounds.collidepoint(mouse_pos) and bg is not None and hover:
        #Regenerate the image on hover
        text_image = font.render(words, True, bg, color) #swap bg and text color

    surface.blit(text_image, text_bounds) #render on screen

    return text_bounds #bounding box returned for collision detection
