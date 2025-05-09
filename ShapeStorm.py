"""
Abheek Tuladhar
Period 4 HCP
HCP Final Project : ShapeStorm
Description: A game where you shoot down enemy shapes that fall from the sky
with numerous abilities and shapes while collecting power ups to survive and make it back to your home planet.
"""

import pygame, sys, random

pygame.init()
pygame.mixer.init()

WIDTH=1300
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

POWERUPS = [plague, slowtime, shield, ammoregen]

#Sounds
music = pygame.mixer.Sound("Audio/Music.mp3")
shot = pygame.mixer.Sound("Audio/shot.wav")
no_ammo = pygame.mixer.Sound("Audio/no_ammo.mp3")
gun_cock = pygame.mixer.Sound("Audio/gun_cock.wav")

music.play(-1)

#Bullet constants
BULLET_WIDTH = 10
BULLET_HEIGHT = 20
BULLET_SPEED = 20
BULLET_COOLDOWN_TIME = 0.8

def drawPlay():
    """
    Draws the play button

    Parameters:
    -----------
    None

    Returns:
    --------
    None
    """

    play = pygame.Rect(37*xu, 24*yu, 10*xu, 10*xu)
    pygame.draw.rect(surface, BROWN, play, 0)
    pygame.draw.polygon(surface, GOLD, [(39*xu, 26*yu), (39*xu, 37*yu), (46*xu, 31*yu)])

def drawDirectionEnemy(x, y, level):
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

    Returns:
    --------
    None
    """

    if level == 'easy':
        pygame.draw.rect(surface, GREEN, (x, y, 1.5*xu, 1.5*xu), 0)

        #Eyes
        pygame.draw.line(surface, BLACK, (x + 0.5*xu, y + 0.3*yu), (x + 0.5*xu, y + 1.0*yu), 1)
        pygame.draw.line(surface, BLACK, (x + 1.1*xu, y + 0.3*yu), (x + 1.1*xu, y + 1.0*yu), 1)

        #Draw Smile
        pygame.draw.arc(surface, BLACK, (x + 0.3*xu, y + 0.5*yu, xu, xu), 3.28, -0.14, 1)

    elif level == 'medium':
        pygame.draw.rect(surface, YELLOW, (x, y, 1.5*xu, 1.5*xu), 0)

        #Eyes
        pygame.draw.line(surface, BLACK, (x + 0.5*xu, y + 0.3*yu), (x + 0.5*xu, y + 1.0*yu), 1)
        pygame.draw.line(surface, BLACK, (x + 1.1*xu, y + 0.3*yu), (x + 1.1*xu, y + 1.0*yu), 1)

        #Draw Smile
        pygame.draw.line(surface, BLACK, (x+0.5*xu, y + 1.5*yu), (x + 1.1*xu, y + 1.5*yu), 1)

        #Draw Eye brows
        pygame.draw.line(surface, BLACK, (x+0.3*xu, y+0.2*yu), (x+0.7*xu, y+0.2*yu), 1)
        pygame.draw.line(surface, BLACK, (x+0.9*xu, y+0.2*yu), (x+1.3*xu, y+0.2*yu), 1)

    elif level == 'hard':
        pygame.draw.rect(surface, RED, (x, y, 1.5*xu, 1.5*xu), 0)

        #Eyes
        pygame.draw.line(surface, BLACK, (x + 0.5*xu, y + 0.5*yu), (x + 0.5*xu, y + 1.3*yu), 1)
        pygame.draw.line(surface, BLACK, (x + 1.1*xu, y + 0.5*yu), (x + 1.1*xu, y + 1.3*yu), 1)

        #Draw Smile
        pygame.draw.arc(surface, BLACK, (x + 0.3*xu, y + 0.5*yu, xu, xu), 3.28, -0.14, 1)

        #Draw Angry Eye brows
        pygame.draw.line(surface, BLACK, (x+0.8*xu, y+0.5*yu), (x+0.2*xu, y+0.1*yu), 1)
        pygame.draw.line(surface, BLACK, (x+0.8*xu, y+0.5*yu), (x+1.2*xu, y+0.1*yu), 1)

    elif level == 'insane':
        pygame.draw.rect(surface, PURPLE, (x, y, 1.5*xu, 1.5*xu), 0)

        #Eyes
        pygame.draw.line(surface, BLACK, (x + 0.5*xu, y + 0.5*yu), (x + 0.5*xu, y + 1.3*yu), 1)
        pygame.draw.line(surface, BLACK, (x + 1.1*xu, y + 0.5*yu), (x + 1.1*xu, y + 1.3*yu), 1)

        #Draw Smile
        pygame.draw.line(surface, BLACK, (x+0.5*xu, y + 1.6*yu), (x + 1.1*xu, y + 1.5*yu), 1)
        pygame.draw.arc(surface, BLACK, (x+0.5*xu, y + 0.9*yu, 0.6*xu, 0.8*xu), 3.28, -0.14, 1)

        #Draw Angry Eye brows
        pygame.draw.line(surface, BLACK, (x+0.8*xu, y+0.5*yu), (x+0.2*xu, y+0.1*yu), 1)
        pygame.draw.line(surface, BLACK, (x+0.8*xu, y+0.5*yu), (x+1.2*xu, y+0.1*yu), 1)


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

    show_message("Directions:", "Consolas", 40, 10*xu, 2* yu, GOLD)
    show_message("<-- --> : Movement", "Consolas", 30, 10*xu, 6*yu, GOLD)
    show_message(" A   D  : Movement", "Consolas", 30, 10*xu, 8*yu, GOLD)
    show_message("Space  : Shoot", "Consolas", 30, 9.2*xu, 10*yu, GOLD) #9.2 to allign the :

    drawDirectionLine(12*yu)

    surface.blit(pygame.transform.scale(plague, (30, 30)), (0, 13*yu)) #draw plague image
    show_message("Kill 50% of the enemies beyond half way line", "Consolas", 15, 10*xu, 14*yu, GOLD)

    surface.blit(pygame.transform.scale(slowtime, (30, 30)), (0, 15*yu)) #draw slowtime image
    show_message("Slow down the enemies for 3 seconds by 50%", "Consolas", 15, 10*xu, 16*yu, GOLD)

    surface.blit(pygame.transform.scale(shield, (30, 30)), (0, 17.5*yu)) #draw shield image
    show_message("Shield for 3 seconds", "Consolas", 15, 6*xu, 18.5*yu, GOLD)

    surface.blit(pygame.transform.scale(ammoregen, (30, 30)), (0, 20*yu)) #draw ammoregen image
    show_message("Reload speed reduced by 50% for 10 seconds", "Consolas", 15, 10*xu, 21*yu, GOLD)

    show_message("Powerups spawn below the line. Shoot them to collect", "Consolas", 15, 10.2*xu, 24*yu, GOLD)

    drawDirectionLine(25*yu)
    drawDirectionLine(25*yu, False, 8*yu)
    drawDirectionLine(29*yu)
    drawDirectionLine(33*yu)

    drawDirectionEnemy(5, 26*yu, 'easy')
    drawDirectionEnemy(5, 30*yu, 'medium')
    drawDirectionEnemy(10.8*xu, 26*yu, 'hard')
    drawDirectionEnemy(10.8*xu, 30*yu, 'insane')

    show_message("Easy", "Consolas", 20, 4*xu, 27*yu, GOLD)
    show_message("Medium", "Consolas", 20, 4*xu, 31*yu, GOLD)
    show_message("Hard", "Consolas", 20, 14*xu, 27*yu, GOLD)
    show_message("Insane", "Consolas", 20, 14*xu, 31*yu, GOLD)

    drawDirectionHeart(6*xu, 26.3*yu, 1)
    drawDirectionHeart(6*xu, 30.5*yu, 2)
    drawDirectionHeart(16*xu, 26.3*yu, 3)
    drawDirectionHeart(16*xu, 30.5*yu, 4)

    #Will do the attirubtes later
    surface.blit(pygame.transform.scale(rotation, (45, 45)), (5, 33.7*yu))
    show_message("Rotation & Speed", "Consolas", 15, 6*xu, 35*yu, GOLD)

    surface.blit(pygame.transform.scale(dodger, (40, 40)), (5, 37*yu))
    surface.blit(pygame.transform.scale(dash, (40, 40)), (35, 37*yu))
    show_message("Can blow air out to dodge bullets", "Consolas", 15, 10*xu, 38.5*yu, GOLD)

    surface.blit(pygame.transform.scale(bumper, (60, 15)), (5, 41*yu))
    show_message("Gains speed when hitting walls", "Consolas", 15, 9.5*xu, 41.5*yu, GOLD)

    surface.blit(pygame.transform.scale(teleport, (40, 40)), (5, 43*yu))
    show_message("Teleport to a random location behind themself", "Consolas", 15, 11*xu, 44.5*yu, GOLD)

    #Powerups:
    drawDirectionLine(47*yu)
    show_message("Powerups:", "Consolas", 40, 10*xu, 49*yu, GOLD)
    drawDirectionLine(51*yu)
    drawDirectionLine(51*yu, False, 11*yu)
    drawDirectionLine(57*yu)

    show_message("1", "Consolas", 30, 9.5*xu, 52.5*yu, GOLD)
    show_message("2", "Consolas", 30, 20*xu, 52.5*yu, GOLD)
    show_message("3", "Consolas", 30, 9.5*xu, 58.5*yu, GOLD)
    show_message("4", "Consolas", 30, 20*xu, 58.5*yu, GOLD)


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


def render_powerups(powerup_list):
    """
    Draws all powerups currently in the powerup_list onto the surface.
    """
    for powerup_data in powerup_list:
        surface.blit(powerup_data['image'], (powerup_data['x'], powerup_data['y']))


def drawScreen(x, current_bullets, powerup_list):
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

    Returns:
    --------
    None
    """

    drawDirections()

    #Draw Pause Button
    pause = pygame.Rect(58*xu, 0, 4*xu, 4*xu)
    pygame.draw.rect(surface, BROWN, pause, 0)
    pygame.draw.rect(surface, GOLD, [58.5*xu, 0.7*yu, xu, 3*xu], 0)
    pygame.draw.rect(surface, GOLD, [60.5*xu, 0.7*yu, xu, 3*xu], 0)

    #Draw Dispensers
    drawDispensers(25*xu)
    drawDispensers(34*xu)
    drawDispensers(43*xu)
    drawDispensers(52*xu)

    #Draw Player:
    surface.blit(player, (x, HEIGHT - 8*yu)) #draw player image

    #Draw Bullets:
    for bullet in current_bullets:
        pygame.draw.rect(surface, bullet['color'], (bullet['x'], bullet['y'], bullet['width'], bullet['height']))

    #Draw Powerups:
    render_powerups(powerup_list)



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
    x = 40*xu
    leftwall = WIDTH//3 + 10
    rightwall = WIDTH - player.get_width() - 5
    bullets = []
    last_shot_time = 0
    cock_done = False
    paused = False
    speed = 15
    powerup_list = []

    powerup_cooldown = 5
    last_powerup_spawn_time = 0

    while True:
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if ( event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE)): #end game
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if current_time - last_shot_time > BULLET_COOLDOWN_TIME * 1000:
                        shot.play()
                        cock_done = False

                        #Create a new bullet originating from the player's cannon
                        bullet_x = x + player.get_width() // 2 - BULLET_WIDTH // 2
                        bullet_y = HEIGHT - 8*yu

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

        if current_time - last_shot_time > BULLET_COOLDOWN_TIME * 1000 and not cock_done:
            gun_cock.play()
            cock_done = True

        #Movement
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and x > leftwall:
            x -= speed
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and x < rightwall:
            x += speed

        #Powerup Spawning
        if current_time - last_powerup_spawn_time > powerup_cooldown * 1000:
            powerup_x = random.randint(int(WIDTH//3 + 40), int(WIDTH - 2*xu - (2*xu))) #Make sure x allows full image width (2*xu)
            powerup_y = random.randint(int(HEIGHT//2), int(HEIGHT - 13*yu - (2*xu))) #Make sure y allows full image height (2*xu)

            powerup = random.choice(POWERUPS)
            powerup = pygame.transform.scale(powerup, (2*xu, 2*xu))

            powerup_list.append({'image': powerup, 'x': powerup_x, 'y': powerup_y})
            last_powerup_spawn_time = current_time

        surface.fill(BLUE)
        drawScreen(x, bullets, powerup_list)

        #Move bullets
        active_bullets = []
        for bullet in bullets:
            bullet['y'] -= bullet['speed']
            if bullet['y'] + bullet['height'] > 0: #If bullet is still on screen
                active_bullets.append(bullet)
        bullets = active_bullets

        pygame.display.update()

main()
