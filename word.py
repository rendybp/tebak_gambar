import os
import pygame
import sys
EXEC_DIR = os.path.dirname(__file__)

class Word(object):
    def __init__(self, word):
        if sys.platform == 'darwin':
            self.word_image = os.path.join('nama_benda', word)
        else:
            self.word_image = os.path.join(EXEC_DIR, "nama_benda", word)
        self.word = word
        self.image = pygame.image.load(self.word_image)
        self.rect = self.image.get_rect()
        self.spelling_word = self.word.split('.')[0]
        self.letters = list(self.spelling_word)
        self.width = self.image.get_width()
        self.length = len(self.letters)
        
    def draw(self, screen, x, y):
        screen.blit(self.image, [x, y])
