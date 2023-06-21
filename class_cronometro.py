import pygame
import sys

class Cronometro:
    def __init__(self, tiempo_inicial):
        self.tiempo = tiempo_inicial
        self.cooldown = pygame.time.get_ticks()  # Variable para controlar el tiempo de espera entre actualizaciones
        self.cooldown_intervalo = 1000  # Intervalo de tiempo en milisegundos entre actualizaciones

        self.fuente = pygame.font.Font(None, 36)
        self.color_texto = (255, 255, 255)
        self.posicion_texto = (400, 10)

    def actualizar(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.cooldown >= self.cooldown_intervalo:
            self.tiempo -= 1
            if self.tiempo < 0:
                self.tiempo = 0
            self.cooldown = tiempo_actual

    def dibujar(self, screen):
        texto = self.fuente.render(str(self.tiempo), True, self.color_texto)
        screen.blit(texto, self.posicion_texto)