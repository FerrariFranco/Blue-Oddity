import pygame
import pygame.mixer
pygame.mixer.init()
pygame.init()
class Personaje():
    def __init__(self, x, y):
        self.contador_pasos = 0
        self.esta_corriendo = False
        self.esta_saltando = False
        self.esta_idle = True

        img = pygame.image.load('img/tiles/roca.png')
        self.imagen = pygame.transform.scale(img, (24, 40))  
        self.rect = self.imagen.get_rect()
        self.rect.x = x - 5
        self.rect.y = y - 5
        self.rect.width -= 20 
        self.rect.height -= 10  
        self.width = 24  
        self.height = 40  
        self.vel_y = 0
        self.vel_x = 0
        self.next_position_y = 0
        self.next_position_x = 0
        self.saltando = False
        self.on_ground = False
        self.salto_presionado = False

        self.direccion_actual = "derecha"
        self.angulo = 0
        self.gravity = True
        self.vida = 20  
        self.contador_pj = 0
        self.barra_vida = pygame.Rect(20, 20, self.vida * 10, 10) 
        
        self.puntos = 0

        self.sprites_idle = [
            pygame.transform.scale(pygame.image.load('img/idle/0.png'), (24, 40)),
            pygame.transform.scale(pygame.image.load('img/idle/1.png'), (24, 40)),
            pygame.transform.scale(pygame.image.load('img/idle/2.png'), (24, 40)),
            pygame.transform.scale(pygame.image.load('img/idle/3.png'), (24, 40)),
            pygame.transform.scale(pygame.image.load('img/idle/4.png'), (24, 40)),
            pygame.transform.scale(pygame.image.load('img/idle/5.png'), (24, 40)),
            pygame.transform.scale(pygame.image.load('img/idle/6.png'), (24, 40))
        ]
        self.idle_index = 0

        self.sprites_corriendo = [
            pygame.transform.scale(pygame.image.load('img/run/0.png'), (24, 40)),
            pygame.transform.scale(pygame.image.load('img/run/1.png'), (24, 40)),
            pygame.transform.scale(pygame.image.load('img/run/2.png'), (24, 40)),
            pygame.transform.scale(pygame.image.load('img/run/3.png'), (24, 40)),
            pygame.transform.scale(pygame.image.load('img/run/4.png'), (24, 40)),
            pygame.transform.scale(pygame.image.load('img/run/5.png'), (24, 40)),
            pygame.transform.scale(pygame.image.load('img/run/6.png'), (24, 40))
        ]
        self.corriendo_index = 0

        self.sprites_saltando = [
            pygame.transform.scale(pygame.image.load('img/jump/0.png'), (24, 40)),
            pygame.transform.scale(pygame.image.load('img/jump/1.png'), (24, 40)),
            pygame.transform.scale(pygame.image.load('img/jump/2.png'), (24, 40)),
            pygame.transform.scale(pygame.image.load('img/jump/3.png'), (24, 40)),
            pygame.transform.scale(pygame.image.load('img/jump/4.png'), (24, 40)),
        ]
        self.saltando_index = 0
        
        
        self.sonido_daño = pygame.mixer.Sound('sfx/hitHurt.wav')
        self.sonido_salto = pygame.mixer.Sound('sfx/jump.wav')


    def manejar_entrada(self):
        
        
                    
                    
        teclas = pygame.key.get_pressed()
        self.esta_corriendo = False
        self.esta_idle = True



        

        if teclas[pygame.K_UP] and not self.salto_presionado:
            self.saltar()

        if not teclas[pygame.K_UP]:
            self.salto_presionado = False

        if teclas[pygame.K_LEFT]:
            self.mover_izquierda()
            self.esta_corriendo = True
            self.esta_idle = False
        elif teclas[pygame.K_RIGHT]:
            self.mover_derecha()
            self.esta_corriendo = True
            self.esta_idle = False

    def saltar(self):
        if not self.saltando and not self.esta_saltando and self.vel_y == 0:
            if self.on_ground or self.salto_presionado:
                self.sonido_salto.play()
                self.vel_y = -11
                self.saltando = True
                self.esta_saltando = True
                self.salto_presionado = True

                self.next_position_y -= 5
        
            
    def mover_izquierda(self):
        self.next_position_x = -6
        self.contador_pasos += 1
        self.direccion_actual = "izquierda"
        self.angulo = 180

    def mover_derecha(self):
        self.next_position_x = 6
        self.contador_pasos += 1
        self.direccion_actual = "derecha"
        self.angulo = 0

    def aplicar_gravedad(self):
        if self.gravity:
            gravedad = 0.5 
            self.aceleracion_y = gravedad
            self.vel_y += self.aceleracion_y
            if self.vel_y > 10:
                self.vel_y = 11
            self.next_position_y += self.vel_y

    def verificar_colision(self, lista_plataformas):
        for plataforma in lista_plataformas:
            if plataforma.rect.colliderect(self.rect.x + self.next_position_x, self.rect.y, self.width-10, self.height-10 ):
                self.next_position_x = 0
            if plataforma.rect.colliderect(self.rect.x, self.rect.y + self.next_position_y, self.width-10, self.height-10):
                if self.vel_y < 0:
                    self.next_position_y = plataforma.rect.bottom - self.rect.top
                    self.vel_y = 0
                
                elif self.vel_y >= 0:
                    self.next_position_y = plataforma.rect.top - self.rect.bottom
                    self.vel_y = 0
                    self.saltando  = False
                    self.esta_saltando = False
                    self.on_ground = True
                    
    def actualizar_barra_vida(self):
        ancho_barra = int(self.vida * 10) 
        self.barra_vida.width = ancho_barra
        
    
    def dañarse(self, lista, pantalla):
        for cosa in lista:
            if cosa.rect.colliderect(self.rect):
                self.vida -=  5
                self.sonido_daño.play()
                self.actualizar_barra_vida()   
                #print(f"Te queda {self.vida * 10} de vida!")
                if self.vida < 0:
                    return True  
                cosa.muriendo = True
                

    def disaparado(self, lista):
        for cosa in lista:
            if cosa.rect.colliderect(self.rect):
                #self.contador_pj += 1
                self.vida -=  3
                self.sonido_daño.play()
                self.actualizar_barra_vida()   
                #print(f"Te queda {self.vida * 10} de vida!")
                if self.vida < 0:
                    return True  
                lista.remove(cosa)
                
    def trampa(self, trampas):
        for trampa in trampas:
            if trampa.rect.colliderect(self.rect):
                #self.contador_pj += 0.001
                self.vida -= 0.1 
                self.actualizar_barra_vida()
                if self.vida < 0:
                    return True  
                
                
    def mostrar_puntos(self, pantalla):
        fuente = pygame.font.SysFont(None, 24) 
        texto = fuente.render(f"Puntos: {self.puntos}", True, (64, 242, 255))
        pantalla.blit(texto, (10, pantalla.get_height() - 30)) 


    def actualizar(self, pantalla, lista):
        self.next_position_x = 0  
        self.next_position_y = 0
        self.manejar_entrada()
        self.aplicar_gravedad()
        self.verificar_colision(lista)
        self.rect.x += self.next_position_x
        self.rect.y += self.next_position_y
        

        if self.esta_corriendo:
            self.corriendo_index += 1
            if self.corriendo_index >= len(self.sprites_corriendo):
                self.corriendo_index = 0
            if self.direccion_actual == "derecha":
                self.imagen = self.sprites_corriendo[self.corriendo_index]
            elif self.direccion_actual == "izquierda":
                self.imagen = pygame.transform.flip(self.sprites_corriendo[self.corriendo_index], True, False)
            
            
        elif self.esta_saltando:
            self.saltando_index += 1
            if self.saltando_index >= len(self.sprites_saltando):
                self.saltando_index = 0
            self.imagen = self.sprites_saltando[self.saltando_index]
            
            
        elif self.esta_idle:
            if self.direccion_actual == "derecha":
                self.imagen = self.sprites_idle[self.idle_index]
            elif self.direccion_actual == "izquierda":
                self.imagen = pygame.transform.flip(self.sprites_idle[self.idle_index], True, False)
        
        #print(self.vel_y)
        
        self.mostrar_puntos(pantalla)
        pygame.draw.rect(pantalla, (0, 255, 0), self.barra_vida) 
        pantalla.blit(self.imagen, self.rect)