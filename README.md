# Pythescape - Projet fin de formation Fun-MOOC

**Pythescape** est un jeu d’évasion (*escape game*) développé en Python, utilisant le module `turtle` pour l’interface graphique. Ce projet a été réalisé dans le cadre d’un projet de fin de formation Python sur la plateforme en ligne **[Fun-MOOC](https://www.fun-mooc.fr/fr/)** et permet de simuler une aventure dans un château rempli d’énigmes, d’objets à collecter et de portes à ouvrir.

---

## 👨‍🏫 Présentation et Objectifs du Projet

### 🏰 Présentation du Projet

Lancelot, équipé de son sac et de sa torche, doit explorer le château du **Python des Neiges** pour trouver la statue de **Sainte Axerror**. Pour l’aider, Merlin lui a fourni un plan détaillé du château, ainsi que des conseils pour collecter des objets et résoudre des énigmes.

**Pythescape** est un jeu où le joueur contrôle Lancelot à travers un plan de château, avec pour objectif de :

+ Se déplacer dans les couloirs et les pièces.
+ Ramasser des objets pour résoudre des énigmes.
+ Ouvrir des portes en répondant correctement aux questions.
+ Atteindre la sortie pour gagner.

![exemple de l'interface du jeu vidéo](img/video_jeu.gif)

---

### 🎯 Objectifs Pédagogiques

À la fin du parcours de formation sur les bases de Python, le but est maintenant de pratiquer et développer un programme complet en Python afin de :

+ Manipuler des fichiers texte pour charger les données du jeu.
+ Utiliser le module ***`turtle`*** pour créer une interface graphique.
+ Gérer les déplacements et les interactions (personnage, objets, portes).
+ S'entraîner à utiliser des Class pour pratiquer la Programmation Orientée Objet.

## 🎮 Fonctionnalités

### Gestion des Données

Les données du jeu sont stockées dans **3 fichiers texte** :

+ `plan_chateau.txt` : Plan du château (murs, portes, objets, sortie).
+ `dico_objets.txt` : Liste des objets et leurs emplacements.
+ `dico_portes.txt` : Questions et réponses pour ouvrir les portes.

### Interface Graphique

+ **Module `turtle`** : Pour l’affichage du plan et les interactions.
+ **Zones d’affichage** :
  + Bandeau d’annonces (en haut).
  + Plan du château (zone centrale).
  + Inventaire des objets (à droite).

  ![wireframe zone d'affichage](img/zonedaffichage.jpg)

---

## 📂 Structure du projet

```bash
📂pythescape/
├── 📂img/
│   ├── video_jeu.gif          # Exemple d'interface du jeu
│   └── zonedaffichage.jpg     # Zones d'affichage
│
├── 📂config/
│   └── CONFIGS.py                 # Constantes et configurations
│
├── 📂data/
│   ├── plan_chateau.txt           # Plan du château
│   ├── dico_objets.txt            # Liste des objets
│   └── dico_portes.txt            # Questions/réponses pour les portes
│
├── castle.py                 # Code principal du jeu
├── app.py                    # Script de lancement du jeu
└── README.md
```

---

## ⚙️ Installation et utilisation

### 🛠️ Prérequis

+ **Python 3.10+**.
+ **Module `turtle`** (inclus dans la bibliothèque standard de Python).

### Étapes d'installation

1. **Cloner le dépôt** :

    ```bash
    git clone git@github.com:YoannMis/pythescape.git  # SSH
    cd pythescape
    ```

2. **Lancer le Jeu** :

    ```bash
    python3 app.py
    ```

## 🚀 Améliorations futures

Voici les fonctionnalités que je prévois d'ajouter :

+ Créer différents scénarios avec différentes cartes et énigmes.
+ Le joueur pourra choisir au départ quelle histoire jouer.
+ Refactorisation du projet afin d'améliorer la lisibilité de code en séparant chaque fonctionnalité dans différents modules.
