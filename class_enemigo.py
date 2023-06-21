import pygame
import random

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, posicion, velocidad):
        super().__init__()
        self.contador_pasos = 0
        img = pygame.image.load('img/tiles/roca.png')
        self.imagen = pygame.transform.scale(img, (30, 30))
        self.rect = self.imagen.get_rect()
        self.rect.x = posicion[0] 
        self.rect.y = posicion[1] +2
        self.width = 30
        self.height = 30
        self.velocidad_x = 2
        self.direccion = random.choice([1, -1])
        self.vel_y = 0
        self.next_position_x = velocidad
        self.next_position_y = 0
        self.vida = 2
        self.visible = True
        self.tiempo_visible = 0 
        
        self.sprites_corriendo = [
            pygame.transform.scale(pygame.image.load('img/enemigo/0.png'), (24, 40)),
            pygame.transform.scale(pygame.image.load('img/enemigo/1.png'), (24, 40)),
            pygame.transform.scale(pygame.image.load('img/enemigo/2.png'), (24, 40)),
            pygame.transform.scale(pygame.image.load('img/enemigo/3.png'), (24, 40)),
            pygame.transform.scale(pygame.image.load('img/enemigo/4.png'), (24, 40)),
            pygame.transform.scale(pygame.image.load('img/enemigo/5.png'), (24, 40)),
            pygame.transform.scale(pygame.image.load('img/enemigo/6.png'), (24, 40)),
            pygame.transform.scale(pygame.image.load('img/enemigo/7.png'), (24, 40)),
        ]
        self.corriendo_index = 0




            
            
    def aplicar_gravedad(self):
        gravedad = 0.2
        self.aceleracion_y = gravedad
        self.vel_y += self.aceleracion_y
        if self.vel_y > 0.4:
            self.vel_y = 0.4
        self.next_position_y += self.vel_y 

    def verificar_colision(self, lista_plataformas):
        for plataforma in lista_plataformas:
            if plataforma.rect.colliderect(self.rect.x + self.next_position_x, self.rect.y, self.width  , self.height ):
                self.direccion *= -1
                
            if plataforma.rect.colliderect(self.rect.x, self.rect.y + self.next_position_y+1, self.width  , self.height):
                if self.vel_y < 0:
                    self.next_position_y = plataforma.rect.bottom - self.rect.top 
                    self.vel_y = 0
                    
                elif self.vel_y >= 0:
                    self.next_position_y = plataforma.rect.top - self.rect.bottom
                    self.vel_y = 0
        if self.rect.x < 20:
            self.direccion = 1

    def desaparecer(self, lista, pantalla, lista_mobs):
        for proyectil in lista:
            if proyectil.colision(self):
                self.vida -= 1
                lista.remove(proyectil)
                
            if self.vida == 0:
                self.animar_muerte(pantalla)
                if self in lista_mobs:
                    lista_mobs.remove(self)
                
                self.visible = False

    def actualizar(self, pantalla, lista_plataformas, lista_proyectiles, lista_mobs):
        if self.visible:
            self.aplicar_gravedad()
            self.verificar_colision(lista_plataformas)
            self.desaparecer(lista_proyectiles, pantalla, lista_mobs)
            self.rect.x += self.next_position_x * self.direccion
            self.rect.y += self.next_position_y
            pantalla.blit(self.imagen, self.rect)
            self.tiempo_visible += 1
        
            if self.tiempo_visible > 12 * 60:  
                self.visible = False
                if self in lista_mobs:
                    lista_mobs.remove(self)
            
    
            self.corriendo_index += 1
            if self.corriendo_index >= len(self.sprites_corriendo):
                self.corriendo_index = 0
            if self.direccion == 1:
                self.imagen = self.sprites_corriendo[self.corriendo_index]
            elif self.direccion == -1:
                self.imagen = pygame.transform.flip(self.sprites_corriendo[self.corriendo_index], True, False)
            
    
    def animar_muerte(self, pantalla):
            cont = 0
            explosiones = [
                pygame.image.load("img/brillos/0.png").convert(),
                pygame.image.load("img/brillos/1.png").convert(),
                pygame.image.load("img/brillos/2.png").convert(),
                pygame.image.load("img/brillos/3.png").convert(),
                pygame.image.load("img/brillos/4.png").convert(),
                pygame.image.load("img/brillos/5.png").convert()

            ]
            
            for frame in explosiones:
                frame = pygame.transform.scale(frame, (80, 100))
                frame.set_colorkey((0, 0, 0))
                self.imagen = explosiones[cont]
                cont += 1
                pygame.display.flip()
                