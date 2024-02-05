import pygame,os
from Objet import liste_objets
from evenement import CarteAleatoire
from evenement import  rencontre_amicale, maladie, tresor_enfoui, vautour, raccourci, blessure

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                       CLASSE PLATEAU  
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Définir le chemin
chemin = [(10,0),(10,1),(10,2),(10,3),(10,4),(10,5),(10,6),(10,7),(10,8),(10,9),(10, 10), (10, 11), (10, 12), (10, 13), (10, 14), (10, 15),
(11, 15), (12, 15), (13, 15), (14, 15), (15, 15), (16, 15), (17, 15), (18, 15), (19, 15),
(19, 14), (19, 13), (19, 12), (19, 11),
(18, 11), (17, 11), (16, 11),
(16, 10), (16, 9), (16, 8), (16, 7), (16, 6), (16, 5), (16, 4), (16, 3),
(17, 3), (18, 3), (19, 3), (20, 3), (21, 3), (22, 3), (23, 3), (24, 3),
(24, 4), (24, 5), (24, 6), (24, 7), (24, 8), (24, 9), (24, 10), (24, 11), (24, 12), (24, 13), (24, 14), (24, 15), (24, 16), (24, 17), (24, 18)]


# Obtenir le répertoire du script actuel
repertoire_script = os.path.dirname(__file__)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Plateau:
    def __init__(self, largeur, hauteur, taille_case):
        """
        Initialise un nouveau plateau de jeu.

        Args:
            largeur (int): La largeur du plateau en nombre de cases.
            hauteur (int): La hauteur du plateau en nombre de cases.
            taille_case (int): La taille d'une case en pixels.
        """
        
        self.largeur = largeur
        self.hauteur = hauteur
        self.taille_case = taille_case
        self.grille = [[None for _ in range(largeur)] for _ in range(hauteur)]
        self.surface = pygame.Surface((largeur * taille_case, hauteur * taille_case))
        
        self.joueurs = []   # Ajouter une liste pour stocker les joueurs
        self.ennemis = []   # Ajouter une liste pour stocker les ennemis
        self.objets = []    # Ajouter une liste pour stocker les objets
        self.carte = CarteAleatoire(largeur, hauteur, taille_case, chemin, liste_objets)
        
        self.evenements = {
            "Rencontre amicale": rencontre_amicale, 
            "Maladie": maladie, 
            "Trésor enfoui": tresor_enfoui,
            "Vautour": vautour, 
            "Raccourci": raccourci, 
            "Blessure": blessure
            
        }
        self.liste_objets = liste_objets
        
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def get_case(self, x, y):
        """
        Renvoie la case à la position (x, y) sur le plateau.

        Args:
            x (int): La position x de la case.
            y (int): La position y de la case.
        """
        return self.grille[y][x]

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def dessiner(self):
        """
        Dessine le plateau.
        """
        try:
            self.surface.fill((255, 255, 255))
            pygame.init()
            # Obtenir les dimensions de l'écran
            infoEcran = pygame.display.Info()
            LARGEUR_ECRAN, HAUTEUR_ECRAN = infoEcran.current_w, infoEcran.current_h

            # Calculer la taille de la case en fonction de la taille de l'écran
            self.taille_case = min(LARGEUR_ECRAN // self.largeur, HAUTEUR_ECRAN // self.hauteur)

            # Redimensionner la surface du plateau pour qu'elle s'adapte à la taille de l'écran
            self.surface = pygame.Surface((LARGEUR_ECRAN, HAUTEUR_ECRAN))

            self.surface.fill((255, 255, 255))

            # Charger l'image de la carte et la redimensionner pour qu'elle s'adapte à la taille de l'écran
            image_path = os.path.join(repertoire_script, 'img', 'fondjeu', 'fondjeu_gameplay.jpg')
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Le fichier {image_path} est introuvable.")

            image = pygame.image.load(image_path)
            image = pygame.transform.scale(image, (LARGEUR_ECRAN, HAUTEUR_ECRAN))

            # Dessiner l'image redimensionnée sur la surface du plateau
            self.surface.blit(image, (0, 0))

            # Dessiner le chemin sur la surface du plateau
            for x, y in chemin:
                pygame.draw.rect(self.surface, (0, 0, 0), (x * self.taille_case, y * self.taille_case, self.taille_case, self.taille_case), 1)

            # Dessiner les événements sur la surface du plateau
            carte = self.carte.generer_carte()
            for x, y, image_path, evenement in carte:
                if evenement and (x, y) not in [(ennemi.x, ennemi.y) for ennemi in self.ennemis]:
                    image = pygame.image.load(self.carte.get_image_path(evenement))
                    image = pygame.transform.scale(image, (self.taille_case, self.taille_case))
                    self.surface.blit(image, (x * self.taille_case, y * self.taille_case))
            
            # Dessiner les joueurs sur la surface du plateau
            for i, joueur in enumerate(self.joueurs):
                joueur.dessiner(self.surface, self.taille_case, i + 1)
                
                # Créer une surface avec le pseudo du joueur
                font = pygame.font.Font(None, 24)
                text = font.render(joueur.pseudo, True, (255, 255, 255))
                
                # Dessiner le pseudo sur le plateau
                self.surface.blit(text, (joueur.x * self.taille_case, joueur.y * self.taille_case))
                
            # Dessiner les ennemis sur la surface du plateau
            for ennemi in self.ennemis:
                ennemi.dessiner(self.surface)
            
            # Dessiner les objets sur la surface du plateau
            for objet in self.objets:
                x, y = objet.x * self.taille_case, objet.y * self.taille_case
                image = pygame.image.load(objet.image_path)
                image = pygame.transform.scale(image, (self.taille_case, self.taille_case))
                self.surface.blit(image, (x, y))
                
            return self.surface
        except Exception as e:
            print(f"Une erreur est survenue lors du dessin du plateau : {e}")
            raise
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def ajouter_ennemi(self, ennemi):
        """
        Ajoute un ennemi à la liste des ennemis sur le plateau.

        Args:
            ennemi (Ennemis): L'ennemi à ajouter.
        """
        self.ennemis.append(ennemi)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def ajouter_objet(self, objet):
        """
        Ajoute un objet à la liste des objets sur le plateau.

        Args:
            objet (Objet): L'objet à ajouter.
        """
        self.objets.append(objet)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def enlever_objet(self, objet):
        """
        Enlève un objet de la liste des objets sur le plateau.

        Args:
            objet (Objet): L'objet à enlever.
        """
        self.objets.remove(objet)

   