import pygame
import sys

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
#max_scroll = 200

#Variables for sprites
#sprite_sheet_image = pygame.image.load("Run.png").convert_alpha()
#sprite_sheet_image = pygame.transform.scale(sprite_sheet_image, (1024, 260))
#sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
cat = pygame.image.load("Idle.png").convert_alpha()
cat = pygame.transform.scale(cat, (150, 150))
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
        self.velocity_y = -15
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
     #Checking for if the player off screen in above.
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
            menu_state = "level_1"
        if level2_button.draw():
            menu_state = "level_2"
        if level3_button.draw():
            menu_state = "level_3"
    if menu_state == "level_1":    
        character.draw()
        character.movement()

    if menu_state == "level_2":  
        character.draw()
        character.movement()

    if menu_state == "level_3":  
        character.draw()
        character.movement()




    
      


       
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