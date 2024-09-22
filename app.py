from castle import *

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


# Class Rules pour faire apparaître dans une fenêtre au démarrage du jeu les règles du jeu
class Rules(Tk):
    def __init__(self) -> None:
        super().__init__()  # Créer une instance de la class Tk avec une fenêtre principale
        self.title("Règles du Jeu Pythescape")  # Titre de la fenêtre principale
        self._window_width = 600  # Largeur de la fenêtre
        self._window_height = 600  # Hauteur de la fenêtre
        self._screen_width = self.winfo_screenwidth()  # Largeur de l'écran où est lancée l'appli
        self._screen_height = self.winfo_screenheight()  # Hauteur de l'écran où est lancée l'appli
        self._center_x = int(
            self._screen_width / 2 - self._window_width / 2)  # Calcul de l'abscisse du centre de l'écran
        self._center_y = int(
            self._screen_height / 2 - self._window_height / 2)  # Calcul de l'ordonnée du centre de l'écran
        # Paramètres de la fenêtre principale
        self.geometry(f"{self._window_width}x{self._window_height}+{self._center_x}+{self._center_y}")
        self.resizable(False, False)  # Empêcher de pouvoir modifier la taille de la fenêtre

        # Ajout d'un widget Label afin d'afficher les règles du jeu
        self._game_rules = Label(self,
                                 text=MESSAGES["rules"],
                                 font=("Helvetica", 14),
                                 justify=CENTER,
                                 wraplength=500,
                                 )
        self._game_rules.pack(pady=30)  # Empaquetage du widget dans la fenêtre

        # Ajout d'un widget Button afin d'avoir un bouton cliquable permettant de lancer le jeu
        self._start_game_btn = ttk.Button(self, text="Ok", command=self._start_game)
        self._start_game_btn.pack(pady=30)  # Empaquetage du widget dans la fenêtre

    def _start_game(self) -> None:
        """Permet de lancer la commande lors l'utilisation du bouton d'action.
        Lance le jeu en cliquant sur le bouton.

        Returns: None
        """
        self.destroy()  # Ferme la fenêtre principale avec les règles du jeu
        Game()()  # Lance la fenêtre Turtle contenant le jeu

    def __call__(self) -> None:
        self.mainloop()

if __name__ == '__main__':
    Rules()()
