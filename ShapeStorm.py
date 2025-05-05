"""
Abheek Tuladhar
Period 4 HCP
HCP Final Project : ShapeStorm
Description: A game where you shoot down enemy shapes that fall from the sky
with numerous abilities and shapes while collecting power ups to survive and make it back to your home planet.
"""

import pygame, sys
pygame.init()

WIDTH=1300
HEIGHT=WIDTH*2/3

size=(WIDTH, HEIGHT)
surface = pygame.display.set_mode(size)

pygame.display.set_caption("ShapeStorm")

BLACK    = (0, 0, 0)
BROWN    = (145, 113, 76)
WHITE    = (255, 255, 255)
GOLD     = (255, 215, 0)
GREEN    = (0, 155, 0)
YELLOW   = (155, 155, 0)
RED      = (155, 0, 0)
PURPLE    = (155, 0, 155)

xu = WIDTH//60
yu = HEIGHT//60

plague = pygame.image.load("images/Plague.png").convert_alpha()
slowtime  = pygame.image.load("images/slowtime.png").convert_alpha()
shield = pygame.image.load("images/shield.png").convert_alpha()
ammoregen = pygame.image.load("images/ammoregen.png").convert_alpha()


def drawDirectionEnemy(x, y, level):
    if level == 'easy':
        pygame.draw.rect(surface, GREEN, (x, y, 1.5*xu, 1.5*xu), 0)
    elif level == 'medium':
        pygame.draw.rect(surface, YELLOW, (x, y, 1.5*xu, 1.5*xu), 0)
    elif level == 'hard':
        pygame.draw.rect(surface, RED, (x, y, 1.5*xu, 1.5*xu), 0)
    elif level == 'insane':
        pygame.draw.rect(surface, PURPLE, (x, y, 1.5*xu, 1.5*xu), 0)


def drawDirectionLine(y, horz = True, length = None):
    if horz:
        pygame.draw.line(surface, GOLD, [0, y], [1/3*WIDTH, y], 5)
    else:
        pygame.draw.line(surface, GOLD, [WIDTH * 1/6, y], [WIDTH * 1/6, y + length], 5)

def drawScreen():
    #Directions
    pygame.draw.rect(surface, BROWN, (0, 0, WIDTH * 1/3, HEIGHT))
    pygame.draw.line(surface, GOLD, (WIDTH * 1/3, HEIGHT//2), (WIDTH, HEIGHT//2), 5)
    drawDirectionLine(4*yu)

    show_message("Directions:", "Consolas", 40, 10*xu, 2* yu, GOLD)
    show_message("<-- --> : Movement", "Consolas", 30, 10*xu, 6*yu, GOLD)
    show_message(" A   D  : Movement", "Consolas", 30, 10*xu, 8*yu, GOLD)
    show_message("Space  : Shoot", "Consolas", 30, 9.2*xu, 10*yu, GOLD) #9.2 to allign the :

    drawDirectionLine(12*yu)

    surface.blit(pygame.transform.scale(plague, (65, 65)), (0, 13*yu)) #draw plague image
    show_message("Kill 50% of the enemies beyond half way line", "Consolas", 15, 12*xu, 15*yu, GOLD)

    surface.blit(pygame.transform.scale(slowtime, (65, 65)), (0, 17*yu)) #draw slowtime image
    show_message("Slow down the enemies for 3 seconds by 50%", "Consolas", 15, 11.6*xu, 19*yu, GOLD)

    surface.blit(pygame.transform.scale(shield, (65, 65)), (0, 22*yu)) #draw shield image
    show_message("Shield for 3 seconds", "Consolas", 15, 7.5*xu, 24*yu, GOLD)

    surface.blit(pygame.transform.scale(ammoregen, (65, 65)), (0, 27*yu)) #draw ammoregen image
    show_message("Reload speed reduced by 50% for 10 seconds", "Consolas", 15, 12*xu, 29*yu, GOLD)

    show_message("Powerups spawn below the half way line", "Consolas", 15, 10*xu, 33*yu, GOLD)

    drawDirectionLine(35*yu)
    drawDirectionLine(35*yu, False, 8*yu)
    drawDirectionLine(43*yu)
    drawDirectionLine(39*yu)

    drawDirectionEnemy(5, 36*yu, 'easy')
    drawDirectionEnemy(5, 40*yu, 'medium')
    drawDirectionEnemy(10.8*xu, 36*yu, 'hard')
    drawDirectionEnemy(10.8*xu, 40*yu, 'insane')



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
    while True:
        for event in pygame.event.get():
            if ( event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE)): #end game
                pygame.quit()
                sys.exit()

        surface.fill(WHITE)
        drawScreen()
        pygame.display.update()

main()
