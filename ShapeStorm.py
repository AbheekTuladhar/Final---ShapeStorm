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

xu = WIDTH//60
yu = HEIGHT//60

def drawDirectionLine(y):
    pygame.draw.line(surface, GOLD, [0, y], [1/3*WIDTH, y], 5)

def drawScreen():
    pygame.draw.rect(surface, BROWN, (0, 0, WIDTH * 1/3, HEIGHT))
    drawDirectionLine(4*yu)

    show_message("Directions:", "Consolas", 40, 10*xu, 2* yu, GOLD)
    show_message("<-- --> : Movement", "Consolas", 30, 10*xu, 6*yu, GOLD)
    show_message(" A   D  : Movement", "Consolas", 30, 10*xu, 8*yu, GOLD)


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
