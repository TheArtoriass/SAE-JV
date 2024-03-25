import random,os,pygame

#Charger le son de combat
combat_sound = pygame.mixer.Sound('son/combat.mp3')

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                    Systèmes de gestion de combat
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Obtenir le répertoire du script actuel
repertoire_script = os.path.dirname(__file__)

class Combat:
    def __init__(self, joueur_actif, ennemi, fenetre, joueur_index):
        self.joueur_actif = joueur_actif
        self.ennemi = ennemi
        self.fenetre = fenetre
        self.joueur_index = joueur_index
        self.type_attaque = ""
        self.repertoire_script = os.path.dirname(__file__)

    def lancer_combat(self):
        if self.ennemi_deja_vaincu():
            return
        try:
            combat_sound.play()
            self.initialiser_affichage()
            self.choisir_type_attaque()
            self.boucle_combat()
        except Exception as e:
            print(f"Une erreur est survenue lors du combat : {e}")

    def ennemi_deja_vaincu(self):
        return (self.ennemi.x, self.ennemi.y) in self.joueur_actif.derniers_ennemis_battus

    def initialiser_affichage(self):
        try:
            pygame.init()
            # Obtenir les dimensions de l'écran
            infoEcran = pygame.display.Info()
            LARGEUR_ECRAN, HAUTEUR_ECRAN = infoEcran.current_w, infoEcran.current_h

            # Calculer la taille de la case en fonction de la taille de l'écran
            taille_case = min(LARGEUR_ECRAN // 20, HAUTEUR_ECRAN // 20)

            # Calculer le nombre de cases en largeur et en hauteur
            largeur_plateau = LARGEUR_ECRAN // taille_case
            hauteur_plateau = HAUTEUR_ECRAN // taille_case

            chemin_police = os.path.join(self.repertoire_script, 'minecraftia', 'Minecraftia-Regular.ttf')
            ma_police = pygame.font.Font(chemin_police, 28)
            blanc = (255, 255, 255)

            text_ligne1 = ma_police.render("Quel type d'attaque voulez-vous faire ?", True, blanc)
            text_ligne2 = ma_police.render("(normal(n)/lente(l)/rapide(r))", True, blanc)

            rect_ligne1 = text_ligne1.get_rect(center=(largeur_plateau * taille_case // 2, hauteur_plateau * taille_case // 2 - 20))
            rect_ligne2 = text_ligne2.get_rect(center=(largeur_plateau * taille_case // 2, hauteur_plateau * taille_case // 2 + 20))

            self.fenetre.blit(text_ligne1, rect_ligne1)
            self.fenetre.blit(text_ligne2, rect_ligne2)
            
        except Exception as e:
            print(f"Une erreur est survenue lors de l'initialisation de l'affichage : {e}")
            raise

        pygame.display.flip()

    def choisir_type_attaque(self):
        try:
            while self.type_attaque not in ["normal", "lente", "rapide"]:
                for evenement in pygame.event.get():
                    if evenement.type == pygame.KEYDOWN:
                        if evenement.unicode in ["n", "N"]:
                            self.type_attaque = "normal"
                        elif evenement.unicode in ["l", "L"]:
                            self.type_attaque = "lente"
                        elif evenement.unicode in ["r", "R"]:
                            self.type_attaque = "rapide"

            self.fenetre.fill((255, 255, 255))
            pygame.display.flip()
            
        except Exception as e:
            print(f"Une erreur est survenue lors du choix du type d'attaque : {e}")
            raise

    def boucle_combat(self):
        try:
            print(self.joueur_actif.nom, self.joueur_actif.force, self.joueur_actif.agilite, self.joueur_actif.vie)
            while self.joueur_actif.vie > 0 and self.ennemi.vieE > 0:
                joueur_de = random.randint(1, 8)
                ennemi_de = random.randint(1, 8)

                if joueur_de > ennemi_de:
                    if self.type_attaque == "normal":
                        degats = joueur_de
                    elif self.type_attaque == "lente":
                        degats = joueur_de + self.joueur_actif.force
                        if ennemi_de > joueur_de:
                            degats = ennemi_de + self.joueur_actif.agilite
                    elif self.type_attaque == "rapide":
                        degats = joueur_de - self.joueur_actif.force
                        if ennemi_de > joueur_de:
                            degats = ennemi_de - self.joueur_actif.agilite
                    self.ennemi.vieE -= degats
                elif joueur_de == ennemi_de:
                    pass
                else:
                    if self.type_attaque == "normal":
                        degats = ennemi_de
                    elif self.type_attaque == "lente":
                        degats = ennemi_de + self.joueur_actif.agilite
                        if degats - self.joueur_actif.force < 1:
                            degats = 1
                    elif self.type_attaque == "rapide":
                        degats = ennemi_de - self.joueur_actif.agilite
                        if degats < 1:
                            degats = 1
                    self.joueur_actif.vie -= degats
                self.joueur_actif.remaining_moves = 0

                if self.joueur_actif.vie <= 0:
                    self.joueur_actif.enlever_tous_objets()
                    message = f"Le joueur {self.joueur_index+1} est vaincu !" 
                    self.joueur_actif.est_vaincu()
                    derniers_ennemis_battus = self.joueur_actif.derniers_ennemis_battus
                    if derniers_ennemis_battus:
                        dernier_ennemi_battu = derniers_ennemis_battus[-1]
                        self.joueur_actif.x, self.joueur_actif.y = dernier_ennemi_battu
                    else:
                        self.joueur_actif.x, self.joueur_actif.y = (10,0)
                    break

                elif self.ennemi.vieE <= 0:
                    message = f"L'ennemi {self.ennemi.nomE} est vaincu !"
                    self.joueur_actif.derniers_ennemis_battus.append((self.ennemi.x, self.ennemi.y))
                    self.ennemi.vieE = self.ennemi.vieEMax
                    break

            self.afficher_message_fin_combat(message,ennemi=self.ennemi.nomE)
        except Exception as e:
            print(f"Une erreur est survenue lors de la boucle de combat : {e}")
            raise

    def afficher_message_fin_combat(self, message, ennemi):
        try:
            # Obtenir les dimensions de la fenêtre
            infoEcran = pygame.display.Info()
            LARGEUR_ECRAN, HAUTEUR_ECRAN = infoEcran.current_w, infoEcran.current_h

            # Charger l'image de fond par défaut et la redimensionner pour qu'elle s'adapte à la taille de la fenêtre
            image_path_default = os.path.join(self.repertoire_script, 'img','fondjeu', 'fondjeu_complet.jpg')
            background_default = pygame.image.load(image_path_default)
            background_default = pygame.transform.scale(background_default, (LARGEUR_ECRAN, HAUTEUR_ECRAN))

            self.fenetre.blit(background_default, (0, 0))
            
             # Position de départ de l'image de fond
            x_background = 0

            # Vitesse de défilement
            background_speed = 1.5


            # Choisir l'image de fond en fonction de l'ennemi
            if ennemi == "Mutant":
                image_path = os.path.join(self.repertoire_script, 'img','combat', 'pokemon_golem.jpg')
            elif ennemi == "Loup infecté":
                image_path = os.path.join(self.repertoire_script, 'img','combat', 'pokemon_loup.jpg')
            elif ennemi == "Rat infecté":
                image_path = os.path.join(self.repertoire_script, 'img','combat', 'pokemon_rat.jpg')
            elif ennemi == "Infecté":
                image_path = os.path.join(self.repertoire_script, 'img','combat', 'pokemon_zombie.jpg')
            else:
                image_path = None

            if image_path is not None:
                # Charger l'image de l'ennemi et la redimensionner pour qu'elle s'adapte à une petite fenêtre
                background_ennemi = pygame.image.load(image_path)
                background_ennemi = pygame.transform.scale(background_ennemi, (LARGEUR_ECRAN // 2, HAUTEUR_ECRAN // 1.2))

                # Positionner la petite fenêtre au centre de l'écran
                position_ennemi = ((LARGEUR_ECRAN - LARGEUR_ECRAN // 2) // 2, (HAUTEUR_ECRAN - HAUTEUR_ECRAN // 1.2) // 2)
                self.fenetre.blit(background_ennemi, position_ennemi)

            chemin_police = os.path.join(self.repertoire_script, 'minecraftia', 'Minecraftia-Regular.ttf')
            ma_police = pygame.font.Font(chemin_police, 28)
            noir = (0, 0, 0)  # Couleur du texte en noir

            texte_message = ma_police.render(message, True, noir)
            rect_texte = texte_message.get_rect()
            rect_texte.center = (LARGEUR_ECRAN // 2, HAUTEUR_ECRAN * 4.1 // 5)  # Positionner le texte plus en bas
            temps_affichage = pygame.time.get_ticks()  # Obtenir le temps actuel

            while pygame.time.get_ticks() - temps_affichage < 3500:  # Boucler pendant 3,5 seconde
                # Déplacer l'image de fond
                x_background -= background_speed

                # Si l'image est complètement défilée hors de l'écran, réinitialiser sa position
                if x_background <= -LARGEUR_ECRAN:
                    x_background = 0

                # Dessiner l'image de fond avec répétition
                self.fenetre.blit(background_default, (x_background, 0))
                self.fenetre.blit(background_default, (x_background + LARGEUR_ECRAN, 0))

                # Dessiner l'image de l'ennemi et le texte
                if image_path is not None:
                    self.fenetre.blit(background_ennemi, position_ennemi)
                self.fenetre.blit(texte_message, rect_texte)

                pygame.display.flip()


            self.fenetre.blit(texte_message, rect_texte)  
        except Exception as e:
            print(f"Une erreur est survenue lors de l'affichage du message de fin de combat : {e}")
            raise