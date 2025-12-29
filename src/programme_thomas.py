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
    
    def update(self, pieces: list["Piece"]):
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
        for x in range(8):
            for y in range(8):
                if self.type == "pawn":
                    if self.color == "white": #si le pion est blanc
                        if x-1 == self.x:
                            for element in pieces:
                                if element.x == x and element.y == y:
                                    coup_possible = False
                                elif element.x == x+1 and element.y == y+1:
                                    self.possible_moves.append([x+1,y+1])
                                elif element.x == x+1 and element.y == y-1:
                                    self.possible_moves.append([x+1,y-1])
                            if coup_possible:
                                self.possible_moves.append([x,y])
                    else: #si le pion est noir
                        if x+1 == self.x:
                            for element in pieces:
                                if element.x == x and element.y == y:
                                    coup_possible = False
                                elif element.x == x-1 and element.y == y+1:
                                    self.possible_moves.append([x-1,y+1])
                                elif element.x == x-1 and element.y == y-1:
                                    self.possible_moves.append([x-1,y-1])
                            if coup_possible:
                                self.possible_moves.append([x,y])
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