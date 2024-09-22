from enum import StrEnum

from castle import *


class Prints(StrEnum):
    TITLE = "Pythescape"
    THEME_CHOICE = """Choisissez un thème."""
    RULES = """Le Python des Neiges

Lancelot entre dans le château au sommet du Python des Neiges, muni de son précieux sac de rangement et de sa torche fraîchement allumée aux feux de Beltane. 
Il doit trouver la statue de sainte Axerror, le chef-d’oeuvre de Gide de Rome, dit le « tyran malfaisant éternel ».

Heureusement, pour l’aider dans sa quête, Merlin, son maître, lui a fourni un plan minutieux des salles et des couloirs du château. 
Ce plan lui sera fort utile, vu l’énormité du bâtiment, tant par sa taille que par le nombre de ses pièces !

Avant de partir, Merlin lui a donné la clef de la porte d’entrée du château et lui a prodigué moults conseils, 
dont celui de bien garder tous les objets qu’il trouvera lors de sa quête : 
ceux-ci lui permettront de répondre aux diverses énigmes que ne manqueront pas de poser les gardes postés devant les portes à l’intérieur du château.

Règles du jeu :
Vous devez amener le Héros de cette aventure représenté par un point rouge jusqu'à la sortie (carré jaune).
Mais votre route sera bloquée par des portes fermées (carrés oranges) qui seront présentes sur votre chemin dans le labyrinthe.
Afin de pouvoir les ouvrir, vous devrez répondre à des énigmes. Pour vous aider à les résoudre vous trouverez des objets disséminés un peu partout dans le labyrinthe (carrés verts) que vous pourrez ramasser.

Que votre aventure commence !"""


class MainWindow(Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(Prints.TITLE.value)  # Titre de la fenêtre principale
        self._window_width = 600  # Largeur de la fenêtre
        self._window_height = 600  # Hauteur de la fenêtre
        self._screen_width = self.winfo_screenwidth()  # Largeur de l'écran où est lancée l'appli
        self._screen_height = self.winfo_screenheight()  # Hauteur de l'écran où est lancée l'appli
        # Calcul de l'abscisse du centre de l'écran
        self._center_x = int(self._screen_width / 2 - self._window_width / 2)
        # Calcul de l'ordonnée du centre de l'écran
        self._center_y = int(self._screen_height / 2 - self._window_height / 2)
        # Paramètres de la fenêtre principale
        self.geometry(f"{self._window_width}x{self._window_height}+{self._center_x}+{self._center_y}")
        self.resizable(False, False)  # Empêcher de pouvoir modifier la taille de la fenêtre

    def __call__(self) -> None:
        self.mainloop()


# Class Rules pour faire apparaître dans une fenêtre au démarrage du jeu les règles du jeu
class Frames(Frame):
    def __init__(self, root) -> None:
        super().__init__()  # Créer une instance de la class Tk avec une fenêtre principale
        # Ajout d'un widget Label afin d'afficher les règles du jeu
        self._game_rules = Label(root,
                                 text=Prints.THEME_CHOICE.value,
                                 font=("Helvetica", 14),
                                 justify=CENTER,
                                 wraplength=500,
                                 )
        self._game_rules.pack(pady=30)  # Empaquetage du widget dans la fenêtre

        # Ajout d'un widget Button afin d'avoir un bouton cliquable permettant de lancer le jeu
        self._start_game_btn = ttk.Button(root, text="Ok", command=self._start_game)
        self._start_game_btn.pack(pady=30)  # Empaquetage du widget dans la fenêtre

    def _start_game(self) -> None:
        """Permet de lancer la commande lors de l'utilisation du bouton d'action.
        Lance le jeu en cliquant sur le bouton.

        Returns: None
        """
        self.destroy()  # Ferme la fenêtre principale avec les règles du jeu
        Game()()  # Lance la fenêtre Turtle contenant le jeu


# Class Game permettant de créer la dynamique du jeu afin de le lancer
class Game:
    def __init__(self) -> None:
        self._screen_turtlescreen = turtle.Screen()  # Créer une instance de la gestion de la fenêtre graphique Turtle
        self._screen_turtlescreen.title("Pythescape")  # Titre de la fenêtre
        self._screen_turtlescreen.setup(width=1000, height=750)  # Taille de la fenêtre
        self._screen_turtlescreen.bgcolor(COULEUR_EXTERIEUR)  # Couleur de fond de la fenêtre

        self._castle = Castle()  # Créer une instance de la class Castle
        self._castle.draw_map()  # Dessiner le plan du château
        self._hero = Hero(self._castle)  # Créer une instance de la class Hero à partir de l'instance castle

    def _main_loop(self):
        """Permet de lancer le jeu.

        Returns: None
        """
        self._hero.move_to()  # Lancer la méthode de déplacement du héros
        self._screen_turtlescreen.mainloop()  # Maintient la fenêtre Turtle ouverte

    def __call__(self) -> None:
        self._main_loop()


if __name__ == '__main__':
    intro = MainWindow()
    intro()

