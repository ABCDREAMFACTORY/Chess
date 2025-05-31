import pygame
from Programs.Menu.menu import Menu
from Programs.Game.game import Menu_chess
# Import the Menu class from menu.py

import time
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Puissance 4 Menu")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)

font = pygame.font.Font("assets/NotoSans-Bold.ttf", SCREEN_WIDTH // 40)
# Create a font object for the title
current_menu =  Menu(screen,font, SCREEN_WIDTH, SCREEN_HEIGHT)# Initialize the current menu
# Initialize the menu

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        current_menu.handle_event(event)
        if current_menu.action is not None:  # Ensure action is not None before proceeding
            if current_menu.action == "Quitter": # Check if the quit action was triggered
                running = False
            elif current_menu.action == "Jouer seul":
                current_menu = Menu_chess(screen, font, SCREEN_WIDTH, SCREEN_HEIGHT)
                pass
            elif current_menu.action == "Jouer en lan":
                print("LAN mode selected")
            elif current_menu.action == "Options":
                print("Options mode selected")
                # You can implement an options menu here to allow the user to adjust settings like sound, difficulty, or controls.
            elif current_menu.action == "Retour":
                current_menu = Menu(screen,font, SCREEN_WIDTH, SCREEN_HEIGHT)

    # Draw the menu
    current_menu.load()
    if current_menu != "self":
        if current_menu.menu == "main":
            current_menu = Menu(screen,font, SCREEN_WIDTH, SCREEN_HEIGHT)
    # Update the display
    pygame.display.flip()

pygame.quit()