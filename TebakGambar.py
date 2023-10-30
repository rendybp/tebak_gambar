import os
import pygame
from pygame.locals import *
from pygame.color import THECOLORS
from word import Word
import random
import sys
from faces import Face

EXEC_DIR = os.path.dirname(__file__)
header_image = pygame.image.load(os.path.join(EXEC_DIR, "judul", "header.png"))  

### Test for platform since the .app bundle behaves strangely
if sys.platform == 'darwin':
    image_dir = os.walk("nama_benda")
else:
    image_dir = os.walk(os.path.join(EXEC_DIR, "nama_benda"))


pygame.init()
pygame.display.set_caption("Tebak Gambar")
#### Globals
screen = pygame.display.set_mode((650, 650))
font = pygame.font.SysFont('Helvetica', 50)
clock = pygame.time.Clock()
image_list = []
right = False
wrong = False
entered_text = []
screen_x, screen_y = screen.get_size()

### Generate list of files from the image folder ####
for root, dir, files in image_dir:
    for file in files:
        if '.DS_Store' not in file:
            image_list.append(file)


### Create inital image on screen
the_word = Word(random.choice(image_list))
#the_word = Word('yo-yo.png')

#### Keys to ignore while entering letters
ignored_keys = ('escape', 'return', 'backspace', 'enter', 'space', 'right shift'\
                ,'left shift', 'left meta', 'right meta', 'f1', 'f2', 'f3', 'f4', 'f5'\
                ,'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'caps lock')

### Faces and groups to hold them
happy = Face('happy')

sad = Face('sad')

happy_group = pygame.sprite.GroupSingle()

sad_group = pygame.sprite.GroupSingle()
hyphen = False

#### main function and loop ###
def main():
   
    global the_word
    global entered_text
    global ignored_keys
    global wrong
    global right
    global hyphen
    
    running = True
    pygame.key.set_repeat(0,0)
    while running:
        cursor = 0
        letter_position = dict()
        key = pygame.key.get_pressed()
        mods = pygame.key.get_mods()
        screen.fill(THECOLORS['white'])
        
        header_x = (screen_x - header_image.get_width()) // 2
        header_y = 5
        screen.blit(header_image, (header_x, header_y))
        
        the_word_x = (screen_x - the_word.width) // 2
        the_word_y = header_y + header_image.get_height() + 5
        
        the_word.draw(screen, the_word_x, the_word_y)
        
        
        # the_word.draw(screen, (screen_x/2 - the_word.width/2), 50)

        ### Begin calculations for total width of area for typing
        num_lines = len(the_word.letters)  ### Number of lines
        underline_width = 40                     ### Width of underlines
        text_total_width = (num_lines * underline_width) + ((num_lines - 1) * 20) ### Total width of lines and spaces
        line_x1 = screen_x/2 - text_total_width/2
        
        ### List to hold where to begin each letter
        letter_beginning_list = []
        
        ### Beginning letter position, will be updated ###
        letter_beginning = screen_x/2 - text_total_width/2
        
        #x2 = letter_beginning
        red = (255, 10, 10)
        white = (255, 255, 255)
        
        ### This establishes the keys for the dict ###
        letter_keys = range(0, the_word.length)
        
        #### Create lines for beneath letters and get size and position to draw letters ####
        #letter_position_dict = dict.fromkeys(letter_keys)
        
        
        for letter in the_word.letters:
            letter_size = font.size(letter)
            #print(letter_size[0])
            letter_beginning_list.append([letter_beginning + (underline_width/2 - letter_size[0]/2), letter])
            correct_letter = font.render(letter, 1, (255, 10, 10))
            letter_size = font.size(letter)                        
            if letter == "-":
                screen.blit(correct_letter, [letter_beginning + (underline_width/2 - letter_size[0]/2), 500])             
            letter_beginning += underline_width + 20 
            
            line_x2 = line_x1 + underline_width 
            pygame.draw.line(screen, THECOLORS['black'], (line_x1, 560), (line_x2, 560), 2)
            line_x1 += underline_width + 20 
            line_x2 += underline_width + 20 
        
        #print(letter_beginning_list)

        letter_dict = dict(zip(letter_keys, letter_beginning_list))
        #print(letter_dict)
        
        
        
        #print(letter_position_dict)

        #### Handle sad face lifespan ####
        if sad.lifespan == 0:
            sad_group.empty()
            wrong = False
        sad_group.update()
        
        ### Handle happy face lifespan ####
        if happy.lifespan == 0:
            happy_group.empty()
            right = False
            the_word = Word(random.choice(image_list))
            happy.reset()
        happy_group.update()
        
        #### Handle answer ####
        if right:
            clock.tick(10)
            happy_group.draw(screen)
            entered_text = []
        if wrong:
            clock.tick(10)
            sad_group.draw(screen)
            entered_text = []

        #### Handle quit key presses ###
        if key[pygame.K_ESCAPE]:
            sys.exit()
        elif (mods & KMOD_META):
            if key[pygame.K_q]:
                sys.exit()
        if hyphen:
            entered_text.append('-')
            hyphen = False

        #### Handle events ###
        for event in pygame.event.get():

            ### Handle closing of window ###
            if event.type == pygame.QUIT:
                    sys.exit()
                
            ### Handle typed letters ###
            if event.type == pygame.KEYDOWN:
                key_value = pygame.key.name(event.key)
                if key_value == 'backspace':
                    if entered_text:
                        entered_text.pop()

                if key_value not in ignored_keys:
                    entered_text.append(key_value)
                    print(entered_text)
                
                if key_value == 'return':
                    hyphen_pos = [i for i,x in enumerate(the_word.letters) if x == '-']
                    print(hyphen_pos)
                    if hyphen_pos:
                        del(the_word.letters[int(hyphen_pos[0])])

                    if entered_text == the_word.letters:
                        happy_group.add(happy)
                        right = True
                    else:
                        sad.reset()
                        sad_group.add(sad)
                        wrong = True
       
        
            
        #### Render typed letters on screen ####
        for letter in entered_text:                                          
            if not letter == 'backspace':
                if letter_dict.get(cursor)[1] == '-':
                    cursor += 1

                correct_letter = font.render(letter, 1, (255, 10, 10))
                letter_size = font.size(letter)                        
                screen.blit(correct_letter, [letter_dict.get(cursor)[0], 500])             
                cursor += 1
        
        pygame.display.update()                                              
        clock.tick(15)
        
if __name__ == "__main__":
    main()

