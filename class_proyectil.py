import pygame
import math

class Proyectil(pygame.sprite.Sprite):
    def __init__(self, tamaño, posición, imagen, ancho_nave, speed, ángulo):
        super().__init__()  # Call the superclass's __init__ method
        self.imagen = pygame.image.load(imagen)
        self.imagen = pygame.transform.scale(self.imagen, (tamaño[0], tamaño[1]))
        self.rect = self.imagen.get_rect()
        self.rect.x = posición[0] + (ancho_nave // 2) - (tamaño[0] // 2)
        self.rect.y = posición[1]
        self.velocidad = speed
        self.ángulo = math.radians(ángulo)  # Convertir el ángulo a radianes
        self.velocidad_x = self.velocidad * math.cos(self.ángulo)  # Componente horizontal de la velocidad
        self.velocidad_y = -self.velocidad * math.sin(self.ángulo)

    
    def mover(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y
    
    
    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, (self.rect.x, self.rect.y))


    def actualizar_proyectiles(lista, screen):
        
        
        for proyectil in lista.copy():  # Copia la lista para evitar problemas al modificarla durante la iteración
            if proyectil.rect.x > 800 or proyectil.rect.x < 0:
                lista.remove(proyectil)
            elif proyectil.rect.y > 600 or proyectil.rect.y < 0:
                lista.remove(proyectil)
            else:
                proyectil.mover()
                proyectil.dibujar(screen)
            
        
                
    def colision(self, otro_rect):
        return self.rect.colliderect(otro_rect)
    
    """ def morir(self, hitbox, contador_pj, done):
        if self.colision(hitbox):
            contador_pj += 1
            vida = 11 - contador_pj
            print(f"Te queda {vida} de vida!")
            if contador_pj == 200:
                print("PERDISTE")
                done = True """
    
    def circulo(self, proyectil_cont, x_e, y_e, angulo):
        
        for x in range(12):
            disparo = Proyectil((15, 15) , (x_e, y_e + 10), "img/41.png", 90, -3, angulo)
            proyectil_cont.append(disparo)
            angulo += 30
    
    def triple_linea(self, proyectil_cont, x_e, y_e, speed, x, y):
        angulo = self.obtener_angulo(x_e,y_e ,x, y )
        for _ in range(8):
            disparo = Proyectil((15, 15), (x_e, y_e + 10), "img/129.png", 90, speed, -angulo)
            proyectil_cont.append(disparo)
            disparo = Proyectil((15, 15), (x_e, y_e + 10), "img/129.png", 90, speed, -angulo+40)
            proyectil_cont.append(disparo)
            disparo = Proyectil((15, 15), (x_e, y_e + 10), "img/129.png", 90, speed, -angulo-40)
            proyectil_cont.append(disparo)
            speed += 1
    def linea(self, proyectil_cont, x_e, y_e, speed, x, y):
        angulo = self.obtener_angulo(x_e,y_e ,x, y )
        for _ in range(8):
            disparo = Proyectil((15, 15), (x_e, y_e + 10), "img/129.png", 90, speed, -angulo)
            proyectil_cont.append(disparo)
            speed += 1
    def arco(self, proyectil_cont, x_e, y_e, angulo):
        
        for x in range(9):
            disparo = Proyectil((15, 15) , (x_e, y_e + 10), "img/41.png", 90, -3, angulo)
            proyectil_cont.append(disparo)
            angulo += 20

    def espiral(self, proyectil_cont, x_e, y_e, angulo, aumento_angulo, aumento_distancia):
        distancia = 0
        for _ in range(30):
            disparo = Proyectil((15, 15), (x_e + distancia * math.cos(math.radians(angulo)), y_e + distancia * math.sin(math.radians(angulo))), "img/41.png", 90, -3, angulo)
            proyectil_cont.append(disparo)
            angulo += aumento_angulo
            distancia += aumento_distancia
            
    
    def obtener_angulo(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        angulo_rad = math.atan2(dy, dx)
        angulo_deg = math.degrees(angulo_rad)
        return angulo_deg   
    
    def bufeo_pj(self, proyectiles, personaje, angulo, distancia):
        bufeado_uno = Proyectil((15, 15), personaje.posicion, "img/21.png", 50, 15, angulo)
        proyectiles.append(bufeado_uno)
        bufeado_uno = Proyectil((15, 15), personaje.posicion, "img/21.png", 50, 15, angulo - distancia)
        proyectiles.append(bufeado_uno)
        bufeado_uno = Proyectil((15, 15), personaje.posicion, "img/21.png", 50, 15, angulo + distancia)
        proyectiles.append(bufeado_uno)
        