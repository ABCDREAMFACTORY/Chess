from button import Button
from Pieces import pawn, knight, bishop, rook, queen, king
import pygame
import math
class Menu_chess:
    def __init__(self, screen , font, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.screen = screen
        self.font = font
        self.title = font.render("Chess",True,"white")
        button_quit = Button(screen, SCREEN_WIDTH-SCREEN_WIDTH/5,0, SCREEN_WIDTH / 5, SCREEN_HEIGHT / 15, "white", "Retour", (0, 0, 0))
        self.buttons = [button_quit]
        self.game = Chess(screen, font, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.menu = "self"
        self.action = None
        self.winner = None
    def load(self):
        self.screen.fill("black")
        self.screen.blit(self.title, (self.screen.get_width() / 2 - self.title.get_width() / 2, 0))
        if self.winner is not None:
            self.screen.blit(self.winner,(self.screen.get_width()/2-self.winner.get_width()/2,self.title.get_height()))
        for button in self.buttons:
            button.draw()
        for button in self.game.buttons:
            button.draw()
        
        self.game.game_load()

        self.end_of_game()
    def handle_event(self,event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.is_clicked(pygame.mouse.get_pos()):
                        self.action = button.action()

                if self.game.current_upgrade is None:
                    for button in self.game.buttons:
                        self.game.play(button)
                else:
                    for button in self.game.buttons_upgrade:
                        self.game.upgrade_play(button)
    def end_of_game(self):
        if self.game.winner is not None:
            self.winner = self.font.render(f"{self.game.winner} has winned",True,"White")


class Chess:
    def __init__(self, screen, font, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.screen = screen
        self.font = font
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.diagonale = math.hypot(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.title = font.render("Chess", True, "white")
        self.buttons = [Button(screen,SCREEN_WIDTH/2-4*int(self.diagonale/20)+j*(int(self.diagonale/20)), SCREEN_HEIGHT/10+i*(int(self.diagonale/20)), int(self.diagonale / 20), int(self.diagonale / 20),color ="#769656" if (i+j)%2 == 1 else "#EEEED2",action = (i,j)) for i in range(8) for j in range(8)]
        self.board = [[rook("Black", screen), knight("Black", screen), bishop("Black", screen), queen("Black", screen), king("Black", screen), bishop("Black", screen), knight("Black", screen), rook("Black", screen)],
                       [pawn("Black",screen) for _ in range(8)],
                       [None for _ in range(8)],
                       [None for _ in range(8)],
                       [None for _ in range(8)],
                       [None for _ in range(8)],
                       [pawn("White",screen) for _ in range(8)],
                        [rook("White", screen), knight("White", screen), bishop("White", screen), queen("White", screen), king("White", screen), bishop("White", screen), knight("White", screen), rook("White", screen)]]
        i = -1
        for row in self.board:
            i += 1
            j = -1
            for piece in row:
                j += 1
                if piece is not None:
                    piece.rect.x = self.buttons[i*8+j].rect.x
                    piece.rect.y = self.buttons[i*8+j].rect.y
        self.first_selection = None
        self.tour_actuelle = "White"
        self.list_actions = []
        self.possible_move = None

        self.pawn_jump = None #Pawn
        self.current_upgrade = None #Upgrade
        self.buttons_upgrade = [Button(screen, (SCREEN_WIDTH-SCREEN_WIDTH/8)+j*int(self.diagonale/20), SCREEN_HEIGHT/2-int(self.diagonale/20)+i*int(self.diagonale/20), int(self.diagonale / 20), int(self.diagonale / 20),color ="#769656" if (i+j)%2 == 1 else "#EEEED2",action= (i*2+j) ) for j in range(2) for i in range(2)] #Upgrade button
        self.buttons_upgrade_board = [queen("White",screen), knight("White",screen), bishop("White",screen), rook("White",screen)] #Upgrade pieces
        i = -1
        for piece in self.buttons_upgrade_board:
            i += 1
            if piece is not None:
                piece.rect.x = self.buttons_upgrade[i].rect.x
                piece.rect.y = self.buttons_upgrade[i].rect.y
        self.pos_white_king = [7,4]
        self.pos_black_king = [0,4]

        self.winner = None
    def draw_board(self):
        for row in self.board:
            for piece in row:
                if piece is not None:
                    self.screen.blit(piece.image, piece.rect)
    def game_load(self):
        self.draw_board()
        if self.current_upgrade is not None:
            self.upgrade()
    def play(self,button):
        if button.rect.collidepoint(pygame.mouse.get_pos()):
            if button.action() != None:
                i,j = button.action()
                print(i,j)
                if self.first_selection is not None and (i,j) == self.first_selection: #Annule le coup
                    self.buttons[i*8+j].color = "#769656" if (i+j)%2 == 1 else "#EEEED2"
                    for move in self.possible_move:
                        if self.list_actions != [] and (self.list_actions[-1][0][0],self.list_actions[-1][0][1]) == move:
                            self.buttons[move[0]*8+move[1]].color = "#ffa500"
                        elif self.list_actions != [] and (self.list_actions[-1][1][0],self.list_actions[-1][1][1]) == move:
                            self.buttons[move[0]*8+move[1]].color = "#a9ff9f"
                        else:
                            self.buttons[move[0]*8+move[1]].color = "#769656" if (move[0]+move[1])%2 == 1 else "#EEEED2"
                    self.first_selection = None
                    
                elif self.first_selection is None and self.board[i][j] is not None and self.board[i][j].color == self.tour_actuelle: #Premier click
                    self.first_selection = (i,j)
                    self.buttons[i*8+j].color = "#f6f669"

                    if not isinstance(self.board[i][j],king) and self.board[i][j] != None: #verification de la piece selectionnée
                        piece = self.board[i][j]
                        if isinstance(piece,pawn):
                            possible_move = piece.verif(self.board,i,j,self.pawn_jump) #verification des coups du pion
                        else:
                            possible_move = piece.verif(self.board,i,j)
                        self.board[i][j] = None #On retire la piece de la case pour verifier si le roi est en echec
                        possible_move_final = [] #Liste des coups possibles
                        for move in possible_move:
                            piece_ennemie = self.board[move[0]][move[1]] #On verifie si la case est occupée par une piece ennemie
                            self.board[move[0]][move[1]] = piece #On test une case possible
                            if self.tour_actuelle == "White":
                                t = self.board[self.pos_white_king[0]][self.pos_white_king[1]].verif_echec(self.board,(self.pos_white_king[0],self.pos_white_king[1]))
                                print(t)
                            else:
                                t = self.board[self.pos_black_king[0]][self.pos_black_king[1]].verif_echec(self.board,(self.pos_black_king[0],self.pos_black_king[1]))
                                print(t)
                                self.board[i][j] = piece
                            self.board[move[0]][move[1]] = piece_ennemie #On remet la piece ennemie sur la case
                            if t != True:
                                possible_move_final.append(move) #On retire le coup si le roi est en echec
                        print(possible_move_final)
                        self.board[i][j] = piece #On remet la piece sur la case
                    else:
                        if self.board[i][j] != None:
                            possible_move_final = self.board[i][j].verif(self.board,i,j)
                    self.possible_move = possible_move_final #On stocke les coups possibles
                    if self.possible_move != []:
                        for move in self.possible_move:
                            self.buttons[move[0]*8+move[1]].color = "#00FF00"


                elif self.first_selection is not None and self.board[i][j] is not None and self.board[i][j].color != self.tour_actuelle or self.board[i][j] is None and self.first_selection is not None and self.first_selection != (i,j):
                    #Deuxieme selection

                    if self.possible_move != []:  #Remet les couleurs d'origine
                        for move in self.possible_move:
                            self.buttons[move[0]*8+move[1]].color = "#769656" if (move[0]+move[1])%2 == 1 else "#EEEED2"
                    
                    self.list_actions.append(((self.first_selection[0],self.first_selection[1]),(i,j))) #ajout de l'action dans la liste des coups

                    self.board[self.first_selection[0]][self.first_selection[1]], self.board[i][j] = None, self.board[self.first_selection[0]][self.first_selection[1]]
                    self.board[i][j].rect.x = self.buttons[i*8+j].rect.x #deplacement de la piece
                    self.board[i][j].rect.y = self.buttons[i*8+j].rect.y #deplacement de la piece
                    #Joue le coup

                    if isinstance(self.board[i][j],(king,rook)):
                        if self.board[i][j].has_rocked == False:
                            self.board[i][j].has_rocked = True #On verifie si la piece a bougé

                    if isinstance(self.board[i][j],king):
                        if self.board[i][j].color == "White":
                            self.pos_white_king = [i,j]
                        else:
                            self.pos_black_king = [i,j]
                        if abs(self.first_selection[1]-j) == 2: #Roque
                            if self.first_selection[1] < j: #Roque à droite
                                self.board[i][7],self.board[i][5] = None, self.board[i][7]
                                self.board[i][5].rect.x = self.buttons[i*8+5].rect.x #deplacement de la piece
                                self.board[i][5].rect.y = self.buttons[i*8+5].rect.y #deplacement de la piece
                            else: #Roque à gauche
                                self.board[i][0],self.board[i][3] = None, self.board[i][0]
                                self.board[i][3].rect.x = self.buttons[i*8+3].rect.x #deplacement de la piece
                                self.board[i][3].rect.y = self.buttons[i*8+3].rect.y#deplacement de la piece

                    self.tour_actuelle = "Black" if self.tour_actuelle == "White" else "White" #change le tour


                    self.buttons[self.first_selection[0]*8+self.first_selection[1]].color = "#ffa500" ##Change les couleurs des cases qui ont été jouées
                    self.buttons[i*8+j].color = "#a9ff9f"


                    if len(self.list_actions) > 1:
                        self.buttons[self.list_actions[-2][0][0]*8+self.list_actions[-2][0][1]].color = "#769656" if (self.list_actions[-2][0][0]+self.list_actions[-2][0][1])%2 == 1 else "#EEEED2"
                        self.buttons[self.list_actions[-2][1][0]*8+self.list_actions[-2][1][1]].color = "#769656" if (self.list_actions[-2][1][0]+self.list_actions[-2][1][1])%2 == 1 else "#EEEED2"
                    
                
                    if isinstance(self.board[i][j],pawn): #cas particuliers du pion
                        if self.pawn_jump != None: #verification du saut du pion
                            if self.board[i][j].color == "White" and i > 0 and i + 1 == self.pawn_jump[0] and j == self.pawn_jump[1]:
                                self.board[i+1][j] = None
                            elif self.board[i][j].color == "Black" and i < 7 and i - 1 == self.pawn_jump[0] and j == self.pawn_jump[1]:
                                self.board[i-1][j] = None
                            else:
                                print(i-1,j,self.pawn_jump)
                                print(i+1,j,self.pawn_jump)

                        if self.board[i][j].has_jumped(i,self.first_selection[0]) == True: #verification du saut du pion
                            self.pawn_jump = (i,j)
                        else:
                            self.pawn_jump = None
                        if self.board[i][j].upgrade(i) == True:
                            self.current_upgrade = (i,j)
                            for piece in self.buttons_upgrade_board:
                                piece.__init__("White" if self.tour_actuelle == "Black" else "Black",self.screen)
                                i = -1
                                for piece in self.buttons_upgrade_board:
                                    i += 1
                                    if piece is not None:
                                        piece.rect.x = self.buttons_upgrade[i].rect.x
                                        piece.rect.y = self.buttons_upgrade[i].rect.y

                    if self.tour_actuelle == "White": #Vérification d'echec et mat
                        mat =self.verif_echec_mat(self.pos_white_king)
                    else:
                        mat = self.verif_echec_mat(self.pos_black_king)
                    if mat:
                        self.winner = "Black" if self.tour_actuelle == "White" else "White"
                        print("Echec et mat")
                    else:
                        print("continue")
                    self.first_selection = None
    def verif_echec_mat(self,pos_king):
        is_attacked,attaqueur =self.board[pos_king[0]][pos_king[1]].verif_echec(self.board,(pos_king[0],pos_king[1]),verif=True)
        if is_attacked:
            print("Echec !")
            list_coup = self.board[pos_king[0]][pos_king[1]].verif_echec_mat(self.board,(self.board[pos_king[0]][pos_king[1]].verif(self.board,pos_king[0],pos_king[1])))
            if list_coup == []:
                if attaqueur is True:
                    return True
                else:
                    print("possible echec et mat")
                    print(attaqueur)
                    for i in range(8):
                        for j in range(8):
                            if self.board[i][j] is not None and self.board[i][j].color == self.tour_actuelle:
                                #if isinstance(self.board[i][j], king):
                                    #if attaqueur in self.board[i][j].verif(self.board, i, j,verif_mat=True):
                                    #    print("peux se faire attaquer par",(i,j))
                                     #   #vérifier que attaqueur n'est pas défendu
                                      #  for k in range(8):
                                       ##     for l in range(8):
                                         #       if self.board[k][l] is not None and self.board[k][l].color != self.tour_actuelle:
                                          #          if isinstance(self.board[i][j], king):
                                           #             if attaqueur in self.board[i][j].verif(self.board,i,j,verif_mat=True):
                                            #                print("ne peux en faite pas (roi)")
                                             #               
                                              #      else:
                                               #         if attaqueur in self.board[i][j].verif(self.board,i,j,verif_mat=True):
                                                #            print("ne peux en faite pas")

                                #else:
                                if not isinstance(self.board[i][j],king):
                                    if attaqueur in self.board[i][j].verif(self.board, i, j):
                                        print("peux se faire attaquer par",(i,j))
                                        #verifier que le roi ne se fait pas attaquer en prenant l'attaqueur
                                        attaqueur_class = self.board[attaqueur[0]][attaqueur[1]]
                                        self.board[attaqueur[0]][attaqueur[1]] = self.board[i][j]
                                        self.board[i][j] = None
                                        if self.board[pos_king[0]][pos_king[1]].verif_echec(self.board,(pos_king[0],pos_king[1])):
                                            print("Ne peux en faite pas")
                                        else:
                                            print("Le peux vraiment")
                                            self.board[i][j] = self.board[attaqueur[0]][attaqueur[1]]
                                            self.board[attaqueur[0]][attaqueur[1]] = attaqueur_class
                                            return False
                                        self.board[i][j] = self.board[attaqueur[0]][attaqueur[1]]
                                        self.board[attaqueur[0]][attaqueur[1]] = attaqueur_class
                    return True
            else: return False

    def upgrade(self):
        for button in self.buttons_upgrade:
            button.draw()
        for piece in self.buttons_upgrade_board:
            if piece is not None:
                self.screen.blit(piece.image, piece.rect)

    def upgrade_play(self,button):
        if button.rect.collidepoint(pygame.mouse.get_pos()):
            piece = button.action()
            self.board[self.current_upgrade[0]][self.current_upgrade[1]] = self.buttons_upgrade_board[piece]
            self.board[self.current_upgrade[0]][self.current_upgrade[1]].rect.x = self.buttons[self.current_upgrade[0]*8+self.current_upgrade[1]].rect.x #deplacement de la piece
            self.board[self.current_upgrade[0]][self.current_upgrade[1]].rect.y = self.buttons[self.current_upgrade[0]*8+self.current_upgrade[1]].rect.y #deplacement de la piece
            self.current_upgrade = None
