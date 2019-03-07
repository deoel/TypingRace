from sys import exit
import pygame_textinput
import pygame, time
from threading import Thread
from config import *


class GuiTypingRace:

    def __init__(self):
        pass

    def fournir_les_mots():
        text = "chadax chadrac kap g-eye orphee mahanga orcha munongo chador nsadi chadax chadrac kap g-eye orphee mahanga orcha munongo chador nsadi"
        # text = "chado chad chadax"
        tabText = text.split(" ")
        
        j = -1
        while True and j!=len(tabText)-1:
            j=j+1
            mot = tabText[j]
            reception_nouveau_mot(mot)
            # time.sleep(0.003)
            
    ######################################
    def reception_nouveau_mot(mot):
        trouver = False
        # trouver des palces vacantes dans le TabObject et y mettre des nouveau mots et s'il n'y en a pas alors on ajoute une nouvelle case
        for i,e in enumerate(TabObject):
            if e["txt"] == "":
                fixer_un_mot(mot, i)
                trouver = True
                print("ancien:",i)
                break
        if not trouver :
            creer_un_nouveau_mot(mot)
            print("nouveau")
            
    ######################################
    def createTextObj(text,font="impact.ttf",taille=30,couleur=(255,255,255)):
        police = pygame.font.Font(font,taille)
        textSurf = police.render(text,True,couleur)
        rect = textSurf.get_rect()
        return textSurf, rect
        
    # création des acteurs
    def create_actors():
        pygame.init()
        
        pygame.display.set_caption("Typping Race")
        global screen
        screen = pygame.display.set_mode((WIDTH,HEIGHT))
        
        global TabObject
        TabObject = []
        
        # Create TextInput-object
        global textinput, textinput_rect
        textinput = pygame_textinput.TextInput()
        textinput_rect = textinput.get_surface().get_rect()
        textinput_rect.top = HEIGHT - 50
        textinput_rect.left = WIDTH/4
        textinput.get_surface().fill((123,123,123))
        textinput.set_text_color(COLOR_WHITE)
        textinput.set_cursor_color(COLOR_WHITE)
        
        global surfDeBord, surfDeBordRect, surfScores, rectScores
        ###################################################
        # SURFACE DE GAUCHE LA SAISIE DES MOTS
        surfDeBord = pygame.Surface((WIDTH/2,HAUT_BORD_RECT))
        surfDeBord.fill((0,255,0))
        surfDeBordRect = surfDeBord.get_rect()
        surfDeBordRect.top = HEIGHT-HAUT_BORD_RECT
        ###################################################
        # SURFACE DE DROTIE LES SCORES
        surfScores = pygame.Surface((WIDTH/2,HAUT_BORD_RECT))
        surfScores.fill((0,255,0))
        rectScores = surfScores.get_rect()
        rectScores.top = HEIGHT-HAUT_BORD_RECT
        rectScores.left = WIDTH/2
        
        global policeScore
        policeScore = pygame.font.Font("impact.ttf",16)
        nouveauScore("car",0)
        nouveauScore("mot",0)
        nouveauScore("gen",0)
        
        #image
        """global geye_img,geye_rec
        geye_img = pygame.image.load("elle.jpg")
        geye_img = geye_img.convert() # convert_alph() pour la transparence des image png
        geye_rec = geye_img.get_rect()"""
        
        global son, son_over
        son = pygame.mixer.Sound("system-fault.ogg")
        son.set_volume(0.1)
        son_over = pygame.mixer.Sound("over.ogg")
        son_over.set_volume(0.1)
        
        global mfont
        mfont = pygame.font.Font("impact.ttf",70)

        
    ################################################
    def nouveauScore(type,val):	
        TAB_SCORES[type]["val"] = val
        text = TAB_SCORES[type]["txt"] 
        TAB_SCORES[type]["surf"] = policeScore.render(text,True,(0,0,0))
        TAB_SCORES[type]["rect"] = TAB_SCORES[type]["surf"].get_rect()
        TAB_SCORES[type]["rect"].top = TAB_SCORES[type]["top"]
        TAB_SCORES[type]["rect"].left = TAB_SCORES[type]["left"]
        
        TAB_SCORES[type]["surf_"] = policeScore.render(str(val),True,(200,120,150))
        TAB_SCORES[type]["rect_"] = TAB_SCORES[type]["surf_"].get_rect()
        TAB_SCORES[type]["rect_"].top = TAB_SCORES[type]["top"]
        TAB_SCORES[type]["rect_"].left = WIDTH - 60
        
    #####################################
    def get_last_num():
        n = 0
        for i,e in enumerate(TabObject):
            if e["num"] > n:
                n = e["num"]
        return n

    #####################################
    def get_first_hidden_index():
        index,n = -1,-1
        for i,e in enumerate(TabObject):
            if (n > e["num"] or n == -1) and e["visible"] == False and e["txt"] != "":
                n = e["num"]
                index = i
        return index

    #####################################
    def fixer_un_mot(word, i):
        num = get_last_num() + 1
        surf,rect = createTextObj(word)
        TabObject[i] = {"surf":surf, "rect":rect, "txt":word, "visible":False, "num":num }
        TabObject[i]["rect"].top = -10

    #####################################
    def creer_un_nouveau_mot(word):
        num = get_last_num() + 1
        surf,rect = createTextObj(word)
        TabObject.append({"surf":surf, "rect":rect, "txt":word, "visible":False, "num":num })
        i = len(TabObject) - 1
        TabObject[i]["rect"].top = -10 

    ######################################
    def mot_existe(mot):
        for i,e in enumerate(TabObject):
            if e["txt"] == mot:
                return i
        return -1

    #######################################
    def	delete_word(i):
        TabObject[i]["rect"].top = -10 
        TabObject[i]["visible"] = False
        TabObject[i]["num"] = get_last_num() + 1
        text = TabObject[i]["txt"]
        TabObject[i]["txt"] = ""
        textinput.clear_text()
        
        if IN_NETWORK:
            envoyer_le_mot_au_serveur(text)
        
    #######################################
    def envoyer_le_mot_au_serveur(text):
        text = "TARGET-WORD->"+text
        if CONNEXION != None:
            CONNEXION.send(text.encode("Utf8"))
        
    #####################################
    def action_event(event,delta):
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                word = textinput.get_text()
                index = mot_existe(word)
                if index >= 0:
                    delete_word(index)
        return True

    ###################################################
    def ajouter_nouveau_mot_alecran():
        # ajouter un word dans le screen
        index = get_first_hidden_index()
        if index != -1:
            TabObject[index]["visible"] = True
        return index
            
    ############ DEPLACEMENT DES MOTS ###################
    def deplacer_les_mots(delta):
        # mettre à jour la position des word visible	
        for i,e in enumerate(TabObject):
            if TabObject[i]["visible"]:	# uniquement les mots visibles
                TabObject[i]["rect"].y += int(SPEED*delta)
                if TabObject[i]["rect"].top > HEIGHT - (HAUT_BORD_RECT+30):
                    suivi_jeux["over"] = True
                    son_over.play()

    #####################################################
    def action_update(delta):
        if suivi_jeux["tick"]%50 == 0:
            index = ajouter_nouveau_mot_alecran()
            if index==-1: # si aucun mot n'a été trouvé, on rehitere la demande
                suivi_jeux["tick"] = 49
            else:
                suivi_jeux["tick"] = 0
                # nouveauScore("mot",int(time.time())%10 )
                # nouveauScore("car",int(time.time())%10 )
                # nouveauScore("gen",int(time.time())%10 )
        if not suivi_jeux["over"]:
            deplacer_les_mots(delta)
        suivi_jeux["tick"] = suivi_jeux["tick"] + 1

    ######################################
    def action_render(ecran):
        ecran.fill((0,0,0))
        # ecran.blit(geye_img,geye_rec)
        ecran.blit(surfDeBord,surfDeBordRect)
        ecran.blit(surfScores,rectScores)
        
        for i in range(len(TabObject)):
            if TabObject[i]["visible"]:  # uniquement les mots visibles
                ecran.blit(TabObject[i]["surf"], TabObject[i]["rect"] )
        
        # textinput_rect.center = (WIDTH/4 , HEIGHT - 50)
        ecran.blit(textinput.get_surface(), textinput_rect)
        
        ecran.blit(TAB_SCORES["car"]["surf"], TAB_SCORES["car"]["rect"])
        ecran.blit(TAB_SCORES["mot"]["surf"], TAB_SCORES["mot"]["rect"])
        ecran.blit(TAB_SCORES["gen"]["surf"], TAB_SCORES["gen"]["rect"])
        
        ecran.blit(TAB_SCORES["car"]["surf_"], TAB_SCORES["car"]["rect_"])
        ecran.blit(TAB_SCORES["mot"]["surf_"], TAB_SCORES["mot"]["rect_"])
        ecran.blit(TAB_SCORES["gen"]["surf_"], TAB_SCORES["gen"]["rect_"])
        
        pygame.display.flip()
        # print("tout va bien!!!")
        
    ######################################
    def main():
        # CONNEXION = conn
        running = True
        clock = pygame.time.Clock()
        
        create_actors()
        # création continue des mots
        if not IN_NETWORK :
            thread = Thread(target=fournir_les_mots)
            thread.start()
        
        while running==True:
            delta_ms = clock.tick(FPS)
            delta_s = delta_ms/1000.0
            events = pygame.event.get()
            for evt in events:
                running = action_event(evt,delta_s)
                
            textinput.update(events)
            if not suivi_jeux["over"]:
                action_update(delta_s)
                action_render(screen)
            
            
        
        pygame.quit()
        exit()
        return 0
	
if __name__ == '__main__':
	print("Bonjour très cher joueur!")
	main()