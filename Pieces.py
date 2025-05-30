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
    def verif(self, board, y, x,jumper = None,verif_mat = False):
        list_move = []

        if self.color == "White":
            if verif_mat == False:
                # Avancer de 1
                if y - 1 >= 0 and board[y - 1][x] == None:
                    list_move.append((y - 1, x))
                    # Avancer de 2 si sur la ligne de départ
                    if y == 6 and board[y - 2][x] == None:
                        list_move.append((y - 2, x))
                # En passant
                if jumper is not None:
                    if (y,x+1) == jumper:
                        list_move.append((y - 1, x + 1))
                    if (y,x-1) == jumper:
                        list_move.append((y - 1, x - 1)) 
            # Capture gauche
            if y - 1 >= 0 and x - 1 >= 0:
                if board[y - 1][x - 1] != None and board[y - 1][x - 1].color == "Black" and verif_mat == False or verif_mat and board[y-1][x-1] is None or verif_mat and board[y-1][x-1].color == "White":
                    list_move.append((y - 1, x - 1))
            # Capture droite
            if y - 1 >= 0 and x + 1 <= 7:
                if board[y - 1][x + 1] != None and board[y - 1][x + 1].color == "Black" and verif_mat == False or verif_mat and board[y-1][x+1] is None or verif_mat and board[y-1][x+1].color == "White":
                    list_move.append((y - 1, x + 1))

        else:  # Black
            if verif_mat == False:
                if y + 1 <= 7 and board[y + 1][x] == None:
                    list_move.append((y + 1, x))
                    if y == 1 and board[y + 2][x] == None:
                        list_move.append((y + 2, x))
                if jumper is not None:
                    if (y,x+1) == jumper:
                        list_move.append((y + 1, x + 1))
                    if (y,x-1) == jumper:
                        list_move.append((y + 1, x - 1))
            if y + 1 <= 7 and x - 1 >= 0:
                if board[y + 1][x - 1] != None and board[y + 1][x - 1].color == "White" and verif_mat == False or verif_mat and board[y+1][x-1] is None or verif_mat and board[y+1][x-1].color == "Black":
                    list_move.append((y + 1, x - 1))
            if y + 1 <= 7 and x + 1 <= 7:
                if board[y + 1][x + 1] != None and board[y + 1][x + 1].color == "White" and verif_mat == False or verif_mat and board[y+1][x+1] is None or verif_mat and board[y+1][x+1].color == "Black":
                    list_move.append((y + 1, x + 1))

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
        self.moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
    def verif(self, board, y, x,verif_mat = False): 
        list_move = []
        # Déplacements possibles du cavalier
        for dy, dx in self.moves:
            new_y = y + dy
            new_x = x + dx
            if 0 <= new_y <= 7 and 0 <= new_x <= 7:
                if board[new_y][new_x] == None or board[new_y][new_x].color != self.color or verif_mat:
                    list_move.append((new_y, new_x))
        return list_move

class bishop:
    def __init__(self,color, screen):
        self.screen = screen
        self.color = color
        self.image = pygame.image.load(f"assets/Pieces/{color}_bishop.png").convert_alpha()
        diagonale = math.hypot(screen.get_width(), screen.get_height())
        self.image = pygame.transform.scale(self.image, (int(diagonale / 20),int(diagonale / 20)))
        self.rect = self.image.get_rect()
    def verif(self, board, y, x,verif_mat = False):
        list_move = []
        # Déplacements diagonaux
        for dy in range(-1, 2, 2):
            for dx in range(-1, 2, 2):
                new_y, new_x = y, x
                while True:
                    new_y += dy
                    new_x += dx
                    if 0 <= new_y <= 7 and 0 <= new_x <= 7:
                        if board[new_y][new_x] == None:
                            list_move.append((new_y, new_x))
                        elif verif_mat and board[new_y][new_x].color == self.color:
                            list_move.append((new_y, new_x))
                            break
                        elif verif_mat and isinstance(board[new_y][new_x],king) and board[new_y][new_x].color != self.color:
                            list_move.append((new_y,new_x))
                        elif board[new_y][new_x].color != self.color:
                            list_move.append((new_y, new_x))
                            break
                        else:
                            break
                    else:
                        break
        return list_move

class rook:
    def __init__(self,color, screen):
        self.screen = screen
        self.color = color
        self.image = pygame.image.load(f"assets/Pieces/{color}_tower.png").convert_alpha()
        diagonale = math.hypot(screen.get_width(), screen.get_height())
        self.image = pygame.transform.scale(self.image, (int(diagonale / 20),int(diagonale / 20)))
        self.rect = self.image.get_rect()
        self.has_rocked = False
    def verif(self, board, y, x,verif_mat = False):
        list_move = []
        # Déplacements verticaux et horizontaux
        for dy in range(-1, 2, 2):
                new_y, new_x = y, x
                while True:
                    new_y += dy
                    if 0 <= new_y <= 7 and 0 <= new_x <= 7:
                        if board[new_y][new_x] == None:
                            list_move.append((new_y, new_x))
                        elif verif_mat and board[new_y][new_x].color == self.color:
                            list_move.append((new_y, new_x))
                            break
                        elif verif_mat and isinstance(board[new_y][new_x],king) and board[new_y][new_x].color != self.color:
                            list_move.append((new_y,new_x))
                        elif board[new_y][new_x].color != self.color:
                            list_move.append((new_y, new_x))
                            break
                        else:
                            break
                    else:
                        break
        for dx in range(-1, 2, 2):
            new_y, new_x = y, x
            while True:
                new_x += dx
                if 0 <= new_y <= 7 and 0 <= new_x <= 7:
                    if board[new_y][new_x] == None:
                        list_move.append((new_y, new_x))
                    elif verif_mat and board[new_y][new_x].color == self.color:
                            list_move.append((new_y, new_x))
                            break
                    elif verif_mat and isinstance(board[new_y][new_x],king) and board[new_y][new_x].color != self.color:
                            list_move.append((new_y,new_x))
                    elif board[new_y][new_x].color != self.color:
                        list_move.append((new_y, new_x))
                        break
                    else:
                        break
                else:
                    break
        return list_move

class queen:
    def __init__(self,color, screen):
        self.screen = screen
        self.color = color
        self.image = pygame.image.load(f"assets/Pieces/{color}_queen.png").convert_alpha()
        diagonale = math.hypot(screen.get_width(), screen.get_height())
        self.image = pygame.transform.scale(self.image, (int(diagonale / 20),int(diagonale / 20)))
        self.rect = self.image.get_rect()
    def verif(self, board, y, x,verif_mat = False):
        list_move = []
        # Déplacements verticaux, horizontaux et diagonaux
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dy == 0 and dx == 0:
                    continue
                new_y, new_x = y, x
                while True:
                    new_y += dy
                    new_x += dx
                    if 0 <= new_y <= 7 and 0 <= new_x <= 7:
                        if board[new_y][new_x] == None:
                            list_move.append((new_y, new_x))
                        elif verif_mat and board[new_y][new_x].color == self.color:
                            list_move.append((new_y, new_x))
                            break
                        elif verif_mat and isinstance(board[new_y][new_x],king) and board[new_y][new_x].color != self.color:
                            list_move.append((new_y,new_x))
                        elif board[new_y][new_x].color != self.color:
                            list_move.append((new_y, new_x))
                            break
                        else:
                            break
                    else:
                        break
        return list_move
class king:
    def __init__(self,color, screen):
        self.screen = screen
        self.color = color
        self.image = pygame.image.load(f"assets/Pieces/{color}_king.png").convert_alpha()
        diagonale = math.hypot(screen.get_width(), screen.get_height())
        self.image = pygame.transform.scale(self.image, (int(diagonale / 20),int(diagonale / 20)))
        self.rect = self.image.get_rect()
        self.has_rocked = False
    def verif(self, board, y, x,verif_mat = False):
        list_move = []
        # Déplacements d'une case dans toutes les directions
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dy == 0 and dx == 0:
                    continue
                new_y = y + dy
                new_x = x + dx
                if 0 <= new_y <= 7 and 0 <= new_x <= 7:
                    if board[new_y][new_x] == None or board[new_y][new_x].color != self.color:
                        list_move.append((new_y, new_x))
        if verif_mat == False:
            list_move = self.verif_echec_mat(board,list_move)
            left,right = self.verif_roque(board,y,x)
            if left:
                list_move.append((y,x-2))
            if right:
                list_move.append((y,x+2))
        return list_move
    def verif_echec(self, board,pos,verif:bool=False):
        # Vérifie si le roi est en échec
        if verif:
            attaquant = None
        for i in range(8):
            for j in range(8):
                if board[i][j] is not None and board[i][j].color != self.color:
                    if isinstance(board[i][j], king):
                        if pos in board[i][j].verif(board, i, j,verif_mat=True) and verif is False:
                            return True
                                
                    else:
                        if pos in board[i][j].verif(board, i, j):
                            if verif is False:
                                return True
                            elif attaquant is None:
                                attaquant = (i,j)
                            else:
                                return True,True
        if verif is False:
            return False
        elif attaquant is None:
            return False,False
        else:
            return True,attaquant
    def verif_echec_mat(self, board,list_move):
        # Vérifie si le roi est en échec et mats
            for i in range(8):
                for j in range(8):
                    if board[i][j] is not None and board[i][j].color != self.color:
                        other_list_move = board[i][j].verif(board, i, j,verif_mat=True)
                        list_move_remove = []
                        for possible_move in list_move:
                            if possible_move in other_list_move:
                                list_move_remove.append(possible_move)
                                if len(list_move_remove) == len(list_move):
                                    return []
                        for move in list_move_remove:
                            list_move.remove(move)
            return list_move
    def verif_roque(self, board, y, x):
        # Vérifie si le roi peut roquer
        if self.has_rocked:
            return False,False
        left,right = False,False
        if self.verif_echec(board, (y,x)):
            return False,False
        if self.color == "White":
            if board[7][0] is not None and isinstance(board[7][0], rook) and not board[7][0].has_rocked and board[7][1] is None and board[7][2] is None and board[7][3] is None and not self.verif_echec(board, (7, 0)) and not self.verif_echec(board, (7, 1)) and not self.verif_echec(board, (7, 2)) and not self.verif_echec(board, (7, 3)):
                left = True
            if board[7][7] is not None and isinstance(board[7][7], rook) and not board[7][7].has_rocked and board[7][5] is None and board[7][6] is None and not self.verif_echec(board, (7, 7)) and not self.verif_echec(board, (7, 5)) and not self.verif_echec(board, (7, 6)):
                right = True

            return left,right
        else:
            if board[0][0] is not None and isinstance(board[0][0], rook) and not board[0][0].has_rocked and board[0][1] is None and board[0][2] is None and board[0][3] is None and not self.verif_echec(board, (0, 0)) and not self.verif_echec(board, (0, 1)) and not self.verif_echec(board, (0, 2)) and not self.verif_echec(board, (0, 3)):
                left = True
            if board[0][7] is not None and isinstance(board[0][7], rook) and not board[0][7].has_rocked and board[0][5] is None and board[0][6] is None and not self.verif_echec(board, (0, 7)) and not self.verif_echec(board, (0, 5)) and not self.verif_echec(board, (0, 6)):
                right = True
            return left,right