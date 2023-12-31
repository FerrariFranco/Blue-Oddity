
from biblioteca_niveles import *

import pygame
import sqlite3

fuente = pygame.font.Font(None, 36)
ruta_fuente = "font/Entanglement-rgpRB.ttf"
fuente_personalizada = pygame.font.Font(ruta_fuente, 70)
ANCHO = 800
ALTO = 600

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)

pygame.init()
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Menú")

reloj = pygame.time.Clock()

fuente = pygame.font.Font(None, 36)
fondo_menu = pygame.image.load("img/fondomenu.jpg")
fondo_menu = pygame.transform.scale(fondo_menu, (ANCHO, ALTO))

def dibujar_texto(texto, fuente, color, x, y):
    superficie = fuente.render(texto, True, color)
    ventana.blit(superficie, (x, y))

def dibujar_botones(opciones):
    for i, opcion in enumerate(opciones):
        pygame.draw.rect(ventana, BLANCO, (300, 170 + i * 100, 200, 50), 1)  
        dibujar_texto(opcion, fuente, BLANCO, 340, 180 + i * 100)

def botones_selector_niveles(opciones):
    try:
        with open("nivel.json", "r") as archivo:
            data = json.load(archivo)
            nivel_actual = data.get("nivel", 0) 
    except FileNotFoundError:
        nivel_actual = 1
    
    if nivel_actual >= 3:
        for i, opcion in enumerate(opciones):
            pygame.draw.rect(ventana, BLANCO, (300, 170 + i * 100, 200, 50), 1)  
            dibujar_texto(opcion, fuente, BLANCO, 340, 180 + i * 100)
    elif nivel_actual == 2:
            pygame.draw.rect(ventana, BLANCO, (300, 170, 200, 50), 1)  
            dibujar_texto("Nivel 1", fuente, BLANCO, 340, 180)
            pygame.draw.rect(ventana, BLANCO, (300, 270 , 200, 50), 1)  
            dibujar_texto("Nivel 2", fuente, BLANCO, 340, 280)
            pygame.draw.rect(ventana, BLANCO, (300, 470, 200, 50), 1)  
            dibujar_texto("Volver", fuente, BLANCO, 340, 480)
    else:
        pygame.draw.rect(ventana, BLANCO, (300, 170, 200, 50), 1)  
        dibujar_texto("Nivel 1", fuente, BLANCO, 340, 180)
        pygame.draw.rect(ventana, BLANCO, (300, 470, 200, 50), 1)  
        dibujar_texto("Volver", fuente, BLANCO, 340, 480)



def mostrar_rankings():
    conn1 = sqlite3.connect("nivel1_ranking.db")
    conn2 = sqlite3.connect("nivel2_ranking.db")

    cursor1 = conn1.cursor()
    cursor2 = conn2.cursor()
    
    cursor1.execute("CREATE TABLE IF NOT EXISTS Puntos_1 (nombre TEXT, puntaje INTEGER)")
    cursor2.execute("CREATE TABLE IF NOT EXISTS Puntos_2 (nombre TEXT, puntaje INTEGER)")
    cursor1.execute("SELECT nombre, puntaje FROM Puntos_1 ORDER BY puntaje DESC LIMIT 3")
    cursor2.execute("SELECT nombre, puntaje FROM Puntos_2 ORDER BY puntaje DESC LIMIT 3")

    resultados1 = cursor1.fetchall()
    resultados2 = cursor2.fetchall()

    conn1.close()
    conn2.close()

    ventana.blit(fondo_menu, (0, 0))

    dibujar_texto("Rankings - Nivel 1", fuente, BLANCO, 300, 100)
    dibujar_texto("Rankings - Nivel 2", fuente, BLANCO, 300, 350)

    for i, resultado in enumerate(resultados1):
        nombre, puntaje = resultado
        texto = f"{i+1}. Nombre: {nombre} - Puntaje: {puntaje}"
        dibujar_texto(texto, fuente, BLANCO, 250, 150 + i * 30)  # Reducir tamaño de fuente

    for i, resultado in enumerate(resultados2):
        nombre, puntaje = resultado
        texto = f"{i+1}. Nombre: {nombre} - Puntaje: {puntaje}"
        dibujar_texto(texto, fuente, BLANCO, 250, 400 + i * 30)  # Reducir tamaño de fuente

    pygame.display.update()

def dibujar_menu_opciones(volumen_musica, volumen_efectos):
    ventana.blit(fondo_menu, (0, 0))

    dibujar_texto("Volumen de Música", fuente, BLANCO, 300, 100)
    dibujar_texto("Volumen de Efectos", fuente, BLANCO, 300, 250)

    dibujar_texto("-", fuente, BLANCO, 250, 150)
    dibujar_texto("+", fuente, BLANCO, 550, 150)

    dibujar_texto("-", fuente, BLANCO, 250, 300)
    dibujar_texto("+", fuente, BLANCO, 550, 300)

    dibujar_texto(f"{int(volumen_musica*100)}", fuente, BLANCO, 390, 150)
    dibujar_texto(f"{int(volumen_efectos*100)}", fuente, BLANCO, 380, 300)

    pygame.draw.rect(ventana, BLANCO, (100, 50, 150, 50), 1)  

    dibujar_texto("Volver", fuente, BLANCO, 125, 60) 
    
def ejecutar_menu():
    pygame.mixer.music.load('sfx/noMEdejansalir.mp3')
    pygame.mixer.music.play(-1)

    volumen_musica = 0.5  
    volumen_efectos = 0.5 

    opcion_menu = None
    nivel = None
    regresar_primer_menu = False
    en_menu_rankings = False
    dificultad = "Facil"
    skin = "Azul"

    while True:
        try:
            with open("nivel.json", "r") as archivo:
                data = json.load(archivo)
                nivel_actual = data.get("nivel", 0) 
        except FileNotFoundError:
            nivel_actual = 1
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
                        opcion_menu = 2
                    elif 350 <= y <= 400:
                        print("Rankings")
                        opcion_menu = 4
                    elif 450 <= y <= 500:
                        pygame.quit()
                        quit()
        

        ventana.blit(fondo_menu, (0, 0))
        dibujar_botones(["Jugar", "Opciones", "Rankings", "Salir"])
        dibujar_texto("Blue Oddity", fuente_personalizada, AZUL, 160, 50)

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
                                visual = mostrar_visuales(ventana, "img/historia/tierra.jpg")
                                if visual:
                                    nivel = 1
                            elif 250 <= y <= 300 and nivel_actual >= 2:
                                visual = mostrar_visuales(ventana, "img/historia/transition.jpg")
                                if visual:
                                    nivel = 2
                            elif 350 <= y <= 400 and nivel_actual >= 3:
                                visual = mostrar_visuales(ventana, "img/historia/cosmo.jpg")
                                if visual:
                                    nivel = 3
                            elif 450 <= y <= 500:
                                regresar_primer_menu = True 
                                break

                ventana.blit(fondo_menu, (0, 0))
                botones_selector_niveles(["Nivel 1", "Nivel 2", "Nivel 3", "Volver"])

                pygame.display.update()
                reloj.tick(60)

                if nivel is not None or regresar_primer_menu:
                    break

            if regresar_primer_menu:
                opcion_menu = None  
            else:
                if nivel == 1:
                    o = primer_nivel(nivel, volumen_musica, volumen_efectos, dificultad)
                elif nivel == 2:
                    o = segundo_nivel(nivel, volumen_musica, volumen_efectos, dificultad)
                elif nivel == 3:
                    o = juego_naves(nivel, volumen_musica, volumen_efectos, dificultad, skin)
                if o == 1:
                    opcion_menu = 1
                    pygame.mixer.music.load("sfx/noMEdejansalir.mp3")
                    pygame.mixer.music.set_volume(volumen_musica)
                    pygame.mixer.music.play(-1)
                elif o == 3:
                    opcion_menu = 4
                    pygame.mixer.music.load("sfx/noMEdejansalir.mp3")
                    pygame.mixer.music.set_volume(volumen_musica)
                    pygame.mixer.music.play(-1)
                    

                else:
                    break
        elif opcion_menu == 2:  

            while opcion_menu == 2:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    elif evento.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()

                        if 250 <= x <= 300 and 150 <= y <= 200:
                            volumen_musica -= 0.1
                            if volumen_musica < 0.0:
                                volumen_musica = 0.0
                            pygame.mixer.music.set_volume(volumen_musica)

                        elif 550 <= x <= 600 and 150 <= y <= 200:
                            volumen_musica += 0.1
                            if volumen_musica > 1.0:
                                volumen_musica = 1.0
                            pygame.mixer.music.set_volume(volumen_musica)

                        elif 250 <= x <= 300 and 300 <= y <= 350:
                            volumen_efectos -= 0.1
                            if volumen_efectos < 0.0:
                                volumen_efectos = 0.0
                            

                        elif 550 <= x <= 600 and 300 <= y <= 350:
                            volumen_efectos += 0.1
                            if volumen_efectos > 1.0:
                                volumen_efectos = 1.0
                            
                        elif 100 <= x <= 250 and 50 <= y <= 100:
                            opcion_menu = None
                        elif 600 <= x <= 700 and 50 <= y <= 100:
                            if dificultad == "Facil":
                                dificultad = "Difícil"
                            else:
                                dificultad = "Facil"
                                
                        elif (600 <= x <= 700 and 500 <= y <= 550) and nivel_actual == 4:
                            if skin == "Azul":
                                skin = "Rojo"
                            elif skin == "Rojo":
                                skin = "Verde"
                            elif skin == "Verde":
                                skin = "Gris"
                            elif skin == "Gris":
                                skin = "Azul"

                pygame.display.update()

                dibujar_menu_opciones(volumen_musica, volumen_efectos)
                pygame.draw.rect(ventana, BLANCO, (600, 50, 150, 50), 1)
                dibujar_texto(dificultad, fuente, BLANCO, 615, 60)
                if nivel_actual == 4:
                    pygame.draw.rect(ventana, BLANCO, (600, 500, 150, 50), 1)
                    dibujar_texto(skin, fuente, BLANCO, 615, 510)

                pygame.display.update()
                reloj.tick(60)

        elif opcion_menu == 4:
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

            pygame.draw.rect(ventana, BLANCO, (50, 50, 150, 50), 1) 
            dibujar_texto("Volver", fuente, BLANCO, 85, 60)  

            pygame.display.update()
            reloj.tick(60)