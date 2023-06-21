import pygame
from biblioteca_niveles import *

ANCHO = 800
ALTO = 600

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

pygame.init()
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Menú")

reloj = pygame.time.Clock()

def dibujar_texto(texto, fuente, color, x, y):
    superficie = fuente.render(texto, True, color)
    ventana.blit(superficie, (x, y))

def dibujar_botones(opciones):
    for i, opcion in enumerate(opciones):
        pygame.draw.rect(ventana, BLANCO, (300, 150 + i * 100, 200, 50))
        dibujar_texto(opcion, fuente, NEGRO, 340, 160 + i * 100)

fuente = pygame.font.Font(None, 36)

opcion_menu = None
nivel = None
regresar_primer_menu = False

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            
            if 300 <= x <= 500:
                if 150 <= y <= 200:
                    print("Jugar")
                    opcion_menu = 1
                elif 250 <= y <= 300:
                    print("Opciones")
                elif 350 <= y <= 400:
                    print("Ver Rankings")
                elif 450 <= y <= 500:
                    pygame.quit()
                    quit()

    ventana.fill(NEGRO)
    dibujar_botones(["Jugar", "Opciones", "Ver Rankings", "Salir"])

    pygame.display.update()
    reloj.tick(60)

    if opcion_menu == 1:
        regresar_primer_menu = False
        nivel = None
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    
                    if 300 <= x <= 500:
                        if 150 <= y <= 200:
                            print("Nivel 1")
                            nivel = 1
                        elif 250 <= y <= 300:
                            print("Nivel 2")
                            nivel = 2
                        elif 350 <= y <= 400:
                            print("Nivel 3")
                            nivel = 3
                        elif 450 <= y <= 500:
                            regresar_primer_menu = True 
                            break

            ventana.fill(NEGRO)
            dibujar_botones(["Nivel 1", "Nivel 2", "Nivel 3", "Volver"])

            pygame.display.update()
            reloj.tick(60)

            if nivel is not None or regresar_primer_menu:
                break

        if regresar_primer_menu:
            opcion_menu = None  
        else:
            if nivel == 1:
                nivel = primer_nivel(nivel)
            elif nivel == 2:
                nivel = segundo_nivel(nivel)
            elif nivel == 3:
                nivel = juego_naves(nivel)

            if nivel is not None:
                opcion_menu = 1
            else:
                break
