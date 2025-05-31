from Programs.Utilities.button import Button
import pygame
class Menu:
    def __init__(self, screen,font,SCREEN_WIDTH,SCREEN_HEIGHT):
        self.screen = screen
        self.title = font.render("Chess", True, "white")
        self.button_play = Button(screen, SCREEN_WIDTH / 2 - SCREEN_WIDTH / 10, SCREEN_HEIGHT * 0.3, SCREEN_WIDTH / 5, SCREEN_HEIGHT / 15, "white", "Jouer seul", (0, 0, 0))
        self.button_play_lan = Button(screen, SCREEN_WIDTH / 2 - SCREEN_WIDTH / 10, SCREEN_HEIGHT * 0.4, SCREEN_WIDTH / 5, SCREEN_HEIGHT / 15, "white", "Jouer en lan", (0, 0, 0), 20)
        self.button_option = Button(screen, SCREEN_WIDTH / 2 - SCREEN_WIDTH / 10, SCREEN_HEIGHT * 0.5, SCREEN_WIDTH / 5, SCREEN_HEIGHT / 15, "white", "Options", (0, 0, 0))
        self.button_quit = Button(screen, SCREEN_WIDTH / 2 - SCREEN_WIDTH / 10, SCREEN_HEIGHT * 0.6, SCREEN_WIDTH / 5, SCREEN_HEIGHT / 15, "white", "Quitter", (0, 0, 0))
        self.buttons = [self.button_play,self.button_play_lan,self.button_option,self.button_quit]
        self.menu = "main"  # Initialize the menu variable
        self.action = None  # Initialize the action variable
    def add_button(self, button):
        self.buttons.append(button)

    def load(self):
        self.screen.fill("black")
        self.screen.blit(self.title, (self.screen.get_width() / 2 - self.title.get_width() / 2, 0))
        for button in self.buttons:
            button.draw()


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for button in self.buttons:
                    if button.is_clicked(pygame.mouse.get_pos()):
                        self.action = button.action()  # Return the action of the clicked button

        return None  # No button was clicked