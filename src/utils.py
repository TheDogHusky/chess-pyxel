import src.app
import src.piece

def get_total_possible_moves(app: src.app.App, color: str, ignore: list[str] = []) -> list[tuple[int, int]]:
    """Retourne une liste de tous les coups possibles pour un joueur donné (color)."""

    total_moves = []
    pieces = app.pieces_white if color == "white" else app.pieces_black

    for piece in pieces:
        if piece.alive and piece.type not in ignore:
            total_moves.extend(piece.possible_moves)
    
    return total_moves

def find_piece_at(app: src.app.App, x: int, y: int) -> src.piece.Piece:
    """Retourne la pièce située aux coordonnées (x, y) si elle est vivante, sinon None."""
    all_pieces = app.pieces_white + app.pieces_black
    for piece in all_pieces:
        if piece.x == x and piece.y == y and piece.alive: # on find la piece que si elle est vivante
            return piece
    return None

def sort_by_type(pieces: list[src.piece.Piece]) -> tuple[dict[str, int], dict[str, int]]:
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

def get_total_alive_pieces(app: src.app.App, color: str) -> int:
    """Retourne le nombre total de pièces vivantes pour un joueur donné (color)."""

    pieces = app.pieces_white if color == "white" else app.pieces_black
    total = 0

    for piece in pieces:
        if piece.alive:
            total += 1
    
    return total

def get_ui_texture_coordinates(piece: src.piece.Piece) -> tuple[int, int]:
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

def get_dead_coordinates(color: str, type: str) -> tuple[int, int]:
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

def filter_type(pieces: list[src.piece.Piece], type: str) -> list[src.piece.Piece]:
    """Retourne une liste de pièces filtrée par type."""

    filtered = []
    for piece in pieces:
        if piece.type == type:
            filtered.append(piece)
    
    return filtered