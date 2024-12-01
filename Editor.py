import pygame
import button
import csv
import pickle

pygame.init()

clock = pygame.time.Clock()
FPS = 60

#game window
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 640
MARGEN_BAJO = 100
MARGEN_LATERAL = 300

pantalla = pygame.display.set_mode((ANCHO_PANTALLA + MARGEN_LATERAL, ALTO_PANTALLA + MARGEN_BAJO))
pygame.display.set_caption('EDITOR DE NIVELES')


#define game variables
ROWS = 16
MAX_COLS = 150
TILE_SIZE = ALTO_PANTALLA // ROWS
TILE_TYPES = 21
nivel = 0
bloque_actual = 0
desp_izq = False
desp_der = False
desplazamiento = 0
vel_desp = 1


#load images
bg_4 = pygame.transform.scale(pygame.image.load('img/fondo/background4a.png').convert_alpha(), (800, 640))
bg_3 = pygame.transform.scale(pygame.image.load('img/fondo/background3.png').convert_alpha(), (800, 640))
bg_2 = pygame.transform.scale(pygame.image.load('img/fondo/background2.png').convert_alpha(), (800, 640))
bg_1 = pygame.transform.scale(pygame.image.load('img/fondo/background1.png').convert_alpha(), (800, 640))
#store tiles in a list
lista_img = []
for x in range(TILE_TYPES):
	img = pygame.image.load(f'img/mundo/{x}.png').convert_alpha()
	img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
	lista_img.append(img)

img_guardado = pygame.image.load('img/save_btn.png').convert_alpha()
img_cargado = pygame.image.load('img/load_btn.png').convert_alpha()


#define colours
VERDE = (144, 201, 120)
BLANCO = (255, 255, 255)
ROJO = (200, 25, 25)

#define font
fuente = pygame.font.SysFont('Futura', 30)

#create empty tile list
datos_mundo = []
for row in range(ROWS):
	r = [-1] * MAX_COLS
	datos_mundo.append(r)

#create ground
for bloque in range(0, MAX_COLS):
	datos_mundo[ROWS - 1][bloque] = 0


#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	pantalla.blit(img, (x, y))


#create function for drawing background
def draw_bg():
	pantalla.fill(VERDE)
	ancho = bg_1.get_width()
	for x in range(4):
		pantalla.blit(bg_1, ((x * ancho) - desplazamiento * 0.5, 0))
		pantalla.blit(bg_2, ((x * ancho) - desplazamiento * 0.6, ALTO_PANTALLA - bg_2.get_height() - 300))
		pantalla.blit(bg_3, ((x * ancho) - desplazamiento * 0.7, ALTO_PANTALLA - bg_3.get_height() - 150))
		pantalla.blit(bg_4, ((x * ancho) - desplazamiento * 0.8, ALTO_PANTALLA - bg_4.get_height()))

#draw grid
def draw_grid():
	#vertical lines
	for c in range(MAX_COLS + 1):
		pygame.draw.line(pantalla, BLANCO, (c * TILE_SIZE - desplazamiento, 0), (c * TILE_SIZE - desplazamiento, ALTO_PANTALLA))
	#horizontal lines
	for c in range(ROWS + 1):
		pygame.draw.line(pantalla, BLANCO, (0, c * TILE_SIZE), (ANCHO_PANTALLA, c * TILE_SIZE))


#function for drawing the world tiles
def draw_world():
	for y, row in enumerate(datos_mundo):
		for x, tile in enumerate(row):
			if tile >= 0:
				pantalla.blit(lista_img[tile], (x * TILE_SIZE - desplazamiento, y * TILE_SIZE))



#create buttons
boton_guardado = button.Button(ANCHO_PANTALLA // 2, ALTO_PANTALLA + MARGEN_BAJO - 50, img_guardado, 1)
boton_carga = button.Button(ANCHO_PANTALLA // 2 + 200, ALTO_PANTALLA + MARGEN_BAJO - 50, img_cargado, 1)
#make a button list
lista_boton = []
col_btn = 0
fila_btn = 0
for i in range(len(lista_img)):
	tile_button = button.Button(ANCHO_PANTALLA + (75 * col_btn) + 50, 75 * fila_btn + 50, lista_img[i], 1)
	lista_boton.append(tile_button)
	col_btn += 1
	if col_btn == 3:
		fila_btn += 1
		col_btn = 0


juego = True
while juego:

	clock.tick(FPS)

	draw_bg()
	draw_grid()
	draw_world()

	draw_text(f'Nivel: {nivel}', fuente, BLANCO, 10, ALTO_PANTALLA + MARGEN_BAJO - 90)
	draw_text('Presione la tecla UP o DOWN para cambiar de nivel', fuente, BLANCO, 10, ALTO_PANTALLA + MARGEN_BAJO - 60)

	#carga y guardado de datos
	if boton_guardado.draw(pantalla):
		with open(f'nivel{nivel}.csv', 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter = ',')
			for row in datos_mundo:
				writer.writerow(row)

	if boton_carga.draw(pantalla):
		desplazamiento = 0
		with open(f'nivel{nivel}.csv', newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter = ',')
			for x, row in enumerate(reader):
				for y, bloque in enumerate(row):
					datos_mundo[x][y] = int(bloque)
				
	pygame.draw.rect(pantalla, VERDE, (ANCHO_PANTALLA, 0, MARGEN_LATERAL, ALTO_PANTALLA))

	#elegir un bloque
	button_count = 0
	for button_count, i in enumerate(lista_boton):
		if i.draw(pantalla):
			bloque_actual = button_count

	#resaltar el bloque seleccionado
	pygame.draw.rect(pantalla, ROJO, lista_boton[bloque_actual].rect, 3)

	if desp_izq == True and desplazamiento > 0:
		desplazamiento -= 5 * vel_desp
	if desp_der == True and desplazamiento < (MAX_COLS * TILE_SIZE) - ANCHO_PANTALLA:
		desplazamiento += 5 * vel_desp

	pos = pygame.mouse.get_pos()
	x = (pos[0] + desplazamiento) // TILE_SIZE
	y = pos[1] // TILE_SIZE

	if pos[0] < ANCHO_PANTALLA and pos[1] < ALTO_PANTALLA:
		if pygame.mouse.get_pressed()[0] == 1:
			if datos_mundo[y][x] != bloque_actual:
				datos_mundo[y][x] = bloque_actual
		if pygame.mouse.get_pressed()[2] == 1:
			datos_mundo[y][x] = -1


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			juego = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				nivel += 1
			if event.key == pygame.K_DOWN and nivel > 0:
				nivel -= 1
			if event.key == pygame.K_LEFT:
				desp_izq = True
			if event.key == pygame.K_RIGHT:
				desp_der = True
			if event.key == pygame.K_RSHIFT:
				vel_desp = 5


		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				desp_izq = False
			if event.key == pygame.K_RIGHT:
				desp_der = False
			if event.key == pygame.K_RSHIFT:
				vel_desp = 1


	pygame.display.update()

pygame.quit()
