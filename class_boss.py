import pygame


class Boss(pygame.sprite.Sprite):
    def __init__(self, tamaño, x, y):
        self.dimension = pygame.Surface(tamaño)
        self.imagen = pygame.image.load("img/90.png")
        self.imagen = pygame.transform.scale(self.imagen, tamaño)
        self.posicion = pygame.Vector2(x, y)
        self.velocidad_x = 0  # Velocidad en el eje x
        self.velocidad_y = 0  # Velocidad en el eje y
        self.visible = True
        self.contador = 0
        self.vida = 350  # Vida inicial del enemigo
        self.vida_maxima = 350  # Vida máxima del enemigo
        self.sonido_muerte = pygame.mixer.Sound("sfx/explosion.wav")
        self.bandera_sonido = True

    def dibujar(self, pantalla):
        if self.visible:
            pantalla.blit(self.imagen, self.posicion)
            # pygame.draw.rect(pantalla, (255, 0, 0), self.hitbox, 1)
    
    def actualizar(self):
        if self.visible:
            self.posicion.x += self.velocidad_x
            self.posicion.y += self.velocidad_y
    
    
    def animar_muerte(self, pantalla):
        explosiones = [
            pygame.image.load("img/expl/4.png").convert(),
            pygame.image.load("img/expl/3.png").convert(),
            pygame.image.load("img/expl/2.png").convert(),
            pygame.image.load("img/expl/1.png").convert(),
            pygame.image.load("img/expl/0.png").convert(),
            pygame.image.load("img/expl/7.png").convert(),
            pygame.image.load("img/expl/8.png").convert(),
            pygame.image.load("img/expl/9.png").convert(),
            pygame.image.load("img/expl/10.png").convert(),
            pygame.image.load("img/expl/11.png").convert(),
            pygame.image.load("img/expl/13.png").convert(),
            pygame.image.load("img/expl/14.png").convert(),
            pygame.image.load("img/expl/15.png").convert(),
            pygame.image.load("img/expl/16.png").convert(),
            pygame.image.load("img/expl/17.png").convert(),
            pygame.image.load("img/expl/19.png").convert(),
            pygame.image.load("img/expl/20.png").convert()
        ]
        
        for frame in explosiones:
            frame = pygame.transform.scale(frame, (80, 100))
            frame.set_colorkey((0, 0, 0))
            pantalla.blit(frame, self.posicion)
            pygame.display.flip()
            pygame.time.wait(100) 
            
            
    def dar_hitbox(self):
        hitbox_x = self.posicion.x 
        hitbox_y = self.posicion.y
        self.hitbox = pygame.Rect(hitbox_x, hitbox_y, 70, 90)
    
    def desaparecer(self, pantalla):
        self.visible = False
        if self.bandera_sonido:
            self.sonido_muerte.play()
            self.bandera_sonido = False
        self.hitbox = pygame.Rect(0, 0, 0, 0)
        
    def dar_direccion(self, x, y):
        if self.posicion.x < x:
            self.posicion.x += 2
        elif self.posicion.x > x:
            self.posicion.x -= 2

        if self.posicion.y < y:
            self.posicion.y += 2
        elif self.posicion.y > y:
            self.posicion.y -= 2

        if self.posicion.x == x and self.posicion.y == y:
            return True
        
        return False

    def dibujar_barra_vida(self, pantalla):
        ancho_vida = (self.vida / self.vida_maxima) * self.dimension.get_width()

        barra_vida = pygame.Rect(self.posicion.x, self.posicion.y - 10, ancho_vida, 5)
        pygame.draw.rect(pantalla, (255, 0, 0), barra_vida)
        
    def verificar_colision(self, proyectiles, pantalla):
        for proyectil in proyectiles:
            if proyectil.colision(self.hitbox):
                proyectiles.remove(proyectil)
                self.contador += 1
                self.vida -= 1 

        self.dibujar_barra_vida(pantalla)
        
        if self.contador == 100:
            return True
        elif self.contador > 350:
                
                self.desaparecer(pantalla)
                return False
                
        
    
    
    """ def verificar_colision(self, proyectiles):
        
        colision_detectada = False
        for proyectil in proyectiles:
            if proyectil.dimension.x < 0 or proyectil.dimension.x > 601 or proyectil.dimension.y > 801 or proyectil.dimension.y < 0:
                proyectiles.remove(proyectil)
            
            if proyectil.colision(self.rect):
                colision_detectada = True
                proyectiles.remove(proyectil)
                break
        if colision_detectada:
            return True
        else:
            return False
                # 
    def matar(self, muerto):
        if muerto:
            self.kill()
    """
