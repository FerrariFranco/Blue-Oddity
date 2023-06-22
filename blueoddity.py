
from biblioteca_niveles import *

import pygame
import sqlite3

fuente = pygame.font.Font(None, 36)

ANCHO = 800
ALTO = 600

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

pygame.init()
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Menú")

reloj = pygame.time.Clock()

fuente = pygame.font.Font(None, 36)

def dibujar_texto(texto, fuente, color, x, y):
    superficie = fuente.render(texto, True, color)
    ventana.blit(superficie, (x, y))

def dibujar_botones(opciones):
    for i, opcion in enumerate(opciones):
        pygame.draw.rect(ventana, BLANCO, (300, 150 + i * 100, 200, 50))
        dibujar_texto(opcion, fuente, NEGRO, 340, 160 + i * 100)

def mostrar_rankings():
    conn1 = sqlite3.connect("nivel1_ranking.db")
    conn2 = sqlite3.connect("nivel2_ranking.db")

    cursor1 = conn1.cursor()
    cursor2 = conn2.cursor()
    
    cursor1.execute("CREATE TABLE IF NOT EXISTS Puntos_1 (fecha TEXT, puntaje INTEGER)")
    cursor2.execute("CREATE TABLE IF NOT EXISTS Puntos_2 (fecha TEXT, puntaje INTEGER)")
    cursor1.execute("SELECT fecha, puntaje FROM Puntos_1 ORDER BY puntaje DESC LIMIT 3")
    cursor2.execute("SELECT fecha, puntaje FROM Puntos_2 ORDER BY puntaje DESC LIMIT 3")

    resultados1 = cursor1.fetchall()
    resultados2 = cursor2.fetchall()

    conn1.close()
    conn2.close()

    ventana.fill(NEGRO)

    dibujar_texto("Rankings - Nivel 1", fuente, BLANCO, 300, 100)
    dibujar_texto("Rankings - Nivel 2", fuente, BLANCO, 300, 350)

    for i, resultado in enumerate(resultados1):
        fecha, puntaje = resultado
        texto = f"{i+1}. Fecha: {fecha} - Puntaje: {puntaje}"
        dibujar_texto(texto, fuente, BLANCO, 250, 150 + i * 30)  # Reducir tamaño de fuente

    for i, resultado in enumerate(resultados2):
        fecha, puntaje = resultado
        texto = f"{i+1}. Fecha: {fecha} - Puntaje: {puntaje}"
        dibujar_texto(texto, fuente, BLANCO, 250, 400 + i * 30)  # Reducir tamaño de fuente

    pygame.display.update()

opcion_menu = None
nivel = None
regresar_primer_menu = False
en_menu_rankings = False

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
                    opcion_menu = 3
                elif 350 <= y <= 400:
                    print("Rankings")
                    opcion_menu = 4
                elif 450 <= y <= 500:
                    pygame.quit()
                    quit()

    ventana.fill(NEGRO)
    dibujar_botones(["Jugar", "Opciones", "Rankings", "Salir"])

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
                o = primer_nivel(nivel)
            elif nivel == 2:
                o = segundo_nivel(nivel)
            elif nivel == 3:
                juego_naves(nivel)
            if o == 1:
                opcion_menu = 1
            elif o == 3:
                opcion_menu = 4
            else:
                break

    if opcion_menu == 4:
        en_menu_rankings = True
        opcion_menu = None

    while en_menu_rankings:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 50 <= x <= 200 and 50 <= y <= 100: 
                    en_menu_rankings = False

        mostrar_rankings()

        pygame.draw.rect(ventana, BLANCO, (50, 50, 150, 50))  
        dibujar_texto("Volver", fuente, NEGRO, 85, 60)  

        pygame.display.update()
        reloj.tick(60)