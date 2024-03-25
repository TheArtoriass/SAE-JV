from Plateau import Plateau, chemin
import random,sys,pygame
from Interface import choisir_personnages, afficher_resultat_de , message_interface, end_game , pause
from Ennemis import liste_ennemis 
from Combat import Combat
from Objet import liste_objets

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                               PROGRAMME MAIN POUR LANCER LE JEU  
#   
#   2023-2024
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def lancer_de():
    """
    Lance un dé à 6 faces.
    """
    return random.randint(1, 6)

if __name__ == "__main__":
    
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                           INITIALISATION
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    pygame.init()

    # Obtenir les dimensions de l'écran
    infoEcran = pygame.display.Info()
    LARGEUR_ECRAN, HAUTEUR_ECRAN = infoEcran.current_w, infoEcran.current_h

    # Calculer la taille de la case en fonction de la taille de l'écran
    taille_case = min(LARGEUR_ECRAN // 20, HAUTEUR_ECRAN // 20)

    # Calculer le nombre de cases en largeur et en hauteur
    largeur_plateau = LARGEUR_ECRAN // taille_case
    hauteur_plateau = HAUTEUR_ECRAN // taille_case


    joueurs = choisir_personnages()
   
    BLANC = (255, 255, 255)
    plateau = Plateau(largeur_plateau, hauteur_plateau, taille_case)
    
    plateau.joueurs.extend(joueurs)
    
    cases_occupees = [(10, 0), (24, 18)]  

    for ennemi in liste_ennemis:
        position = random.choice(chemin)
        while position in cases_occupees or any(position[:2] == evenement[:2] for evenement in plateau.carte):  
            position = random.choice(chemin)
        ennemi.x, ennemi.y = position
        cases_occupees.append(position) 
        plateau.ajouter_ennemi(ennemi)

    for objet in liste_objets:
        position = random.choice(chemin)
        while position in cases_occupees or any(position[:2] == evenement[:2] for evenement in plateau.carte): 
            position = random.choice(chemin)
        objet.x, objet.y = position
        cases_occupees.append(position)
        plateau.ajouter_objet(objet)
        
    
    # Créer une fenêtre en plein écran
    fenetre = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN), pygame.FULLSCREEN)

    
    joueur_actif = joueurs[0]
    print(joueur_actif.pseudo)
    
    joueur_index = 0
    de_restant = 0
    tour_complet = False
    message = ""
    continuer = True
    
    pause_active = False
        
    pygame.mixer.init()
    #On lance la musique du jeu
    pygame.mixer.music.load("musique_jeu.mp3")
    #On met la musique en boucle
    pygame.mixer.music.play(-1)
    
    # variable pour suivre le début du tour actuel
    debut_tour = pygame.time.get_ticks()
    
    # Avant la boucle principale
    temps_total_pause = 0
    
    # Charger le son de pas
    pas_bruit = pygame.mixer.Sound('son/pas_bruit.wav')
    
    #charge le son ramasse objet 
    ramasse_objet = pygame.mixer.Sound('son/ramasse_objet.mp3')
    
    #charge le son d'event
    event = pygame.mixer.Sound('son/event.mp3')
    
    #Charger le son de combat
    combat_sound = pygame.mixer.Sound('son/combat.mp3')


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                           BOUCLE PRINCIPALE
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    while continuer:
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evenement.type == pygame.KEYDOWN:
                # Si le joueur appuie sur la touche espace et qu'il n'a pas encore lancé le dé et que le tour n'est pas complet
                if evenement.key == pygame.K_SPACE and de_restant == 0 and not tour_complet:
                    #On lance le dé et on affiche le résultat
                    resultat_de = lancer_de()
                    afficher_resultat_de(resultat_de)
                    #pygame.time.wait(2000) # Pause de 2 secondes pour voir la valeur du dé
                    de_restant = resultat_de
                    
                    #On met à jour le début du tour
                    debut_tour = pygame.time.get_ticks()
                    
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                              DEPLACEMENT 
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                # Si le joueur appuie sur la touche échap, on met le jeu en pause
                if evenement.key == pygame.K_ESCAPE:
                    pause_active = True
                    
                # Si le joueur a encore des cases à parcourir et que le tour n'est pas complet
                elif de_restant > 0 and not tour_complet:
                    if evenement.key == pygame.K_LEFT:
                        if (joueur_actif.x - 1, joueur_actif.y) in chemin:
                            joueur_actif.deplacer('gauche')
                            de_restant -= 1
                            pas_bruit.play()
                    elif evenement.key == pygame.K_RIGHT:
                        if (joueur_actif.x + 1, joueur_actif.y) in chemin:
                            joueur_actif.deplacer('droite')
                            de_restant -= 1
                            pas_bruit.play()
                    elif evenement.key == pygame.K_UP:
                        if (joueur_actif.x, joueur_actif.y - 1) in chemin:
                            joueur_actif.deplacer('haut')
                            de_restant -= 1
                            pas_bruit.play()
                    elif evenement.key == pygame.K_DOWN:
                        if (joueur_actif.x, joueur_actif.y + 1) in chemin:
                            joueur_actif.deplacer('bas')
                            de_restant -= 1
                            pas_bruit.play()
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                           On regarde quand le Dé arrive à zéro s'il y a un objet ou un evenement
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                    if de_restant == 0:
                        # Vérifier si le joueur actuel est sur une case contenant un objet
                        for objet in plateau.objets:
                            if objet.x == joueur_actif.x and objet.y == joueur_actif.y:
                                joueur_actif.prendre_objet(objet)
                                ramasse_objet.play()
                                plateau.enlever_objet(objet)
                                
                                    
                        # Vérifier si le joueur actuel est sur un événement
                        for evenement in plateau.carte:
                            if joueur_actif.x == evenement[0] and joueur_actif.y == evenement[1]:
                                event.play()
                                evenement_nom = evenement[3]
                                evenement_methode = plateau.evenements[evenement_nom]
                                evenement_methode(joueur_actif,plateau.ennemis)
                                pygame.display.flip()
                                break

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                           Le combat si on croise un ennemi
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
       
                    if joueur_actif.peut_combattre:
                        for ennemi in plateau.ennemis:
                            if joueur_actif.x == ennemi.x and joueur_actif.y == ennemi.y:
                                combat_sound.play()
                                combat = Combat(joueur_actif, ennemi, fenetre, joueur_index)
                                
                                combat.lancer_combat()

                                joueur_actif.position_precedente = (joueur_actif.x, joueur_actif.y)
                                if joueur_actif.vie > 0:
                                    joueur_actif.remaining_moves = 0
                                    break
                                else:
                                    joueur_actif.x, joueur_actif.y = joueur_actif.position_precedente
                                    joueur_actif.remaining_moves = 0
                                    break
                                
                    #SI on arrive sur les coordonnées (16,18) alors le joueur actif à gagné
                    if joueur_actif.x == 24 and joueur_actif.y == 18:
                        
                        end_game(joueur_index)
                        pygame.mixer.music.stop()
                        
                    #On passe au joueur suivant
                    if de_restant == 0:
                        joueur_index = (joueur_index + 1) % len(joueurs)
                        joueur_actif = joueurs[joueur_index]
                        if joueur_index == 0:
                            tour_complet = True
                            
                    
         # Si la pause est active, on affiche l'écran de pause
        if pause_active:
            temps_pause = pygame.time.get_ticks()
            continuer = pause(fenetre)
            temps_apres_pause = pygame.time.get_ticks()
            debut_tour += temps_apres_pause - temps_pause
            pause_active = False
        else:
            temps_total_pause = 0
            if tour_complet:
                tour_complet = False
                
        # Lors de la vérification du temps écoulé
        if pygame.time.get_ticks() - debut_tour - temps_total_pause > 60000 and len(joueurs) > 1:
            # On passe au joueur suivant
            joueur_index = (joueur_index + 1) % len(joueurs)
            joueur_actif = joueurs[joueur_index]
            de_restant = 0
            if joueur_index == 0:
                tour_complet = True
            # Réinitialiser le début du tour
            debut_tour = pygame.time.get_ticks()
                                     
        fenetre.fill(BLANC)
        fenetre.blit(plateau.dessiner(), (0, 0))
        #On affiche les différentes indications sur la fenêtre pygame
        message_interface(joueur_index,de_restant,joueur_actif,joueurs)

pygame.quit()
