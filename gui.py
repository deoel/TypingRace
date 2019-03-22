from sys import exit
import pygame_textinput
import pygame, time
from config import *
from threading import Thread

class Gui(Thread):

	def __init__(self,width,height,bordBottomHeight):
		Thread.__init__(self)
		self.tick = 0
		self.over = False	
		self.tabLabelWord = []
		self.width = width
		self.height = height
		self.bordBottomHeight = bordBottomHeight
		self.height_jeux = height - bordBottomHeight
	
	def run(self):
		self.drawScreen()
		self.drawBordBottom()
		self.addInputTextOnBordB()
		self.addScorePartOnBordB()		
		self.showWindow()
		
	def drawScreen(self):
		pygame.init()
		
		pygame.display.set_caption("Typping Race")
		self.screen = pygame.display.set_mode((self.width,self.height))
		self.policeScore = pygame.font.Font("fonts/impact.ttf",16)
		self.mfont = pygame.font.Font("fonts/impact.ttf",70)
				
		
	def drawBordBottom(self):
		width_2 = self.width/2 # largeur de la fenêtre divisée par deux
		size 	= (width_2, self.bordBottomHeight) # dimenssion de deux rectangle du tableau de bord
		top 	= self.height_jeux # hauteur qui sépare le tableau de bord 
		green_color = (0,255,0)
		###################################################
		# SURFACE DE GAUCHE LA SAISIE DES MOTS
		self.surfDeBord = pygame.Surface(size)
		self.surfDeBord.fill(green_color)
		self.surfDeBordRect = self.surfDeBord.get_rect()
		self.surfDeBordRect.top = top
		###################################################
		# SURFACE DE DROTIE LES SCORES
		self.surfScores = pygame.Surface(size)
		self.surfScores.fill(green_color)
		self.rectScores = self.surfScores.get_rect()
		self.rectScores.top = top
		self.rectScores.left = width_2
		
	def addInputTextOnBordB(self):
		self.textinput = pygame_textinput.TextInput()
		self.textinput_rect = self.textinput.get_surface().get_rect()
		self.textinput_rect.top = self.height - 50
		self.textinput_rect.left = self.width/4
		self.textinput.get_surface().fill((123,123,123))
		# self.textinput.set_text_color(COLOR_WHITE)
		# self.textinput.set_cursor_color(COLOR_WHITE)
		
	def addScorePartOnBordB(self):
		w = self.width/2 + 4
		self.TAB_SCORES = {
			"mot":{"val":0,"txt":"Score des mots saisis:"
					,"surf":None,"rect":None
					,"surf_":None,"rect_":None,"top":self.height_jeux+4,"left":w},
			"car":{"val":0,"txt":"Score des caractères tappés:"
					,"surf":None,"rect":None
					,"surf_":None,"rect_":None,"top":self.height_jeux+24,"left":w},
			"gen":{"val":0,"txt":"Score général:"
					,"surf":None,"rect":None
					,"surf_":None,"rect_":None
					,"top":self.height_jeux+48,"left":w}}
			
		self.updateScore("car",0)
		self.updateScore("mot",0)
		self.updateScore("gen",0)

	################################################
	def updateScore(self,type,val):	
		self.TAB_SCORES[type]["val"] = val
		text = self.TAB_SCORES[type]["txt"] 
		self.TAB_SCORES[type]["surf"] = self.policeScore.render(text,True,(0,0,0))
		self.TAB_SCORES[type]["rect"] = self.TAB_SCORES[type]["surf"].get_rect()
		self.TAB_SCORES[type]["rect"].top = self.TAB_SCORES[type]["top"]
		self.TAB_SCORES[type]["rect"].left = self.TAB_SCORES[type]["left"]
		
		self.TAB_SCORES[type]["surf_"] = self.policeScore.render(str(val),True,(200,120,150))
		self.TAB_SCORES[type]["rect_"] = self.TAB_SCORES[type]["surf_"].get_rect()
		self.TAB_SCORES[type]["rect_"].top = self.TAB_SCORES[type]["top"]
		self.TAB_SCORES[type]["rect_"].left = self.width - 60
	
	def currentScore(self,type):
		return self.TAB_SCORES[type]["val"]
		
	def showWindow(self):
		running = True
		clock = pygame.time.Clock()
		
		while running==True:
			events = pygame.event.get()
			for evt in events:
				running = self.get_player_action(evt)
					
			self.textinput.update(events)
			if not self.over:
				self.addWordLabelOnScreen( )
				delta_s = clock.tick(FPS)/1000.0
				self.moveWordLabelOnScreen(delta_s)
				self.render_screen_element()
		
		pygame.quit()
		exit()
		return 0
		
	def createWordLabel(self, word):
		
		num = 0
		if len(self.tabLabelWord) != 0:
			index = len(self.tabLabelWord) - 1
			lastLabel = self.tabLabelWord[index]
			num = lastLabel["num"] + 1
			
		font="fonts/CurvedSquare.ttf"
		taille=30
		couleur=(255,255,255)
		police = pygame.font.Font(font,taille)
		surf = police.render(word,True,couleur)
		rect = surf.get_rect()
		
		data = {"surf":surf, "rect":rect, "txt":word, "visible":False, "num":num }
		data["rect"].top = -10
		self.tabLabelWord.append(data)
		return rect.width,len(self.tabLabelWord)-1
				
	def addWordLabelOnScreen(self):
		# ajouter un word dans le screen
		if self.tick == 50:
			index,n = -1,-1
			# trouvons le mot caché avec le N° d'ordre le plus petit
			for i,e in enumerate(self.tabLabelWord):
				if (n > e["num"] or n == -1) and e["visible"] == False and e["txt"] != "":
					n = e["num"]
					index = i
			
			
			self.tick = 49
			# on ajouter le mot trouvé sur le screen
			if index != -1:
				self.tabLabelWord[index]["visible"] = True
				self.tick = 0
				
		self.tick = self.tick + 1
		
	def moveWordLabelOnScreen(self,delta):
		# mettre à jour la position des word visible	
		for i,e in enumerate(self.tabLabelWord):
			if self.tabLabelWord[i]["visible"]:	# uniquement les mots visibles
				self.tabLabelWord[i]["rect"].y += int(SPEED*delta)
				if self.tabLabelWord[i]["rect"].top > self.height_jeux - 30:
					self.over = True
					
					son_over = pygame.mixer.Sound("over.ogg")
					son_over.set_volume(0.1)
					son_over.play()
	
	def setCoordonateWordLabel(self,index,left):
		self.tabLabelWord[index]["rect"].left = left
	
	#####################################
	def get_player_action(self,event):
		if event.type == pygame.QUIT:
			return False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN:
				word = self.textinput.get_text().lower()
				self.delete_word_if_exist(word)
		return True
	
	def delete_word_if_exist(self,word):
		for i,e in enumerate(self.tabLabelWord):
			if e["txt"] == word and e["visible"] :
				self.textinput.clear_text()
				del self.tabLabelWord[i]				
				self.updateScore("car",(self.currentScore("car")+len(word)))
				self.updateScore("mot",(self.currentScore("mot")+1))
				# if IN_NETWORK:
						# self.envoyer_le_mot_au_serveur(text)
		
				break

	######################################
	def render_screen_element(self):
		self.screen.fill((0,0,0))
		# self.screen.blit(geye_img,geye_rec)
		self.screen.blit(self.surfDeBord,self.surfDeBordRect)
		self.screen.blit(self.surfScores,self.rectScores)
		
		for i in range(len(self.tabLabelWord)):
			if self.tabLabelWord[i]["visible"]:	# uniquement les mots visibles
				self.screen.blit(self.tabLabelWord[i]["surf"], self.tabLabelWord[i]["rect"] )
		
		# textinput_rect.center = (WIDTH/4 , HEIGHT - 50)
		self.screen.blit(self.textinput.get_surface(), self.textinput_rect)
		
		self.screen.blit(self.TAB_SCORES["car"]["surf"], self.TAB_SCORES["car"]["rect"])
		self.screen.blit(self.TAB_SCORES["mot"]["surf"], self.TAB_SCORES["mot"]["rect"])
		self.screen.blit(self.TAB_SCORES["gen"]["surf"], self.TAB_SCORES["gen"]["rect"])
		
		self.screen.blit(self.TAB_SCORES["car"]["surf_"], self.TAB_SCORES["car"]["rect_"])
		self.screen.blit(self.TAB_SCORES["mot"]["surf_"], self.TAB_SCORES["mot"]["rect_"])
		self.screen.blit(self.TAB_SCORES["gen"]["surf_"], self.TAB_SCORES["gen"]["rect_"])
		
		pygame.display.flip()
		
