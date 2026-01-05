#le code n'est pas fini mais si quelqu'un veut lire où j'en suis, voilà un aperçu


class Piece:
    def __init__(self, type, coords=(0,0), color="white"):
        self.alive = True
        self.x = coords[0]
        self.y = coords[1]
        self.has_moved = False
        self.color = color
        self.possible_moves = []
        self.board = []
        self.type = type


    def bouger(self, x, y):
        if not self.has_moved:
            self.has_moved = True
        self.x = x
        self.y = y

    """def update(self, pieces):
        self.possible_moves = []
        if self.type == "pawn": #pions
            if self.color == "white":
                if self.x + 1 < 8:
                    self.possible_moves.append([self.x+1,self.y])
            else:
                if self.x - 1 >= 0:
                    self.possible_moves.append([self.x-1,self.y])
        elif self.type == "rook": #tour
            coup_possible = True
            for i in range(self.x,8):
                for j in range(pieces):
                    if [self.x + i, self.y] == pieces[1]:
                        #cette partie du code permet de savoir si on peut ajouter un coup a la liste
                        #pas possible de "sauter" par dessus un pion
                        if pieces.color != self.color:
                            self.possible_moves.append[self.x + i,self.y]
                        coup_possible = False
                if not coup_possible:
                    self.possible_moves.append[self.x + i,self.y]
            coup_possible = True
            for i in range(self.x,-1, -1):
                for j in range(pieces):
                    if [self.x + i, self.y] == pieces[1]: 
                        if pieces.color != self.color:
                            self.possible_moves.append[self.x + i,self.y]
                        coup_possible = False
                if not coup_possible:
                    self.possible_moves.append[self.x + i,self.y]
            coup_possible = True
            for i in range(self.y,8):
                for j in range(pieces):
                    if [self.x, self.y + i] == pieces[1]: 
                        if pieces.color != self.color:
                            self.possible_moves.append[self.x,self.y + i]
                        coup_possible = False
                if not coup_possible:
                    self.possible_moves.append[self.x,self.y + i]
            coup_possible = True
            for i in range(self.y,-1, -1):
                for j in range(pieces):
                    if [self.x, self.y + i] == pieces[1]: 
                        if pieces.color != self.color:
                            self.possible_moves.append[self.x,self.y + i]
                        coup_possible = False
                if not coup_possible:
                    self.possible_moves.append[self.x,self.y + i]
        elif self.type == "knight": #cavalier
            for i in range(4): #4 possibilités: haut, bas, gauche, droite
                for j in range(2):
                    if 
        elif self.type == "bishop": #fou
            pass
        elif self.type == "queen": #rennes
            pass
        else: #pour le roi
            pass""" #j'ai tout mis dans une docstring parce qu'on sait jamais
    
    def get_positions_theoriques_pawn(self, pieces_adverses: list["Piece"]):
        """
        Docstring for get_positions_theoriques_pawn
        
        :param self: Description
        :param pieces_adverses: Utile pour déterminer si le pion peut faire un coup en diagonale
        :type pieces_adverses: list["Piece"]
        """
        if self.color == "white":
            self.possible_moves.append([self.x, self.y + 1])
            for element in pieces_adverses:
                if element.x == self.x + 1 and element.y == self.y + 1:
                    self.possible_moves.append([self.x + 1, self.y + 1])
                elif element.x == self.x - 1 and element.y == self.y + 1:
                    self.possible_moves.append([self.x - 1, self.y + 1])
            if not self.has_moved:
                self.possible_moves.append([self.x, self.y + 2])
        elif self.color == "black":
            self.possible_moves.append([self.x, self.y - 1])
            for element in pieces_adverses:
                if element.x == self.x + 1 and element.y == self.y - 1:
                    self.possible_moves.append([self.x + 1, self.y - 1])
                elif element.x == self.x - 1 and element.y == self.y - 1:
                    self.possible_moves.append([self.x - 1, self.y - 1])
            if not self.has_moved:
                self.possible_moves.append([self.x, self.y - 2])

    def get_position_theorique_rook(self, pieces_adverses):
        min_x = 0
        max_x = 7
        min_y = 0
        max_y = 7
        """ici, je fais 2 boucles, une pour x et une pour y. J'ajoute toutes les cases sur la ligne et la colonne de la tour comme theoriquement possible
        excepté là où il se trouve déjà"""

        for element in pieces_adverses:
            if element.x < self.x and min_x < element.x:
                min_x = element.x
            elif element.x > self.x and max_x > element.x:
                max_x = element.x
            elif element.y < self.y and min_y < element.y:
                min_y = element.y
            elif element.y > self.y and max_y > element.y:
                max_x = element.y
        for i in range(8): #je fais d'abord pour x
                if min_x <= i and i <= max_x and i != self.x:
                    self.possible_moves.append([i, self.y])
        for i in range(8): #je fais pour y
            if i != self.y and min_y <= i and i <= max_y:
                self.possible_moves.append([self.x, i])

    def get_position_theorique_bishop(self):
        pass
        
    def get_position_theorique_knight(self):
        pass

    def get_position_theorique_queen(self):
        pass

    def get_position_theorique_king(self):
        pass

    def get_positions_theoriques(self, pieces_adverses: list["Piece"]):
        if self.type == "pawn":
            self.get_positions_theoriques_pawn(pieces_adverses)
        elif self.type == "rook":
            self.get_position_theorique_rook(pieces_adverses)
        elif self.type == "bishop":
            self.get_position_theorique_bishop()

    def limites_plateau(self):
        coups_impossibles = []
        nb_coups = 0 #il permet de, faire en sorte que lors de la suppression des elements de la liste de coups, le décalage qui se crée naturellement avec pop soit corrigé
        for i in range(len(self.possible_moves)):
            if self.possible_moves[i][0] > 7 or self.possible_moves[i][0] < 0 or self.possible_moves[i][1] > 7 or self.possible_moves[i][1] < 0:
                coups_impossibles.append(i - nb_coups)
                nb_coups += 1
        for i in range(len(coups_impossibles)):
            self.possible_moves[coups_impossibles[i]].pop()
    
    def collision(self, pieces_alliees: list["Piece"]):
        collision = []
        correction_decalage = 0
        for i in range(len(pieces_alliees)):
            for j in range(len(self.possible_moves)):
                if pieces_alliees[i].x == self.possible_moves[j][0] and pieces_alliees[i].y == self.possible_moves[j][1]:
                    collision.append(j - correction_decalage)
                    correction_decalage += 1
        for i in range(len(collision)):
            self.possible_moves[collision[i]].pop()

    def update_papa(self, pieces_blanches: list["Piece"], pieces_noires: list["Piece"]):
        self.possible_moves = [] #on réinitialise la liste de coups possibles
        # mets a jour la liste des coups possibles pour une pièce (self)
        # calcul des coups possibles pour la pièce en fonction de la position des autres pions de la même couleur
            # calcul des positions théoriques en fonction du type de piece
            # detection sortie du plateau
            # detection collision avec pièce de la même couleur
        if self.color == "white":
            self.get_positions_theoriques(pieces_noires)
        elif self.color == "black":
            self.get_positions_theoriques(pieces_blanches)
        self.limites_plateau #on enleve les coups qui tapent hors du plateau
        if self.color == "white":
            self.collision(pieces_blanches)
        elif self.color == "black":
            self.collision(pieces_noires)


    def update(self, pieces_blanches: list["Piece"], pieces_noires: list["Piece"]):

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
                    if element.x == self.x and element.y == self.y + direction:
                        coup_possible = False
                if coup_possible:
                    self.possible_moves.append([self.x, self.y + direction])
                    if not self.has_moved:
                        if 0 <= self.y + direction + direction<= 7:
                            for element in pieces_blanches + pieces_noires:
                                if element.x == self.x and element.y == self.y + direction:
                                    coup_possible = False
                            if coup_possible:
                                self.possible_moves.append([self.x, self.y + direction + direction])
            
            for i in [-1,1]:
                for element in pieces_blanches + pieces_noires:
                    if element.x == self.x + i and element.y == self.y + direction and self.color != element.color:
                        self.possible_moves.append([self.x + i, self.y + direction])

            


            """if self.color == "white":
                for element in pieces_noires:
                    if element.x == self.x + 1 and element.y == self.y + 1:
                        self.possible_moves.append([self.x + 1, self.y + 1])
                    elif element.x == self.x - 1 and element.y == self.y + 1:
                        self.possible_moves.append([self.x - 1, self.y + 1])
                    elif element.x == self.x and element.y == self.y + 1:
                        coup_possible = False
                    elif not self.has_moved and not element.x == self.x and not element.y == self.y + 2 and coup_possible == True:
                        self.possible_moves.append([self.x, self.y + 2])
                if coup_possible == True:
                    self.possible_moves.append([self.x, self.y + 1])

            elif self.color == "black":
                for element in pieces_blanches:
                    if element.x == self.x + 1 and element.y == self.y - 1:
                        self.possible_moves.append([self.x + 1, self.y - 1])
                    elif element.x == self.x - 1 and element.y == self.y - 1:
                        self.possible_moves.append([self.x - 1, self.y - 1])
                    elif element.x == self.x and element.y == self.y - 1:
                        coup_possible = False
                    elif not self.has_moved and not element.x == self.x and not element.y == self.y - 2 and coup_possible == True:
                        self.possible_moves.append([self.x, self.y - 2])
                if coup_possible == True:
                    self.possible_moves.append([self.x, self.y - 1])"""
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

    def update_v0(self, pieces: list["Piece"]):
        # ici, on définit toutes les variables puisqu'une fois la boucle lancée, on veut que les modifications apportées fonctionnent correctement
        coup_possible = True
        limites_cree = False
        limit_max_x = 7
        limit_mini_x = 0
        limit_max_y = 7
        limit_mini_y = 0
        plus_plus = 7
        plus_moins = 7
        moins_moins = -7
        moins_plus = -7
        liste_provisoire = []
        self.possible_moves = [] #on réinitialise les coups possibles a chaques coups
        """on calcul, selon le type de pion, les coups possibles en prenant en compte les pions de sa couleur et ceux de
        l'adversaire"""
        for x in range(8):
            for y in range(8):
                if self.type == "pawn":
                    avance_un = True
                    avance_deux = True
                    if self.color == "white": #si le pion est blanc
                        if x == self.x:
                            for element in pieces:
                                if element.color != self.color:
                                    if element.x == self.x + 1 and element.y == self.y + 1:
                                        self.possible_moves.append([x + 1,y + 1])
                                    elif element.x == self.x - 1 and element.y == self.y + 1:
                                        self.possible_moves.append([x - 1,y + 1])
                                    elif  element.x == self.x and element.y == self.y + 1:
                                        coup_possible = False
                                        avance_un = False
                                    elif  element.x == self.x and element.y == self.y + 2:
                                        coup_possible = False
                                        avance_deux = False
                            if self.x == x and self.y + 1 == y and avance_un == True:
                                self.possible_moves.append([x,y])
                                coup_possible = True
                            elif self.x == x and self.y + 2 == y and not self.has_moved and avance_deux == True and coup_possible == True:
                                self.possible_moves.append([x,y])
                                coup_possible = True
                    else: #si le pion est noir
                        if x == self.x:
                            for element in pieces:
                                if element.color != self.color:
                                    if element.x == self.x + 1 and element.y == self.y - 1:
                                        self.possible_moves.append([x + 1,y + 1])
                                    elif element.x == self.x - 1 and element.y == self.y - 1:
                                        self.possible_moves.append([x - 1,y + 1])
                                    elif  element.x == self.x and element.y == self.y - 1:
                                        coup_possible = False
                                        avance_un = False
                                    elif  element.x == self.x and element.y == self.y - 2:
                                        coup_possible = False
                                        avance_deux = False
                            if self.x == x and self.y - 1 == y and avance_un == True:
                                self.possible_moves.append([x,y])
                                coup_possible = True
                            elif self.x == x and self.y - 2 == y and not self.has_moved and avance_deux == True and coup_possible == True:
                                self.possible_moves.append([x,y])
                                coup_possible = True
                elif self.type == "rook":
                    if not limites_cree:
                        #si les limites de déplacement ne sont pas créés, ont les créer pour savoir quelles pieces limites
                        for element in pieces:
                            if element.x == self.x and limit_mini_y < element.y < self.y:
                                if element.color != self.color:
                                    limit_mini_y = element.y
                                else:
                                    limit_mini_y = element.y + 1
                            elif element.x == self.x and element.y > self.y:
                                if element.color != self.color:
                                    limit_max_y = element.y
                                else:
                                    limit_max_y = element.y - 1
                            elif element.y == self.y and limit_mini_x < element.x < self.x:
                                if element.color != self.color:
                                    limit_mini_x = element.x
                                else:
                                    limit_mini_x = element.x + 1
                            elif element.y == self.y and element.x > self.x:
                                if element.color != self.color:
                                    limit_mini_x = element.y
                                else:
                                    limit_mini_x = element.y + 1
                        limites_cree = True
                    """cette partie de la fonction vérifie si la case sélectionnée avec les 2 boucles for est accessible par la tour.
                    Elle vérifie aussi si, dans le cas où une piece barre la route, elle est dans la meme équipe ou si elle est adversaire auquel cas elle doit être accessible par la tour"""
                    if x == self.x and limit_mini_y <= y <= limit_max_y:
                        self.possible_moves.append([x,y])
                    elif y == self.y and limit_mini_x <= x <= limit_max_x:
                        self.possible_moves.append([x,y])
                elif self.type == "bishop":
                    if not limites_cree:
                        X = self.x
                        Y = self.y
                        limite_calcul = 0
                        while X > 0 or Y > 0:
                            X -= 1
                            Y -= 1
                            limite_calcul -= 1
                        moins_moins = limite_calcul

                        X = self.x
                        Y = self.y
                        while X < 7 and Y < 7:
                            X += 1
                            Y += 1
                            limite_calcul += 1
                        plus_plus = limite_calcul

                        X = self.x
                        Y = self.y
                        while X > 0 and Y < 7:
                            X -= 1
                            Y += 1
                            limite_calcul -=1
                        moins_plus = limite_calcul

                        X = self.x
                        Y = self.y
                        while X < 7 and Y > 0:
                            X += 1
                            Y -= 1
                            limite_calcul +=1
                        plus_moins = limite_calcul
                        
                        limites_cree = True
                        for element in pieces:
                            if element.x < self.x and element.y < self.y:
                                if self.x - element.x > moins_moins and self.y - element.y > moins_moins:
                                    if self.x - element.x == self.y - element.y:
                                        if self.color != element.color:
                                            moins_moins = self.x - element.x
                                        else:
                                            moins_moins = self.x - element.x + 1
                            elif element.x > self.x and element.y > self.y:
                                if self.x - element.x < plus_plus and self.y - element.y < plus_plus:
                                    if self.x - element.x == self.y - element.y:
                                        if self.color != element.color:
                                            plus_plus = self.y - element.y
                                        else:
                                            plus_plus = self.y - element.y - 1
                            elif element.x > self.x and element.y < self.y:
                                if self.x - element.x < plus_moins and ((self.y - element.y) * -1) < plus_moins:
                                    if self.x - element.x == (self.y*(-1)) - element.y < plus_moins:
                                        if self.color != element.color:
                                            plus_moins = self.x - element.x
                                        else:
                                            plus_moins = self.x - element.x - 1
                            elif element.x < self.x and element.y > self.y:
                                if self.x - element.x > moins_plus and self.y - element.y < moins_plus:
                                    if self.x - element.x == (self.y*(-1)) - element.y:
                                        if self.color != element.color:
                                            moins_plus = self.x - element.x
                                        else:
                                            moins_plus = self.x - element.x + 1
                    else:
                        if x - self.x == y - self.y:
                            if x - self.x >= moins_moins and x - self.x <= plus_plus:
                                self.possible_moves.append([x,y])
                        elif x - self.x == (y - self.y) * -1:
                            if x - self.x >= moins_plus and x - self.x <= plus_moins:
                                self.possible_moves.append([X,y])
                elif self.type == "queen":
                    if not limites_cree:
                        X = self.x
                        Y = self.y
                        limite_calcul = 0
                        while X > 0 or Y > 0:
                            X -= 1
                            Y -= 1
                            limite_calcul -= 1
                        moins_moins = limite_calcul

                        X = self.x
                        Y = self.y
                        while X < 7 and Y < 7:
                            X += 1
                            Y += 1
                            limite_calcul += 1
                        plus_plus = limite_calcul

                        X = self.x
                        Y = self.y
                        while X > 0 and Y < 7:
                            X -= 1
                            Y += 1
                            limite_calcul -=1
                        moins_plus = limite_calcul

                        X = self.x
                        Y = self.y
                        while X < 7 and Y > 0:
                            X += 1
                            Y -= 1
                            limite_calcul +=1
                        plus_moins = limite_calcul
                        
                        for element in pieces:
                            if element.x == self.x and limit_mini_y < element.y < self.y:
                                if element.color != self.color:
                                    limit_mini_y = element.y
                                else:
                                    limit_mini_y = element.y + 1
                            elif element.x == self.x and element.y > self.y:
                                if element.color != self.color:
                                    limit_max_y = element.y
                                else:
                                    limit_max_y = element.y - 1
                            elif element.y == self.y and limit_mini_x < element.x < self.x:
                                if element.color != self.color:
                                    limit_mini_x = element.x
                                else:
                                    limit_mini_x = element.x + 1
                            elif element.y == self.y and element.x > self.x:
                                if element.color != self.color:
                                    limit_mini_x = element.y
                                else:
                                    limit_mini_x = element.y + 1
                            elif element.x < self.x and element.y < self.y:
                                if self.x - element.x > moins_moins and self.y - element.y > moins_moins:
                                    if self.x - element.x == self.y - element.y:
                                        if self.color != element.color:
                                            moins_moins = self.x - element.x
                                        else:
                                            moins_moins = self.x - element.x + 1
                            elif element.x > self.x and element.y > self.y:
                                if self.x - element.x < plus_plus and self.y - element.y < plus_plus:
                                    if self.x - element.x == self.y - element.y:
                                        if self.color != element.color:
                                            plus_plus = self.y - element.y
                                        else:
                                            plus_plus = self.y - element.y - 1
                            elif element.x > self.x and element.y < self.y:
                                if self.x - element.x < plus_moins and ((self.y - element.y) * -1) < plus_moins:
                                    if self.x - element.x == (self.y*(-1)) - element.y < plus_moins:
                                        if self.color != element.color:
                                            plus_moins = self.x - element.x
                                        else:
                                            plus_moins = self.x - element.x - 1
                            elif element.x < self.x and element.y > self.y:
                                if self.x - element.x > moins_plus and self.y - element.y < moins_plus:
                                    if self.x - element.x == (self.y*(-1)) - element.y:
                                        if self.color != element.color:
                                            moins_plus = self.x - element.x
                                        else:
                                            moins_plus = self.x - element.x + 1
                    else:
                        if x - self.x == y - self.y:
                            if moins_moins <= x - self.x <= plus_plus:
                                self.possible_moves.append([x,y])
                        elif x - self.x == (y - self.y) * -1:
                            if moins_plus <= x - self.x <= plus_moins:
                                self.possible_moves.append([X,y])
                        elif x == self.x and limit_mini_y <= y <= limit_max_y:
                            self.possible_moves.append([x,y])
                        elif y == self.y and limit_mini_x <= x <= limit_max_x:
                            self.possible_moves.append([x,y])
                elif self.type == "knight":
                    if not len(liste_provisoire): # préférable de vérifier si la longueur est nulle que de comparer à une liste vide ou de dire "not liste_provisoire"
                        if self.x + 1 == x and self.y + 2 == y:
                            liste_provisoire.append([x,y])
                        elif self.x - 1 == x and self.y + 2 == y:
                            liste_provisoire.append([x,y])
                        elif self.x + 1 == x and self.y - 2 == y:
                            liste_provisoire.append([x,y])
                        elif self.x - 1 == x and self.y - 2 == y:
                            liste_provisoire.append([x,y])
                        elif self.x + 2 == x and self.y + 1 == y:
                            liste_provisoire.append([x,y])
                        elif self.x + 2 == x and self.y - 1 == y:
                            liste_provisoire.append([x,y])
                        elif self.x - 2 == x and self.y + 1 == y:
                            liste_provisoire.append([x,y])
                        elif self.x - 2 == x and self.y - 1 == y:
                            liste_provisoire.append([x,y])
                    for element in pieces:
                        if element.color == self.color:
                            for i in range(len(liste_provisoire)):
                                if (element.x, element.y) == liste_provisoire[i]:
                                    liste_provisoire.pop(i)
                    self.possible_moves.extend(liste_provisoire) # on ajoute tous les éléments de la liste provisoire à possible_moves d'un coup
                elif self.type == "king":
                    if not len(liste_provisoire):
                        if self.x + 1 == x and self.y == y:
                            liste_provisoire.append([x,y])
                        elif self.x + 1 == x and self.y + 1 == y:
                            liste_provisoire.append([x,y])
                        elif self.x + 1 == x and self.y - 1 == y:
                            liste_provisoire.append([x,y])
                        elif self.x - 1 == x and self.y == y:
                            liste_provisoire.append([x,y])
                        elif self.x - 1 == x and self.y + 1 == y:
                            liste_provisoire.append([x,y])
                        elif self.x - 1 == x and self.y - 1 == y:
                            liste_provisoire.append([x,y])
                        elif self.x == x and self.y + 1 == y:
                            liste_provisoire.append([x,y])
                        elif self.x == x and self.y - 1 == y:
                            liste_provisoire.append([x,y])
                    for element in pieces:
                        if element.color == self.color:
                            for i in range(len(liste_provisoire)):
                                if liste_provisoire[i] == (element.x, element.y):
                                    liste_provisoire.pop(i)
                    
                    



    def deplacement(self, x, y):
        """cette fonction prend en argument une piece et les coordonnées de destination sélectionnées et renvoie un booleen pour
        dir si le coup peut être joué ou pas"""
        return (x, y) in self.possible_moves