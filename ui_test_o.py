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


from time import sleep
import pyxel

# class piece, représente une pièce (un pion, un knight, etc..)
class Piece:
    def __init__(self, type, coords=(0,0), color="white"):
        self.type = type # le type de pion: "knight", "rook", "pawn", etc..
        self.x = coords[0] # coordonnée x en numéro de case
        self.y = coords[1] # y en numéro de case
        self.alive = True # est vivant ou morte
        self.possible_moves = [] # les coups possibles ex: [(0,1),(5,2)] 
        self.color = color # ou "black", la couleur de la pièce


class App:
    def __init__(self):
        # initialisation de la fenêtre pyxel. NE PAS CHANGER LES VALEURS!
        pyxel.init(224, 192)

        # On charge les éléments de l'interface
        self.ui = pyxel.load("chess.pyxres")
        self.hover = "" # "menu_close" "menu_open" "menu_1" "menu_2" "board-x-y" -> sur quel élément on passe la souris
        self.player_turn = 0 # 0 = joueur 1, 1 = joueur 2 -> le tour du joueur
        self.menu_opened = False # le menu est-il ouvert?
        self.pieces_white = [] # contient les pièces des blancs
        self.pieces_black = [] # contient les pièces des noirs
        self.selected_piece = None # quelle pièce est sélectionnée

        # on montre la sourit, initialise le jeu et le lance!
        pyxel.mouse(True)
        self.init_game()
        pyxel.run(self.update, self.draw)

    # run à chaque frame en premier
    def update(self):
        # on met à jour l'interface utilisateur
        self.update_ui()

    # cette fonction sert à initialiser les différentes variables du jeu qui prendraient trop de place visuellement dans le __init__
    def init_game(self):
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

        self.pieces_white[0].possible_moves = [(0,2), (2,2)]

    def draw(self):
        pyxel.cls(0)
        self.draw_board()
        self.draw_pieces()
        self.draw_ui()

    def next_turn():
        #met la logique d'après chaque tour ici, le for piece in pieces, ...
        pass # à implémenter

    def update_ui(self):
        self.update_hover()
        self.update_clicks()

    def update_hover(self):
        if pyxel.mouse_x < 16 and pyxel.mouse_y < 16:
            if not self.menu_opened:
                self.hover = "menu_open"
            else:
                self.hover = "menu_close"
        elif self.menu_opened:
            if pyxel.mouse_x < 64 and 17 <= pyxel.mouse_y <= 32:
                self.hover = "menu_1"
            elif pyxel.mouse_x < 64 and 33 <= pyxel.mouse_y <= 48:
                self.hover = "menu_2"
            else:
                self.hover = ""
        elif 48 <= pyxel.mouse_x <= 176 and 32 <= pyxel.mouse_y <= 160:
            self.hover = "board-" + str((pyxel.mouse_x - 48) // 16) + "-" + str((pyxel.mouse_y - 32) // 16)
        else:
            self.hover = ""

    def update_clicks(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if self.hover == "menu_open":
                self.menu_opened = True
            elif self.hover == "menu_close":
                self.menu_opened = False
            elif self.hover == "menu_1":
                print("RECOMMENCER")
                self.player_turn = 1 - self.player_turn
                print(self.player_turn)
            elif self.hover == "menu_2":
                pyxel.quit()
            elif self.hover == "" and self.menu_opened:
                self.menu_opened = False
            elif self.hover == "" and not self.menu_opened:
                self.selected_piece = None
            elif "board" in self.hover:
                _, x, y = self.hover.split("-")
                x = int(x)
                y = int(y)
                self.handle_piece_selection(x, y)

    def handle_piece_selection(self, x, y):
        # gère ici le fait de faire bouger une pièce
        # en gros tu check si le mec clique dans une case où le pion peut bouger (coord in piece.possible_moves truc du genre) et si oui tu changes les coordonnées du pion et execute self.next_turn()
        # la mort des pions est gérée par la fonction piece.update() de thomas!
        piece = self.find_piece_at(x, y)
        if piece:
            if (self.player_turn == 0 and piece in self.pieces_white) or (self.player_turn == 1 and piece in self.pieces_black):
                self.selected_piece = (x, y)

    def find_piece_at(self, x, y):
        all_pieces = self.pieces_white + self.pieces_black
        for piece in all_pieces:
            if piece.x == x and piece.y == y and piece.alive:
                return piece
        return None

    def draw_board(self):
        for x in range(8):
            for y in range(8):
                if (x + y) % 2 == 0:
                    pyxel.rect(x * 16 + 48, y * 16 + 32, 16, 16, pyxel.COLOR_PEACH)
                else:
                    pyxel.rect(x * 16 + 48, y * 16 + 32, 16, 16, pyxel.COLOR_BROWN)
        for x in range(8):
            for y in range(8):
                if self.selected_piece == (x, y):
                    pyxel.rectb(x * 16 + 48, y * 16 + 32, 16, 16, pyxel.COLOR_DARK_BLUE)
                    # utilisation de piece.possible_moves pour afficher les coups possibles
                    for move in self.find_piece_at(x, y).possible_moves:
                        mx, my = move
                        pyxel.rectb(x * 16 + 48, my * 16 + 32, 16, 16, pyxel.COLOR_LIGHT_BLUE)

    def draw_pieces(self):
        pieces = self.pieces_white + self.pieces_black
        for piece in pieces:
            if piece.alive:
                self.draw_piece(piece)
    
    def draw_piece(self, piece):
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

        pyxel.blt(piece.x * 16 + 48, piece.y * 16 + 32, 0, sx, sy, 16, 16, 0)

    def draw_ui(self):
        if self.menu_opened and self.hover not in ["menu_1", "menu_2"]:
            pyxel.blt(0, 17, 0, 0, 16, 64, 32)

        if self.hover == "menu_open":
            pyxel.blt(0, 0, 0, 16, 0, 16, 16)
        elif self.hover == "menu_close":
            if self.menu_opened:
                pyxel.blt(0, 17, 0, 0, 16, 64, 32)
                pyxel.blt(0, 0, 0, 48, 0, 16, 16)
            pyxel.blt(0, 0, 0, 48, 0, 16, 16)
        elif self.hover == "menu_1" and self.menu_opened:
            pyxel.blt(0, 17, 0, 0, 48, 64, 32)
            pyxel.blt(0, 0, 0, 32, 0, 16, 16)
        elif self.hover == "menu_2" and self.menu_opened:
            pyxel.blt(0, 17, 0, 0, 80, 64, 32)
            pyxel.blt(0, 0, 0, 32, 0, 16, 16)
        else:
            if self.menu_opened:
                pyxel.blt(0, 0, 0, 32, 0, 16, 16)
            else: 
                pyxel.blt(0, 0, 0, 0, 0, 16, 16)

        if self.player_turn == 0:
            pyxel.rect(208, 0, 16, 16, pyxel.COLOR_LIME) # carré j1
            pyxel.rect(208, 176, 16, 16, pyxel.COLOR_LIGHT_BLUE) # carré j2
        else:
            pyxel.rect(208, 0, 16, 16, pyxel.COLOR_LIGHT_BLUE) # carré j1
            pyxel.rect(208, 176, 16, 16, pyxel.COLOR_LIME) # carré j2

        pyxel.rect(64, 0, 96, 16, pyxel.COLOR_LIGHT_BLUE) # barre j1 remplie
        pyxel.rect(64, 192 - 16, 96, 16, pyxel.COLOR_LIGHT_BLUE) # barre j2 remplie

        self.draw_texts()

    def draw_texts(self):
        if self.menu_opened:
            pyxel.text(5, 22, "Recommencer", pyxel.COLOR_BLACK) # Position pour que le texte soit centré dans le bouton
            pyxel.text(5, 38, "Quitter", pyxel.COLOR_BLACK) # Position pour que le texte soit centré dans le bouton
        pyxel.text(210, 5, "J 1", pyxel.COLOR_WHITE)
        pyxel.text(210, 182, "J 2", pyxel.COLOR_WHITE)


    def castling(self): # Roque - permet au roi de se déplacer de 2 cases avec une tour
        # Vérifier le tour du joueur actuel
        if self.player_turn == 0:
            # Roque pour les blancs (joueur 1)
            # Récupérer le roi blanc et les tours blanches
            king = self.find_piece_at(4, 0)
            left_rook = self.find_piece_at(0, 0)  # Tour de gauche (case a1)
            right_rook = self.find_piece_at(7, 0)  # Tour de droite (case h1)
            
            # Vérifier que le roi et les tours sont présents et à leur position initiale
            if king and king.type == "king" and left_rook and left_rook.type == "rook" and right_rook and right_rook.type == "rook":
                # Vérifier si le roi blanc est sélectionné
                if self.selected_piece == (4, 0):
                    # TODO: Implémenter la logique du roque blanc
                    # - Vérifier que le roi n'est pas en échec
                    # - Vérifier que les cases entre le roi et la tour sont vides
                    # - Déplacer le roi et la tour
                    # Roque possible pour les blancs
                    pass
        else:
            # Roque pour les noirs (joueur 2)
            # Récupérer le roi noir et les tours noires
            king = self.find_piece_at(4, 7)
            left_rook = self.find_piece_at(0, 7)  # Tour de gauche (case a8)
            right_rook = self.find_piece_at(7, 7)  # Tour de droite (case h8)
            
            # Vérifier que le roi et les tours sont présents et à leur position initiale
            if king and king.type == "king" and left_rook and left_rook.type == "rook" and right_rook and right_rook.type == "rook":
                # Vérifier si le roi noir est sélectionné
                if self.selected_piece == (4, 7):
                    # TODO: Implémenter la logique du roque noir
                    # - Vérifier que le roi n'est pas en échec
                    # - Vérifier que les cases entre le roi et la tour sont vides
                    # - Déplacer le roi et la tour
                    # Roque possible pour les noirs
                    pass
            


#     def __init__(self, type, coords=(0,0), color="white"):
#         self.type = type # le type de pion: "knight", "rook", "pawn", etc..
#         self.x = coords[0] # coordonnée x en numéro de case
#         self.y = coords[1] # y en numéro de case
#         self.alive = True # est vivant ou morte
#         self.possible_moves = [] # les coups possibles ex: [(0,1),(5,2)] 
#         self.color = color # ou "black", la couleur de la pièce



App()