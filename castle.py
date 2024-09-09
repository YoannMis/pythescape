from pathlib import Path
import turtle

# Import des données du fichier CONFIGS
from config.CONFIGS import *

# ---CHEMINS VERS LES FICHIERS DE DONNÉES DE JEU---
# Chemin vers le dossier /data/
DATA_DIR = Path(__file__).resolve().parent / "data"
# Chemin vers le fichier contenant le plan du château
CASTLE_MAP_PATH = DATA_DIR / fichier_plan
# Chemin vers le fichier contenant le plan du château
OBJECTS_PATH = DATA_DIR / fichier_objets
# Chemin vers le fichier contenant le plan du château
QUESTIONS_PATH = DATA_DIR / fichier_questions

# ---RÉCUPÉRATION DES DONNÉES CONTENUES DANS LES FICHIERS DE DONNÉES---
# Récupération de la liste des colonnes et lignes de la grille représentant le plan du château
with open(CASTLE_MAP_PATH, "r") as f:
    CASTLE_GRID = [line.strip().split(" ") for line in f.readlines()]
# Conversion du fichier .txt dico_objets.txt en un str au format dictionnaire :
# {tuple(coordonnées objet): "description de l'objet"}
with open(OBJECTS_PATH, "r") as f:
    OBJECTS = "{" + f.read().replace("), ", "): ").replace("\n", ", ") + "}"
# Conversion du fichier .txt portes_objets.txt en un str au format dictionnaire :
# {tuple(coordonnées porte): tuple("question", "réponse")}
with open(QUESTIONS_PATH, "r") as f:
    QUESTIONS = "{" + f.read().replace("), ", "): ").replace("\n", ", ") + "}"

# ---DIMENSIONS DE L'ESPACE DE JEU ET DU PLAN DU CHÂTEAU---
WIDTH = abs(ZONE_PLAN_MINI[0]) + abs(ZONE_PLAN_MAXI[0])  # Hauteur de la zone d'affichage du château
HEIGHT = abs(ZONE_PLAN_MINI[1]) + abs(ZONE_PLAN_MAXI[1])  # Largeur de la zone d'affichage du château
ROWS = len(CASTLE_GRID)  # Nombre de lignes dans la grille
COLUMNS = len(CASTLE_GRID[0])  # Nombre de colonnes dans la grille
MAX_SQUARES_IN_HEIGHT = HEIGHT // ROWS  # Longueur maximale des côtés des carrés qui rentrent en hauteur
MAX_SQUARES_IN_WIDTH = WIDTH // COLUMNS  # Longueur maximale des côtés des carrés qui rentrent en largeur
# Longueur maximale des côtés des carrés afin qu'ils puissent rentrer en hauteur et largeur sur la grille
SQUARE_SIDE_LEN = MAX_SQUARES_IN_HEIGHT if MAX_SQUARES_IN_HEIGHT <= MAX_SQUARES_IN_WIDTH else MAX_SQUARES_IN_WIDTH
HALF_SQUARE = SQUARE_SIDE_LEN / 2  # moitié de la longueur du carré pour trouver le centre du carré
DEFAULT_SHAPESIZE = 20  # nombre de px par défaut d'un objet Turtle nécessaire pour convertir la taille en px
GRID_SHAPESIZE = SQUARE_SIDE_LEN / DEFAULT_SHAPESIZE  # Conversion en px de la taille d'un élément à afficher à l'écran

# ---ÉLÉMENTS DU PLAN DU CHÂTEAU---
CORRIDOR = 0  # Couloir
WALL = 1  # Mur
GOAL = 2  # But/sortie
DOOR = 3  # Porte
OBJECT = 4  # Objet

# ---DICT DES DIFFÉRENTS MESSAGES DU JEU À AFFICHER---
MESSAGES = {"win": "Bravo ! Vous avez gagné !",
            "closed door": "Cette porte est fermée. Répondez à l'énigme posée par le garde pour l'ouvrir.",
            "opened door": "La porte s'ouvre !",
            "wrong": "Mauvaise réponse.",
            "start": "Vous devez amener le Héro (point rouge) jusqu'à la sortie (case jaune).",
            "object": "Vous avez trouvé un objet : ",
            "inventory": "INVENTAIRE :",
            }

# Dict contenant les coordonnées (sous forme de tuple) de chaque case de la grille représentant le château comme clés
# Et un tuple (contenant le numéro correspondant à l'élément représenté par la case, les coordonnées en px Turtle de la case) comme valeurs
MAP_COORDS = {}
x_coord = ZONE_PLAN_MINI[0] + HALF_SQUARE  # coordonnée x en px Turtle du centre de la case en haut à gauche de la grille
y_coord = ZONE_PLAN_MAXI[1] - HALF_SQUARE  # coordonnée y en px Turtle du centre de la case en haut à gauche de la grille
for x in range(ROWS):
    for y in range(COLUMNS):
        # MAP_COORDS = {(x, y): (n° représentant objet, (x en px Ttle, y en px Ttle))}
        MAP_COORDS[(x, y)] = (int(CASTLE_GRID[x][y]), (x_coord, y_coord))
        x_coord += SQUARE_SIDE_LEN  # On passe au centre de la case de la colonne suivante
    # On se déplace aux coordonnées du centre de la case de la ligne suivante
    y_coord -= SQUARE_SIDE_LEN
    x_coord = ZONE_PLAN_MINI[0] + HALF_SQUARE


# Class Castle permettant d'afficher à l'écran le plan du château
class Castle(turtle.Turtle):
    def __init__(self) -> None:
        super().__init__()  # Héritage de la Class Turtle
        self.hideturtle()  # Cacher la tortue au démarrage du jeu
        self.pencolor(COULEUR_CASES)  # Couleur du contour de la tortue, blanc
        self.shape("square")  # Forme de la tortue, un carré
        self.shapesize(GRID_SHAPESIZE)  # Taille de la tortue
        self.penup()  # La tortue ne dessine pas
        self.speed(0)  # Vitesse de déplacement le plus rapide possible
        self.stampids = {DOOR: {}, OBJECT: {}}  # Dict permettant de stocker les coordonnées des objets et portes

    def store_stampid(self, stampid: int, coords: tuple, map_element: int) -> None:
        """Stocke dans le dict self.stampid les 'stamp-id' par leurs coordonnées des 'stamps'
        créés avec la méthode turtle.stamp() correspondants à ceux générés pour représenter
        les objets ou les portes sur le plan du château.

        Args:
            stampid (int): stamp-id
            coords (tuple): coordonnées de l'objet ou la porte
            map_element (int): objet ou porte

        Returns: None
        """
        # Si l'élément créé du plan du château est un objet ou une porte, l'ajouter dans le dict.
        if map_element in self.stampids:
            self.stampids[map_element][coords] = stampid

    def draw_map(self) -> None:
        """Dessine le plan du château en utilisant la méthode stamp() du module Turtle.

        Returns: None
        """
        for coords in MAP_COORDS:
            # Récupère la couleur de l'élément du plan du château à dessiner
            self.fillcolor(COULEURS[MAP_COORDS[coords][0]])
            # Déplace la tortue aux coordonnées Turtle correspondant à l'élément du plan du château
            self.goto(MAP_COORDS[coords][1])
            stampid = self.stamp()  # Dessine l'élément à l'emplacement donné
            # Si l'élément est une porte ou un objet, enregistre cet élément avec ses coordonnées et son stamp-id.
            self.store_stampid(stampid, coords, MAP_COORDS[coords][0])


# Class DisplayOnScreen permettant d'afficher les différents messages et l'inventaire à l'écran
class DisplayOnScreen(turtle.Turtle):
    BASIC_FONT = ("Arial", 16, "normal")  # Police d'écriture utilisée pour afficher le texte
    WINNING_FONT = ("Arial", 22, "bold")  # Police d'écriture pour afficher le message de victoire

    def __init__(self, start_position: tuple, message: str) -> None:
        """Initialisation des attributs de classe.

        Args:
            start_position (tuple): coordonnées Turtle de la position de départ de la tortue
            message (str): message à afficher
        """
        super().__init__()  # Héritage de la Class Turtle
        self.hideturtle()  # Cacher la tortue au démarrage du jeu
        self.penup()  # La tortue ne dessine pas
        self.goto(start_position)  # Déplacer la tortue au point de départ
        self.write(message, font=DisplayOnScreen.BASIC_FONT)  # Afficher le message de démarrage

    def write_message(self, message: str, text_color: str = "black", font: tuple = BASIC_FONT) -> None:
        """Affiche le message donné en argument selon la police choisie.

        Args:
        message (str): message à afficher
        font (tuple): format de la police d'écriture

        Returns: None
        """
        self.clear()  # Effacer les messages précédents
        self.color(text_color)
        self.write(message, font=font)  # Écrire le message


# Class Hero permettant d'afficher le héros du jeu et les différents déplacements/actions du personnage
class Hero(turtle.Turtle):
    def __init__(self, castle_turtle: Castle) -> None:
        """Initialisation des attributs de classe.

        Args:
            castle_turtle (Castle): objet Turtle créé avec la classe Castle
        """
        super().__init__()  # Héritage de la Class Turtle
        self.game_window = turtle.Screen()  # Initier une fenêtre Turtle avec laquelle interagir

        # Attributs de la tortue représentant le héros
        self.hideturtle()  # Cacher la tortue au démarrage du jeu
        self.color(COULEUR_PERSONNAGE)  # Couleur de la tortue, rouge
        self.shape("circle")  # Forme de la tortue, un rond
        self.shapesize(RATIO_PERSONNAGE * GRID_SHAPESIZE)  # Taille de la tortue
        self.penup()  # La tortue ne dessine pas
        self.speed(0)  # Vitesse de déplacement le plus rapide possible
        self.castle_turtle = castle_turtle  # Récupération de la tortue créée à partir de la classe Castle

        # Création d'une tortue 'shadow' représentant l'ombre du héros qui affichera les cases déjà vues
        self.shadow = turtle.Turtle()  # Initialisation de la tortue
        self.shadow.hideturtle()  # Cacher la tortue au démarrage
        self.shadow.penup()  # La tortue ne dessine pas
        self.shadow.color(COULEUR_CASES, COULEUR_VUE)  # Couleur de la tortue, beige
        self.shadow.shape("square")  # Forme de la tortue, carré
        self.shadow.shapesize(GRID_SHAPESIZE)  # Taille de la tortue = taille d'une case
        self.cur_position = list(self.starting_position())  # Liste contenant les coordonnées de la position actuelle de la tortue

        # Dict contenant en clés les coordonnées des objets se trouvant dans la grille avec leur description comme valeurs
        self.dict_objects = Hero.into_dict(OBJECTS)
        # Dict contenant en clés les coordonnées des portes se trouvant dans la grille
        # avec les questions auxquelles répondre comme valeurs
        self.dict_questions = Hero.into_dict(QUESTIONS)

        # Création d'une tortue 'message' à partir de la classe DisplayOnScreen permettant d'afficher les messages
        # Avec un message de départ
        self.message = DisplayOnScreen(POINT_AFFICHAGE_ANNONCES, MESSAGES["start"])

        # Création d'une tortue 'inventory' à partir de la classe DisplayOnScreen permettant d'afficher l'inventaire
        # Avec un message de départ
        self.inventory = DisplayOnScreen(POINT_AFFICHAGE_INVENTAIRE, MESSAGES["inventory"])
        self.objects = []  # Liste des objects ramassés

    @property
    def tuple_cur_position(self):
        """Convertit la position actuelle (self.cur_position) en tuple.

        Returns: un tuple
        """
        return tuple(self.cur_position)

    @staticmethod
    def into_dict(text: str) -> dict:
        """Converti un fichier txt en dictionnaire exploitable
        pour gérer les évènements du jeu en fonction de leur emplacement sur le plan du château.

        Args:
        text (str): str correspondant au fichier .txt à convertir

        Returns (dict): {tuple(coordonnées objet): "description de l'objet"}
            ou {tuple(coordonnées porte): tuple("question", "réponse")}
        """
        return eval(text)

    def starting_position(self) -> tuple[int, int]:
        """Déplace les tortues correspondant au héros et à son ombre à leur position de départ.

        Returns: les coordonnées de la position de départ
        """
        self.goto((MAP_COORDS[POSITION_DEPART][1]))
        self.shadow.goto((MAP_COORDS[POSITION_DEPART][1]))
        self.showturtle()  # Rend visible la tortue du héros
        return POSITION_DEPART

    def cant_move(self) -> bool:
        """Vérifie si le héros peut avancer.

        Returns: True si le héros ne peut pas avancer, False sinon
        """
        position = self.tuple_cur_position
        # Vérifier si le héros est hors de la carte ou s'il est sur un mur
        if position not in MAP_COORDS or MAP_COORDS[position][0] == WALL:
            return True
        return False

    def go_up(self):
        print(f"last position: tuple{self.tuple_cur_position} ; list{self.cur_position}")
        cur_position = list(self.tuple_cur_position)
        print(f"current position: {cur_position}")
        self.cur_position[0] -= 1
        print(f"current position: tuple{self.tuple_cur_position} ; list{self.cur_position}")
        if self.cant_move():
            print(f"cant move position: tuple{self.tuple_cur_position} ; list{self.cur_position}")
            self.cur_position[0] += 1
            print(f"cant move after position: tuple{self.tuple_cur_position} ; list{self.cur_position}")
        elif self.tuple_cur_position in self.dict_questions:
            self.door_opening(self.tuple_cur_position, cur_position)
        else:
            # print(self.cant_move())
            y = self.ycor()
            self.sety(y + SQUARE_SIDE_LEN)
            self.shadow.stamp()
            self.shadow.sety(y + SQUARE_SIDE_LEN)
            self.clear_map_element(self.tuple_cur_position)
            self.get_object(self.tuple_cur_position)
        if self.which_element() == GOAL:
            self.message.write_message(MESSAGES["win"], font=DisplayOnScreen.WINNING_FONT)
        # print(self.cur_position)

    def go_down(self):
        print(f"last position: tuple{self.tuple_cur_position} ; list{self.cur_position}")
        cur_position = list(self.tuple_cur_position)
        print(f"current position: {cur_position}")
        self.cur_position[0] += 1
        print(f"current position: tuple{self.tuple_cur_position} ; list{self.cur_position}")
        if self.cant_move():
            print(f"cant move position: tuple{self.tuple_cur_position} ; list{self.cur_position}")
            self.cur_position[0] -= 1
            print(f"cant move after position: tuple{self.tuple_cur_position} ; list{self.cur_position}")
        elif self.tuple_cur_position in self.dict_questions:
            self.door_opening(self.tuple_cur_position, cur_position)
        else:
            # print(self.cant_move())
            y = self.ycor()
            self.sety(y - SQUARE_SIDE_LEN)
            self.shadow.stamp()
            self.shadow.sety(y - SQUARE_SIDE_LEN)
            self.clear_map_element(self.tuple_cur_position)
            self.get_object(self.tuple_cur_position)
        if self.which_element() == GOAL:
            self.message.write_message(MESSAGES["win"], font=DisplayOnScreen.WINNING_FONT)
        # print(self.cur_position)

    def go_left(self):
        print(f"last position: tuple{self.tuple_cur_position} ; list{self.cur_position}")
        cur_position = list(self.tuple_cur_position)
        print(f"current position: {cur_position}")
        self.cur_position[1] -= 1
        print(f"current position: tuple{self.tuple_cur_position} ; list{self.cur_position}")
        if self.cant_move():
            print(f"cant move position: tuple{self.tuple_cur_position} ; list{self.cur_position}")
            self.cur_position[1] += 1
            print(f"cant move after position: tuple{self.tuple_cur_position} ; list{self.cur_position}")
        elif self.tuple_cur_position in self.dict_questions:
            self.door_opening(self.tuple_cur_position, cur_position)
        else:
            # print(self.cant_move())
            x = self.xcor()
            self.setx(x - SQUARE_SIDE_LEN)
            self.shadow.stamp()
            self.shadow.setx(x - SQUARE_SIDE_LEN)
            self.clear_map_element(self.tuple_cur_position)
            self.get_object(self.tuple_cur_position)
        if self.which_element() == GOAL:
            self.message.write_message(MESSAGES["win"], font=DisplayOnScreen.WINNING_FONT)
        # print(self.cur_position)

    def go_right(self):
        print(f"last position: tuple{self.tuple_cur_position} ; list{self.cur_position}")
        cur_position = list(self.tuple_cur_position)
        print(f"current position: {cur_position}")
        self.cur_position[1] += 1
        print(f"current position: tuple{self.tuple_cur_position} ; list{self.cur_position}")
        if self.cant_move():
            print(f"cant move position: tuple{self.tuple_cur_position} ; list{self.cur_position}")
            self.cur_position[1] -= 1
            print(f"cant move after position: tuple{self.tuple_cur_position} ; list{self.cur_position}")
        elif self.tuple_cur_position in self.dict_questions:
            self.door_opening(self.tuple_cur_position, cur_position)
        else:
            # print(self.cant_move())
            x = self.xcor()
            self.setx(x + SQUARE_SIDE_LEN)
            self.shadow.stamp()
            self.shadow.setx(x + SQUARE_SIDE_LEN)
            self.clear_map_element(self.tuple_cur_position)
            self.get_object(self.tuple_cur_position)
        if self.which_element() == GOAL:
            self.message.write_message(MESSAGES["win"], font=DisplayOnScreen.WINNING_FONT)
        # print(self.cur_position)

    def move_to(self) -> None:
        """Permet de déplacer le héros avec les flèches du clavier.

        Returns: None
        """
        self.game_window.onkeypress(self.go_up, "Up")  # Quand on appuie sur la flèche du haut, le perso monte.
        self.game_window.onkeypress(self.go_down, "Down")  # Quand on appuie sur la flèche du bas, le perso descend.
        self.game_window.onkeypress(self.go_left,
                                    "Left")  # Quand on appuie sur la flèche de gauche, le perso va à gauche.
        self.game_window.onkeypress(self.go_right,
                                    "Right")  # Quand on appuie sur la flèche de droite, le perso va à droite.
        self.game_window.listen()  # Récupère les entrées clavier

    def which_element(self) -> int:
        """Renvoie l'élément sur le plan du château correspondant à la position du héros.

        Returns: Valeur de l'élément
        """
        return MAP_COORDS[self.tuple_cur_position][0]

    def clear_map_element(self, stamp_position: tuple[int, int]) -> None:
        element = self.which_element()
        if element in self.castle_turtle.stampids:
            try:
                self.castle_turtle.clearstamp(self.castle_turtle.stampids[element][stamp_position])
                del self.castle_turtle.stampids[element][stamp_position]
            except KeyError:
                pass

            # pprint(self.castle_turtle.stampids)

    def get_object(self, object_coord: tuple[int, int]) -> None:
        if object_coord in self.dict_objects:
            self.objects.append(self.dict_objects[object_coord])
            self.display_object()
            del self.dict_objects[object_coord]
            # pprint(self.dict_objects)

    def display_object(self) -> None:
        """Permet d'afficher les objets ramassés dans l'inventaire
        et d'afficher un message indiquant quel objet a été ramassé.

        Returns: None
        """
        self.inventory.sety(self.inventory.ycor() - 30)  # Déplace la tortue de l'inventaire à la ligne suivante
        # La tortue 'inventaire' affiche l'objet dans l'inventaire en incrémentant le N° d'objet ramassé.
        self.inventory.write(f"N°{len(self.objects)} : {self.objects[-1]}", font=DisplayOnScreen.BASIC_FONT)
        # La tortue 'message' affiche l'objet ramassé dans l'encadré des messages
        self.message.write_message(f"{MESSAGES['object']}{self.objects[-1]}", font=DisplayOnScreen.BASIC_FONT)

    def ask_question(self, door_coord: tuple[int, int]) -> str:
        """Permet d'afficher une fenêtre contextuelle permettant de poser la question
        qui servira à ouvrir la porte. Retourne ensuite la réponse à la question entrée
        par le joueur.

        Args:
            door_coord (tuple): coordonnées de la porte à ouvrir

        Returns (str): Retourne l'input du joueur
        """
        return self.game_window.textinput("Question", self.dict_questions[door_coord][0])

    def door_opening(self, door_coord: tuple[int, int], last_position: list[int, int]) -> None:
        """Gère l'ouverture des portes. Récupère la réponse du joueur aux questions.
        Si la réponse est juste, ouvre la porte. Sinon la porte reste fermée.
        Affiche les messages correspondants indiquant le statut de la porte en fonction
        des réponses données.

        Args:
            door_coord (tuple): coordonnées de la porte
            last_position (list): position du joueur devant la porte

        Returns: None
        """
        self.message.write_message(MESSAGES["closed door"], text_color="red")  # Indique que la porte est fermée
        answer = self.ask_question(door_coord)  # Pose la question correspondante et enregistre la réponse du joueur
        # Si la réponse est juste
        if answer == self.dict_questions[door_coord][1]:
            # Indiquer que la porte est ouverte
            self.message.write_message(MESSAGES["opened door"], text_color="green")
            self.clear_map_element(door_coord)  # Effacer la porte du plan du château
            del self.dict_questions[door_coord]  # Supprimer la question du dictionnaire des questions
            self.goto(MAP_COORDS[door_coord][1])  # Le héros se déplace sur l'emplacement de la porte
            self.shadow.stamp()
            self.shadow.goto(MAP_COORDS[door_coord][1])
        else:
            # Sinon indiquer que la réponse est fausse
            self.message.write_message(MESSAGES["wrong"], text_color="red")
            self.cur_position = last_position  # Le héros reprend sa position d'origine en restant bloqué devant la porte

        self.game_window.listen()  # Continuer à récupérer les entrées clavier


class Game:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.setup(width=1000, height=750)
        self.castle = Castle()
        self.castle.draw_map()
        self.hero = Hero(self.castle)

    def main_loop(self):
        self.hero.move_to()
        self.screen.mainloop()

    def __call__(self) -> None:
        self.main_loop()


if __name__ == '__main__':
    Game()()



