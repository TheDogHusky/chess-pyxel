# title: Pyxel-Chess
# author: Adam Billard, Owen Fouillet, Thomas
# desc: A pyxel chess game, made for the NSI project of the Simone Veil high school
# site: https://github.com/TheDogHusky/chess-pyxel
# version: 0.1

# coordonnées bouton menu : (0,0) -> (16,16)
# coordonnées option 1 : (0,17) -> (64,32)
# coordonnées option 2 : (0,33) -> (64,48)

# Le menu se déplie vers le bas

# bouton open menu: pyxel.blt(0, 0, 0, 0, 0, 16, 16)
# bouton open menu hover: pyxel.blt(0, 0, 0, 16, 0, 16, 16)
# bouton close menu: pyxel.blt(0, 0, 0, 32, 0, 16, 16)
# bouton close menu hover: pyxel.blt(0, 0, 0, 48, 0, 16, 16)
# menu ouvert normal: pyxel.blt(0, 17, 0, 0, 16, 64, 32)
# menu option 1 hover: pyxel.blt(0, 17, 0, 0, 48, 64, 32)
# menu option 2 hover: pyxel.blt(0, 17, 0, 0, 80, 64, 32)

import pyxel
from programme_thomas import Piece
from typing import List

# class piece, représente une pièce (un pion, un knight, etc..)
# class Piece:
#     def __init__(self, type, coords=(0,0), color="white"):
#         self.type = type # le type de pion: "knight", "rook", "pawn", etc..
#         self.x = coords[0] # coordonnée x en numéro de case
#         self.y = coords[1] # y en numéro de case
#         self.has_moved = False
#         self.alive = True # est vivant ou morte
#         self.possible_moves = [] # les coups possibles ex: [(0,1),(5,2)]
#         self.color = color # ou "black", la couleur de la pièce


class App:
    """Classe principale de l'application Pyxel-Chess."""

    def __init__(self):
        # initialisation de la fenêtre pyxel. NE PAS CHANGER LES VALEURS!
        pyxel.init(224, 192, title="Pyxel-Chess",fps=60)

        # On charge les éléments de l'interface
        self.ui = pyxel.load("chess.pyxres")
        self.hover = "" # "menu_close" "menu_open" "menu_1" "menu_2" "board-x-y" -> sur quel élément on passe la souris
        self.player_turn = 0 # 0 = joueur 1, 1 = joueur 2 -> le tour du joueur
        self.menu_opened = False # le menu est-il ouvert ?
        self.selected_piece = None # quelle pièce est sélectionnée ?
        self.waiting_promotion = None # Instance de Piece

        # Pour ces propriétés ci dessous, on a choisi cette façon de faire car les règles de jeu on deux dimensions:
        # Une dimension de détection, donc dans on sélectionne une pièce, montrer ce qui est possible.
        # Une dimension d'exécution, donc quand on clique pour bouger une pièce, on effectue les actions nécessaires.
        
        self.castling_possible = {
            "white": False,
            "black": False
        } # indique si le roque est possible pour chaque couleur, et dans quel sens. Format: {"color": [is_possible: bool, (coords_x, coords_y)]} -> coords indiquent un élément des possible_moves du roi pour le roque
        self.en_passant_possible = {
            "white": None,
            "black": None
        } # indique si une prise en passant est possible pour chaque couleur. Format: {"color": Piece} -> Piece est le pion adverse pouvant être capturé en passant
        
        self.pieces_black: List[Piece] = []
        self.pieces_white: List[Piece] = []

        # on montre la sourit, initialise le jeu et le lance !
        pyxel.mouse(True)
        self.init_game()
        pyxel.run(self.update, self.draw)

    def update(self):
        """Met à jour l'état de l'application à chaque frame."""

        # on met à jour l'interface utilisateur
        self.update_ui()

    def init_game(self):
        """
        Initialise le plateau de jeu avec les pièces aux positions de départ.
        Elle contient aussi du code un peu trop gros pour le __init__, et permet de reset le jeu en cas de clic sur "recommencer" dans le menu.
        """

        # on crée les pions selon les règles de l'échec
        for i in range(0, 2):
            self.pieces_white.append(Piece("knight", (1 + i * 5, 0)))
            self.pieces_black.append(Piece("knight", (1 + i * 5, 7), "black"))
            self.pieces_white.append(Piece("rook", (i * 7, 0)))
            self.pieces_black.append(Piece("rook", (i * 7, 7), "black"))
            self.pieces_white.append(Piece("bishop", (2 + i * 3, 0)))
            self.pieces_black.append(Piece("bishop", (2 + i * 3, 7), "black"))
        for i in range(8):
            self.pieces_white.append(Piece("pawn", (i, 1)))
            self.pieces_black.append(Piece("pawn", (i, 6), "black"))
        self.pieces_black.append(Piece("queen", (3, 7), "black"))
        self.pieces_white.append(Piece("queen", (3, 0)))
        self.pieces_black.append(Piece("king", (4, 7), "black"))
        self.pieces_white.append(Piece("king", (4, 0)))

        for piece in self.pieces_black + self.pieces_white:
            piece.update(self.pieces_black, self.pieces_white) # mise à jour initiale des coups possibles

    def draw(self):
        """Dessine l'interface utilisateur à chaque frame."""

        # On clear le jeu avec comme couleur de fond du noir
        pyxel.cls(1)
        # on dessine le plateau, les pièces, l'interface, les pièces mortes et l'interface de promotion
        self.draw_board()
        self.draw_pieces()
        self.draw_ui()
        self.draw_dead_pieces()
        self.draw_promotion_interface()
    
    def update_ui(self):
        """Met à jour l'état de l'interface utilisateur. (propriétés seulement, pas le dessin)"""

        self.update_hover()
        self.update_clicks()

    def update_hover(self):
        """Met à jour l'élément sur lequel la souris passe."""

        # Coordonnées du bouton menu en haut à droite
        if pyxel.mouse_x < 16 and pyxel.mouse_y < 16:
            # si le menu est fermé, on passe la souris sur le bouton "ouvrir le menu", sinon sur "fermer le menu"
            self.hover = "menu_open" if not self.menu_opened else "menu_close"
        elif self.menu_opened: # sinon, si on ne passe pas la souris sur le bouton du menu, et que le menu est ouvert, alors on passe sûrement la souris sur un bouton du menu
            if pyxel.mouse_x < 64 and 17 <= pyxel.mouse_y <= 32: # coordonnées du bouton de menu 1
                self.hover = "menu_1"
            elif pyxel.mouse_x < 64 and 33 <= pyxel.mouse_y <= 48: # coordonnées du bouton de menu 2
                self.hover = "menu_2"
            else:
                self.hover = "" # on a pas la souris sur le menu
        elif 48 <= pyxel.mouse_x <= 176 and 32 <= pyxel.mouse_y <= 160: # si on a la souris sur le plateau
            self.hover = "board-" + str((pyxel.mouse_x - 48) // 16) + "-" + str((pyxel.mouse_y - 32) // 16) # on met self.hover au format "board-<case-y>-<case-z>"
        elif self.waiting_promotion: # si on a une promotion en attente, on check si la souris est sur une des options
            piece = self.waiting_promotion
            where = (piece.x * 16 + 48, piece.y * 16 + 16) if piece.color == "black" else (piece.x * 16 + 48, piece.y * 16 + 48)
            
            if where[0] <= pyxel.mouse_x <= where[0] + 16 and where[1] <= pyxel.mouse_y <= where[1] + 16:
                self.hover = "promote_queen"
            elif where[0] + 16 <= pyxel.mouse_x <= where[0] + 32 and where[1] <= pyxel.mouse_y <= where[1] + 16:
                self.hover = "promote_bishop"
            elif where[0] + 32 <= pyxel.mouse_x <= where[0] + 48 and where[1] <= pyxel.mouse_y <= where[1] + 16:
                self.hover = "promote_rook"
            elif where[0] + 48 <= pyxel.mouse_x <= where[0] + 64 and where[1] <= pyxel.mouse_y <= where[1] + 16:
                self.hover = "promote_knight"
            else:
                self.hover = ""
        else:
            self.hover = "" # la souris n'est sur rien !

    def restart(self):
        """
        Réinitialise le jeu en remettant toutes les pièces à leur position de départ.
        Utilisé lors du clic sur "Recommencer" dans le menu.
        """

        self.player_turn = 0
        self.pieces_black = []
        self.pieces_white = []
        self.init_game()
        self.selected_piece = None
        self.waiting_promotion = None
        self.en_passant_possible = {
            "white": None,
            "black": None
        }
        self.castling_possible = {
            "white": False,
            "black": False
        }

    def update_clicks(self):
        """Gère les clics de la souris et effectue les actions appropriées."""

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT): # seulement clic gauche
            # Logique : on regarde sur quoi on passait la souris, et on effecture des actions en conséquence
            if self.hover == "menu_open":
                self.menu_opened = True
            elif self.hover == "menu_close":
                self.menu_opened = False
            elif self.hover == "menu_1":
                self.restart()
                self.menu_opened = False
            elif self.hover == "menu_2":
                self.menu_opened = False
                pyxel.quit()
            elif self.hover == "" and self.menu_opened: # si on est sur rien et on clique, alors que le menu est ouvert, on le ferme (UX)
                self.menu_opened = False
            elif self.hover == "" and not self.menu_opened: # Si on clique sur rien et qu'on avait sélectionné une pièce, alors on la déselectionne (UX)
                self.selected_piece = None
            elif "board" in self.hover: # On gère la logique de clic sur le plateau
                _, x, y = self.hover.split("-")
                x = int(x)
                y = int(y)
                self.handle_board_click(x, y)
            elif "promote" in self.hover:
                _, piece_type = self.hover.split("_") # on récupère le type de pièce sur laquelle on a cliqué
                self.handle_promotion_click(piece_type)

    def handle_promotion_click(self, piece_type):
        """Gère le clic sur une option de promotion de pion."""

        if self.waiting_promotion:
            # on récupère l'index de la pièce en promotion dans la liste des pièces
            piece = self.waiting_promotion
            pieces_list = self.pieces_white if piece.color == "white" else self.pieces_black
            index = pieces_list.index(piece)

            if piece.color == "white":
                del self.pieces_white[index]
                self.pieces_white.insert(index, Piece(piece_type, (piece.x, piece.y), "white"))
            else: 
                del self.pieces_black[index]
                self.pieces_black.insert(index, Piece(piece_type, (piece.x, piece.y), "black"))
            # on remplace la pièce par une autre de type piece_type
            self.waiting_promotion = None

    def handle_board_click(self, x, y):
        """Gère le clic sur une case du plateau aux coordonnées (x, y)."""

        if self.waiting_promotion: # si on a une promotion en attente, on ne peut pas bouger de pièce
            return

        piece = self.find_piece_at(x, y) # on chope la pièce aux coordonnées
        if piece: # si y'a une pièce
            if (self.player_turn == 0 and piece in self.pieces_white) or (self.player_turn == 1 and piece in self.pieces_black): # si c'est le tour du joueur de la pièce
                self.selected_piece = [x, y] # on sélectionne la pièce
                self.check_rules() # vérifie les règles spéciales
                
                return
        if self.selected_piece:
            selected = self.find_piece_at(self.selected_piece[0], self.selected_piece[1])
            self.castling_move(x, y) # on check si on doit faire un roque
            if self.en_passant_possible["white"] or self.en_passant_possible["black"]:
                self.en_passant_move(selected) # on check si on doit faire une prise en passant
                return
            
            if selected and [x, y] in selected.possible_moves: # vérifie si la pièce peut aller à cet endroit
                opponent = piece # on stocke la pièce adverse (si y'en a une)
                piece = selected # on récupère la pièce sélectionnée
                piece.bouger(x,y) # on déplace la pièce

                if opponent and opponent.alive and opponent.color != piece.color:
                    opponent.alive = False

                self.next_turn() # on passe au tour suivant

                return

    def next_turn(self):
        pieces_total = self.pieces_black + self.pieces_white
        for piece_to_update in pieces_total:
            piece_to_update.update(self.pieces_black, self.pieces_white)
        self.selected_piece = None # on désélectionne la pièce
        self.promotion() # on check si on doit promouvoir un pion
        self.player_turn = 1 - self.player_turn # on change de joueur

    def check_rules(self):
        """Vérifie et applique les règles spéciales des échecs lors d'un déplacement de pièce."""

        self.castling()
        self.en_passant()
        # à implémenter: le reste des règles

    def find_piece_at(self, x, y):
        """Retourne la pièce située aux coordonnées (x, y) si elle est vivante, sinon None."""
        all_pieces = self.pieces_white + self.pieces_black
        for piece in all_pieces:
            if piece.x == x and piece.y == y and piece.alive: # on find la piece que si elle est vivante
                return piece
        return None

    def draw_board(self):
        """Dessine le plateau de jeu avec les cases et les surlignages."""
        
        for x in range(8):
            for y in range(8): # plateau en 8*8 cases
                if (x + y) % 2 == 0: # une case sur deux, on change la couleur (faut que le plateau soit beau)
                    pyxel.rect(x * 16 + 48, y * 16 + 32, 16, 16, pyxel.COLOR_PEACH)
                else:
                    pyxel.rect(x * 16 + 48, y * 16 + 32, 16, 16, pyxel.COLOR_BROWN)
        
        # on gère le fait de surligner la pièce sélectionnée et les coups possibles
        if self.selected_piece:
            x, y = self.selected_piece[0], self.selected_piece[1]
            pyxel.rectb(x * 16 + 48, y * 16 + 32, 16, 16, pyxel.COLOR_DARK_BLUE) # case de pièce sélectionnée
            # utilisation de piece.possible_moves pour afficher les coups possibles
            selected = self.find_piece_at(x, y)
            if selected:
                for move in selected.possible_moves: # pour chaque coup possible, on met en valeur
                    mx, my = move
                    pyxel.rectb(mx * 16 + 48, my * 16 + 32, 16, 16, pyxel.COLOR_LIGHT_BLUE)

    def draw_pieces(self):
        """Dessine toutes les pièces vivantes sur le plateau de jeu."""

        pieces = self.pieces_white + self.pieces_black
        for piece in pieces:
            if piece.alive: # seulement si elles sont en vie
                self.draw_piece(piece)

    def draw_dead_pieces(self):
        """Dessine les pièces mortes sur l'interface utilisateur."""

        pieces = self.pieces_white + self.pieces_black
        pieces_dead = [piece for piece in pieces if not piece.alive] # on filtre les pièces mortes des pièces vivantes

        pieces_by_type = self.sort_by_type(pieces_dead) # on trie les pièces par leur type

        for key in pieces_by_type[0].keys(): # noirs
            if pieces_by_type[0][key]: # si on a une pièce de ce type morte
                coords = self.get_dead_coordinates("black", key) # on récupère les coordonnées où afficher les pièces mortes
                texture_coords = self.get_ui_texture_coordinates(Piece(key, (0,0), "black")) # on récupère les coordonnées des textures des pièces
                number = pieces_by_type[0][key]
                pyxel.blt(coords[0], coords[1], 0, texture_coords[0], texture_coords[1], 16, 16, 0) # on dessine les pièces aux coordonnées corrected
                pyxel.text(coords[0] + 10, coords[1], f"x{number}", pyxel.COLOR_BLACK) # un petit indicateur du nombre de pièces mortes du type
        
        for key in pieces_by_type[1].keys(): # blanc
            if pieces_by_type[1][key]:
                coords = self.get_dead_coordinates("white", key)
                texture_coords = self.get_ui_texture_coordinates(Piece(key, (0,0), "white"))
                number = pieces_by_type[1][key]

                pyxel.blt(coords[0], coords[1], 0, texture_coords[0], texture_coords[1], 16, 16, 0)
                pyxel.text(coords[0] + 10, coords[1], f"x{number}", pyxel.COLOR_BLACK)

    def sort_by_type(self, pieces):
        """Trie les pièces mortes par type et couleur."""

        # on renverra deux dictionnaires dans un tableau avec à l'intérieur pour chasue type (clé) son nombre de pièces mortes du type (value)
        val = {
            "pawn": 0,
            "rook": 0,
            "knight": 0,
            "bishop": 0,
            "queen": 0,
            "king": 0
        }

        val_white = {
            "pawn": 0,
            "rook": 0,
            "knight": 0,
            "bishop": 0,
            "queen": 0,
            "king": 0
        }

        for piece in pieces:
            if piece.color == "black":
                val[piece.type] += 1
            else:
                val_white[piece.type] += 1
        
        return (val, val_white)

    def get_ui_texture_coordinates(self, piece):
        """Retourne les coordonnées (sx, sy) de la texture de la pièce dans le fichier pyxres."""

        # on stocke les valeurs "hard coded" des positions des textures dans des dictionnaires
        # clé: le type de pièce, valeur: un tuple avec les coordonnées (x, y)
        coords_white = {
            "pawn": (64, 80),
            "rook": (64, 48),
            "knight": (64, 96),
            "bishop": (64, 16),
            "queen": (64, 64),
            "king": (64, 32)
        }
        coords_black = {
            "pawn": (80, 80),
            "rook": (80, 48),
            "knight": (80, 96),
            "bishop": (80, 16),
            "queen": (80, 64),
            "king": (80, 32)
        }

        sx, sy = 0, 0

        if piece.color == "white":
            sx, sy = coords_white[piece.type]
        else:
            sx, sy = coords_black[piece.type]

        return (sx, sy)
    
    def draw_piece(self, piece):
        """Dessine une pièce sur le plateau de jeu aux coordonnées correctes."""

        coords = self.get_ui_texture_coordinates(piece) # on récupère les coordonnées de la texture de la pièce dans 
        sx, sy = coords[0], coords[1]

        pyxel.blt(piece.x * 16 + 48, piece.y * 16 + 32, 0, sx, sy, 16, 16, 0) # on la dessine aux coordonnées correctes

    def get_dead_coordinates(self, color, type):
        """Retourne les coordonnées (x, y) où dessiner les pièces mortes de type 'type' et couleur 'color'."""

        coords_white = {
            "pawn": (64, 0),
            "rook": (80, 0),
            "knight": (96, 0),
            "bishop": (112, 0),
            "queen": (128, 0),
            "king": (144, 0)
        }

        coords_black = {
            "pawn": (64, 176),
            "rook": (80, 176),
            "knight": (96, 176),
            "bishop": (112, 176),
            "queen": (128, 176),
            "king": (144, 176)
        }

        return coords_black[type] if color == "black" else coords_white[type]

    def draw_ui(self):
        """Dessine l'interface utilisateur (UI) à chaque frame."""

        # ---------------------------
        #    Les menus et boutons
        # ---------------------------
        if self.hover == "menu_open": # si on a la souris sur le bouton "ouvrir le menu"
            pyxel.blt(0, 0, 0, 16, 0, 16, 16)
        else: # sinon, on dessine le bouton menu normal
            pyxel.blt(0, 0, 0, 0, 0, 16, 16)

        if self.menu_opened:
            if self.hover == "menu_close": # souris sur bouton "fermer le menu"
                pyxel.blt(0, 0, 0, 48, 0, 16, 16)
            else:
                pyxel.blt(0, 0, 0, 32, 0, 16, 16)
            
            if self.hover == "menu_1": # menu ouvert et souris sur bouton 1 du menu
                pyxel.blt(0, 17, 0, 0, 48, 64, 32)
            elif self.hover == "menu_2": # menu ouvert et souris sur bouton 2 du menu
                pyxel.blt(0, 17, 0, 0, 80, 64, 32)
            else: # menu ouvert et souris pas sur menu
                pyxel.blt(0, 17, 0, 0, 16, 64, 32)

        # --------------------------
        # L'interface niveau joueur
        # --------------------------
        if self.player_turn == 0:
            pyxel.rect(208, 0, 16, 16, pyxel.COLOR_LIME) # carré j1
            pyxel.rect(208, 176, 16, 16, pyxel.COLOR_LIGHT_BLUE) # carré j2
        else:
            pyxel.rect(208, 0, 16, 16, pyxel.COLOR_LIGHT_BLUE) # carré j1
            pyxel.rect(208, 176, 16, 16, pyxel.COLOR_LIME) # carré j2

        pyxel.rect(64, 0, 96, 16, pyxel.COLOR_LIGHT_BLUE) # barre j1 remplie
        pyxel.rect(64, 192 - 16, 96, 16, pyxel.COLOR_LIGHT_BLUE) # barre j2 remplie

        self.draw_texts() # on dessine ensuite les textes

    def draw_texts(self):
        """Dessine les textes de l'interface utilisateur."""

        if self.menu_opened: # dessin des textes du menu
            pyxel.text(5, 22, "Recommencer", pyxel.COLOR_BLACK) # Position pour que le texte soit centré dans le bouton
            pyxel.text(5, 38, "Quitter", pyxel.COLOR_BLACK) # Position pour que le texte soit centré dans le bouton
        pyxel.text(213, 5, "J1", pyxel.COLOR_WHITE)
        pyxel.text(213, 182, "J2", pyxel.COLOR_WHITE)

# ======================== Owen ======================== #

    def castling_move(self, x, y):
        if self.castling_possible["white"] and self.player_turn == 0:
            king = self.find_piece_at(4, 0)
            if (2, 0) in king.possible_moves: # roque côté dame
                rook = self.find_piece_at(0, 0)
                rook.bouger(3, 0)
                king.bouger(2, 0)
                self.castling_possible["white"] = False # on reset la possibilité de roque pour les blancs
                self.next_turn()
            else: # roque côté roi
                rook = self.find_piece_at(7, 0)
                rook.bouger(5, 0)
                king.bouger(6, 0)
                self.next_turn()
            self.castling_possible["white"] = False # on reset la possibilité de roque pour les blancs
        elif self.castling_possible["black"] and self.player_turn == 1:
            king = self.find_piece_at(4, 7)
            if (2, 7) in king.possible_moves: # roque côté dame
                rook = self.find_piece_at(0, 7)
                rook.bouger(3, 7)
                king.bouger(2, 7)
                self.next_turn()
            else: # roque côté roi
                rook = self.find_piece_at(7, 7)
                rook.bouger(5, 7)
                king.bouger(6, 7)
                self.next_turn()
            self.castling_possible["black"] = False # on reset la possibilité de roque pour les noirs

    def castling(self):
        # Vérifier le tour du joueur actuel
        if self.player_turn == 0: # Roque pour les blancs (joueur 1)
            # Récupérer le roi blanc et les tours blanches
            king = self.find_piece_at(4, 0)
            left_rook = self.find_piece_at(0, 0)  # Tour de gauche (case a1)
            right_rook = self.find_piece_at(7, 0)  # Tour de droite (case h1)
            if king and king.type == "king" and left_rook and left_rook.type == "rook" and right_rook and right_rook.type == "rook": # Vérifier que le roi et les tours sont présents et à leur position initiale
                if self.selected_piece and self.selected_piece == [4, 0]: # Vérifier si le roi blanc est sélectionné
                    if not self.find_piece_at(1, 0) and not self.find_piece_at(2, 0) and not self.find_piece_at(3, 0): # Roque côté dame
                        if left_rook.has_moved == False and king.has_moved == False: # Vérifier que ni le roi ni la tour n'ont bougé
                            if (2,0) not in king.possible_moves: king.possible_moves.append((2, 0)) # ajouter le roque côté dame aux coups possibles du roi
                            self.castling_possible["white"] = True # indiquer que le roque côté dame est possible pour les blancs
                    if not self.find_piece_at(5, 0) and not self.find_piece_at(6, 0): # Roque côté roi
                        if right_rook.has_moved == False and king.has_moved == False:
                            if (6,0) not in king.possible_moves: king.possible_moves.append((6, 0)) # ajouter le roque côté roi aux coups possibles du roi
                            self.castling_possible["white"] = True # indiquer que le roque côté roi est possible pour les blancs
        else: # Roque pour les noirs (joueur 2)
            # Récupérer le roi noir et les tours noires
            king = self.find_piece_at(4, 7)
            left_rook = self.find_piece_at(0, 7)  # Tour de gauche (case a8)
            right_rook = self.find_piece_at(7, 7)  # Tour de droite (case h8)
            if king and king.type == "king" and left_rook and left_rook.type == "rook" and right_rook and right_rook.type == "rook": # Vérifier que le roi et les tours sont présents et à leur position initiale
                if self.selected_piece and self.selected_piece == [4, 7]: # Vérifier si le roi noir est sélectionné
                    if not self.find_piece_at(1, 7) and not self.find_piece_at(2, 7) and not self.find_piece_at(3, 7): # Roque côté dame
                        if left_rook.has_moved == False and king.has_moved == False: # Vérifier que ni le roi ni la tour n'ont bougé
                            if (2,7) not in king.possible_moves: 
                                king.possible_moves.append((2, 7)) # ajouter le roque côté dame aux coups possibles du roi
                            self.castling_possible["black"] = True # indiquer que le roque côté dame est possible pour les noirs
                    if not self.find_piece_at(5, 7) and not self.find_piece_at(6, 7): # Roque côté roi
                        if right_rook.has_moved == False and king.has_moved == False:
                            if (6,7) not in king.possible_moves: 
                                king.possible_moves.append((6, 7)) # ajouter le roque côté roi aux coups possibles du roi
                            self.castling_possible["black"] = True # indiquer que le roque côté roi est possible pour les noirs

    def en_passant_move(self, selected):
        if self.en_passant_possible["white"] and self.player_turn == 0: # prise en passant pour les blancs
            pawn = self.find_piece_at(self.en_passant_possible["white"].x, self.en_passant_possible["white"].y)
            if pawn and pawn.type == "pawn":
                selected.bouger(pawn.x, pawn.y + 1)
                self.en_passant_possible["white"] = None
                pawn.alive = False
                self.next_turn()
        elif self.en_passant_possible["black"]: # prise en passant pour les noirs
            pawn = self.find_piece_at(self.en_passant_possible["black"].x, self.en_passant_possible["black"].y)
            if pawn and pawn.type == "pawn":
                print("found pawn")
                selected.bouger(pawn.x, pawn.y - 1)
                pawn.alive = False
                self.en_passant_possible["black"] = None
                self.next_turn()

    def en_passant(self):
        """
        Effectue une prise en passant au échecs.
        La prise en passant est une règle spéciale du jeu d'échecs qui permet à un pion
        de capturer un pion adverse dans des circonstances particulières:
        1. Un pion adverse vient de se déplacer de deux cases en avant depuis sa position
            initiale et s'arrête à côté de votre pion.
        2. Votre pion peut alors capturer le pion adverse comme s'il n'avait avancé que
            d'une seule case.
        3. Cette capture doit être effectuée immédiatement, sinon elle n'est plus possible
            au coup suivant.
        4. La prise en passant ne peut être exécutée que par un pion et seulement contre
            un autre pion.
        """
        # Vérifier le tour du joueur actuel
        if self.player_turn == 0:  # Prise en passant pour les blancs
            for piece in self.pieces_white:
                if piece.type == "pawn" and piece.alive:
                    # Vérifier les cases à gauche et à droite du pion blanc
                    for dx in [-1, 1]: # gauche et droite
                        enemy_x = piece.x + dx
                        enemy_y = piece.y
                        enemy_piece = self.find_piece_at(enemy_x, enemy_y) # on cherche la pièce ennemie
                        
                        # Vérifier s'il y a un pion noir adjacent
                        if enemy_piece and enemy_piece.type == "pawn" and enemy_piece.color == "black":
                            # Ajouter la prise en passant comme coup possible
                            en_passant_move = (enemy_x, enemy_y + 1)
                            if en_passant_move not in piece.possible_moves:
                                piece.possible_moves.append(en_passant_move)
                            self.en_passant_possible["white"] = enemy_piece # Stocker le pion noir pouvant être capturé en passant

        else:  # Prise en passant pour les noirs
            for piece in self.pieces_black:
                if piece.type == "pawn" and piece.alive:
                    # Vérifier les cases à gauche et à droite du pion noir
                    for dx in [-1, 1]:
                        enemy_x = piece.x + dx
                        enemy_y = piece.y
                        enemy_piece = self.find_piece_at(enemy_x, enemy_y)
                        
                        # Vérifier s'il y a un pion blanc adjacent
                        if enemy_piece and enemy_piece.type == "pawn" and enemy_piece.color == "white":
                            # Ajouter la prise en passant comme coup possible
                            en_passant_move = (enemy_x, enemy_y - 1)
                            if en_passant_move not in piece.possible_moves:
                                piece.possible_moves.append(en_passant_move)
                            self.en_passant_possible["black"] = enemy_piece # Stocker le pion noir pouvant être capturé en passant

    def draw_promotion_interface(self):
        """Dessine l'interface de promotion des pions lorsqu'une promotion est en attente."""

        piece = self.waiting_promotion # on récupère la pièce en attente de promotion
        if piece:
            where = (piece.x * 16 + 48, piece.y * 16 + 16) if piece.color == "black" else (piece.x * 16 + 48, piece.y * 16 + 48) # on calcule où dessiner l'interface de promotion


            pyxel.rect(where[0], where[1], 64, 16, pyxel.COLOR_WHITE) # fond blanc de l'interface
            if self.hover == "promote_bishop": # si on survole l'option "fou"
                pyxel.rect(where[0] + 16, where[1], 16, 16, pyxel.COLOR_DARK_BLUE) # on surligne l'option
            elif self.hover == "promote_knight": # si on survole l'option "cavalier"
                pyxel.rect(where[0] + 48, where[1], 16, 16, pyxel.COLOR_DARK_BLUE)
            elif self.hover == "promote_rook": # si on survole l'option "tour"
                pyxel.rect(where[0] + 32, where[1], 16, 16, pyxel.COLOR_DARK_BLUE)
            elif self.hover == "promote_queen": # si on survole l'option "reine"
                pyxel.rect(where[0], where[1], 16, 16, pyxel.COLOR_DARK_BLUE)

            # on dessine les options de promotion
            coords = self.get_ui_texture_coordinates(Piece("queen", (0,0), piece.color)) # reine
            pyxel.blt(where[0], where[1], 0, coords[0], coords[1], 16, 16, 0)
            coords = self.get_ui_texture_coordinates(Piece("bishop", (0,0), piece.color)) # fou
            pyxel.blt(where[0] + 16, where[1], 0, coords[0], coords[1], 16, 16, 0)
            coords = self.get_ui_texture_coordinates(Piece("rook", (0,0), piece.color)) # tour
            pyxel.blt(where[0] + 32, where[1], 0, coords[0], coords[1], 16, 16, 0)
            coords = self.get_ui_texture_coordinates(Piece("knight", (0,0), piece.color)) # cavalier
            pyxel.blt(where[0] + 48, where[1], 0, coords[0], coords[1], 16, 16, 0)


    def promotion(self):
        """
        Gère la promotion des pions aux échecs.
        La promotion est une règle spéciale qui permet à un pion d'être transformé en
        une autre pièce (généralement une reine) lorsqu'il atteint la dernière rangée
        du côté adverse du plateau.
        1. Lorsqu'un pion atteint la huitième rangée (pour les blancs) ou la première
            rangée (pour les noirs), il peut être promu.
        2. Le joueur peut choisir de promouvoir le pion en une reine, une tour, un
            fou ou un cavalier.
        3. La pièce choisie remplace immédiatement le pion sur la case où il a été
            promu.
        """
        if self.player_turn == 0: # promotion pour les blancs
            for piece in self.pieces_white: # on parcourt les pièces blanches
                if piece.type == "pawn" and piece.y == 7 and piece.alive:
                    self.waiting_promotion = piece
        else: # promotion pour les noirs
            for piece in self.pieces_black: # on parcourt les pièces noires
                if piece.type == "pawn" and piece.y == 0 and piece.alive:
                    self.waiting_promotion = piece


App()