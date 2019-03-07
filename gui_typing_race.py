from sys import exit
import pygame_textinput
import pygame, time
from threading import Thread
from config import *
from word import Word
import os


class GuiTypingRace:

    def __init__(self):
        pass
    
    def run(self):
        self.main()

    def fournir_les_mots(self):
        word_processing = Word()
        file_name = "dic_words.txt"
        dir_path = os.path.dirname(os.path.realpath(__file__))
        path_file = os.path.join(dir_path, file_name)
        tabText = word_processing.get_all_words(path_file)
        
        j = -1
        while True and j!=len(tabText)-1:
            j=j+1
            mot = tabText[j]
            self.reception_nouveau_mot(mot)
            # time.sleep(0.003)
            
    def reception_nouveau_mot(self,mot):
        trouver = False
        # trouver des palces vacantes dans le TabObject et y mettre des nouveau mots et s'il n'y en a pas alors on ajoute une nouvelle case
        for i,e in enumerate(self.TabObject):
            if e["txt"] == "":
                self.fixer_un_mot(mot, i)
                trouver = True
                print("ancien:",i)
                break
        if not trouver :
            self.creer_un_nouveau_mot(mot)
            print("nouveau")
            
    ######################################
    def createTextObj(self,text,font="impact.ttf",taille=30,couleur=(255,255,255)):
        police = pygame.font.Font(font,taille)
        textSurf = police.render(text,True,couleur)
        rect = textSurf.get_rect()
        return textSurf, rect
        
    # création des acteurs
    def create_actors(self):
        pygame.init()
        
        pygame.display.set_caption("Typping Race")
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        
        self.TabObject = []
        
        # Create TextInput-object
        self.textinput = pygame_textinput.TextInput()
        self.textinput_rect = self.textinput.get_surface().get_rect()
        self.textinput_rect.top = HEIGHT - 50
        self.textinput_rect.left = WIDTH/4
        self.textinput.get_surface().fill((123,123,123))
        self.textinput.set_text_color(COLOR_WHITE)
        self.textinput.set_cursor_color(COLOR_WHITE)
        
        global surfDeBord, surfDeBordRect, surfScores, rectScores
        ###################################################
        # SURFACE DE GAUCHE LA SAISIE DES MOTS
        self.surfDeBord = pygame.Surface((WIDTH/2,HAUT_BORD_RECT))
        self.surfDeBord.fill((0,255,0))
        self.surfDeBordRect = self.surfDeBord.get_rect()
        self.surfDeBordRect.top = HEIGHT-HAUT_BORD_RECT
        ###################################################
        # SURFACE DE DROTIE LES SCORES
        surfScores = pygame.Surface((WIDTH/2,HAUT_BORD_RECT))
        surfScores.fill((0,255,0))
        rectScores = surfScores.get_rect()
        rectScores.top = HEIGHT-HAUT_BORD_RECT
        rectScores.left = WIDTH/2
        
        self.policeScore = pygame.font.Font("impact.ttf",16)
        self.nouveauScore("car",0)
        self.nouveauScore("mot",0)
        self.nouveauScore("gen",0)
        
        #son
        self.son = pygame.mixer.Sound("system-fault.ogg")
        self.son.set_volume(0.1)
        self.son_over = pygame.mixer.Sound("over.ogg")
        self.son_over.set_volume(0.1)
        
        global mfont
        mfont = pygame.font.Font("impact.ttf",70)

        
    ################################################
    def nouveauScore(self,type,val):	
        TAB_SCORES[type]["val"] = val
        text = TAB_SCORES[type]["txt"] 
        TAB_SCORES[type]["surf"] = self.policeScore.render(text,True,(0,0,0))
        TAB_SCORES[type]["rect"] = TAB_SCORES[type]["surf"].get_rect()
        TAB_SCORES[type]["rect"].top = TAB_SCORES[type]["top"]
        TAB_SCORES[type]["rect"].left = TAB_SCORES[type]["left"]
        
        TAB_SCORES[type]["surf_"] = self.policeScore.render(str(val),True,(200,120,150))
        TAB_SCORES[type]["rect_"] = TAB_SCORES[type]["surf_"].get_rect()
        TAB_SCORES[type]["rect_"].top = TAB_SCORES[type]["top"]
        TAB_SCORES[type]["rect_"].left = WIDTH - 60
        
    #####################################
    def get_last_num(self):
        n = 0
        for i,e in enumerate(self.TabObject):
            if e["num"] > n:
                n = e["num"]
        return n

    #####################################
    def get_first_hidden_index(self):
        index,n = -1,-1
        for i,e in enumerate(self.TabObject):
            if (n > e["num"] or n == -1) and e["visible"] == False and e["txt"] != "":
                n = e["num"]
                index = i
        return index

    #####################################
    def fixer_un_mot(self,word, i):
        num = self.get_last_num() + 1
        surf,rect = self.createTextObj(word)
        self.TabObject[i] = {"surf":surf, "rect":rect, "txt":word, "visible":False, "num":num }
        self.TabObject[i]["rect"].top = -10

    #####################################
    def creer_un_nouveau_mot(self,word):
        num = self.get_last_num() + 1
        surf,rect = self.createTextObj(word)
        self.TabObject.append({"surf":surf, "rect":rect, "txt":word, "visible":False, "num":num })
        i = len(self.TabObject) - 1
        self.TabObject[i]["rect"].top = -10 

    ######################################
    def mot_existe(self,mot):
        for i,e in enumerate(self.TabObject):
            if e["txt"] == mot:
                return i
        return -1

    #######################################
    def	delete_word(self,i):
        self.TabObject[i]["rect"].top = -10 
        self.TabObject[i]["visible"] = False
        self.TabObject[i]["num"] = self.get_last_num() + 1
        text = self.TabObject[i]["txt"]
        self.TabObject[i]["txt"] = ""
        self.textinput.clear_text()
        
        if IN_NETWORK:
            self.envoyer_le_mot_au_serveur(text)
        
    #######################################
    def envoyer_le_mot_au_serveur(self,text):
        text = "TARGET-WORD->"+text
        if CONNEXION != None:
            CONNEXION.send(text.encode("Utf8"))
        
    #####################################
    def action_event(self,event,delta):
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                word = self.textinput.get_text()
                index = self.mot_existe(word)
                if index >= 0:
                    self.delete_word(index)
        return True

    ###################################################
    def ajouter_nouveau_mot_alecran(self):
        # ajouter un word dans le screen
        index = self.get_first_hidden_index()
        if index != -1:
            self.TabObject[index]["visible"] = True
        return index
            
    ############ DEPLACEMENT DES MOTS ###################
    def deplacer_les_mots(self,delta):
        # mettre à jour la position des word visible	
        for i,e in enumerate(self.TabObject):
            if self.TabObject[i]["visible"]:	# uniquement les mots visibles
                self.TabObject[i]["rect"].y += int(SPEED*delta)
                if self.TabObject[i]["rect"].top > HEIGHT - (HAUT_BORD_RECT+30):
                    suivi_jeux["over"] = True
                    self.son_over.play()

    #####################################################
    def action_update(self,delta):
        if suivi_jeux["tick"]%50 == 0:
            index = self.ajouter_nouveau_mot_alecran()
            if index==-1: # si aucun mot n'a été trouvé, on rehitere la demande
                suivi_jeux["tick"] = 49
            else:
                suivi_jeux["tick"] = 0
                # nouveauScore("mot",int(time.time())%10 )
                # nouveauScore("car",int(time.time())%10 )
                # nouveauScore("gen",int(time.time())%10 )
        if not suivi_jeux["over"]:
            self.deplacer_les_mots(delta)
        suivi_jeux["tick"] = suivi_jeux["tick"] + 1

    ######################################
    def action_render(self,ecran):
        ecran.fill((0,0,0))
        # ecran.blit(geye_img,geye_rec)
        ecran.blit(self.surfDeBord,self.surfDeBordRect)
        ecran.blit(surfScores,rectScores)
        
        for i in range(len(self.TabObject)):
            if self.TabObject[i]["visible"]:  # uniquement les mots visibles
                ecran.blit(self.TabObject[i]["surf"], self.TabObject[i]["rect"] )
        
        # textinput_rect.center = (WIDTH/4 , HEIGHT - 50)
        ecran.blit(self.textinput.get_surface(), self.textinput_rect)
        
        ecran.blit(TAB_SCORES["car"]["surf"], TAB_SCORES["car"]["rect"])
        ecran.blit(TAB_SCORES["mot"]["surf"], TAB_SCORES["mot"]["rect"])
        ecran.blit(TAB_SCORES["gen"]["surf"], TAB_SCORES["gen"]["rect"])
        
        ecran.blit(TAB_SCORES["car"]["surf_"], TAB_SCORES["car"]["rect_"])
        ecran.blit(TAB_SCORES["mot"]["surf_"], TAB_SCORES["mot"]["rect_"])
        ecran.blit(TAB_SCORES["gen"]["surf_"], TAB_SCORES["gen"]["rect_"])
        
        pygame.display.flip()
        # print("tout va bien!!!")
        
    ######################################
    def main(self):
        # CONNEXION = conn
        running = True
        clock = pygame.time.Clock()
        
        self.create_actors()
        # création continue des mots
        if not IN_NETWORK :
            thread = Thread(target=self.fournir_les_mots)
            thread.start()
        
        while running==True:
            delta_ms = clock.tick(FPS)
            delta_s = delta_ms/1000.0
            events = pygame.event.get()
            for evt in events:
                running = self.action_event(evt,delta_s)
                
            self.textinput.update(events)
            if not suivi_jeux["over"]:
                self.action_update(delta_s)
                self.action_render(self.screen)
            
            
        
        pygame.quit()
        exit()
        return 0

if __name__ == '__main__':
    print("Start Typing Race")
    g = GuiTypingRace()
    g.run()
    print("Finish")


