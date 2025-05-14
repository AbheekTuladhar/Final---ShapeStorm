import pygame

pygame.init()
pygame.mixer.init()

WIDTH=1000
HEIGHT=WIDTH*2/3

size=(WIDTH, HEIGHT)
surface = pygame.display.set_mode(size)

pygame.display.set_caption("ShapeStorm")

BLACK    = (0, 0, 0)
BROWN    = (145, 113, 76)
WHITE    = (255, 255, 255)
GOLD     = (255, 215, 0)
GREEN    = (0, 200, 0)
YELLOW   = (200, 200, 0)
RED      = (200, 0, 0)
PURPLE   = (200, 0, 200)
BLUE     = (173, 216, 230)

xu = WIDTH//60
yu = HEIGHT//60

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

POWERUPS = [plague, shield, shield, slowtime, slowtime, slowtime, ammoregen, ammoregen, ammoregen, ammoregen] #Certain powerups are more common then others
POWERUP_NAMES = ['plague', 'shield', 'shield', 'slowtime', 'slowtime', 'slowtime', 'ammoregen', 'ammoregen', 'ammoregen', 'ammoregen']

#Sounds
music = pygame.mixer.Sound("Audio/Music.mp3")
shot = pygame.mixer.Sound("Audio/shot.wav")
no_ammo = pygame.mixer.Sound("Audio/no_ammo.mp3")
gun_cock = pygame.mixer.Sound("Audio/gun_cock.wav")


def drawPlay():
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

    play_rect = pygame.Rect(37*xu, 24*yu, 10*xu, 10*xu)

    pygame.draw.rect(surface, BROWN, play_rect, 0)
    pygame.draw.polygon(surface, GOLD, [(39*xu, 26*yu), (39*xu, 37*yu), (46*xu, 31*yu)])

    return play_rect


def drawEnemy(x, y, level, size):
    """
    Draws the enemies on the left side of the screen

    Parameters:
    -----------
    x : int
        The x-coordinate of the top left of the enemy.
    y : int
        The y-coordinate of the top left of the enemy.
    level : str
        The level of the enemy.
    size : float
        The size of the enemy

    Returns:
    --------
    None
    """

    if level == 'easy':
        pygame.draw.rect(surface, GREEN, (x, y, size*xu, size*xu), 0)

        #Eyes
        pygame.draw.line(surface, BLACK, (x + (size * (0.5/1.5))*xu, y + (size * (0.3/1.5))*yu), (x + (size * (0.5/1.5))*xu, y + (size * (1.0/1.5))*yu), 1)
        pygame.draw.line(surface, BLACK, (x + (size * (1.1/1.5))*xu, y + (size * (0.3/1.5))*yu), (x + (size * (1.1/1.5))*xu, y + (size * (1.0/1.5))*yu), 1)

        #Draw Smile
        pygame.draw.arc(surface, BLACK, (x + (size * 0.3/1.5)*xu, y + (size * 0.5/1.5)*yu, (size * xu * (1/1.5)), (size * xu * (1/1.5))), 3.28, -0.14, 1)

    elif level == 'medium':
        pygame.draw.rect(surface, YELLOW, (x, y, size*xu, size*xu), 0)

        #Eyes
        pygame.draw.line(surface, BLACK, (x + (size * 0.5/1.5)*xu, y + (size * 0.3/1.5)*yu), (x + (size * 0.5/1.5)*xu, y + (size * 1.0/1.5)*yu), 1)
        pygame.draw.line(surface, BLACK, (x + (size * 1.1/1.5)*xu, y + (size * 0.3/1.5)*yu), (x + (size * 1.1/1.5)*xu, y + (size * 1.0/1.5)*yu), 1)

        #Draw Smile
        pygame.draw.line(surface, BLACK, (x + (size * 0.5/1.5)*xu, y + (size * 1.5/1.5)*yu), (x + (size * 1.1/1.5)*xu, y + (size * 1.5/1.5)*yu), 1)

        #Draw Eye brows
        pygame.draw.line(surface, BLACK, (x + (size * 0.3/1.5)*xu, y + (size * 0.2/1.5)*yu), (x + (size * 0.7/1.5)*xu, y + (size * 0.2/1.5)*yu), 1)
        pygame.draw.line(surface, BLACK, (x + (size * 0.9/1.5)*xu, y + (size * 0.2/1.5)*yu), (x + (size * 1.3/1.5)*xu, y + (size * 0.2/1.5)*yu), 1)

    elif level == 'hard':
        pygame.draw.rect(surface, RED, (x, y, size*xu, size*xu), 0)

        #Eyes
        pygame.draw.line(surface, BLACK, (x + (size * 0.5/1.5)*xu, y + (size * 0.5/1.5)*yu), (x + (size * 0.5/1.5)*xu, y + (size * 1.3/1.5)*yu), 1)
        pygame.draw.line(surface, BLACK, (x + (size * 1.1/1.5)*xu, y + (size * 0.5/1.5)*yu), (x + (size * 1.1/1.5)*xu, y + (size * 1.3/1.5)*yu), 1)

        #Draw Smile
        pygame.draw.arc(surface, BLACK, (x + (size * 0.3/1.5)*xu, y + (size * 0.5/1.5)*yu, (size * xu * (1/1.5)), (size * xu * (1/1.5))), 3.28, -0.14, 1)

        #Draw Angry Eye brows
        pygame.draw.line(surface, BLACK, (x + (size * 0.8/1.5)*xu, y + (size * 0.5/1.5)*yu), (x + (size * 0.2/1.5)*xu, y + (size * 0.1/1.5)*yu), 1)
        pygame.draw.line(surface, BLACK, (x + (size * 0.8/1.5)*xu, y + (size * 0.5/1.5)*yu), (x + (size * 1.2/1.5)*xu, y + (size * 0.1/1.5)*yu), 1)

    elif level == 'insane':
        pygame.draw.rect(surface, PURPLE, (x, y, size*xu, size*xu), 0)

        #Eyes
        pygame.draw.line(surface, BLACK, (x + (size * 0.5/1.5)*xu, y + (size * 0.5/1.5)*yu), (x + (size * 0.5/1.5)*xu, y + (size * 1.3/1.5)*yu), 1)
        pygame.draw.line(surface, BLACK, (x + (size * 1.1/1.5)*xu, y + (size * 0.5/1.5)*yu), (x + (size * 1.1/1.5)*xu, y + (size * 1.3/1.5)*yu), 1)

        #Draw Smile
        pygame.draw.line(surface, BLACK, (x+(size * 0.5/1.5)*xu, y + (size * 1.6/1.5)*yu), (x + (size * 1.1/1.5)*xu, y + (size * 1.5/1.5)*yu), 1)
        pygame.draw.arc(surface, BLACK, (x + (size * 0.5/1.5)*xu, y + (size * 0.6/1.5)*yu, (size * xu * (0.8/1.5)), (size * xu * (1/1.5))), 3.28, -0.14, 1)

        #Draw Angry Eye brows
        pygame.draw.line(surface, BLACK, (x + (size * 0.8/1.5)*xu, y + (size * 0.5/1.5)*yu), (x + (size * 0.2/1.5)*xu, y + (size * 0.1/1.5)*yu), 1)
        pygame.draw.line(surface, BLACK, (x + (size * 0.8/1.5)*xu, y + (size * 0.5/1.5)*yu), (x + (size * 1.2/1.5)*xu, y + (size * 0.1/1.5)*yu), 1)


def drawDirectionLine(y, horz = True, length = None):
    """
    Draws the lines on the left side of the screen

    Parameters:
    -----------
    y : int
        The y-coordinate of the line.
    horz : bool, optional
        Whether the line is horizontal or vertical. Defaults to True.
    length : int, optional
        The length of the line. Defaults to None.

    Returns:
    --------
    None
    """

    if horz:
        pygame.draw.line(surface, GOLD, [0, y], [1/3*WIDTH, y], 5)
    else:
        pygame.draw.line(surface, GOLD, [WIDTH * 1/6, y], [WIDTH * 1/6, y + length], 5)


def drawDirectionHeart(x, y, amount):
    """
    Draws the hearts on the left side of the screen

    Parameters:
    -----------
    x : int
        The x-coordinate of the top left of the heart.
    y : int
        The y-coordinate of the top left of the heart.
    amount : int
        The number of hearts to draw.

    Returns:
    --------
    None
    """

    for i in range(amount):
        surface.blit(heart, (x+i*xu, y))


def drawDirections():
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
    pygame.draw.rect(surface, BROWN, (0, 0, WIDTH * 1/3, HEIGHT))
    pygame.draw.line(surface, GOLD, (WIDTH * 1/3, HEIGHT//2), (WIDTH, HEIGHT//2), 5)
    drawDirectionLine(4*yu)

    show_message("Directions:", "Consolas", 30, 10*xu, 2* yu, GOLD)
    show_message("<-- --> : Movement", "Consolas", 20, 10*xu, 6*yu, GOLD)
    show_message(" A   D  : Movement", "Consolas", 20, 10*xu, 8*yu, GOLD)
    show_message("Space  : Shoot", "Consolas", 20, 9.2*xu, 10*yu, GOLD) #9.2 to allign the :

    drawDirectionLine(12*yu)

    surface.blit(pygame.transform.scale(plague, (30, 30)), (0, 13*yu)) #draw plague image
    show_message("Kill 50% of the enemies beyond half way line", "Consolas", 10, 10.5*xu, 14.5*yu, GOLD)

    surface.blit(pygame.transform.scale(slowtime, (30, 30)), (0, 15*yu)) #draw slowtime image
    show_message("Slow down the enemies for 3 seconds by 50%", "Consolas", 10, 10*xu, 16.5*yu, GOLD)

    surface.blit(pygame.transform.scale(shield, (30, 30)), (0, 17.5*yu)) #draw shield image
    show_message("Shield for 3 seconds", "Consolas", 10, 6*xu, 19*yu, GOLD)

    surface.blit(pygame.transform.scale(ammoregen, (30, 30)), (0, 20*yu)) #draw ammoregen image
    show_message("Reload speed reduced by 50% for 10 seconds", "Consolas", 10, 10*xu, 21.5*yu, GOLD)

    show_message("Powerups spawn below the line. Shoot them to collect", "Consolas", 10, 10.2*xu, 24*yu, GOLD)

    drawDirectionLine(25*yu)
    drawDirectionLine(25*yu, False, 8*yu)
    drawDirectionLine(29*yu)
    drawDirectionLine(33*yu)

    drawEnemy(5, 26*yu, 'easy', 1.5)
    drawEnemy(5, 30*yu, 'medium', 1.5)
    drawEnemy(10.8*xu, 26*yu, 'hard', 1.5)
    drawEnemy(10.8*xu, 30*yu, 'insane', 1.5)

    show_message("Easy", "Consolas", 15, 4*xu, 27*yu, GOLD)
    show_message("Medium", "Consolas", 15, 4*xu, 31*yu, GOLD)
    show_message("Hard", "Consolas", 15, 14*xu, 27*yu, GOLD)
    show_message("Insane", "Consolas", 15, 14*xu, 31*yu, GOLD)

    drawDirectionHeart(6*xu, 26.3*yu, 1)
    drawDirectionHeart(6*xu, 30.5*yu, 2)
    drawDirectionHeart(16*xu, 26.3*yu, 3)
    drawDirectionHeart(16*xu, 30.5*yu, 4)

    #Will do the attirubtes later
    surface.blit(pygame.transform.scale(rotation, (35, 35)), (5, 33.7*yu))
    show_message("Rotation & Speed", "Consolas", 10, 6*xu, 35*yu, GOLD)

    surface.blit(pygame.transform.scale(dodger, (30, 30)), (5, 37*yu))
    surface.blit(pygame.transform.scale(dash, (30, 30)), (35, 37*yu))
    show_message("Can blow air out to dodge bullets", "Consolas", 10, 10*xu, 38.5*yu, GOLD)

    surface.blit(pygame.transform.scale(bumper, (40, 10)), (5, 41*yu))
    show_message("Gains speed when hitting walls", "Consolas", 10, 9.5*xu, 41.5*yu, GOLD)

    surface.blit(pygame.transform.scale(teleport, (35, 35)), (5, 43*yu))
    show_message("Teleport to a random location behind themself", "Consolas", 10, 11*xu, 44.5*yu, GOLD)

    #Powerups:
    drawDirectionLine(47*yu)
    show_message("Powerups:", "Consolas", 40, 10*xu, 49*yu, GOLD)
    drawDirectionLine(51*yu)
    drawDirectionLine(51*yu, False, 11*yu)
    drawDirectionLine(56*yu)

    show_message("1", "Consolas", 30, 9.5*xu, 52.5*yu, GOLD)
    show_message("2", "Consolas", 30, 20*xu, 52.5*yu, GOLD)
    show_message("3", "Consolas", 30, 9.5*xu, 57.5*yu, GOLD)
    show_message("4", "Consolas", 30, 20*xu, 57.5*yu, GOLD)


def drawDispensers(x):
    """
    Draws the dispensers on the screen

    Parameters:
    -----------
    x : int
        The x-coordinate of the top left of the dispenser.

    Returns:
    --------
    None
    """

    pygame.draw.rect(surface, BLACK, (x, 0, xu, 2*yu))
    pygame.draw.rect(surface, BLACK, (x-xu, 2*yu, 3*xu, 2*yu), 0)
    pygame.draw.rect(surface, BLACK, (x-2*xu, 4*yu, 5*xu, 4*yu), 0)


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


def drawScreen(x, current_bullets, powerup_list, collected_powerup_list):
    """
    Draws the screen with all the elements

    Parameters:
    -----------
    x : int
        The x-coordinate of the player
    current_bullets : list
        The list of current bullets on the screen
    powerup_list : list
        The list of active powerups on the screen.
    collected_powerup_list : list
        The list of collected powerups.

    Returns:
    --------
    None
    """

    drawDirections()

    #Draw Pause Button
    pause = pygame.Rect(58.5*xu, 0, 4*xu, 4*xu)
    pygame.draw.rect(surface, BROWN, pause, 0)
    pygame.draw.rect(surface, GOLD, [59*xu, 0.7*yu, xu, 3*xu], 0)
    pygame.draw.rect(surface, GOLD, [61*xu, 0.7*yu, xu, 3*xu], 0)

    #Draw Dispensers
    drawDispensers(25*xu)
    drawDispensers(34*xu)
    drawDispensers(43*xu)
    drawDispensers(52*xu)

    #Draw Player:
    surface.blit(player, (x, HEIGHT - 10*yu)) #draw player image

    #Draw Bullets:
    for bullet in current_bullets:
        pygame.draw.rect(surface, bullet['color'], (bullet['x'], bullet['y'], bullet['width'], bullet['height']))

    #Draw Powerups:
    draw_powerups(powerup_list)

    #Draw the collected powerups
    for powerup in collected_powerup_list:
        powerup['image'] = pygame.transform.scale(powerup['image'], (3*xu, 3*xu))

        if collected_powerup_list.index(powerup) == 0:
            surface.blit(powerup['image'], (3.5*xu, HEIGHT - 9.5*yu))
        elif collected_powerup_list.index(powerup) == 1:
            surface.blit(powerup['image'], (14*xu, HEIGHT - 9.5*yu))
        elif collected_powerup_list.index(powerup) == 2:
            surface.blit(powerup['image'], (3.5*xu, HEIGHT - 4.5*yu))
        elif collected_powerup_list.index(powerup) == 3:
            surface.blit(powerup['image'], (14*xu, HEIGHT - 4.5*yu))


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
        The x-coordinate of the center of the text.
    y : int
        The y-coordinate of the center of the text.
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

    if text_bounds.collidepoint(mouse_pos) and bg != None and hover:
        #Regenerate the image on hover
        text_image = font.render(words, True, bg, color) #swap bg and text color

    surface.blit(text_image, text_bounds) #render on screen

    return text_bounds #bounding box returned for collision detection
