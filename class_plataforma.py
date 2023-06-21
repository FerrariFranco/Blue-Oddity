import pygame
pygame.init()
class Plataforma:
    def __init__(self, origen, tamaño, imagen):
            img = pygame.image.load(imagen)
            self.image = pygame.transform.scale(img, tamaño)
            self.rect = pygame.Rect(origen, tamaño)
        
    def dibujar(self, screen):
        screen.blit(self.image, self.rect)
    
