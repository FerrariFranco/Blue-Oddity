import pygame
import pygame.mixer
import random
from class_proyectil import *
pygame.mixer.init()
pygame.init()

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, posicion, velocidad, tipo):
        super().__init__()
        self.contador_pasos = 0
        img = pygame.image.load('img/tiles/roca.png')
        self.imagen = pygame.transform.scale(img, (30, 30))
        self.rect = self.imagen.get_rect()
        self.rect.x = posicion[0] 
        self.rect.y = posicion[1] +2
        self.width = 30
        self.height = 30
        self.velocidad_x = velocidad
        self.direccion = random.choice([1, -1])
        self.vel_y = 0
        self.next_position_x = velocidad
        self.next_position_y = 0
        self.vida = 2
        self.visible = True
        self.tiempo_visible = 0 
        self.muriendo = False
        self.frame_actual = 0  # Índice del frame actual de la animación de muerte
        self.frame_duration = 100  # Duración en milisegundos de cada frame de la animación
        self.tiempo_frame = 0
        self.tipo = tipo
        self.tiempo_disparo = 0
        self.lista_proyectiles = []
        self.animacion_muerte = [
                        pygame.image.load("img/brillos/0.png").convert(),
                        pygame.image.load("img/brillos/1.png").convert(),
                        pygame.image.load("img/brillos/2.png").convert(),
                        pygame.image.load("img/brillos/3.png").convert(),
                        pygame.image.load("img/brillos/4.png").convert(),
                        pygame.image.load("img/brillos/5.png").convert(),
                        pygame.image.load("img/brillos/6.png").convert(),
                        pygame.image.load("img/brillos/7.png").convert(),
                        pygame.image.load("img/brillos/8.png").convert(),
                        pygame.image.load("img/brillos/9.png").convert(),
                        pygame.image.load("img/brillos/10.png").convert()
                    ]
        
        for image in self.animacion_muerte:
            image.set_colorkey((0, 0, 0)) 
        if tipo == 1:
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
        elif tipo == 2:
            self.sprites_corriendo = [
                pygame.transform.scale(pygame.image.load('img/enemigo/00.png'), (24, 40)),
                pygame.transform.scale(pygame.image.load('img/enemigo/11.png'), (24, 40)),
                pygame.transform.scale(pygame.image.load('img/enemigo/22.png'), (24, 40)),
                pygame.transform.scale(pygame.image.load('img/enemigo/33.png'), (24, 40)),
                pygame.transform.scale(pygame.image.load('img/enemigo/44.png'), (24, 40)),
                pygame.transform.scale(pygame.image.load('img/enemigo/55.png'), (24, 40)),
                pygame.transform.scale(pygame.image.load('img/enemigo/66.png'), (24, 40)),
                pygame.transform.scale(pygame.image.load('img/enemigo/77.png'), (24, 40)),
            ]
            self.corriendo_index = 0
            
        self.sonido_muerte = pygame.mixer.Sound('sfx/explosion.wav')
        self.sonido_disparo = pygame.mixer.Sound('sfx/enemyshoot.wav')
        self.sonido_muerte_bandera = True




            
            
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
                self.muriendo = True

    def actualizar(self, pantalla, lista_plataformas, lista_proyectiles, lista_mobs):
        if self.visible:
            if self.muriendo:
                if self.sonido_muerte_bandera:
                    self.sonido_muerte.play()
                    self.sonido_muerte_bandera = False

                self.actualizar_animacion_muerte(pantalla, lista_mobs)
            else:
                if self.tipo == 2:
                    if self.direccion == -1:
                        ang = 0
                    else:
                        ang = 180
                    tiempo_actual = pygame.time.get_ticks()
                    if tiempo_actual - self.tiempo_disparo >= 2000:  # 2000 ms = 2 segundos
                        # Crear un nuevo proyectil
                        proyectil = Proyectil((15, 15), (self.rect.x + 3, self.rect.y), "img/41.png", 90, -6, ang)
                        self.sonido_disparo.play()
                        self.lista_proyectiles.append(proyectil)
                        self.tiempo_disparo = tiempo_actual
                self.aplicar_gravedad()
                self.verificar_colision(lista_plataformas)
                self.desaparecer(lista_proyectiles, pantalla, lista_mobs)
                self.rect.x += self.next_position_x * self.direccion
                self.rect.y += self.next_position_y
                pantalla.blit(self.imagen, self.rect)
                self.tiempo_visible += 1

                if self.tiempo_visible > 12 * 60:  
                    self.muriendo = True
                
                self.corriendo_index += 1
                if self.corriendo_index >= len(self.sprites_corriendo):
                    self.corriendo_index = 0
                if self.direccion == 1:
                    self.imagen = self.sprites_corriendo[self.corriendo_index]
                elif self.direccion == -1:
                    self.imagen = pygame.transform.flip(self.sprites_corriendo[self.corriendo_index], True, False)
    
    def actualizar_animacion_muerte(self, pantalla, lista_mobs):
        if self.frame_actual < len(self.animacion_muerte):
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_frame >= self.frame_duration:
                self.imagen = self.animacion_muerte[self.frame_actual]
                # Establecer las dimensiones del rectángulo en 0 para que no se dibuje
                self.rect.width = 0
                self.rect.height = 0
                pantalla.blit(self.imagen, self.rect)
                self.frame_actual += 1
                self.tiempo_frame = tiempo_actual
        else:
            
            self.visible = False
            if self in lista_mobs:
                
                lista_mobs.remove(self)
                
    
