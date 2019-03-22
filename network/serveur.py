import socket, sys, threading, random, time

phrase = """ administrateurs système ont souvent besoin de concevoir des petits programmes
pour automatiser certaines tâches. Ils utilisent généralement l’interpréteur de commandes, qui offre une syntaxe basique pourconcevoir des séquences d’opérations. 
Toutefois ce système est très limité et n’offre que des fonctionnalités de très haut
niveau : certaines opérations sur le système ne sont pas possibles sans appels à des
programmes annexes.
Utiliser des langages de plusbas niveau comme le C permet de lever ces limitations,
mais la conception des scripts devient vite fastidieuse et délicate. 
Python, conçu à l’origine pour ce cas de figure, s’intercale entre l’interpréteur de commandes et le C, en proposant un niveau intermédiaire, c’est-à-dire un shell surpuissant,
et dans le même temps un langage de programmation plus simple et plus direct.
Bien que ce genre de besoin soit plus fréquent sur  systèmes Unices ( systèmes
de la famille Unix), il n’est plus rare de rencontrer des administrateurs Windows qui
aient adopté Python pour la conception de leurs scripts système."""

	
phrase = "Server side open a socket on a port listen for a message from a client and send an echo reply echoes lines until eof when client closes socket spawns a thread to handle each client connection threads share global memory space with main thread this is more portable than fork threads work on standard Windows systems but process forks do not"
	
DICTIONNAIRE_JEU = phrase.split(" ")


class ThreadClient(threading.Thread):
	"""object thread gérant la réception des messages"""
	def __init__(self, conn):
		threading.Thread.__init__(self)
		self.connexion = conn 			# réf du socket de connexion
		self.thread_name = ""
		self.score_word = 0
		self.score_caracter = 0
		
	def run(self):
		# dialogue avec le lcient:
		nom = self.getName()				# chaque thread possède un nom
		self.thread_name = nom
		while 1:
			try:
				message_recu = self.connexion.recv(1024).decode("utf8")
				if(not self.analyser_message_client(message_recu)):
					break
			except socket.error:
				print("La connexion a été perdue.")
				break
		# fermeture de la connexion avec le joueur
		print(D_client[self.thread_name]["player"]," vient de quitter le jeu")
		self.connexion.close() # couper la connexion avec les serveur
		
	# si l'analyse du message échoue alors on coupe la communication avec le joueur
	def analyser_message_client(self,msg):
		tab = msg.split("->")
		cle = tab[0].upper()
		
		# vérifier si le mot tappé est dans la liste de mots afficher à l'écran du joueur
		if cle == "TARGET-WORD" and len(tab)==2 :
			self.verifier_mot(tab[1])
		
		elif cle == "LOST-WORD" and len(tab)==2 :		# si un mot disparait de l'ecrant du joueur	
			D_player_word[self.thread_name].remove(tab[1])
		
		elif cle == "MATCH" and tab[1] == "PERDU":	# si le joueur a perdu
			self.retire_moi_jai_perdu()
			return False
		
		elif cle == "NOM" and len(tab)==2:					# fixer le nom exacte du joueur
			D_client[self.thread_name]["player"] = tab[1]
			msg = "Bienvenu "+tab[1]+",\nNous attendons encore tous les joueurs avec de lancer le jeu.\nEt donc Merci de patienter."
			self.envoyer_msg_au_joueur(msg)
			print(msg)
			
		elif cle == "START" and len(tab)==2:					# fixer le nom exacte du joueur
			D_client[self.thread_name]["start"] = tab[1].upper()
			print("Bien Noté ",D_client[self.thread_name]["player"])
		
		
		if self.suis_le_gagnant():												# si le joueur est le gagnant
			nom_joueur = D_client[self.thread_name]["player"]
			print("Le gagnant est: %s" % nom_joueur )
			return False
		
		return True
	
	# si le joueur a perdu, son thread est retiré du dictionnaire et tous les autres sont informés
	def retire_moi_jai_perdu(self):
		del D_client[self.thread_name]
		# L_id_player.remove(self.thread_name)
		msg = ("info->Plus que %s Joueur(s), %s vient de perdre,." %( len(D_client), client["player"]) )
		print(msg)
		self.envoyer_a_tous_les_players(msg)
		
	# vérifie si je suis le gagnant, càd le seul sur le jeux
	def suis_le_gagnant(self):
		return len(D_client) == 1 and self.score_word != 0
		
		
	def verifier_mot(self,mot):
		"""vérifie si un mot tapé par le client est encore dans la liste"""
		if mot in D_player_word[self.thread_name]:
			self.score_caracter+= len(mot)
			self.score_word+= 1
			D_player_word[self.thread_name].remove(mot) #
			self.envoyer_msg_au_joueur("SC_C-> %s " % self.score_caracter)
			time.sleep(0.5)
			self.envoyer_msg_au_joueur("SC_W-> %s " % self.score_word)
			time.sleep(0.5)
			self.envoyer_msg_au_joueur("KILL-> %s " % mot)
		else:
			self.envoyer_msg_au_joueur("MISS->\""+mot+"\" n'est pas sur la liste")
			
	# permet d'envoyer un même message à tous les joueurs 
	def envoyer_a_tous_les_players(msg):
		# faire suivre le message à tous les autres joueurs
		for cle in D_client:
			D_client[cle]["conx"].send(msg.encode("UTF8"))
		
	def envoyer_msg_au_joueur(self,msg):		
			self.connexion.send(msg.encode("UTF8"))
			

# =================================================================

def send_msg_to_players(msge):
	global D_client
	for cle in D_client:
		D_client[cle]["conx"].send(msge.encode("UTF8"))
		
def are_all_players_ready():
	global D_client
	result = True
	msge = "Etes-vous ready to start???"
	for cle in D_client:
		if D_client[cle]["start"] != "YES" :
			if D_client[cle]["start"] != "DEJA-ASCK":
				player = D_client[cle]["player"]
				text = "START->\n\nSalut "+player+" "+msge
				D_client[cle]["conx"].send(text.encode("UTF8"))
				D_client[cle]["start"] = "DEJA-ASCK"
			result = False
	return result
		
def demarrer_le_jeu():
	"""demarre le jeu, génère les mots et crée une copie pour chaque joueur"""
	while 1:
		words = selectionnner_mots()
		envoyer_les_mots_aux_joueurs(words)
		print("Mots lancés:",words)
		time.sleep(3)
		
def envoyer_les_mots_aux_joueurs(words):
	"""envoi un mot à tous les joueurs, puis un autre, puis un autre"""
	global D_client,D_player_word
	for word in words:
		for cle in D_client:
			D_client[cle]["conx"].send(("TARGET-WORD->"+word).encode("UTF8"))
			D_player_word[cle].append(word)			
		
def selectionnner_mots():
	global DICTIONNAIRE_JEU
	taille = len(DICTIONNAIRE_JEU)
	nbr_mot = 2
	word = []
	for i in range(nbr_mot):
		j = random.randrange(0, taille )
		word.append(DICTIONNAIRE_JEU[j])
	return word

	

HOST = '127.0.0.1'
PORT = 50000
counter = 0  # compteur de connexions actives

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	mySocket.bind((HOST,PORT))
except socket.error:
	print("la liaision du socket à l'adresse choisie a choué.")
	sys.exit()
	
print("Serveur prêt, en attente de requêtes...")
mySocket.listen(5)


# attente et prise en charge des connexions clientes
D_client = {} # dictionnaire au format : {nom_thread:{player:"nom du joueur",conx:Objet Connexion},...}
L_id_player = []
D_player_word = {} # de la forme {nom_thread:[mot1,mot2,...],...}
nbr_player = 2
while 1:
	connexion, adresse = mySocket.accept()
	
	th = ThreadClient(connexion)#créer un nouvel objet thread pour gérer la connexion:
	th.start()	
	
	client 						= {}
	thread_name				= th.getName()
	client["player"] 	= thread_name		# le nom du thread rattacher au client
	client["start"] 	= ""		# le nom du thread rattacher au client
	client["conx"] 		= connexion			# l'objet qui va permettre d'échanger avec le joueur
	D_client[thread_name] = client		# mémoriser la connexion dans le dictionnaire
	D_player_word[thread_name] = []
	
	msg = "NOM->Vous êtes bien connecté, Vous indiquez votre nom SVP! "
	connexion.send(msg.encode("UTF8")) # envoi du message au client
	
	print("Clien %s connecté, adresseIP %s, port %s." %(thread_name,adresse[0],adresse[1]))
	if nbr_player == len(D_client):
		print("le nombre des jouers est atteint\nLancement du test de connectivité:\n")
		while(not are_all_players_ready()):
			time.sleep(1)
		break # arrêt de la grande boucle
	# vérifier si tout le monde a dit oui
print("+++++DEMARRAGE DU JEU+++++")
time.sleep(10)
demarrer_le_jeu()
