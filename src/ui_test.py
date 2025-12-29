# title: Pyxel-Chess
# author: Adam Billard, Owen Fouillet, Thomas
# desc: A pyxel chess game, made for the NSI project of the Simone Veil high school
# site: https://github.com/TheDogHusky/chess-pyxel
# version: 0.1

# Créé par abillard2, le 02/12/2025 en Python 3.7

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

        # on montre la sourit, initialise le jeu et le lance !
        pyxel.mouse(True)
        self.init_game()
        pyxel.run(self.update, self.draw)

    # run à chaque frame en premier
    def update(self):
        # on met à jour l'interface utilisateur
        self.update_ui()

    # cette fonction sert à initialiser les différentes variables du jeu qui prendraient trop de place visuellement dans le __init__
    def init_game(self):
        self.pieces_black = []
        self.pieces_white = []
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
            piece.update(self.pieces_black + self.pieces_white)

    # Sert à dessiner les graphismes
    def draw(self):
        # On clear le jeu avec comme couleur de fond du noir
        pyxel.cls(1)
        self.draw_board()
        self.draw_pieces()
        self.draw_ui()
        self.draw_dead_pieces()
        self.draw_promotion_interface()

    # Fonction utilisée lors de chaque tour afin de gérer la mise en place du prochain tour
    def next_turn(self):
        #met la logique d'après chaque tour ici, le for piece in pieces, ...
        pass # à implémenter
    
    # Permet de mettre à jour l'interface (seulement les propriétés, pas la dessiner)
    def update_ui(self):
        self.update_hover()
        self.update_clicks()

    # Permet de mettre à jour ce sur quoi la souris passe
    def update_hover(self):
        # Coordonnées du bouton menu en haut à droite
        if pyxel.mouse_x < 16 and pyxel.mouse_y < 16:
            if not self.menu_opened: # si le menu est fermé, alors on est sur le bouton "ouvrir le menu"
                self.hover = "menu_open"
            else:
                self.hover = "menu_close" # sinon, on passe la souris sur le bouton "fermer le menu" (x)
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
            where = (piece.x * 16 + 48, (piece.y - 7) * 16 + 16) if piece.color == "black" else (piece.x * 16 + 48, (piece.y + 7) * 16 + 48)
            
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

    # utilisé pour le bouton recommencer, on réinitialise tout
    def restart(self):
        self.player_turn = 0
        self.init_game()
        self.selected_piece = None
        self.waiting_promotion = None

    # utilisé pour mettre à jour sur quoi on a cliqué
    def update_clicks(self):
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
        # gère ici le fait de faire bouger une pièce
        # en gros tu check si le mec clique dans une case où le pion peut bouger (coord in piece.possible_moves truc du genre) et si oui tu changes les coordonnées du pion et execute self.next_turn()
        # la mort des pions est gérée par la fonction piece.update() de thomas!
        piece = self.find_piece_at(x, y) # on chope la pièce aux coordonnées
        if piece: # si y'a une pièce
            if (self.player_turn == 0 and piece in self.pieces_white) or (self.player_turn == 1 and piece in self.pieces_black): # si c'est le tour du joueur de la pièce
                self.selected_piece = (x, y) # on sélectionne la pièce
                if (x,y) in piece.possible_moves: # vérifie si la pièce peut aller à cet endroit
                    self.check_rules() # vérifie si on fait un roque
                    piece.bouger(x,y) # on déplace la pièce
                    pieces_total = self.pieces_black + self.pieces_white
                    for piece_to_update in pieces_total:
                        piece_to_update.update(pieces_total)
                    self.selected_piece = None # on déselectionne la pièce
                    self.player_turn = 1 - self.player_turn # on change de joueur

    def check_rules(self):
        self.castling()
        self.en_passant()
        self.promotion()
        # à implémenter: le reste des règles

    # permet de récupérer une instance de la classe pièce dans App avec les coordonnées sur le plateau
    def find_piece_at(self, x, y):
        all_pieces = self.pieces_white + self.pieces_black
        for piece in all_pieces:
            if piece.x == x and piece.y == y and piece.alive: # on find la piece que si elle est vivante
                return piece
        return None

    # Permet de dessiner le plateau
    def draw_board(self):
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
            for move in self.find_piece_at(x, y).possible_moves: # pour chaque coup possible, on met en valeur
                mx, my = move
                pyxel.rectb(mx * 16 + 48, my * 16 + 32, 16, 16, pyxel.COLOR_LIGHT_BLUE)

    # Permet de dessiner toutes les pièces sur le plateau
    def draw_pieces(self):
        pieces = self.pieces_white + self.pieces_black
        for piece in pieces:
            if piece.alive: # seulement si elles sont en vie
                self.draw_piece(piece)

    # Permet de dessiner les pièces mortes en haut sur les barres des joueurs
    def draw_dead_pieces(self):
        pieces = self.pieces_white + self.pieces_black
        pieces_dead = [piece for piece in pieces if not piece.alive] # on filtre les pièces mortes des pièces vivantes

        pieces_by_type = self.sort_by_type(pieces_dead) # on trie les pièces par leur type

        for key in pieces_by_type[0].keys(): # noirs
            if pieces_by_type[0][key]: # si on a une pièce de ce type morte
                coords = self.get_dead_coordinates("black", key) # on récupère les coordonnées où afficher les pièces mortes
                texture_coords = self.get_ui_texture_coordinates(Piece(key, (0,0), "black")) # on récupère les coordonnées des textures des pièces
                number = pieces_by_type[0][key]

                pyxel.blt(coords[0], coords[1], 0, texture_coords[0], texture_coords[1], 16, 16, 0) # on dessine les pièces aux coordonnées corrected
                pyxel.text(coords[0] + 11, coords[1], f"x{number}", pyxel.COLOR_BLACK) # un petit indicateur du nombre de pièces mortes du type
        
        for key in pieces_by_type[1].keys(): # blanc
            if pieces_by_type[1][key]:
                coords = self.get_dead_coordinates("white", key)
                texture_coords = self.get_ui_texture_coordinates(Piece(key, (0,0), "white"))
                number = pieces_by_type[1][key]

                pyxel.blt(coords[0], coords[1], 0, texture_coords[0], texture_coords[1], 16, 16, 0)
                pyxel.text(coords[0] + 11, coords[1], f"x{number}", pyxel.COLOR_BLACK)

    # permet de trier les pièces par leur type
    def sort_by_type(self, pieces):
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

    # Permet de récupérer les coordonnées des textures pour une pièce dans le fichier pyxres
    def get_ui_texture_coordinates(self, piece):
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
    
    # Permet de dessiner une pièce
    def draw_piece(self, piece):
        coords = self.get_ui_texture_coordinates(piece) # on récupère les coordonnées de la texture de la pièce dans 
        sx, sy = coords[0], coords[1]

        pyxel.blt(piece.x * 16 + 48, piece.y * 16 + 32, 0, sx, sy, 16, 16, 0) # on la dessine aux coordonnées correctes

    # Permet de récupérer les coordonnées où afficher les pièces mortes pour chaque type
    def get_dead_coordinates(self, color, type):
        coords_white = {
            "pawn": (64, 0),
            "rook": (80, 0),
            "knight": (96, 0),
            "bishop": (112, 0),
            "queen": (128, 0),
            "king": (144, 0)
        }

        coords_black = {
            "pawn": (64, 192),
            "rook": (80, 192),
            "knight": (96, 192),
            "bishop": (112, 192),
            "queen": (128, 192),
            "king": (144, 192)
        }

        return coords_black[type] if color == "black" else coords_white[type]

    # Permet de dessiner l'interface utilisateur (ui)
    def draw_ui(self):
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

    # Permet de dessiner les textes sur l'interface
    def draw_texts(self):
        if self.menu_opened: # dessin des textes du menu
            pyxel.text(5, 22, "Recommencer", pyxel.COLOR_BLACK) # Position pour que le texte soit centré dans le bouton
            pyxel.text(5, 38, "Quitter", pyxel.COLOR_BLACK) # Position pour que le texte soit centré dans le bouton
        pyxel.text(210, 5, "J 1", pyxel.COLOR_WHITE)
        pyxel.text(210, 182, "J 2", pyxel.COLOR_WHITE)

    def castling(self):
        # Vérifier le tour du joueur actuel
        if self.player_turn == 0: # Roque pour les blancs (joueur 1)
            # Récupérer le roi blanc et les tours blanches
            king = self.find_piece_at(4, 0)
            left_rook = self.find_piece_at(0, 0)  # Tour de gauche (case a1)
            right_rook = self.find_piece_at(7, 0)  # Tour de droite (case h1)4
            if king and king.type == "king" and left_rook and left_rook.type == "rook" and right_rook and right_rook.type == "rook": # Vérifier que le roi et les tours sont présents et à leur position initiale
                if self.selected_piece == (4, 0): # Vérifier si le roi blanc est sélectionné
                    if not self.find_piece_at(1, 0) and not self.find_piece_at(2, 0) and not self.find_piece_at(3, 0): # Roque côté dame
                        if left_rook.has_moved == False and king.has_moved == False:
                            left_rook.bouger(3, 0) # tour se déplace à côté du roi
                            king.bouger(2, 0) # roi se déplace
                    if not self.find_piece_at(5, 0) and not self.find_piece_at(6, 0): # Roque côté roi
                        if right_rook.has_moved == False and king.has_moved == False:
                            right_rook.bouger(5, 0) # tour se déplace à côté du roi
                            king.bouger(6, 0) # roi se déplace
        else: # Roque pour les noirs (joueur 2)
            # Récupérer le roi noir et les tours noires
            king = self.find_piece_at(4, 7)
            left_rook = self.find_piece_at(0, 7)  # Tour de gauche (case a8)
            right_rook = self.find_piece_at(7, 7)  # Tour de droite (case h8)
            if king and king.type == "king" and left_rook and left_rook.type == "rook" and right_rook and right_rook.type == "rook": # Vérifier que le roi et les tours sont présents et à leur position initiale
                if self.selected_piece == (4, 7): # Vérifier si le roi noir est sélectionné
                    if not self.find_piece_at(1, 7) and not self.find_piece_at(2, 7) and not self.find_piece_at(3, 7): # Roque côté dame
                        if left_rook.has_moved == False and king.has_moved == False:
                            left_rook.bouger(3, 7) # tour se déplace à côté du roi
                            king.bouger(2, 7) # roi se déplace
                    if not self.find_piece_at(5, 7) and not self.find_piece_at(6, 7): # Roque côté roi
                        if right_rook.has_moved == False and king.has_moved == False:
                            right_rook.bouger(5, 7) # tour se déplace à côté du roi
                            king.bouger(6, 7) # roi se déplace

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
        pass # TODO implémenter la prise en passant

    def draw_promotion_interface(self):
        piece = self.waiting_promotion
        if piece:
            where = (piece.x * 16 + 48, (piece.y - 7) * 16 + 16) if piece.color == "black" else (piece.x * 16 + 48, (piece.y + 7) * 16 + 48) # TODO FIX THIS CAUSE THE COORDINATES ARE INCORRECT SINCE I USED TO PUT THE WHITE PROMOTIONNAL PANEL IN THE WHITE SECTION (MAKE INVERSE)

            pyxel.rect(where[0], where[1], 64, 16, pyxel.COLOR_WHITE)
            if self.hover == "promote_bishop":
                pyxel.rect(where[0] + 16, where[1], 16, 16, pyxel.COLOR_DARK_BLUE)
            elif self.hover == "promote_knight":
                pyxel.rect(where[0] + 48, where[1], 16, 16, pyxel.COLOR_DARK_BLUE)
            elif self.hover == "promote_rook":
                pyxel.rect(where[0] + 32, where[1], 16, 16, pyxel.COLOR_DARK_BLUE)
            elif self.hover == "promote_queen":
                pyxel.rect(where[0], where[1], 16, 16, pyxel.COLOR_DARK_BLUE)

            coords = self.get_ui_texture_coordinates(Piece("queen", (0,0), piece.color))
            pyxel.blt(where[0], where[1], 0, coords[0], coords[1], 16, 16, 0)
            coords = self.get_ui_texture_coordinates(Piece("bishop", (0,0), piece.color))
            pyxel.blt(where[0] + 16, where[1], 0, coords[0], coords[1], 16, 16, 0)
            coords = self.get_ui_texture_coordinates(Piece("rook", (0,0), piece.color))
            pyxel.blt(where[0] + 32, where[1], 0, coords[0], coords[1], 16, 16, 0)
            coords = self.get_ui_texture_coordinates(Piece("knight", (0,0), piece.color))
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



# ======================= AFK Zone ======================== #
#                                                           #
#                                                           #
# ========================================================= #