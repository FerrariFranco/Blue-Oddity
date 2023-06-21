import pygame
pygame.init()
class Trampa:
    def __init__(self, origen, tamaño, imagen):
            img = pygame.image.load(imagen)
            self.image = pygame.transform.scale(img, tamaño)
            self.rect = pygame.Rect(origen, tamaño)
            
            self.sprites = [
            pygame.transform.scale(pygame.image.load('img/trampas/0.png'), tamaño),
            pygame.transform.scale(pygame.image.load('img/trampas/1.png'), tamaño),
            pygame.transform.scale(pygame.image.load('img/trampas/2.png'), tamaño),
            pygame.transform.scale(pygame.image.load('img/trampas/3.png'), tamaño),
            pygame.transform.scale(pygame.image.load('img/trampas/4.png'), tamaño),
            pygame.transform.scale(pygame.image.load('img/trampas/5.png'), tamaño),
            pygame.transform.scale(pygame.image.load('img/trampas/6.png'), tamaño),
            pygame.transform.scale(pygame.image.load('img/trampas/7.png'), tamaño),
            pygame.transform.scale(pygame.image.load('img/trampas/8.png'), tamaño),
            pygame.transform.scale(pygame.image.load('img/trampas/9.png'), tamaño),
            pygame.transform.scale(pygame.image.load('img/trampas/10.png'), tamaño),
            pygame.transform.scale(pygame.image.load('img/trampas/11.png'), tamaño),
            pygame.transform.scale(pygame.image.load('img/trampas/12.png'), tamaño),
            pygame.transform.scale(pygame.image.load('img/trampas/13.png'), tamaño),
            pygame.transform.scale(pygame.image.load('img/trampas/14.png'), tamaño),
            pygame.transform.scale(pygame.image.load('img/trampas/15.png'), tamaño)
        ]
            self.sprite_index = 0
        
    def dibujar(self, screen):
        self.sprite_index += 1
        if self.sprite_index >= len(self.sprites):
            self.sprite_index = 0
        self.image = self.sprites[self.sprite_index]
        screen.blit(self.image, self.rect)
    
