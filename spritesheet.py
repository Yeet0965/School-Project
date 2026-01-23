import pygame

class SpriteSheet():
    def __init__(self, image):
        self.sheet = image
    
    def get_image(self, sheet, width, height, colour, frame):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(sheet,(0, 0), ((frame * width), 0, width, height))
        image.set_colorkey(colour)
   
        return image
