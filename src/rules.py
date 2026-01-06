# src/rules.py - Gestion des règles spéciales des échecs
# En charge: owen

import src.app
import src.utils
import src.piece

def check_rules(app: src.app.App) -> None:
    """Vérifie et applique les règles spéciales des échecs lors d'un déplacement de pièce."""

    castling(app)
    en_passant(app)

def promotion(app: src.app.App) -> None:
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
        if app.player_turn == 0: # promotion pour les blancs
            for piece in app.pieces_white: # on parcourt les pièces blanches
                if piece.type == "pawn" and piece.y == 7 and piece.alive:
                    app.waiting_promotion = piece
        else: # promotion pour les noirs
            for piece in app.pieces_black: # on parcourt les pièces noires
                if piece.type == "pawn" and piece.y == 0 and piece.alive:
                    app.waiting_promotion = piece

def castling_move(app: src.app.App) -> None:
    """Effectue le roque aux échecs quand le joueur le demande."""
    if app.castling_possible["white"] and app.player_turn == 0:
        king = src.utils.find_piece_at(app, 4, 0)
        if (2, 0) in king.possible_moves: # roque côté dame
            rook = src.utils.find_piece_at(app, 0, 0)
            rook.bouger(3, 0)
            king.bouger(2, 0)
            app.castling_possible["white"] = False # on reset la possibilité de roque pour les blancs
            app.next_turn()
        else: # roque côté roi
            rook = src.utils.find_piece_at(app, 7, 0)
            rook.bouger(5, 0)
            king.bouger(6, 0)
            app.next_turn()
        app.castling_possible["white"] = False # on reset la possibilité de roque pour les blancs
    elif app.castling_possible["black"] and app.player_turn == 1:
        king = src.utils.find_piece_at(app, 4, 7)
        if (2, 7) in king.possible_moves: # roque côté dame
            rook = src.utils.find_piece_at(app, 0, 7)
            rook.bouger(3, 7)
            king.bouger(2, 7)
            app.next_turn()
        else: # roque côté roi
            rook = src.utils.find_piece_at(app, 7, 7)
            rook.bouger(5, 7)
            king.bouger(6, 7)
            app.next_turn()
        app.castling_possible["black"] = False # on reset la possibilité de roque pour les noirs

def castling(app: src.app.App) -> None:
    """Vérifie si le roque est possible et l'ajoute aux coups possibles du roi."""
    # Vérifier le tour du joueur actuel tu voc plus??
    if app.player_turn == 0: # Roque pour les blancs (joueur 1)
        # Récupérer le roi blanc et les tours blanches
        king = src.utils.find_piece_at(app, 4, 0)
        left_rook = src.utils.find_piece_at(app, 0, 0)  # Tour de gauche (case a1)
        right_rook = src.utils.find_piece_at(app, 7, 0)  # Tour de droite (case h1)
        if king and king.type == "king" and left_rook and left_rook.type == "rook" and right_rook and right_rook.type == "rook": # Vérifier que le roi et les tours sont présents et à leur position initiale
            if app.selected_piece and app.selected_piece == [4, 0]: # Vérifier si le roi blanc est sélectionné
                if not src.utils.find_piece_at(app, 1, 0) and not src.utils.find_piece_at(app, 2, 0) and not src.utils.find_piece_at(app, 3, 0): # Roque côté dame
                    if left_rook.has_moved == False and king.has_moved == False: # Vérifier que ni le roi ni la tour n'ont bougé
                        if (2,0) not in king.possible_moves: king.possible_moves.append((2, 0)) # ajouter le roque côté dame aux coups possibles du roi
                        app.castling_possible["white"] = True # indiquer que le roque côté dame est possible pour les blancs
                if not src.utils.find_piece_at(app, 5, 0) and not src.utils.find_piece_at(app, 6, 0): # Roque côté roi
                    if right_rook.has_moved == False and king.has_moved == False:
                        if (6,0) not in king.possible_moves: king.possible_moves.append((6, 0)) # ajouter le roque côté roi aux coups possibles du roi
                        app.castling_possible["white"] = True # indiquer que le roque côté roi est possible pour les blancs
    else: # Roque pour les noirs (joueur 2)
        # Récupérer le roi noir et les tours noires
        king = src.utils.find_piece_at(app, 4, 7)
        left_rook = src.utils.find_piece_at(app, 0, 7)  # Tour de gauche (case a8)
        right_rook = src.utils.find_piece_at(app, 7, 7)  # Tour de droite (case h8)
        if king and king.type == "king" and left_rook and left_rook.type == "rook" and right_rook and right_rook.type == "rook": # Vérifier que le roi et les tours sont présents et à leur position initiale
            if app.selected_piece and app.selected_piece == [4, 7]: # Vérifier si le roi noir est sélectionné
                if not src.utils.find_piece_at(app, 1, 7) and not src.utils.find_piece_at(app, 2, 7) and not src.utils.find_piece_at(app, 3, 7): # Roque côté dame
                    if left_rook.has_moved == False and king.has_moved == False: # Vérifier que ni le roi ni la tour n'ont bougé
                        if (2,7) not in king.possible_moves: 
                            king.possible_moves.append((2, 7)) # ajouter le roque côté dame aux coups possibles du roi
                        app.castling_possible["black"] = True # indiquer que le roque côté dame est possible pour les noirs
                if not src.utils.find_piece_at(app, 5, 7) and not src.utils.find_piece_at(app, 6, 7): # Roque côté roi
                    if right_rook.has_moved == False and king.has_moved == False:
                        if (6,7) not in king.possible_moves: 
                            king.possible_moves.append((6, 7)) # ajouter le roque côté roi aux coups possibles du roi
                        app.castling_possible["black"] = True # indiquer que le roque côté roi est possible pour les noirs

def en_passant_move(app: src.app.App, selected: src.piece.Piece) -> None:
    """Effectue une prise en passant aux échecs quand le joueur le demande."""
    if app.en_passant_possible["white"] and app.player_turn == 0: # prise en passant pour les blancs
        pawn = src.utils.find_piece_at(app, app.en_passant_possible["white"].x, app.en_passant_possible["white"].y)
        if pawn and pawn.type == "pawn":
            selected.bouger(pawn.x, pawn.y + 1)
            app.en_passant_possible["white"] = None
            pawn.alive = False
            app.next_turn()
    elif app.en_passant_possible["black"]: # prise en passant pour les noirs
        pawn = src.utils.find_piece_at(app, app.en_passant_possible["black"].x, app.en_passant_possible["black"].y)
        if pawn and pawn.type == "pawn":
            print("found pawn")
            selected.bouger(pawn.x, pawn.y - 1)
            pawn.alive = False
            app.en_passant_possible["black"] = None
            app.next_turn()

def en_passant(app: src.app.App) -> None:
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
    if app.player_turn == 0:  # Prise en passant pour les blancs
        for piece in app.pieces_white:
            if piece.type == "pawn" and piece.alive:
                # Vérifier les cases à gauche et à droite du pion blanc
                for dx in [-1, 1]: # gauche et droite
                    enemy_x = piece.x + dx
                    enemy_y = piece.y
                    enemy_piece = src.utils.find_piece_at(app, enemy_x, enemy_y) # on cherche la pièce ennemie
                    
                    # Vérifier s'il y a un pion noir adjacent
                    if enemy_piece and enemy_piece.type == "pawn" and enemy_piece.color == "black":
                        # Ajouter la prise en passant comme coup possible
                        en_passant_move = (enemy_x, enemy_y + 1)
                        if en_passant_move not in piece.possible_moves:
                            piece.possible_moves.append(en_passant_move)
                        app.en_passant_possible["white"] = enemy_piece # Stocker le pion noir pouvant être capturé en passant

    else:  # Prise en passant pour les noirs
        for piece in app.pieces_black:
            if piece.type == "pawn" and piece.alive:
                # Vérifier les cases à gauche et à droite du pion noir
                for dx in [-1, 1]:
                    enemy_x = piece.x + dx
                    enemy_y = piece.y
                    enemy_piece = src.utils.find_piece_at(app, enemy_x, enemy_y)
                    
                    # Vérifier s'il y a un pion blanc adjacent
                    if enemy_piece and enemy_piece.type == "pawn" and enemy_piece.color == "white":
                        # Ajouter la prise en passant comme coup possible
                        en_passant_move = (enemy_x, enemy_y - 1)
                        if en_passant_move not in piece.possible_moves:
                            piece.possible_moves.append(en_passant_move)
                        app.en_passant_possible["black"] = enemy_piece # Stocker le pion noir pouvant être capturé en passant

def check_checkmate(app: src.app.App) -> None:
    """Vérifie si un joueur est en échec et mat."""
    if app.player_turn == 0:
        # comparer les coups possibles des noirs avec les coups possibles du roi blanc
        # Rechercher le roi blanc
        king = next((p for p in app.pieces_white if p.type == "king" and p.alive), None)
        print(king)
        if not king:
            # TODO si pas de roi trouvé, fin de la partie
            app.end_game("black")
            return
        # Rassembler tous les coups possibles des noirs
        black_moves = src.utils.get_total_possible_moves(app, "black")
        white_moves = src.utils.get_total_possible_moves(app, "white")
        white_blocked_moves = []
        if king.possible_moves:
            print("avant check:", king.possible_moves)
            for move in king.possible_moves:
                if move in black_moves:
                    king.possible_moves.remove(move) 
            # if not king.possible_moves:
            #     # échec et mat
            #     app.end_game("black")
            #     return
        if (king.x, king.y) in black_moves: # le roi blanc est en échec
            print("Le roi blanc est en échec.")
            if white_moves: # il y a des coups possibles pour les blancs
                for move in white_moves: # on vérifie si un coup blanc peut contrer un coup noir
                    if move in black_moves: # un coup noir est contré
                        white_blocked_moves.append(move)
                if len(white_blocked_moves) == len(black_moves): # si aucun coup noir n'est contré
                    # échec et mat
                    app.end_game("black")
                    return
        # TODO corriger la détezction de coup noir bloqué par un coup blanc
        # TODO ajouter que si les coups possibles des blancs peuvent manger le roi noir dès le début du tour alors échec et mat et parie gagné pour les blancs

    else:
        # TODO implémenter la vérification pour les noirs
        pass