# Fichier piece.py contenant la classe Piece et ses méthodes
# En charge: thomas

class Piece:
    """Classe représentant une pièce d'échecs."""
    def __init__(self, type, coords=(0,0), color="white"):
        self.alive = True
        self.x = coords[0]
        self.y = coords[1]
        self.has_moved = False
        self.color = color
        self.possible_moves = []
        self.board = []
        self.type = type
        self.initial_2steps = False # pour les pions, savoir s'ils ont fait leur premier déplacement de 2 cases (utile pour la prise en passant)
        self.initial_2steps_turn = -1 # pour savoir à quel tour le pion a fait son déplacement initial de 2 cases

    def bouger(self, tours_played: int, x, y):
        """Met à jour les coordonnées de la pièce et son état de déplacement."""
        if not self.has_moved:
            self.has_moved = True
            if (self.color == "white" and y - self.y == 2) or (self.color == "black" and self.y - y == 2): # vérifie si le pion a fait son déplacement initial de 2 cases
                self.initial_2steps = True
                self.initial_2steps_turn = tours_played  # le tour doit être mis à jour dans la méthode update du jeu
        else:
            self.initial_2steps = False
        self.x = x
        self.y = y
    
    def update(self, tours_played: int, pieces_blanches: list["Piece"], pieces_noires: list["Piece"]):
        """Met à jour les coups possibles de la pièce en fonction de sa position actuelle et de l'état du plateau."""

        if self.initial_2steps and tours_played - self.initial_2steps_turn > 1:
            self.initial_2steps = False

        tableau_pieces = [[None for i in range(8)] for i in range(8)]
        for element in pieces_noires:
            if element.alive:
                tableau_pieces[element.y][element.x]=element

        for element in pieces_blanches:
            if element.alive:
                tableau_pieces[element.y][element.x]=element
        
        # ici, on définit toutes les variables puisqu'une fois la boucle lancée, on veut que les modifications apportées fonctionnent correctement
        coup_possible = True
        self.possible_moves = [] #on réinitialise les coups possibles a chaques coups
        if self.type == "pawn":
            if self.color == "white":
                direction = 1
            else:
                direction = -1
            #si la case devant est vide, pour avancer de 1
            if 0 <= self.y + direction <= 7:
                for element in pieces_blanches + pieces_noires:
                    if element.x == self.x and element.y == self.y + direction and element.alive == True:
                        coup_possible = False
                if coup_possible:
                    self.possible_moves.append([self.x, self.y + direction])
                    if not self.has_moved:
                        if 0 <= self.y + direction + direction <= 7:
                            coup_possible = True
                            for element in pieces_blanches + pieces_noires:
                                if element.x == self.x and element.y == self.y + direction + direction and element.alive == True:
                                    coup_possible = False
                            if coup_possible:
                                self.possible_moves.append([self.x, self.y + direction + direction])
            
            for i in [-1,1]:
                for element in pieces_blanches + pieces_noires:
                    if element.x == self.x + i and element.y == self.y + direction and self.color != element.color and element.alive == True:
                        self.possible_moves.append([self.x + i, self.y + direction])
        elif self.type == "rook":
            # je teste les déplacements vers la droite
            case_disponible = True
            case_x = self.x
            case_y = self.y
            while case_disponible and case_x < 7:
                case_x += 1
                # test si la case est disponible (vide ou pièce adversaire)
                case_courrante: Piece=tableau_pieces[case_y][case_x]
                if case_courrante == None:
                    #case vide, je continue
                    self.possible_moves.append([case_x, case_y])
                elif case_courrante.color != self.color:
                    #case occupée par un adversaire, j'ajoute et je m'arrête
                    self.possible_moves.append([case_x, case_y])
                    case_disponible=False
                else:
                    #j'ai rencontré un pion de ma couleur
                    case_disponible=False

            # je teste les déplacements vers la gauche
            case_disponible = True
            case_x = self.x
            case_y = self.y
            while case_disponible and case_x > 0:
                case_x -= 1
                # test si la case est disponible (vide ou pièce adversaire)
                case_courrante: Piece=tableau_pieces[case_y][case_x]
                if case_courrante == None:
                    #case vide, je continue
                    self.possible_moves.append([case_x, case_y])
                elif case_courrante.color != self.color:
                    #case occupée par un adversaire, j'ajoute et je m'arrête
                    self.possible_moves.append([case_x, case_y])
                    case_disponible=False
                else:
                    #j'ai rencontré un pion de ma couleur
                    case_disponible=False

            # je teste les déplacements vers le bas
            case_disponible = True
            case_x = self.x
            case_y = self.y
            while case_disponible and case_y < 7:
                case_y += 1
                # test si la case est disponible (vide ou pièce adversaire)
                case_courrante: Piece=tableau_pieces[case_y][case_x]
                if case_courrante == None:
                    #case vide, je continue
                    self.possible_moves.append([case_x, case_y])
                elif case_courrante.color != self.color:
                    #case occupée par un adversaire, j'ajoute et je m'arrête
                    self.possible_moves.append([case_x, case_y])
                    case_disponible=False
                else:
                    #j'ai rencontré un pion de ma couleur
                    case_disponible=False

            # je teste les déplacements vers le haut
            case_disponible = True
            case_x = self.x
            case_y = self.y
            while case_disponible and case_y > 0:
                case_y -= 1
                # test si la case est disponible (vide ou pièce adversaire)
                case_courrante: Piece=tableau_pieces[case_y][case_x]
                if case_courrante == None:
                    #case vide, je continue
                    self.possible_moves.append([case_x, case_y])
                elif case_courrante.color != self.color:
                    #case occupée par un adversaire, j'ajoute et je m'arrête
                    self.possible_moves.append([case_x, case_y])
                    case_disponible=False
                else:
                    #j'ai rencontré un pion de ma couleur
                    case_disponible=False
        elif self.type == "bishop":
            case_disponible = True
            case_x = self.x
            case_y = self.y
            while case_disponible and case_x < 7 and case_y < 7:
                case_x += 1
                case_y += 1
                # test si la case est disponible (vide ou pièce adversaire)
                case_courrante: Piece=tableau_pieces[case_y][case_x]
                if case_courrante == None:
                    #case vide, je continue
                    self.possible_moves.append([case_x, case_y])
                elif case_courrante.color != self.color:
                    #case occupée par un adversaire, j'ajoute et je m'arrête
                    self.possible_moves.append([case_x, case_y])
                    case_disponible=False
                else:
                    #j'ai rencontré un pion de ma couleur
                    case_disponible=False
            case_disponible = True
            case_x = self.x
            case_y = self.y
            while case_disponible and case_x > 0 and case_y < 7:
                case_x -= 1
                case_y += 1
                # test si la case est disponible (vide ou pièce adversaire)
                case_courrante: Piece=tableau_pieces[case_y][case_x]
                if case_courrante == None:
                    #case vide, je continue
                    self.possible_moves.append([case_x, case_y])
                elif case_courrante.color != self.color:
                    #case occupée par un adversaire, j'ajoute et je m'arrête
                    self.possible_moves.append([case_x, case_y])
                    case_disponible=False
                else:
                    #j'ai rencontré un pion de ma couleur
                    case_disponible=False
            case_disponible = True
            case_x = self.x
            case_y = self.y
            while case_disponible and case_x < 7 and case_y > 0:
                case_x += 1
                case_y -= 1
                # test si la case est disponible (vide ou pièce adversaire)
                case_courrante: Piece=tableau_pieces[case_y][case_x]
                if case_courrante == None:
                    #case vide, je continue
                    self.possible_moves.append([case_x, case_y])
                elif case_courrante.color != self.color:
                    #case occupée par un adversaire, j'ajoute et je m'arrête
                    self.possible_moves.append([case_x, case_y])
                    case_disponible=False
                else:
                    #j'ai rencontré un pion de ma couleur
                    case_disponible=False
            case_disponible = True
            case_x = self.x
            case_y = self.y
            while case_disponible and case_x > 0 and case_y > 0:
                case_x -= 1
                case_y -= 1
                # test si la case est disponible (vide ou pièce adversaire)
                case_courrante: Piece=tableau_pieces[case_y][case_x]
                if case_courrante == None:
                    #case vide, je continue
                    self.possible_moves.append([case_x, case_y])
                elif case_courrante.color != self.color:
                    #case occupée par un adversaire, j'ajoute et je m'arrête
                    self.possible_moves.append([case_x, case_y])
                    case_disponible=False
                else:
                    #j'ai rencontré un pion de ma couleur
                    case_disponible=False
        elif self.type == "queen":
            # je teste les déplacements vers la droite
            case_disponible = True
            case_x = self.x
            case_y = self.y
            while case_disponible and case_x < 7:
                case_x += 1
                # test si la case est disponible (vide ou pièce adversaire)
                case_courrante: Piece=tableau_pieces[case_y][case_x]
                if case_courrante == None:
                    #case vide, je continue
                    self.possible_moves.append([case_x, case_y])
                elif case_courrante.color != self.color:
                    #case occupée par un adversaire, j'ajoute et je m'arrête
                    self.possible_moves.append([case_x, case_y])
                    case_disponible=False
                else:
                    #j'ai rencontré un pion de ma couleur
                    case_disponible=False

            # je teste les déplacements vers la gauche
            case_disponible = True
            case_x = self.x
            case_y = self.y
            while case_disponible and case_x > 0:
                case_x -= 1
                # test si la case est disponible (vide ou pièce adversaire)
                case_courrante: Piece=tableau_pieces[case_y][case_x]
                if case_courrante == None:
                    #case vide, je continue
                    self.possible_moves.append([case_x, case_y])
                elif case_courrante.color != self.color:
                    #case occupée par un adversaire, j'ajoute et je m'arrête
                    self.possible_moves.append([case_x, case_y])
                    case_disponible=False
                else:
                    #j'ai rencontré un pion de ma couleur
                    case_disponible=False

            # je teste les déplacements vers le bas
            case_disponible = True
            case_x = self.x
            case_y = self.y
            while case_disponible and case_y < 7:
                case_y += 1
                # test si la case est disponible (vide ou pièce adversaire)
                case_courrante: Piece=tableau_pieces[case_y][case_x]
                if case_courrante == None:
                    #case vide, je continue
                    self.possible_moves.append([case_x, case_y])
                elif case_courrante.color != self.color:
                    #case occupée par un adversaire, j'ajoute et je m'arrête
                    self.possible_moves.append([case_x, case_y])
                    case_disponible=False
                else:
                    #j'ai rencontré un pion de ma couleur
                    case_disponible=False

            # je teste les déplacements vers le haut
            case_disponible = True
            case_x = self.x
            case_y = self.y
            while case_disponible and case_y > 0:
                case_y -= 1
                # test si la case est disponible (vide ou pièce adversaire)
                case_courrante: Piece=tableau_pieces[case_y][case_x]
                if case_courrante == None:
                    #case vide, je continue
                    self.possible_moves.append([case_x, case_y])
                elif case_courrante.color != self.color:
                    #case occupée par un adversaire, j'ajoute et je m'arrête
                    self.possible_moves.append([case_x, case_y])
                    case_disponible=False
                else:
                    #j'ai rencontré un pion de ma couleur
                    case_disponible=False
            case_disponible = True
            case_x = self.x
            case_y = self.y
            while case_disponible and case_x < 7 and case_y < 7:
                case_x += 1
                case_y += 1
                # test si la case est disponible (vide ou pièce adversaire)
                case_courrante: Piece=tableau_pieces[case_y][case_x]
                if case_courrante == None:
                    #case vide, je continue
                    self.possible_moves.append([case_x, case_y])
                elif case_courrante.color != self.color:
                    #case occupée par un adversaire, j'ajoute et je m'arrête
                    self.possible_moves.append([case_x, case_y])
                    case_disponible=False
                else:
                    #j'ai rencontré un pion de ma couleur
                    case_disponible=False
            case_disponible = True
            case_x = self.x
            case_y = self.y
            while case_disponible and case_x > 0 and case_y < 7:
                case_x -= 1
                case_y += 1
                # test si la case est disponible (vide ou pièce adversaire)
                case_courrante: Piece=tableau_pieces[case_y][case_x]
                if case_courrante == None:
                    #case vide, je continue
                    self.possible_moves.append([case_x, case_y])
                elif case_courrante.color != self.color:
                    #case occupée par un adversaire, j'ajoute et je m'arrête
                    self.possible_moves.append([case_x, case_y])
                    case_disponible=False
                else:
                    #j'ai rencontré un pion de ma couleur
                    case_disponible=False
            case_disponible = True
            case_x = self.x
            case_y = self.y
            while case_disponible and case_x < 7 and case_y > 0:
                case_x += 1
                case_y -= 1
                # test si la case est disponible (vide ou pièce adversaire)
                case_courrante: Piece=tableau_pieces[case_y][case_x]
                if case_courrante == None:
                    #case vide, je continue
                    self.possible_moves.append([case_x, case_y])
                elif case_courrante.color != self.color:
                    #case occupée par un adversaire, j'ajoute et je m'arrête
                    self.possible_moves.append([case_x, case_y])
                    case_disponible=False
                else:
                    #j'ai rencontré un pion de ma couleur
                    case_disponible=False
            case_disponible = True
            case_x = self.x
            case_y = self.y
            while case_disponible and case_x > 0 and case_y > 0:
                case_x -= 1
                case_y -= 1
                # test si la case est disponible (vide ou pièce adversaire)
                case_courrante: Piece=tableau_pieces[case_y][case_x]
                if case_courrante == None:
                    #case vide, je continue
                    self.possible_moves.append([case_x, case_y])
                elif case_courrante.color != self.color:
                    #case occupée par un adversaire, j'ajoute et je m'arrête
                    self.possible_moves.append([case_x, case_y])
                    case_disponible=False
                else:
                    #j'ai rencontré un pion de ma couleur
                    case_disponible=False
        elif self.type == "king":
            #on itere sur les tuples pour savoir si le coups est possible à ces coordonnées relatives
            directions = [[1,0],[1,-1],[1,1],[0,-1],[0,0],[0,1],[-1,-1],[-1,0],[-1,1]]
            for dx, dy in directions: #découvert en faisant des tests que mettre deux variables en même temps fonctionne
                nx = self.x + dx
                ny = self.y + dy
                if 0 <= nx <= 7 and 0 <= ny <= 7:
                    piece = tableau_pieces[ny][nx]
                    if piece == None or piece.color != self.color:
                        self.possible_moves.append([nx,ny])
        elif self.type == "knight":
            #on applique la même logique que pour le roi avec les positions relatives. juste que cette fois ci, les deplacements
            #correspondent à ceux du cavalier
            directions = [[1, 2],[2, 1],[2, -1],[1, -2],[-1, -2],[-2, -1],[-2, 1],[-1, 2]]
            for dx, dy in directions:
                nx = self.x + dx
                ny = self.y + dy
                if 0 <= nx <= 7 and 0 <= ny <= 7:
                    piece = tableau_pieces[ny][nx]
                    if piece == None or piece.color != self.color:
                        self.possible_moves.append([nx,ny])

    def deplacement(self, x, y):
        """cette fonction prend en argument une piece et les coordonnées de destination sélectionnées et renvoie un booleen pour
        dire si le coup peut être joué ou pas"""
        return (x, y) in self.possible_moves