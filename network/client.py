import socket, sys, threading, time
import test_pygame
class ThreadReception(threading.Thread):
	"""object thread gérant la réception des messages"""
	def __init__(self, HOST, PORT):
		threading.Thread.__init__(self)
		self.SC_W = 0
		self.SC_C = 0
		self.connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.connexion.connect((HOST, PORT))
		except socket.error:
			print("La connexion a échoué.")
			sys.exit()
		print("Connexion établie avec le serveur.")

		#self.start = False
		
	def run(self):
		self.dialogue_avec_serveur()
		
	# envoyer le nom du joueur au serveur et indiquer que le joueur est pret
	def dialogue_avec_serveur(self):
		# dialogue avec le serveur:
		print("Echange avec le serveur!!!!")
		while 1:
			msg = self.connexion.recv(1024).decode("utf8")
			tab = msg.split("->")
			cle = tab[0].upper()
			self.analyse_msg_serveur(cle,tab)
		
		self.connexion.close() # couper la connexion avec les serveur
		
	def analyse_msg_serveur(self,cle,tab):		
		# vérifier si le mot tappé est dans la liste de mots afficher à l'écran du joueur
		if cle == "TARGET-WORD" and len(tab)==2 :
			print("nouvelle reception du serveur: ",tab[1])	# on affiche au joueur les mot à saisir
			########################################################
			# INSERER UN NOUVEAU MOT DANS LE JEU
			test_pygame.reception_nouveau_mot(tab[1])
			# FIN INSERTION
			########################################################
		elif cle == "SC_W" and len(tab)==2 :
			self.SC_W = tab[1]
		elif cle == "SC_C" and len(tab)==2 :
			self.SC_C = tab[1]
		elif cle == "KILL" and len(tab)==2 :
			self.supprimer_un_mot(tab[1])
		
		# presentation du joueur
		elif cle in ["NOM","START"] and len(tab)==2 :
			rep = input(tab[1])
			self.envoyer_message(cle+"->"+rep)
			if(cle=="START" and rep.upper() == "YES"):
				# self.start = True
				try:
					# threading.Thread(target=self.saisir_mot, args=()).start()
					threading.Thread(target=test_pygame.main, args=()).start()
					test_pygame.connexion = self.connexion
					time.sleep(3)
					
					# thread = Thread(target=)
					# test_pygame.fournir_les_mots()
				except:
					print("************* Thread saisir mot did not start.*****************")

				# on peut démarrer le thread de saisie des mots
		else :
			print("Serveur--> "+("->".join(tab)))
	
	# il supprime un mot et affiche les scores du joueur
	def supprimer_un_mot(self,mot):
		print(mot," Eliminer.............")	
		print("Nombre des mots: ",self.SC_W)	
		print("Nombre des caractères: ",self.SC_C)
		test_pygame.nouveauScore("mot", self.SC_W )
		test_pygame.nouveauScore("car", self.SC_C )
		test_pygame.nouveauScore("gen", (int(self.SC_C) * int(self.SC_W)) )
	
	# saisie un mot et l'envoi au serveur
	def saisir_mot(self):
		while 1:
			mot = input("Saisir-> ")
			mot = "TARGET-WORD->"+mot
			self.envoyer_message(mot)
			
	def envoyer_message(self,text):
		self.connexion.send(text.encode("Utf8"))
	
	
HOST = '127.0.0.1'
PORT = 50000
th = ThreadReception(HOST, PORT)
th.start()

# time.sleep(60*60)


