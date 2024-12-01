import os
import random
import json
import csv
import pygame

pygame.init()

#Constantes
#PANTALLA
ANCHO_PANTALLA = 800
ALTO_PANTALLA = int(ANCHO_PANTALLA * 0.8)
FONDO = (33, 29, 46)
#COLORES
ROJO = (255, 0, 0)
BLANCO = (255,255,255)
VERDE = (0, 255, 0)
NEGRO = (0,0,0)
#JUGADOR
MOV_IZQ = False
MOV_DER = False
DISPARA = False
#FISICAS
GRAVEDAD = 0.75
#graficos
FPS = 60
COLUMNAS = 150
RENGLONES = 16
CHUNK = ALTO_PANTALLA // RENGLONES
TIPOS_BLOQUES = 21
DESPLAZAMIENTO_PANT = 0
DESPLAZAMIENTO_TIMER = 200
DESPLAZAMIENTO_FONDO = 0

NIVEL = 1
MAX_NIVEL = 3
INICIO_JUEGO = False

clock = pygame.time.Clock()
fuente = pygame.font.SysFont('bates shower', 20)

# Configuración de la pantalla
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption('Juego shooter - plataforma')

#MUSICA



#IMGS
    #boton
incio_bt = pygame.image.load('img/fondo/inicio_bt.png').convert_alpha()
final_bt = pygame.image.load('img/fondo/fin_bt.png').convert_alpha()
reiniciar_bt = pygame.image.load('img/fondo/reinicio_bt.png').convert_alpha()
    #fondo
bg_1 = pygame.transform.scale(pygame.image.load('img/fondo/background1.png').convert_alpha(), (ANCHO_PANTALLA, ALTO_PANTALLA))
bg_2 = pygame.transform.scale(pygame.image.load('img/fondo/background2.png').convert_alpha(), (ANCHO_PANTALLA, ALTO_PANTALLA))
bg_3 = pygame.transform.scale(pygame.image.load('img/fondo/background3.png').convert_alpha(), (ANCHO_PANTALLA, ALTO_PANTALLA))
bg_4 = pygame.transform.scale(pygame.image.load('img/fondo/background4a.png').convert_alpha(), (ANCHO_PANTALLA, ALTO_PANTALLA))
#--------------
bg_5 = pygame.transform.scale(pygame.image.load('img/fondo/bg1.png').convert_alpha(), (ANCHO_PANTALLA, ALTO_PANTALLA))
bg_6 = pygame.transform.scale(pygame.image.load('img/fondo/bg2.png').convert_alpha(), (ANCHO_PANTALLA, ALTO_PANTALLA))
bg_7 = pygame.transform.scale(pygame.image.load('img/fondo/bg3.png').convert_alpha(), (ANCHO_PANTALLA, ALTO_PANTALLA))
bg_8 = pygame.transform.scale(pygame.image.load('img/fondo/bg4.png').convert_alpha(), (ANCHO_PANTALLA, ALTO_PANTALLA))
#--------------
bg_9 = pygame.transform.scale(pygame.image.load('img/fondo/1.png').convert_alpha(), (ANCHO_PANTALLA, ALTO_PANTALLA))
bg_10 = pygame.transform.scale(pygame.image.load('img/fondo/2.png').convert_alpha(), (ANCHO_PANTALLA, ALTO_PANTALLA))
bg_11 = pygame.transform.scale(pygame.image.load('img/fondo/3.png').convert_alpha(), (ANCHO_PANTALLA, ALTO_PANTALLA))
bg_12 = pygame.transform.scale(pygame.image.load('img/fondo/4.png').convert_alpha(), (ANCHO_PANTALLA, ALTO_PANTALLA))
bg_13 = pygame.transform.scale(pygame.image.load('img/fondo/5.png').convert_alpha(), (ANCHO_PANTALLA, ALTO_PANTALLA))
bg_14 = pygame.transform.scale(pygame.image.load('img/fondo/6.png').convert_alpha(), (ANCHO_PANTALLA, ALTO_PANTALLA))

menu_img = pygame.transform.scale(pygame.image.load('img/fondo/menu_img.png').convert_alpha(), (ANCHO_PANTALLA, ALTO_PANTALLA))

lista_img = []
for x in range(TIPOS_BLOQUES):
    img = pygame.image.load(f'img/mundo/{x}.png')
    img = pygame.transform.scale(img, (CHUNK, CHUNK))
    lista_img.append(img)

bala_img = pygame.transform.scale(pygame.image.load('img/icons/disparo/0.png').convert_alpha(), (45,40))
moneda_img = pygame.transform.scale(pygame.image.load('img/icons/moneda/0.png').convert_alpha(), (12,15))


def fondo():
    pantalla.fill(FONDO)
    if NIVEL == 1:
        ancho = bg_1.get_width()
        for x in range (6):
            pantalla.blit(bg_1, ((x * ancho) - DESPLAZAMIENTO_FONDO * 0.5, 0))
            pantalla.blit(bg_2, ((x * ancho) - DESPLAZAMIENTO_FONDO * 0.6, 0))
            pantalla.blit(bg_3, ((x * ancho) - DESPLAZAMIENTO_FONDO * 0.7, 0))
            pantalla.blit(bg_4, ((x * ancho) - DESPLAZAMIENTO_FONDO * 0.8, 0))
    elif NIVEL == 2:
        ancho = bg_5.get_width()
        for x in range (6):
            pantalla.blit(bg_5, ((x * ancho) - DESPLAZAMIENTO_FONDO * 0.5, 0))
            pantalla.blit(bg_6, ((x * ancho) - DESPLAZAMIENTO_FONDO * 0.6, 0))
            pantalla.blit(bg_7, ((x * ancho) - DESPLAZAMIENTO_FONDO * 0.7, 0))
            pantalla.blit(bg_8, ((x * ancho) - DESPLAZAMIENTO_FONDO * 0.8, 0))
    else:
        ancho = bg_9.get_width()
        for x in range (6):
            pantalla.blit(bg_9, ((x * ancho) - DESPLAZAMIENTO_FONDO * 0.5, 0))
            pantalla.blit(bg_10, ((x * ancho) - DESPLAZAMIENTO_FONDO * 0.6, 0))
            pantalla.blit(bg_11, ((x * ancho) - DESPLAZAMIENTO_FONDO * 0.7, 0))
            pantalla.blit(bg_12, ((x * ancho) - DESPLAZAMIENTO_FONDO * 0.8, 0))
            pantalla.blit(bg_13, ((x * ancho) - DESPLAZAMIENTO_FONDO * 0.8, 0))
            pantalla.blit(bg_14, ((x * ancho) - DESPLAZAMIENTO_FONDO * 0.8, 0))

def dibujar_texto(texto, fuente, color, x, y):
    imagen_texto = fuente.render(texto, True, color)
    pantalla.blit(imagen_texto, (x, y))

def reiniciar_nivel():
    grupo_enemigo.empty()
    grupo_bala.empty()
    grupo_items.empty()
    grupo_decoracion.empty()
    grupo_agua.empty()
    grupo_salida.empty()

    data = []
    for ren in range(RENGLONES):
        r = [-1] * COLUMNAS # -1 = bloque vacio
        data.append(r)

    return data

#CLASE JUGADOR/ENEMIGO
class Character(pygame.sprite.Sprite):
    def __init__(self, tipo, x, y, escala, velocidad, ammo):
        super().__init__()
        self.ban = 1
        self.tipo = tipo
        self.esta_vivo = True
        self.vida = 100
        self.vida_max = 100
        self.monedas = 0
        self.velocidad = velocidad
        self.municion = ammo
        self.municion_inicial = ammo
        self.disparo_cooldown = 0
        self.direccion = 1
        self.vel_y = 0
        self.salto = False
        self.en_aire = True
        self.giro = False
        self.animaciones = []
        self.indice_frame = 0
        self.accion = 0 # 0 = idle, 1 = caminar, 2 = saltar, 3 = disparo
        self.tiempo = pygame.time.get_ticks()

        #IA VARIABLES
        self.contador_mov = 0
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.en_reposo = False
        self.contador_reposo = 0


        tipos_animaciones = ['idle', 'run', 'salto', 'disparo', 'muerte']
        for tipo in tipos_animaciones:
            tempLista = []
            num_frames = len(os.listdir(f'img/{self.tipo}/{tipo}'))
            for i in range(num_frames):
                img = pygame.image.load(f'img/{self.tipo}/{tipo}/{i}.png').convert_alpha()
                if tipo == 'run' and self.tipo == 'enemy':
                    img = pygame.transform.scale(img, (int(img.get_width() * escala*2), int(img.get_height() * escala*2)))
                elif tipo == 'idle' and self.tipo == 'enemy':
                    img = pygame.transform.scale(img, (int(img.get_width() * escala*1), int(img.get_height() * escala*1)))
                else:
                    img = pygame.transform.scale(img, (int(img.get_width() * escala), int(img.get_height() * escala)))
                tempLista.append(img)
            self.animaciones.append(tempLista)

        self.imagen = self.animaciones[self.accion][self.indice_frame]
        self.rect = self.imagen.get_rect()
        self.rect.center = (x, y)
        self.ancho = self.imagen.get_width()
        self.altura = self.imagen.get_height()

    def update(self):
        self.actualiza_animacion()
        self.revisar_vida()
        #actualizar cooldown
        if self.disparo_cooldown > 0:
            self.disparo_cooldown -= 1

    def movimiento(self, mov_izq, mov_der):
        pantalla_desp = 0

        dx = 0
        dy = 0
        #movimiento a la izquierda
        if mov_izq:
            dx = -self.velocidad
            self.direccion = -1
            self.giro = True
        #movimiento a la derecha
        if mov_der:
            dx = self.velocidad
            self.direccion = 1
            self.giro = False

        #salto
        if self.salto is True and self.en_aire is False:
            self.vel_y = -12
            self.salto = False
            self.en_aire = True

        #gravedad
        self.vel_y += GRAVEDAD
        if self.vel_y > 10:
            self.vel_y = 10

        dy += self.vel_y

        #revisar colision con el suelo
        for bloque in mundo.lista_obstaculos:
            #Colision en el eje x
            if bloque[1].colliderect(self.rect.x + dx, self.rect.y, self.ancho, self.altura):
                dx = 0
                if self.tipo == 'enemy':
                    self.direccion *= -1
                    self.contador_mov = 0
            #Colision en el eje y
            if bloque[1].colliderect(self.rect.x, self.rect.y + dy, self.ancho, self.altura):
                #Colsion en salto
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = bloque[1].bottom - self.rect.top
                #Colision en caida
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.en_aire = False
                    dy = bloque[1].top - self.rect.bottom

        if pygame.sprite.spritecollide(self, grupo_agua, False):
            self.vida = 0

        nivel_completo = False
        if pygame.sprite.spritecollide(self, grupo_salida, False):
            nivel_completo = True

        if self.rect.bottom > ALTO_PANTALLA:
            self.vida = 0

        if self.tipo == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > ANCHO_PANTALLA:
                dx = 0

        self.rect.x += dx
        self.rect.y += dy

        #actualizar desplazamiento
        if self.tipo == 'player':
            if (self.rect.right > ANCHO_PANTALLA - DESPLAZAMIENTO_TIMER and DESPLAZAMIENTO_FONDO < (mundo.tam_nivel * CHUNK) - ANCHO_PANTALLA)\
                or (self.rect.left < DESPLAZAMIENTO_TIMER and DESPLAZAMIENTO_FONDO > abs(dx)):
                self.rect.x -= dx
                pantalla_desp = -dx

        return pantalla_desp, nivel_completo

    def disparo(self):
        if self.disparo_cooldown == 0 and self.municion > 0:
            self.disparo_cooldown = 30
            if self.tipo == 'player':
                bala = Bala(self.rect.centerx + (1.1 * self.rect.size[0] * self.direccion), self.rect.centery - 8, self.direccion)
                self.municion -= 1
                #self.vida -= 5
            else:
                bala = Bala(self.rect.centerx + (1.3 * self.rect.size[0] * self.direccion), self.rect.centery- 5, self.direccion)
                self.municion -= 1
            grupo_bala.add(bala)
            print('vida disp:' + str(self.vida))

    def IA(self):
        if self.esta_vivo and player.esta_vivo:
            #Aletoriedad para el reposo
            if self.en_reposo is False and random.randint(1, 200) == 1:
                self.actualiza_accion(0)
                self.en_reposo = True
                self.contador_reposo = 50

            #colision con el jugador
            if self.vision.colliderect(player.rect):
                self.actualiza_accion(3)
                self.disparo()

            else:
                #movimiento
                if self.en_reposo is False:
                    if self.direccion == 1:
                        ia_mov_der = True
                    else:
                        ia_mov_der = False
                    ia_mov_izq = not ia_mov_der
                    self.movimiento(ia_mov_izq, ia_mov_der)
                    self.actualiza_accion(1)

                    self.contador_mov += 1

                    #Vision del enemigo
                    self.vision.center = (self.rect.centerx + 75 * self.direccion, self.rect.centery)

                    #Cambio de direccion
                    if self.contador_mov >= CHUNK:
                        self.contador_mov *= -1
                        self.direccion *= -1
                else:
                    self.contador_reposo -= 1
                    if self.contador_reposo <= 0:
                        self.en_reposo = False

        self.rect.x += DESPLAZAMIENTO_PANT

    def actualiza_animacion(self):
        if self.accion == 3:
            ANIMACION_COOLDOWN = 70
        else:
            ANIMACION_COOLDOWN = 35
        self.imagen = self.animaciones[self.accion][self.indice_frame]
        if pygame.time.get_ticks() - self.tiempo > ANIMACION_COOLDOWN:
            self.tiempo = pygame.time.get_ticks()
            self.indice_frame += 1
        if self.indice_frame >= len(self.animaciones[self.accion]):
            if self.accion == 4:
                if self.ban == 1:
                    self.rect.y += 25
                    self.ban = 0
                self.indice_frame = len(self.animaciones[self.accion]) - 1
            else:
                self.indice_frame = 0

    def actualiza_accion(self, nueva_accion):
        if nueva_accion != self.accion:
            self.accion = nueva_accion
            self.indice_frame = 0
            self.tiempo = pygame.time.get_ticks()

    def revisar_vida(self):
        if self.vida <= 0:
            self.vida = 0
            self.velocidad = 0
            self.esta_vivo = False
            self.actualiza_accion(4)

    def draw(self):
        pantalla.blit(pygame.transform.flip(self.imagen, self.giro, False), self.rect)

class Mundo():
    def __init__(self):
        self.lista_obstaculos = []

    def proceso_data(self, data):
        self.tam_nivel = len(data[0])
        for y, ren in enumerate(data):
            for x, bloque in enumerate(ren):
                if bloque >= 0:
                    img = lista_img[bloque]
                    img_rect = img.get_rect()
                    img_rect.x = x * CHUNK
                    img_rect.y = y * CHUNK
                    chunk_data = (img, img_rect)
                    if bloque >= 0 and bloque <= 8:
                        self.lista_obstaculos.append(chunk_data)
                    elif bloque >= 9 and bloque <= 10:
                        agua = Agua(img, x*CHUNK, y*CHUNK)
                        grupo_agua.add(agua)
                    elif bloque >= 11 and bloque <= 14:
                        decoracion = Decoracion(img, x*CHUNK, y*CHUNK)
                        grupo_decoracion.add(decoracion)
                    elif bloque == 15:
                        #INSTANCIACION DE JUGADOR/ENEMIGO
                        player = Character('player',x*CHUNK, y*CHUNK,0.23, 6, 15)
                        barra_vida =Barra_Vida(10,10, player.vida, player.vida)
                    elif bloque == 16:
                        enemy = Character('enemy',x*CHUNK, y*CHUNK,0.25, 3, 20)
                        grupo_enemigo.add(enemy)
                    elif bloque == 17:
                        item_box = Item('ammo', x*CHUNK, y*CHUNK,1.5)
                        grupo_items.add(item_box)
                    elif bloque == 18:
                        item_box = Item('vida', x*CHUNK, y*CHUNK,1.5)
                        grupo_items.add(item_box)
                    elif bloque == 19:
                        item_box = Item('moneda', x*CHUNK, y*CHUNK,1.5)
                        grupo_items.add(item_box)
                    elif bloque == 20:
                        salida = Salida(img, x*CHUNK, y*CHUNK)
                        grupo_salida.add(salida)

        return player, barra_vida

    def draw(self):
        for tile in self.lista_obstaculos:
            tile[1][0] += DESPLAZAMIENTO_PANT
            pantalla.blit(tile[0], tile[1])

class Decoracion(pygame.sprite.Sprite):
    def __init__(self, img, x, y) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + CHUNK // 2, y + (CHUNK - self.image.get_height()))

    def update(self):
        self.rect.x += DESPLAZAMIENTO_PANT

class Agua(pygame.sprite.Sprite):
    def __init__(self, img, x, y) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + CHUNK // 2, y + (CHUNK - self.image.get_height()))

    def update(self):
        self.rect.x += DESPLAZAMIENTO_PANT

class Salida(pygame.sprite.Sprite):
    def __init__(self, img, x, y) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + CHUNK // 2, y + (CHUNK - self.image.get_height()))

    def update(self):
        self.rect.x += DESPLAZAMIENTO_PANT

#CLASE ITEMS
class Item(pygame.sprite.Sprite):
    def __init__(self, tipo_item, x, y, escala) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.tipo_item = tipo_item
        self.animaciones = []
        self.indice_frame = 0

        num_frames = len(os.listdir(f'img/icons/{self.tipo_item}'))
        for i in range(num_frames):
            img = pygame.image.load(f'img/icons/{self.tipo_item}/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * escala), int(img.get_height() * escala)))
            self.animaciones.append(img)

        self.image = self.animaciones[self.indice_frame]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + CHUNK // 2, y + (CHUNK - self.image.get_height()))
        self.contador = 0

    def update(self):
        self.rect.x += DESPLAZAMIENTO_PANT
        #animacion
        VEL_ANIMACION = 6
        self.contador += 1
        if self.contador >= VEL_ANIMACION:
            self.contador = 0
            self.indice_frame += 1
            if self.indice_frame >= len(self.animaciones):
                self.indice_frame = 0
            self.image = self.animaciones[self.indice_frame]

        #colision
        if pygame.sprite.collide_rect(self, player):
            #revisar que tipo de item toco
            if self.tipo_item == 'vida':
                player.vida += 50
                if player.vida > player.vida_max:
                    player.vida = 100
            elif self.tipo_item == 'ammo':
                player.municion += 3
            else:
                player.monedas += 1
            self.kill()

class Barra_Vida():
    def __init__(self, x, y, vida, max_vida) -> None:
        self.x = x
        self.y = y
        self.vida = vida
        self.max_vida = max_vida

    def draw(self, vida):
        #actualizar con vida nueva
        self.vida = vida
        #calcular radio
        prop = self.vida / self.max_vida
        pygame.draw.rect(pantalla, NEGRO, (103, 26, 154, 24))
        pygame.draw.rect(pantalla, ROJO, (105, 28, 150, 20))
        pygame.draw.rect(pantalla, VERDE, (105, 28, 150 * prop, 20))

#CLASE BALA/DISPARO
class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y, direccion) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.velocidad = 8
        self.direccion = direccion

        self.animaciones = []
        self.indice_frame = 0

        izq = False

        if self.direccion == -1:
            izq = True

        for i in range(5):
            img = pygame.image.load(f'img/icons/disparo/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (60, 60))
            img = pygame.transform.flip(img, izq, False)
            self.animaciones.append(img)

        self.image = self.animaciones[self.indice_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.ancho = self.image.get_width()
        self.largo = self.image.get_height()
        self.contador = 0

    def update(self):
        #animacion
        VEL_ANIMACION = 6
        self.contador += 1
        if self.contador >= VEL_ANIMACION:
            self.contador = 0
            self.indice_frame += 1
            if self.indice_frame >= len(self.animaciones):
                self.indice_frame = len(self.animaciones) - 2
            self.image = self.animaciones[self.indice_frame]

        #mover bala
        self.rect.x += (self.direccion * self.velocidad) + DESPLAZAMIENTO_PANT
        #checar si la bala sale de la pantalla
        if self.rect.right < 0 or self.rect.left > ANCHO_PANTALLA:
            self.kill()

        #colision con la pared
        for bloque in mundo.lista_obstaculos:
            if self.direccion == -1:
                if bloque[1].colliderect(self.rect.x + 15, self.rect.y, self.ancho, self.largo):
                    self.kill()
            else:
                if bloque[1].colliderect(self.rect.x - 15, self.rect.y, self.ancho, self.largo):
                    self.kill()


        #checar colision con el jugador
        if pygame.sprite.spritecollide(player, grupo_bala, False):
            if player.esta_vivo:
                player.vida -= 5
                print('vida player:' + str(player.vida))
                self.kill()

        #checar colision con enemigos
        for enemy in grupo_enemigo:
            if pygame.sprite.spritecollide(enemy, grupo_bala, False):
                if enemy.esta_vivo:
                    enemy.vida -= 25
                    print('vida enemigo:' + str(enemy.vida))
                    self.kill()

#Clase boton
class Boton():
    def __init__(self,x, y, imagen, escala):
        ancho = imagen.get_width()
        alto = imagen.get_height()
        self.imagen = pygame.transform.scale(imagen, (int(ancho * escala), int(alto * escala)))
        self.rect = self.imagen.get_rect()
        self.rect.topleft = (x, y)
        self.clickeado = False

    def draw(self, surface):
        accion = False

        #posicion del mouse
        pos = pygame.mouse.get_pos()

        #revisar la colision con los botones
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clickeado is False:
                accion = True
                self.clickeado = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clickeado = False

        #diujar boton
        surface.blit(self.imagen, (self.rect.x, self.rect.y))
        return accion

#JSON
with open('preguntas.json', 'r') as file:
    preguntas_data = json.load(file)

def Pregunta(fuente, pregunta, color, posx, posy, user_input):
    pantalla.fill(NEGRO)

    texto = fuente.render(pregunta["pregunta"], True, color)
    respuesta_usuario = fuente.render(user_input, True, color)

    pantalla.blit(texto, (posx, posy))
    pantalla.blit(respuesta_usuario, (posx, posy + 60))

    pygame.display.flip()

def Mensaje(fuente, mensaje, color, posx, posy):
    texto = fuente.render(mensaje, True, color)
    pantalla.blit(texto, (posx, posy))
    pygame.display.flip()

#Crear botones
boton_inicio = Boton(ANCHO_PANTALLA // 2 - 130, ALTO_PANTALLA // 2 - 150, incio_bt, 1)
boton_final = Boton(ANCHO_PANTALLA // 2 - 110, ALTO_PANTALLA // 2 + 50, final_bt, 1)
boton_reinicio = Boton(ANCHO_PANTALLA // 2 - 100, ALTO_PANTALLA // 2 - 50, reiniciar_bt, 2)

#GRUPOS
grupo_bala = pygame.sprite.Group()
grupo_enemigo = pygame.sprite.Group()
grupo_items = pygame.sprite.Group()
grupo_decoracion = pygame.sprite.Group()
grupo_agua = pygame.sprite.Group()
grupo_salida = pygame.sprite.Group()

mundo_data = []
for ren in range(RENGLONES):
    r = [-1] * COLUMNAS
    mundo_data.append(r)

#CARGAR NIVEL
with open(f'nivel{NIVEL}.csv', newline='') as csvfile:
    lector = csv.reader(csvfile, delimiter=',')
    for x, ren in enumerate(lector):
        for y, bloque in enumerate(ren):
            mundo_data[x][y] = int(bloque)

mundo = Mundo()
player, barra_vida = mundo.proceso_data(mundo_data)

pantalla_completa = False
SCREENRECT = pygame.Rect(0,0,800,640)
bestdepth = pygame.display.mode_ok(SCREENRECT.size, 0, 32)

input_text = ""
preguna_actual = random.choice(preguntas_data['preguntas'])
sig_nivel = False

#CICLO DE JUEGO
juego = True
while juego:
    clock.tick(FPS)

    if INICIO_JUEGO is False:
        #dibujar menu
        pantalla.fill(NEGRO)
        pantalla.blit(bg_1, (0, 0))
        pantalla.blit(menu_img, (0, 0))

        if boton_inicio.draw(pantalla):
            INICIO_JUEGO = True
        if boton_final.draw(pantalla):
            juego = False

    else:
        #fondo
        fondo()
        #mapeo de mundo
        mundo.draw()

        #mostrar barra de vida
        barra_vida.draw(player.vida)

        #mostrar vida
        dibujar_texto('Salud: ', fuente, BLANCO, 10, 20)

        #mostrar municion
        dibujar_texto('Municion: ', fuente, BLANCO, 10, 60)
        for x in range(player.municion):
            pantalla.blit(bala_img, (107 + (x * 13), 55))

        #mostrar monedas
        dibujar_texto('Monedas: ', fuente, BLANCO, 10, 100)
        for x in range(player.monedas):
            pantalla.blit(moneda_img, (129 + (x * 15), 110))

        player.update()
        player.draw()

        for enemy in grupo_enemigo:
            enemy.IA()
            enemy.update()
            enemy.draw()

        #actualizar y dibujar grupos
        grupo_bala.update()
        grupo_items.update()
        grupo_decoracion.update()
        grupo_agua.update()
        grupo_salida.update()
        grupo_bala.draw(pantalla)
        grupo_items.draw(pantalla)
        grupo_decoracion.draw(pantalla)
        grupo_agua.draw(pantalla)
        grupo_salida.draw(pantalla)

        if player.esta_vivo:
            if DISPARA:
                player.disparo()
                player.actualiza_accion(3) # disparo
            elif player.en_aire:
                player.actualiza_accion(2) # salto
            elif MOV_DER or MOV_IZQ:
                player.actualiza_accion(1) # run
            else:
                player.actualiza_accion(0) # idle

            DESPLAZAMIENTO_PANT, nivel_completo = player.movimiento(MOV_IZQ, MOV_DER)
            DESPLAZAMIENTO_FONDO -= DESPLAZAMIENTO_PANT

            if nivel_completo:
                NIVEL += 1
                DESPLAZAMIENTO_FONDO = 0
                mundo_data = reiniciar_nivel()
                if NIVEL <= MAX_NIVEL:
                    with open(f'nivel{NIVEL}.csv', newline='') as csvfile:
                        lector = csv.reader(csvfile, delimiter=',')
                        for x, ren in enumerate(lector):
                            for y, bloque in enumerate(ren):
                                mundo_data[x][y] = int(bloque)

                    mundo = Mundo()
                    player, barra_vida = mundo.proceso_data(mundo_data)

        else:
            DESPLAZAMIENTO_PANT = 0

            if boton_reinicio.draw(pantalla):
                DESPLAZAMIENTO_FONDO = 0

                mundo_data = reiniciar_nivel()
                with open(f'nivel{NIVEL}.csv', newline='') as csvfile:
                    lector = csv.reader(csvfile, delimiter=',')
                    for x, ren in enumerate(lector):
                        for y, bloque in enumerate(ren):
                            mundo_data[x][y] = int(bloque)

                mundo = Mundo()
                player, barra_vida = mundo.proceso_data(mundo_data)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            juego = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                juego = False

            if evento.key == pygame.K_f:
                if not pantalla_completa:
                    print("pantalla completa")
                    screen_backup = pantalla.copy()
                    pantalla = pygame.display.set_mode(SCREENRECT.size, 0 | pygame.FULLSCREEN, bestdepth)
                    pantalla.blit(screen_backup, (0,0))
                else:
                    print("pantalla ventana")
                    screen_backup = pantalla.copy()
                    pantalla = pygame.display.set_mode(SCREENRECT.size, 0, bestdepth)
                    pantalla.blit(screen_backup, (0,0))
                pygame.display.flip()
                pantalla_completa = not pantalla_completa
            if evento.key == pygame.K_a:
                MOV_IZQ = True
            if evento.key == pygame.K_d:
                MOV_DER = True
            if evento.key == pygame.K_w and player.esta_vivo:
                player.salto = True
            if evento.key == pygame.K_SPACE:
                DISPARA = True

        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_a:
                MOV_IZQ = False
            if evento.key == pygame.K_d:
                MOV_DER = False
            if evento.key == pygame.K_SPACE:
                DISPARA = False

        #if evento.type == pygame.MOUSEBUTTONDOWN:
        #    if evento.button == 1:
        #        DISPARA = True

        #if evento.type == pygame.MOUSEBUTTONUP:
        #    if evento.button == 1:
        #        DISPARA = False

    pygame.display.update()

pygame.quit()
