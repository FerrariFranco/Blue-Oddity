import pygame
from class_jugador import *
from class_plataforma import *
from class_proyectil import *
import sys
import pygame.mixer
pygame.init()
pygame.mixer.init()



def cargar_imagen(ruta, tamaño):
    imagen = pygame.image.load(ruta)
    imagen = pygame.transform.scale(imagen, tamaño)
    return imagen

def dibujar_plataformas(plataformas, screen):
    for plataforma in plataformas:
        plataforma.dibujar(screen)

def actualizar_personaje(personaje, screen, plataformas):
    personaje.actualizar(screen, plataformas)

def crear_proyectil(personaje, disparos, proyectiles_group, cooldown, cadencia, contador):
    sonido_proyectil = pygame.mixer.Sound("sfx/laserShoot.wav")
    tiempo_actual = pygame.time.get_ticks()
    if tiempo_actual - cooldown >= cadencia:
        sonido_proyectil.play()
        balas = Proyectil((15, 15), (personaje.rect.x, personaje.rect.y), "img/267.png", 50, 8, personaje.angulo)
        disparos.append(balas)
        proyectiles_group.add(balas)
        cooldown = tiempo_actual
        contador += 1
    return cooldown, contador

def actualizar_proyectiles(disparos, screen):
    Proyectil.actualizar_proyectiles(disparos, screen)
    
    
    


def mostrar_mensaje(texto, pantalla):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    font = pygame.font.Font(None, 36)
    text = font.render(texto, True, WHITE)
    text_rect = text.get_rect(center=(pantalla.get_width()/2, pantalla.get_height()/2))
    pantalla.blit(text, text_rect)
    pygame.display.flip()
    
    
    
def menu_intermedio(screen):
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    next_button = pygame.Rect(200, 300, 250, 50)
    rankings_button = pygame.Rect(200, 380, 250, 50)
    fondo = pygame.image.load("img/fondo_mapa.jpg")
    fondo = pygame.transform.scale(fondo, (800, 600))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if next_button.collidepoint(event.pos):
                        return True
                    elif rankings_button.collidepoint(event.pos):
                        return False
        
        screen.blit(fondo, (0, 0))
        pygame.draw.rect(screen, (120, 120, 120), next_button)
        pygame.draw.rect(screen, (120, 120, 120), rankings_button)

        next_text = font.render("MENÚ DE NIVELES", True, (255, 255, 255))
        rankings_text = font.render("Rankings", True, (255, 255, 255))

        screen.blit(next_text, (next_button.x + 10, next_button.y + 10))
        screen.blit(rankings_text, (rankings_button.x + 10, rankings_button.y + 10))

        felicidades_text = font.render("¡Felicidades! Completaste el nivel", True, (255, 255, 255))
        felicidades_rect = felicidades_text.get_rect(center=(screen.get_width() // 2, 50))
        screen.blit(felicidades_text, felicidades_rect)

        pygame.display.flip()
        clock.tick(60)