import pygame
import sys
import spritesheet
from pygame.locals import *
#import sprite
pygame.init()
#import the pygame module

screen = pygame.display.set_mode((1620, 780))
pygame.display.set_caption("My Game")
background = pygame.image.load("background.png").convert()
background = pygame.transform.scale(background, (1620, 780))
#Create a window with an interface

#frame rate
clock = pygame.time.Clock()
FPS = 60

#The variable containing images of the buttons
start = pygame.image.load("start.png").convert_alpha()
exit =  pygame.image.load("exit.png").convert_alpha()

level1_img = pygame.image.load("level1.png").convert_alpha()
level1_img = pygame.transform.scale(level1_img, (86, 96))

level2_img = pygame.image.load("level2.png").convert_alpha()
level2_img = pygame.transform.scale(level2_img, (86, 96))

level3_img = pygame.image.load("level3.png").convert_alpha()
level3_img = pygame.transform.scale(level3_img, (86, 96))


#Game Variable
menu_state = "home"
gravity = 1
tile_size = 60
game_over = 0
#max_scroll = 200

#Variables for sprites
cat = pygame.image.load("Idle.png").convert_alpha()
cat = pygame.transform.scale(cat, (150, 150))
endpoint = pygame.image.load("endpoint.png").convert_alpha()
platform2 = pygame.image.load("platform2.png").convert_alpha()

#Create animation list
#animation_list = []
#animation_steps = 4
#last_update = pygame.time.get_ticks()
#animation = 300
#frame = 0

#black = (0, 0, 0)

#for x in range (animation_steps):
    #animation_list.append(sprite_sheet.get_image(sprite_sheet_image, 256, 256, black, 0))

#frame_0 = sprite_sheet.get_image(sprite_sheet_image, 256, 256, black, x)


#colours
white = (255, 255, 255)


#Player class
class Player():
   def __init__(self, x, y):
      self.image = cat
      self.width = 84
      self.height = 130
      self.rect = pygame.Rect(0, 0, self.width, self.height)
      self.rect.center = (x, y)
      self.flip = False

      self.velocity_y = 0
      self.jumped = False
      self.space_pressed = False
    
    #Key inputs
   def movement(self):
     delta_x = 0
     delta_y = 0 

    #get key inputs
     key = pygame.key.get_pressed()
     if key [pygame.K_SPACE] and self.jumped == False:
        self.velocity_y = -20
        self.jumped = True
        self.space_pressed = True
     if not key[pygame.K_SPACE]:
        self.space_pressed = False
     if key[pygame.K_SPACE]:
        self.jumped = False
     if key[pygame.K_a]:
        delta_x = -10
        self.flip = True
     if key[pygame.K_d]:
        delta_x = 10
        self.flip = False


       
     
     #adding gravity
     self.velocity_y +=1 
     if self.velocity_y > 10:
        #makes it never go past to 10
        self.velocity_y = 10
     
     delta_y += self.velocity_y

#check for collision
     for tile in level.tile_list:
        #checing for collision in x axis
        if tile[1].colliderect(self.rect.x + delta_x, self.rect.y, self.width, self.height):
            delta_x = 0
        #checking for collision in y axis
        if tile[1].colliderect(self.rect.x, self.rect.y + delta_y, self.width, self.height):
           #Checking if below is ground for jumping amd hitting head
           if self.velocity_y < 0:
              delta_y = tile[1].bottom - self.rect.top
              self.velocity_y = 0
              #Checking if above is ground for falling and hitting feet
           elif self.velocity_y >= 0:
              delta_y = tile[1].top - self.rect.bottom
              self.velocity_y = 0
        #checking for collision with hazards
        if pygame.sprite.spritecollide(self, hazards, False):
           self.rect.x = 60
           self.rect.y = 720

    #checking for if player goes off screen or not
     if self.rect.left + delta_x < 0:
         delta_x = -self.rect.left
  
  
     if self.rect.right + delta_x > 1620:
         delta_x = 1620 - self.rect.right
     #checking for if player goes off screen in below
     if self.rect.bottom + delta_y >= 780:
        delta_y = 780 - self.rect.bottom
        self.velocity_y = 0
        self.jumped = False
    #checking for if player goes off screen in above
     if self.rect.top + delta_y <= 0:
        delta_y = 0

     

    #update position
     self.rect.x += delta_x
     self.rect.y += delta_y
   
       
   def draw(self):
      screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 30, self.rect.y - 18))
      pygame.draw.rect(screen, white, self.rect, 2)
      

character = Player(100, 500)


#classes of buttons
class Button():

    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
#Makes buttons
    def draw(self):
        action = False
        #Get the postion of the mouse
        mouse_position = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_position):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

#creating instances
start_button = Button (1200, 200, start)
exit_button = Button (1200, 400, exit)
level1_button = Button (1300, 150, level1_img)
level2_button = Button (1300, 350, level2_img)
level3_button = Button (1300, 550, level3_img)

def grid():
   # horizontal lines (13 tiles)
    for line in range(0, 13):   
        pygame.draw.line(
            screen,
            (255, 255, 255),
            (0, line * tile_size),
            (1620, line * tile_size)
        )

    # vertical lines (27 tiles)
    for line in range(0, 27):  
        pygame.draw.line(
            screen,
            (255, 255, 255),
            (line * tile_size, 0),
            (line * tile_size, 780)
        )

class Load_World():
   def __init__(self,data):
     #storing the data
     self.tile_list = []
      #iterate through each of the row
     row_count = 0
     for row in data:
         collumn_count = 0
         #within each row, look at individuall column
         for tile in row:
             if tile == 1:
            #transform the image into 60x60 tile square
                 image = pygame.transform.scale(platform2, (tile_size, tile_size))
                 #create the rectangle object for further collision set up
                 image_rect = image.get_rect()
                 #Creating the images by incrementing coordinates as iteration continue
                 image_rect.x = collumn_count * tile_size
                 image_rect.y = row_count * tile_size
                 #saving 2 values into tile tuple
                 tile = (image, image_rect)
                 self.tile_list.append(tile)





             if tile == 2:
                hazard = Hazard(collumn_count * tile_size, row_count * tile_size)
                hazards.add(hazard)
            

             collumn_count += 1
         row_count += 1   


   def draw(self):
     for tile in self.tile_list:
         screen.blit(tile[0], tile[1])

hazards = pygame.sprite.Group()
class Hazard(pygame.sprite.Sprite):
    def __init__(self, x, y):
     pygame.sprite.Sprite.__init__(self)
     image = pygame.image.load("hazard.png")
     self.image = pygame.transform.scale(image, (tile_size, tile_size))
     self.rect = self.image.get_rect()
     self.rect.x = x
     self.rect.y = y         

level1_data =[
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0 , 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0 , 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0],
[0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0 , 0],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

level2_data =[
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0],
[0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0],
[0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0],
[0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0],
[0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0],
[0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0],
[0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

level3_data =[
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]







running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        #pressing "x" at the corner of the window quits the game
        if event.type == pygame.QUIT:
            running = False
      
                
#Does not make the window crash after running and allow the user to close the app anytime they wish
    screen.blit(background, (0,0))
    if menu_state == "home":
        
        
        if start_button.draw():
         menu_state = "choose_levels"
            
#If the exit button is clicked it quit the game
        if exit_button.draw():
         pygame.quit()
         sys.exit()
    #Draws the levels buttons due to game variable being changed
    #Allows the user to choose levels
    if menu_state == "choose_levels":
        if level1_button.draw():
            level = Load_World(level1_data)
            menu_state = "level_1"
        if level2_button.draw():
            level = Load_World(level2_data)
            menu_state = "level_2"
        if level3_button.draw():
            level = Load_World(level3_data)
            menu_state = "level_3"
    if menu_state == "level_1":    
        character.draw()
        character.movement()
        level.draw()
        hazards.draw(screen)
        grid()
        

    if menu_state == "level_2":  
        character.draw()
        character.movement()
        level.draw()
        hazards.draw(screen)
        grid()

    if menu_state == "level_3":  
        character.draw()
        character.movement()
        level.draw()
        hazards.draw(screen)
        grid()




    
      


       
    pygame.display.flip()
pygame.quit()













 #Animation updating
     #current_time = pygame.time.get_ticks()
     #if current_time - last_update >= animation:
        #frame +=1
        #if frame >= len(animation_list):
          #frame = 0
        #last_update = current_time

      #show animate sprites
     #screen.blit(animation_list[frame], (0, 0))
     #Draw character