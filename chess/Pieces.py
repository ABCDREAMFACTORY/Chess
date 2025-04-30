import pygame
import math
class pawn:
    def __init__(self,color, screen):
        self.screen = screen
        self.color = color
        diagonale = math.hypot(screen.get_width(), screen.get_height())
        self.image = pygame.image.load(f"assets/Pieces/{color}_pawn.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(diagonale / 20),int(diagonale / 20)))
        self.rect = self.image.get_rect()
    def verif(self, board, y, x,jumper = None):
        list_move = []

        if self.color == "White":
            # Avancer de 1
            if y - 1 >= 0 and board[y - 1][x] == None:
                list_move.append((y - 1, x))
                # Avancer de 2 si sur la ligne de départ
                if y == 6 and board[y - 2][x] == None:
                    list_move.append((y - 2, x))
            # Capture gauche
            if y - 1 >= 0 and x - 1 >= 0:
                if board[y - 1][x - 1] != None and board[y - 1][x - 1].color == "Black":
                    list_move.append((y - 1, x - 1))
            # Capture droite
            if y - 1 >= 0 and x + 1 <= 7:
                if board[y - 1][x + 1] != None and board[y - 1][x + 1].color == "Black":
                    list_move.append((y - 1, x + 1))
            # En passant
            if jumper is not None:
                print("jumper",jumper)
                print("y,x",y,x)
                if (y,x+1) == jumper:
                    list_move.append((y - 1, x + 1))
                if (y,x-1) == jumper:
                    list_move.append((y - 1, x - 1)) 

        else:  # Black
            if y + 1 <= 7 and board[y + 1][x] == None:
                list_move.append((y + 1, x))
                if y == 1 and board[y + 2][x] == None:
                    list_move.append((y + 2, x))
            if y + 1 <= 7 and x - 1 >= 0:
                if board[y + 1][x - 1] != None and board[y + 1][x - 1].color == "White":
                    list_move.append((y + 1, x - 1))
            if y + 1 <= 7 and x + 1 <= 7:
                if board[y + 1][x + 1] != None and board[y + 1][x + 1].color == "White":
                    list_move.append((y + 1, x + 1))
            if jumper is not None:
                print("jumper",jumper)
                print("y,x",y,x)
                if (y,x+1) == jumper:
                    list_move.append((y + 1, x + 1))
                if (y,x-1) == jumper:
                    list_move.append((y + 1, x - 1))

        return list_move
    def has_jumped(self,y,y2):
        if self.color == "White":
            if y == 4 and y2 == 6:
                return True
        else:
            if y == 3 and y2 == 1:
                return True
    def upgrade(self,y):
        if self.color == "White":
            if y == 0:
                return True
        else:
            if y == 7:
                return True
        return False

        

class knight:
    def __init__(self,color, screen):
        self.screen = screen
        self.color = color
        self.image = pygame.image.load(f"assets/Pieces/{color}_knight.png").convert_alpha()
        diagonale = math.hypot(screen.get_width(), screen.get_height())
        self.image = pygame.transform.scale(self.image, (int(diagonale / 20),int(diagonale / 20)))
        self.rect = self.image.get_rect()

class bishop:
    def __init__(self,color, screen):
        self.screen = screen
        self.color = color
        self.image = pygame.image.load(f"assets/Pieces/{color}_bishop.png").convert_alpha()
        diagonale = math.hypot(screen.get_width(), screen.get_height())
        self.image = pygame.transform.scale(self.image, (int(diagonale / 20),int(diagonale / 20)))
        self.rect = self.image.get_rect()

class rook:
    def __init__(self,color, screen):
        self.screen = screen
        self.color = color
        self.image = pygame.image.load(f"assets/Pieces/{color}_tower.png").convert_alpha()
        diagonale = math.hypot(screen.get_width(), screen.get_height())
        self.image = pygame.transform.scale(self.image, (int(diagonale / 20),int(diagonale / 20)))
        self.rect = self.image.get_rect()

class queen:
    def __init__(self,color, screen):
        self.screen = screen
        self.color = color
        self.image = pygame.image.load(f"assets/Pieces/{color}_queen.png").convert_alpha()
        diagonale = math.hypot(screen.get_width(), screen.get_height())
        self.image = pygame.transform.scale(self.image, (int(diagonale / 20),int(diagonale / 20)))
        self.rect = self.image.get_rect()

class king:
    def __init__(self,color, screen):
        self.screen = screen
        self.color = color
        self.image = pygame.image.load(f"assets/Pieces/{color}_king.png").convert_alpha()
        diagonale = math.hypot(screen.get_width(), screen.get_height())
        self.image = pygame.transform.scale(self.image, (int(diagonale / 20),int(diagonale / 20)))
        self.rect = self.image.get_rect()
