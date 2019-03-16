TITLE_TYPING_RACE = "Typing Race"
IN_NETWORK = False
CONNEXION = None
WIDTH = 600
HEIGHT = 480
HAUT_BORD_RECT = 100
FPS = 30
SPEED = 50
COLOR_WHITE = (255,255,255)
COLOR_JAUNE = (255,255,0)
TXT_WIDTH = 200
TXT_HEIGHT = 30
ESPACEMENT = 40

HEIGHT_JEUX = HEIGHT - HAUT_BORD_RECT
w = WIDTH/2 + 4

TAB_SCORES = {
	"mot":{"val":0,"txt":"Score des mots saisis:"
			,"surf":None,"rect":None
			,"surf_":None,"rect_":None,"top":HEIGHT_JEUX+4,"left":w},
	"car":{"val":0,"txt":"Score des caractères tappés:"
			,"surf":None,"rect":None
			,"surf_":None,"rect_":None,"top":HEIGHT_JEUX+24,"left":w},
	"gen":{"val":0,"txt":"Score général:"
			,"surf":None,"rect":None
			,"surf_":None,"rect_":None
			,"top":HEIGHT_JEUX+48,"left":w}}

# global suivi_jeux # le nombre des tick qui sépare deux défilements de mots
suivi_jeux = {"tick":0,"over":False}