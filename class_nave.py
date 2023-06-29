import pygame

class Nave(pygame.sprite.Sprite):
    def __init__(self, tamaño, origen, imagen):
        pygame.sprite.Sprite.__init__(self)
        self.dimension = pygame.Surface(tamaño)
        self.imagen = pygame.image.load(imagen)
        self.imagen = pygame.transform.scale(self.imagen, tamaño)
        self.posicion = origen
        self.vida = 20  
        self.contador_pj = 0
        self.barra_vida = pygame.Rect(20, 20, self.vida * 10, 10) 

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.posicion)
        pygame.draw.rect(pantalla, (255, 0, 0), self.hitbox, 1)
        pygame.draw.rect(pantalla, (0, 255, 0), self.barra_vida) 
    
    def mover(self, delta_x, delta_y):
        nueva_posicion_x = self.posicion[0] + delta_x
        nueva_posicion_y = self.posicion[1] + delta_y

        if 0 <= nueva_posicion_x <= 750:
            self.posicion = (nueva_posicion_x, self.posicion[1])
        if 0 <= nueva_posicion_y <= 550:
            self.posicion = (self.posicion[0], nueva_posicion_y)
    
    def mover_hitbox(self, width, height):
        hitbox_x = self.posicion[0] + 19
        hitbox_y = self.posicion[1] + 20
        self.hitbox = pygame.Rect(hitbox_x, hitbox_y, width, height)
    
    def actualizar_barra_vida(self):
        ancho_barra = int(self.vida * 10) 
        self.barra_vida.width = ancho_barra
    
    def verificar_colision(self, proyectil_cont):
        sonido_retry = pygame.mixer.Sound("sfx/retry.wav")
        for proyectil in proyectil_cont:
            if proyectil.colision(self.hitbox):
                self.contador_pj += 1
                self.vida = 20 - self.contador_pj * 2
                self.actualizar_barra_vida()   
                #print(f"Te queda {self.vida * 10} de vida!")
                if self.vida < 0:
                    sonido_retry.play()
                    print("PERDISTE")
                    return True  

                proyectil_cont.remove(proyectil)