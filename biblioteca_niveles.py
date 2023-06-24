import pygame
import random
import os
from class_jugador import *
from class_plataforma import *
from class_proyectil import *
from class_nave import *
from class_boss import *
from funciones_primer_nivel import *
from class_cronometro import *
from class_enemigo import *
from class_trampas import *
from class_consumibles import *
import datetime
import sqlite3
import pygame.mixer
import pygame.mixer_music

pygame.init()
pygame.mixer.init()

def primer_nivel(nivel, vm, ve):
    
    width = 800
    height = 600

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Blue Oddity")

    fondo = cargar_imagen("img/fondo_mapa2.jpg", (width, height))
    
    fecha_hora_actual = datetime.datetime.now()
    formato_fecha_hora = fecha_hora_actual.strftime("%Y-%m-%d %H:%M:%S")
    
    cronometro = Cronometro(60)
    
    clock = pygame.time.Clock()
    
    
    
    pygame.mixer.music.load('sfx/nose.wav')
    pygame.mixer.music.play(-1)


    personaje = Personaje(100, 600)
    velocidad_mov = 2

    plat1 = Plataforma((500, 450), (400, 21), 'img/tiles\plat_horizontal.png')
    plat3 = Plataforma((540, 360), (70, 21), 'img/tiles\plat_horizontal.png')
    plat9 = Plataforma((680, 300), (130, 21), 'img/tiles\plat_horizontal.png')
    plat11 = Plataforma((470, 270), (70, 21), 'img/tiles\plat_horizontal.png')
    plat12 = Plataforma((300, 270), (70, 21), 'img/tiles\plat_horizontal.png')
    plat13 = Plataforma((150, 230), (70, 21), 'img/tiles\plat_horizontal.png')
    plat14 = Plataforma((0, 100), (200, 21), 'img/tiles\plat_horizontal.png')
    plat15 = Plataforma((600, 100), (200, 21), 'img/tiles\plat_horizontal.png')
    plat7 = Plataforma((380, 470), (120, 21), 'img/tiles\plat_horizontal.png')
    plat8 = Plataforma((250, 490), (130, 21), 'img/tiles\plat_horizontal.png')
    plat5 = Plataforma((0, 0), (800, 20), 'img/tiles\plat_horizontal.png')
    plat10 = Plataforma((300, 150), (250, 20), 'img/tiles\plat_horizontal.png')

    plat6 = Plataforma((784, 0), (16, 570), 'img/tiles\plat_vertical.png')
    plat4 = Plataforma((0, 0), (16, 570), 'img/tiles\plat_vertical.png')
    plat2 = Plataforma((0, 570), (800, 30), 'img/tiles/roca.png')

    plataformas = [plat1, plat2, plat3, plat4, plat6, plat5, plat7, plat8, plat9, plat10, plat11, plat12, plat13, plat14, plat15]
    
    trap1 = Trampa((400, 440), (25, 25), 'img/trampas/0.png')
    trap2 = Trampa((740, 275), (25, 25), 'img/trampas/0.png')
    trap3 = Trampa((150, 205), (25, 25), 'img/trampas/0.png')
    trap4 = Trampa((300, 125), (25, 25), 'img/trampas/0.png')
    trap5 = Trampa((525, 125), (25, 25), 'img/trampas/0.png')
    trampas = [trap1, trap2, trap3, trap4, trap5]
    
    disparos = []
    lanzando = False
    cadencia = 350  
    cooldown = pygame.time.get_ticks()
    contador_balas = 0

    enemigos = []
    spawn_enemigo = 0
    enemigo_spawns = [(50, 40), (600, 40), (600, 510)]
    
    sonido_gema = pygame.mixer.Sound('sfx/pickupCoin (1).wav')
    sonido_vida = pygame.mixer.Sound('sfx/pickupCoin.wav')
    
    consumibles_spawn = [(660, 40), (680, 250), (180, 180), (80, 420),  (100, 40)]
    consumibles = []
    tiempo_ultimo_consumible = pygame.time.get_ticks()
    intervalo_consumibles = 2500


    proyectiles_group = pygame.sprite.Group()
    
    gameover = False
    pausa = False

    done = True

    pygame.mixer_music.set_volume(vm)


    while done:
        pygame.mixer.music.get_busy()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pausa = not pausa
                    
        
        if pausa:
            mostrar_mensaje("PAUSA", screen)
            while pausa:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        pausa = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pausa = False
                clock.tick(60)
            continue
        if not gameover:
            if pygame.key.get_pressed()[pygame.K_z]:
                lanzando = True
            else:
                lanzando = False

            screen.blit(fondo, (0, 0))
            dibujar_plataformas(plataformas, screen)
            
            
            
            for trampa in trampas:
                trampa.dibujar(screen)
                if trampa.rect.colliderect(personaje.rect):
                    if personaje.trampa(trampas):
                        gameover = True
                
            
            timess = pygame.time.get_ticks()

            if timess - tiempo_ultimo_consumible >= intervalo_consumibles:
                ubicacion_consumible = random.choice(consumibles_spawn)
                consumible_existente = False

                for consumible in consumibles:
                    if consumible.rect.collidepoint(ubicacion_consumible):
                        consumible_existente = True
                        break

                if not consumible_existente:
                    tipo_consumible = random.choice(["vida", "gema"])
                    consumible = Consumibles(ubicacion_consumible, (30, 30), tipo_consumible)
                    consumibles.append(consumible)

                tiempo_ultimo_consumible = timess

            for consumible in consumibles:
                consumible.dibujar(screen)

                # Verificar colisiones con el personaje
                if consumible.rect.colliderect(personaje.rect):
                    if consumible.tipo == "vida":
                        if personaje.vida < 15:
                            sonido_vida.play()
                            personaje.vida += 5
                        personaje.puntos += 40
                        personaje.actualizar_barra_vida()
                    elif consumible.tipo == "gema":
                        sonido_gema.play()
                        personaje.puntos += 100
                    consumibles.remove(consumible)

            if lanzando:
                cooldown, contador_balas = crear_proyectil(personaje, disparos, proyectiles_group, cooldown, cadencia, contador_balas)

            actualizar_proyectiles(disparos, screen)
            actualizar_personaje(personaje, screen, plataformas)

            cronometro.actualizar()
            cronometro.dibujar(screen)

            proyectiles_group.update()

            tiempo = pygame.time.get_ticks()

            if tiempo - spawn_enemigo >= 3000:
                enemigo = Enemigo(random.choice(enemigo_spawns), 4, 1)
                enemigos.append(enemigo)
                spawn_enemigo = tiempo

            for enemigo in enemigos:
                enemigo.actualizar(screen, plataformas, disparos, enemigos)
                if personaje.dañarse(enemigos, screen):
                    gameover = True
                    
                    
            for i in range(pygame.mixer.get_num_channels()):
                canal = pygame.mixer.Channel(i)
                canal.set_volume(ve) 
            pygame.display.flip()

            clock.tick(60)
            
            if cronometro.tiempo == 30:
                with sqlite3.connect("nivel1_ranking.db") as conexión:
                    cursor = conexión.cursor()
                    cursor.execute("CREATE TABLE IF NOT EXISTS Puntos_1 (fecha TEXT, puntaje INTEGER)")
                    sentencia_sql = "INSERT INTO Puntos_1 (fecha, puntaje) VALUES (?, ?)"
                    cursor.execute(sentencia_sql, (formato_fecha_hora, personaje.puntos))
                    conexión.commit()
                if menu_intermedio(screen):
                    opcion_menu = 1

                    return opcion_menu
                if not menu_intermedio(screen):
                    opcion_menu = 3

                    return opcion_menu
                
        if gameover:
                
                mostrar_mensaje("PERDISTE. Presiona R para volver a intentar.", screen)
            
            
                keys = pygame.key.get_pressed()
                if keys[pygame.K_r] and gameover:
                    personaje.gravity = False
                    gameover = False
                    personaje = Personaje(100, 580)


    pygame.quit()
    return nivel

def segundo_nivel(nivel, vm, ve):
    
    width = 800
    height = 600

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Blue Oddity")

    fondo = cargar_imagen("img/fondo_mapa_final.jpg", (width, height))

    cronometro = Cronometro(60)

    pygame.mixer.music.load('sfx/nose.wav')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(vm)
    
    clock = pygame.time.Clock()

    personaje = Personaje(80, 480)
    velocidad_mov = 2


    plat5 = Plataforma((0, 0), (800, 20), 'img/tiles\plat_horizontal.png')


    plat6 = Plataforma((784, 0), (16, 570), 'img/tiles\plat_vertical.png')
    plat4 = Plataforma((0, 0), (16, 570), 'img/tiles\plat_vertical.png')
    plat2 = Plataforma((0, 570), (800, 30), 'img/tiles/roca.png')
    nave_estacionada = Plataforma((700, 40), (100, 50), "img\shipblue\shipblue0006.png")

    plat14 = Plataforma((16, 71), (400, 21), 'img/tiles\plat_horizontal.png')
    plat15 = Plataforma((500, 71), (300, 21), 'img/tiles\plat_horizontal.png')

    plat1 = Plataforma((16, 152), (50, 21), 'img/tiles\plat_horizontal.png')
    plat22 = Plataforma((150, 152), (650, 21), 'img/tiles\plat_horizontal.png')

    plat3 = Plataforma((16, 233), (600, 21), 'img/tiles\plat_horizontal.png')
    plat7 = Plataforma((700, 233), (100, 21), 'img/tiles\plat_horizontal.png')

    plat8 = Plataforma((16, 314), (250, 21), 'img/tiles\plat_horizontal.png')
    plat9 = Plataforma((350, 314), (600, 21), 'img/tiles\plat_horizontal.png')

    plat10 = Plataforma((16, 395), (400, 21), 'img/tiles\plat_horizontal.png')
    plat11 = Plataforma((500, 395), (300, 21), 'img/tiles\plat_horizontal.png')

    plat12 = Plataforma((16, 476), (600, 21), 'img/tiles\plat_horizontal.png')
    plat13 = Plataforma((700, 476), (100, 21), 'img/tiles\plat_horizontal.png')

    enemigos = []
    spawn_enemigo = 0
    enemigo_spawns = [(50, 40), (600, 40), (50, 510), (600, 510), (50, 200), (750, 200)]

    consumibles_spawn = [(660, 520), (680, 260), (180, 190), (80, 430),  (100, 50)]
    consumibles = []
    tiempo_ultimo_consumible = pygame.time.get_ticks()
    intervalo_consumibles = 1500
    sonido_gema = pygame.mixer.Sound('sfx/pickupCoin (1).wav')
    sonido_vida = pygame.mixer.Sound('sfx/pickupCoin.wav')

    fecha_hora_actual = datetime.datetime.now()
    formato_fecha_hora = fecha_hora_actual.strftime("%Y-%m-%d %H:%M:%S")
    
    plataformas = [plat1,plat2,nave_estacionada, plat22 , plat3, plat4, plat6, plat5, plat7, plat8, plat9, plat10, plat11, plat12, plat13, plat14, plat15]

    disparos = []
    lanzando = False
    cadencia = 350  
    cooldown = pygame.time.get_ticks()
    contador_balas = 0
    proyectiles_group = pygame.sprite.Group()

    gameover = False
    pausa = False
    done = True

    
    while done:
        
        pygame.mixer.music.get_busy()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pausa = not pausa
                    
        
        if pausa:
            mostrar_mensaje("PAUSA", screen)
            while pausa:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        pausa = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pausa = False
                clock.tick(60)
            continue
        if not gameover:
            if pygame.key.get_pressed()[pygame.K_z]:
                lanzando = True
            else:
                lanzando = False

            screen.blit(fondo, (0, 0))
            dibujar_plataformas(plataformas, screen)
            
            
                
            
            timess = pygame.time.get_ticks()

            if timess - tiempo_ultimo_consumible >= intervalo_consumibles:
                ubicacion_consumible = random.choice(consumibles_spawn)
                consumible_existente = False

                for consumible in consumibles:
                    if consumible.rect.collidepoint(ubicacion_consumible):
                        consumible_existente = True
                        break

                if not consumible_existente:
                    tipo_consumible = random.choice(["vida", "gema"])
                    consumible = Consumibles(ubicacion_consumible, (30, 30), tipo_consumible)
                    consumibles.append(consumible)

                tiempo_ultimo_consumible = timess

            for consumible in consumibles:
                consumible.dibujar(screen)

                # Verificar colisiones con el personaje
                if consumible.rect.colliderect(personaje.rect):
                    if consumible.tipo == "vida":
                        if personaje.vida < 15:
                            sonido_vida.play()
                            personaje.vida += 5
                        personaje.puntos += 40
                        personaje.actualizar_barra_vida()
                    elif consumible.tipo == "gema":
                        sonido_gema.play()
                        personaje.puntos += 100
                    consumibles.remove(consumible)

            if lanzando:
                cooldown, contador_balas = crear_proyectil(personaje, disparos, proyectiles_group, cooldown, cadencia, contador_balas)

            actualizar_proyectiles(disparos, screen)
            actualizar_personaje(personaje, screen, plataformas)

            cronometro.actualizar()
            cronometro.dibujar(screen)

            proyectiles_group.update()

            tiempo = pygame.time.get_ticks()

            if tiempo - spawn_enemigo >= 3000:
                enemigo = Enemigo(random.choice(enemigo_spawns), 2, 2)
                enemigos.append(enemigo)
                spawn_enemigo = tiempo

            for enemigo in enemigos:
                enemigo.actualizar(screen, plataformas, disparos, enemigos)
                Proyectil.actualizar_proyectiles(enemigo.lista_proyectiles, screen)
                if personaje.disaparado(enemigo.lista_proyectiles):
                    gameover = True

            for i in range(pygame.mixer.get_num_channels()):
                canal = pygame.mixer.Channel(i)
                canal.set_volume(ve) 
            
            pygame.display.flip()

            clock.tick(60)

            
            
            if cronometro.tiempo == 55:
                personaje.gravity = False
                with sqlite3.connect("nivel2_ranking.db") as conexión:
                    cursor = conexión.cursor()
                    cursor.execute("CREATE TABLE IF NOT EXISTS Puntos_2 (fecha TEXT, puntaje INTEGER)")
                    # Insertar los datos en la tabla
                    sentencia_sql = "INSERT INTO Puntos_2 (fecha, puntaje) VALUES (?, ?)"
                    cursor.execute(sentencia_sql, (formato_fecha_hora, personaje.puntos))
                    # Confirmar los cambios en la base de datos
                    conexión.commit()
                if menu_intermedio(screen):
                    opcion_menu = 1
                    return opcion_menu
                if not menu_intermedio(screen):
                    opcion_menu = 3
                    return opcion_menu
        if gameover:
                mostrar_mensaje("PERDISTE. Presiona R para volver a intentar.", screen)
            
            
                keys = pygame.key.get_pressed()
                if keys[pygame.K_r] and gameover:
                    gameover = False
                    personaje = Personaje(100, 600)
    
    pygame.quit()
    return nivel


def juego_naves(estado_juego, vm, ve):
    
    width = 800
    height = 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Blue Oddity")

    pygame.mixer.music.load('sfx/bossfight.wav')
    pygame.mixer.music.play(-1)
    
    #FONDO
    folder_path = "img/animacion"  
    frame_files = sorted(os.listdir(folder_path))
    frames = []

    for file_name in frame_files:
        file_path = os.path.join(folder_path, file_name)
        frame = pygame.image.load(file_path)
        frame = pygame.transform.scale(frame, (width, height))  
        frames.append(frame)

    clock = pygame.time.Clock()
    frame_index = 0
    done = False
    game_over = False 

    #PJ
    nave = Nave((50, 50), (500, height // 2))
    velocidad_mov = 5
    movimiento_x = 0
    movimiento_y = 0


    proyectiles = []
    disparando = False
    cadencia_disparo = 70  
    tiempo_ultimo_disparo = pygame.time.get_ticks()
    sonido_proyectil = (pygame.mixer.Sound("sfx/click.wav"))
    buff = False

    shift_presionado = False
    imagen_adicional = pygame.image.load("img/158.png")
    imagen_adicional = pygame.transform.scale(imagen_adicional, (10, 10))
    sonido_buff = pygame.mixer.Sound("sfx/powerUp.wav")


    #Boss
    x_b = 400
    y_b = 100

    proyectil_cont = []
    cadencia_boss = 400
    ultimo_disparo_enemigo = pygame.time.get_ticks() 
    patron = 1
    boss = Boss((80, 100),x_b, y_b)
    sonido_boss = pygame.mixer.Sound("sfx/bossattack.wav")

    direcciones = [(400, 100), (160, 40), (400, 100), (600, 300), (620, 140)]
    direccion_actual = 0 
    tiempo_estatico = 360  
    patron_actual = 0

    #Dificultad
    modo_lunatico = False

    # Contador para el tiempo estático
    contador_estatico = 0

    pygame.mixer.music.set_volume(vm)
    win = True

    while not done:
        pygame.mixer.music.get_busy()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                done = True
        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                movimiento_x = -velocidad_mov
            elif keys[pygame.K_RIGHT]:
                movimiento_x = velocidad_mov
            else:
                movimiento_x = 0
            
            if keys[pygame.K_UP]:
                movimiento_y = -velocidad_mov
            elif keys[pygame.K_DOWN]:
                movimiento_y = velocidad_mov
            else:
                movimiento_y = 0
            
            if keys[pygame.K_z]:
                disparando = True
            else:
                disparando = False
            
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                shift_presionado = True
            else:
                shift_presionado = False


            nave.mover(movimiento_x, movimiento_y)
            nave.mover_hitbox(10, 10)
            
            

            screen.blit(frames[frame_index], (0, 0))
            frame_index = (frame_index + 1) % len(frames)


            if disparando:
                tiempo_actual = pygame.time.get_ticks()
                if tiempo_actual - tiempo_ultimo_disparo >= cadencia_disparo:
                    balas = Proyectil((15, 15), nave.posicion, "img/21.png", 50, 15, 90)
                    sonido_proyectil.play()
                    if buff:
                        if shift_presionado:
                            balas.bufeo_pj(proyectiles, nave, 90, 7)
                            tiempo_ultimo_disparo = tiempo_actual
                        else:
                            balas.bufeo_pj(proyectiles, nave, 90, 20)
                            tiempo_ultimo_disparo = tiempo_actual
                    else:
                        proyectiles.append(balas)
                        tiempo_ultimo_disparo = tiempo_actual
            
            Proyectil.actualizar_proyectiles(proyectiles, screen)
            
            
            tiempo = pygame.time.get_ticks()
            
            if boss.visible:
                boss.dar_hitbox()
                if tiempo - ultimo_disparo_enemigo >= cadencia_boss:
                    
                    disparo = Proyectil((15, 15) , (boss.posicion[0], boss.posicion[1] + 10), "img/41.png", 90, -3, 0)
                    
                    match patron:
                        case 1:
                            if modo_lunatico:
                                disparo.espiral(proyectil_cont, boss.posicion[0], boss.posicion[1], 0, 30, 10)
                            sonido_boss.play()
                            disparo.triple_linea(proyectil_cont, boss.posicion[0], boss.posicion[1], 2, nave.hitbox.x, nave.hitbox.y)
                            patron += 1
                        case 2:
                            disparo.arco (proyectil_cont, boss.posicion[0], boss.posicion[1], 0)
                            patron += 1
                        case 3:
                            disparo.circulo(proyectil_cont, boss.posicion[0], boss.posicion[1], 0)
                            sonido_boss.play()
                            if modo_lunatico:
                                patron += 1
                            else:
                                patron = 1
                        case 4:
                            sonido_boss.play()
                            disparo.linea(proyectil_cont, boss.posicion[0], boss.posicion[1], 2, nave.hitbox.x, nave.hitbox.y)
                            patron = 1
                    ultimo_disparo_enemigo = tiempo
            
            
            if boss.dar_direccion(*direcciones[direccion_actual]):
                contador_estatico += 1
                
                if contador_estatico >= tiempo_estatico:
                    direccion_actual = (direccion_actual + 1) % len(direcciones)
                    contador_estatico = 0
                    
                    if direccion_actual == 0:
                        patron_actual = (patron_actual + 1) % len(direcciones)
            
            direccion_actual = (direccion_actual + patron_actual * len(direcciones)) % len(direcciones)
            
            
            Proyectil.actualizar_proyectiles(proyectil_cont, screen)
            
            game_over = nave.verificar_colision(proyectil_cont)

            nave.dibujar(screen)
            
            if shift_presionado:
                screen.blit(imagen_adicional, (nave.posicion[0] + 19, nave.posicion[1]+20))
                velocidad_mov = 2.5
            else:
                velocidad_mov = 5
            
            if boss.verificar_colision(proyectiles, screen):
                buff = True
                sonido_buff.play()
            elif boss.verificar_colision(proyectiles, screen) == False:
                if win:
                    boss.animar_muerte(screen)
                    print("GANASTE")
                    win = False
            
            
            boss.actualizar()
            boss.dibujar(screen)
            
            for i in range(pygame.mixer.get_num_channels()):
                canal = pygame.mixer.Channel(i)
                canal.set_volume(ve) 
        if not win:
            mostrar_mensaje(f"GANASTE! Juego hecho por Franco Ferrari", screen)
            nave.vida = 20
        if game_over:
            
            mostrar_mensaje("PERDISTE. Presiona R para volver a intentar.", screen)
        
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r] and game_over:
            game_over = False
            nave = Nave((50, 50), (width/2, height/2))

        pygame.display.flip()
        clock.tick(60)
    return estado_juego