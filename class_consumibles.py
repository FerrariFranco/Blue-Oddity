import pygame
pygame.init()
class Consumibles:
    def __init__(self, origen, tamaño, tipo):
        if tipo == "vida":
            imagen = "img/consumibles/vida.png"  # Reemplaza "ruta_de_la_imagen_vida" con la ruta correcta para el consumible de vida
        elif tipo == "gema":
            imagen = "img/consumibles/gema.png"

        img = pygame.image.load(imagen)
        self.image = pygame.transform.scale(img, tamaño)
        self.rect = pygame.Rect(origen, tamaño)
        self.tipo = tipo
            
        
    def dibujar(self, screen):
        screen.blit(self.image, self.rect)
        
    

        
    