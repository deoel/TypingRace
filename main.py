from gui import Gui
from word_manager import WordManager
import os
from config import *
from random import randrange

class Main:
	def __init__(self):
		self.tick = 0
		self.over = False
		
		wordManager = WordManager()
		file_name = "dic_words.txt"
		dir_path = os.path.dirname(os.path.realpath(__file__))
		path_file = os.path.join(dir_path, file_name)
		words = wordManager.get_all_words(path_file)
		
		if not IN_NETWORK :
			width = 1000
			height = 700
			bordHeight = 100
			gui = Gui(width,height,bordHeight)
			gui.start()
			
			for w in words:
				larg,index = gui.createWordLabel(w)
				left = randrange(width - larg)
				gui.setCoordonateWordLabel(index,left)
				
		

if __name__ == '__main__':
		print("Start Typing Race")
		g = Main()
		print("Finish")