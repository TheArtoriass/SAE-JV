import pygame
import random
import os


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
            # Choisir l'image de fond en fonction de l'ennemi
            if ennemi == "Mutant":
                image_path = os.path.join(self.repertoire_script, 'img','combat', 'combat_golem.jpg')
            elif ennemi == "Loup infecté":
                image_path = os.path.join(self.repertoire_script, 'img','combat', 'combat_loup.jpg')
            elif ennemi == "Rat infecté":
                image_path = os.path.join(self.repertoire_script, 'img','combat', 'combat_rat.jpg')
            elif ennemi == "Infecté":
                image_path = os.path.join(self.repertoire_script, 'img','combat', 'combat_zombie.jpg')
            else:
                image_path = os.path.join(self.repertoire_script, 'img','fondjeu', 'fondjeu_complet.jpg')
                print("rien")

            # Obtenir les dimensions de la fenêtre
            infoEcran = pygame.display.Info()
            LARGEUR_ECRAN, HAUTEUR_ECRAN = infoEcran.current_w, infoEcran.current_h

            # Charger l'image de fond et la redimensionner pour qu'elle s'adapte à la taille de la fenêtre
            background = pygame.image.load(image_path)
            background = pygame.transform.scale(background, (LARGEUR_ECRAN, HAUTEUR_ECRAN))

            self.fenetre.blit(background, (0, 0))    
            chemin_police = os.path.join(self.repertoire_script, 'minecraftia', 'Minecraftia-Regular.ttf')
            ma_police = pygame.font.Font(chemin_police, 28)
            noir = (0, 0, 0)  # Couleur du texte en noir

            texte_message = ma_police.render(message, True, noir)
            rect_texte = texte_message.get_rect()
            rect_texte.center = (LARGEUR_ECRAN // 2, HAUTEUR_ECRAN * 4 // 5)  # Positionner le texte plus en bas
            self.fenetre.blit(texte_message, rect_texte)


            pygame.display.flip()
            pygame.time.delay(1500)      
        except Exception as e:
            print(f"Une erreur est survenue lors de l'affichage du message de fin de combat : {e}")
            raise