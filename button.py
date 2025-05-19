import pygame
class Button:
    def __init__(self,surface,x,y,width=0,height=0,color="white",text = None,text_color = (255,255,255),taille = 25,shape = "rectangle",radius = 0,action = None):
        self.shape = shape
        if shape == "rectangle":
            self.rect = pygame.Rect(x,y,width,height)
            self.rect.center = (x + width / 2, y + height / 2)
        elif shape == "circle":
            self.player_pos = pygame.Vector2(x,y)
            self.radius = radius
        self.color = color
        self.taille_text = pygame.font.Font(pygame.font.get_default_font(), taille)
        self.text = text
        self.text_render = self.taille_text.render(text, 1,text_color)
        self.surface = surface
        self.act = self.text if action == None else action
    def draw(self):
        if self.shape == "rectangle":
            pygame.draw.rect(self.surface,self.color,self.rect)
        elif self.shape == "circle":
            pygame.draw.circle(self.surface,self.color,self.player_pos,self.radius)
        if self.text != None:
            if self.shape == "rectangle":
                self.surface.blit(self.text_render,self.text_render.get_rect(center = self.rect.center))
            elif self.shape == "circle":
                self.surface.blit(self.text_render,self.text_render.get_rect(center = self.player_pos))
    def is_clicked(self,pos):
        if self.shape == "rectangle":
            if self.rect.collidepoint(pos):
                return True
        elif self.shape == "circle":
            if (pos[0] - self.player_pos.x) ** 2 + (pos[1] - self.player_pos.y) ** 2 <= self.radius ** 2:
                return True

        return False
    def change_color(self,color):
        self.color = color
    def action(self):
        return self.act