import pygame,os,random
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                       CLASSE ENNEMIS
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Obtenir le répertoire du script actuel
pygame.init()

# Obtenir les dimensions de l'écran
infoEcran = pygame.display.Info()
LARGEUR_ECRAN, HAUTEUR_ECRAN = infoEcran.current_w, infoEcran.current_h


repertoire_script = os.path.dirname(__file__)
taille_case = min(LARGEUR_ECRAN // 20, HAUTEUR_ECRAN // 20)

# Définir le chemin
chemin = [(10,0),(10,1),(10,2),(10,3),(10,4),(10,5),(10,6),(10,7),(10,8),(10,9),(10, 10), (10, 11), (10, 12), (10, 13), (10, 14), (10, 15),
(11, 15), (12, 15), (13, 15), (14, 15), (15, 15), (16, 15), (17, 15), (18, 15), (19, 15),
(19, 14), (19, 13), (19, 12), (19, 11),
(18, 11), (17, 11), (16, 11),
(16, 10), (16, 9), (16, 8), (16, 7), (16, 6), (16, 5), (16, 4), (16, 3),
(17, 3), (18, 3), (19, 3), (20, 3), (21, 3), (22, 3), (23, 3), (24, 3),
(24, 4), (24, 5), (24, 6), (24, 7), (24, 8), (24, 9), (24, 10), (24, 11), (24, 12), (24, 13), (24, 14), (24, 15), (24, 16), (24, 17), (24, 18)]


class Ennemis:
    """
    Classe représentant un ennemi dans le jeu.
    """
    def __init__(self, nomE, forceE, vieE, agiliteE, x_departE, y_departE, image_path,taille_case):
        """
        Initialise une instance de la classe Ennemis.

        Args:
            nomE (str): Le nom de l'ennemi.
            forceE (int): La force de l'ennemi.
            vieE (int): Les points de vie de l'ennemi.
            agiliteE (int): L'agilité de l'ennemi.
            x_departE (int): La position en x de départ de l'ennemi sur le plateau.
            y_departE (int): La position en y de départ de l'ennemi sur le plateau.
            image_path (str): Le chemin de l'image de l'ennemi.
            taille_case (int): La taille en pixels d'une case sur le plateau.
        """
        self.nomE = nomE
        self.forceE = forceE
        self.vieE = vieE
        self.agiliteE = agiliteE
        self.x = x_departE
        self.y = y_departE
        self.image = pygame.image.load(image_path)                                      # Charger l'image du joueur
        self.image = pygame.transform.scale(self.image, (taille_case, taille_case))     # Redimensionner l'image
        
        self.taille_case = taille_case
        self.vieEMax = vieE
        
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
    def dessiner(self, surface):
            """
            Dessine l'ennemi sur la surface donnée.

            Args:
                surface (pygame.Surface): La surface sur laquelle dessiner l'ennemi.
            """
            try:
                if not isinstance(surface, pygame.Surface):
                    raise TypeError("L'argument 'surface' doit être une instance de pygame.Surface.")
                if not isinstance(self.image, pygame.Surface):
                    raise ValueError("L'attribut 'self.image' doit être défini et être une instance de pygame.Surface.")
                if not isinstance(self.x, (int, float)) or not isinstance(self.y, (int, float)):
                    raise ValueError("Les attributs 'self.x' et 'self.y' doivent être des nombres.")
                surface.blit(self.image, (self.x * self.taille_case, self.y * self.taille_case))
            except Exception as e:
                print(f"Une erreur est survenue lors du dessin de l'ennemi : {e}")
                raise
            
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            
    def get_cases_occupees(self):
        """
        Renvoie une liste contenant les coordonnées de la case occupée par l'ennemi.

        Returns:
            list: Une liste contenant un tuple de deux entiers représentant les coordonnées de la case occupée par l'ennemi.
        """
        try:
            if not isinstance(self.x, (int, float)) or not isinstance(self.y, (int, float)):
                raise ValueError("Les attributs 'self.x' et 'self.y' doivent être des nombres.")
            return [(self.x, self.y)]
        except Exception as e:
            print(f"Une erreur est survenue lors de la récupération des cases occupées par l'ennemi : {e}")
            raise
        
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                   Création d'une liste d'ennemis 
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class EnnemiAnime(Ennemis):
    def __init__(self, nom, vie, force, agilite, x, y, chemin_sprite, taille_case):
        super().__init__(nom, vie, force, agilite, x, y, chemin_sprite, taille_case)

        # Charger le sprite et le diviser en frames
        sprite_sheet = pygame.image.load(chemin_sprite).convert_alpha()
        largeur_frame, hauteur_frame = 32, 32
        nouvelle_largeur, nouvelle_hauteur = 42, 42
        self.frames = []
        for y in range(sprite_sheet.get_height() // hauteur_frame):
            for x in range(sprite_sheet.get_width() // largeur_frame):
                frame = pygame.Surface((largeur_frame, hauteur_frame), pygame.SRCALPHA)
                frame.blit(sprite_sheet, (0, 0), (x * largeur_frame, y * hauteur_frame, largeur_frame, hauteur_frame))
                frame = pygame.transform.scale(frame, (nouvelle_largeur, nouvelle_hauteur))
                self.frames.append(frame)

        self.index_frame = 0

    def dessiner(self, fenetre):
        # Obtenir un rectangle de la même taille que le sprite et le positionner
        rect = self.frames[self.index_frame].get_rect()
        rect.topleft = (self.x * self.taille_case, self.y * self.taille_case)

        # Dessiner le sprite
        fenetre.blit(self.frames[self.index_frame], rect)

        # Passer à la frame suivante
        self.index_frame = (self.index_frame + 1) % len(self.frames)

liste_ennemis = [
    EnnemiAnime("Rat infecté", 0, 6, 0,*random.choice(chemin), os.path.join(repertoire_script, 'img', 'ennemis', 'rat-idle.png'), taille_case),
    EnnemiAnime("Rat infecté", 0, 6, 0,*random.choice(chemin), os.path.join(repertoire_script, 'img', 'ennemis', 'rat-idle.png'), taille_case),
    EnnemiAnime("Rat infecté", 0, 6, 0,*random.choice(chemin), os.path.join(repertoire_script, 'img', 'ennemis', 'rat-idle.png'), taille_case),

    EnnemiAnime("Loup infecté", 0, 8, 0, *random.choice(chemin), os.path.join(repertoire_script, 'img', 'ennemis', 'loup.png'), taille_case),
    EnnemiAnime("Loup infecté", 0, 8, 0, *random.choice(chemin), os.path.join(repertoire_script, 'img', 'ennemis', 'loup.png'), taille_case),
    EnnemiAnime("Loup infecté", 0, 8, 0, *random.choice(chemin), os.path.join(repertoire_script, 'img', 'ennemis', 'loup.png'), taille_case),

    EnnemiAnime("Infecté", 0, 10, 0, *random.choice(chemin), os.path.join(repertoire_script, 'img', 'ennemis', 'Infecte.png'), taille_case),
    EnnemiAnime("Infecté", 0, 10, 0, *random.choice(chemin), os.path.join(repertoire_script, 'img', 'ennemis', 'Infecte.png'), taille_case),
    EnnemiAnime("Infecté", 0, 10, 0, *random.choice(chemin), os.path.join(repertoire_script, 'img', 'ennemis', 'Infecte.png'), taille_case),

    EnnemiAnime("Gorille Mutant", 0, 13, 0, *random.choice(chemin), os.path.join(repertoire_script, 'img', 'ennemis', 'Gorille.png'), taille_case),
    EnnemiAnime("Gorille Mutant", 0, 13, 0, *random.choice(chemin), os.path.join(repertoire_script, 'img', 'ennemis', 'Gorille.png'), taille_case),
    EnnemiAnime("Gorille Mutant", 0, 13, 0, *random.choice(chemin), os.path.join(repertoire_script, 'img', 'ennemis', 'Gorille.png'), taille_case),
    
    EnnemiAnime("Expérience ratée", 0, 15, 0, *random.choice(chemin), os.path.join(repertoire_script, 'img', 'ennemis', 'Dragon.png'), taille_case),
    
]



