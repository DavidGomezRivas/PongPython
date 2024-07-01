import pygame
import sys
import random

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
ancho_pantalla = 800
alto_pantalla = 600
pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
pygame.display.set_caption('Pong con Pygame')

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Configuración de la pelota
radio_pelota = 15
velocidad_pelota_x = 7
velocidad_pelota_y = 7
pelota = pygame.Rect(ancho_pantalla // 2 - radio_pelota, alto_pantalla // 2 - radio_pelota, radio_pelota * 2, radio_pelota * 2)

# Configuración de las palas
ancho_pala = 10
alto_pala = 100
velocidad_pala = 10
velocidad_pala_ia = 5  # Velocidad máxima de la IA reducida
pala_izquierda = pygame.Rect(50, alto_pantalla // 2 - alto_pala // 2, ancho_pala, alto_pala)
pala_derecha = pygame.Rect(ancho_pantalla - 50 - ancho_pala, alto_pantalla // 2 - alto_pala // 2, ancho_pala, alto_pala)

# Variables de puntuación
puntos_izquierda = 0
puntos_derecha = 0
fuente = pygame.font.Font(None, 36)

# Variable para controlar el movimiento de la pelota
pelota_en_movimiento = False

# Función para dibujar el juego
def dibujar(pantalla, pelota, pala_izquierda, pala_derecha, puntos_izquierda, puntos_derecha):
    pantalla.fill(NEGRO)
    pygame.draw.ellipse(pantalla, BLANCO, pelota)
    pygame.draw.rect(pantalla, BLANCO, pala_izquierda)
    pygame.draw.rect(pantalla, BLANCO, pala_derecha)
    
    texto_puntos = fuente.render(f"{puntos_izquierda} - {puntos_derecha}", True, BLANCO)
    pantalla.blit(texto_puntos, (ancho_pantalla // 2 - texto_puntos.get_width() // 2, 10))
    pygame.display.flip()

# Función para mostrar el menú
def mostrar_menu():
    while True:
        pantalla.fill(NEGRO)
        titulo = fuente.render('Pong con Pygame', True, BLANCO)
        boton_jugar = fuente.render('Jugar', True, BLANCO)
        boton_jugar_ia = fuente.render('Jugar contra IA', True, BLANCO)
        boton_como_jugar = fuente.render('Cómo Jugar', True, BLANCO)
        boton_salir = fuente.render('Salir', True, BLANCO)

        pantalla.blit(titulo, (ancho_pantalla // 2 - titulo.get_width() // 2, 100))
        pantalla.blit(boton_jugar, (ancho_pantalla // 2 - boton_jugar.get_width() // 2, 200))
        pantalla.blit(boton_jugar_ia, (ancho_pantalla // 2 - boton_jugar_ia.get_width() // 2, 250))
        pantalla.blit(boton_como_jugar, (ancho_pantalla // 2 - boton_como_jugar.get_width() // 2, 300))
        pantalla.blit(boton_salir, (ancho_pantalla // 2 - boton_salir.get_width() // 2, 350))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.get_rect(topleft=(ancho_pantalla // 2 - boton_jugar.get_width() // 2, 200)).collidepoint(evento.pos):
                    return 'jugar'
                if boton_jugar_ia.get_rect(topleft=(ancho_pantalla // 2 - boton_jugar_ia.get_width() // 2, 250)).collidepoint(evento.pos):
                    return 'jugar_ia'
                if boton_como_jugar.get_rect(topleft=(ancho_pantalla // 2 - boton_como_jugar.get_width() // 2, 300)).collidepoint(evento.pos):
                    return 'como_jugar'
                if boton_salir.get_rect(topleft=(ancho_pantalla // 2 - boton_salir.get_width() // 2, 350)).collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()

# Función para mostrar las instrucciones
def mostrar_instrucciones():
    while True:
        pantalla.fill(NEGRO)
        instrucciones = [
            "Instrucciones del Juego:",
            "Jugador 1: Usa las teclas 'A' y 'D' para mover la pala.",
            "Jugador 2: Usa las teclas de flecha izquierda y derecha para mover la pala.",
            "Presiona ESPACIO para iniciar el movimiento de la pelota.",
            "El primer jugador en anotar 10 puntos gana."
        ]

        for i, linea in enumerate(instrucciones):
            texto = fuente.render(linea, True, BLANCO)
            pantalla.blit(texto, (ancho_pantalla // 2 - texto.get_width() // 2, 100 + i * 40))

        boton_volver = fuente.render('Volver', True, BLANCO)
        pantalla.blit(boton_volver, (ancho_pantalla // 2 - boton_volver.get_width() // 2, alto_pantalla - 100))
        
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_volver.get_rect(topleft=(ancho_pantalla // 2 - boton_volver.get_width() // 2, alto_pantalla - 100)).collidepoint(evento.pos):
                    return

# Bucle principal del juego
def main():
    global pelota_en_movimiento, puntos_izquierda, puntos_derecha
    while True:
        seleccion = mostrar_menu()
        if seleccion == 'jugar':
            puntos_izquierda, puntos_derecha = 0, 0
            pelota_en_movimiento = False
            juego(ia=False)
        elif seleccion == 'jugar_ia':
            puntos_izquierda, puntos_derecha = 0, 0
            pelota_en_movimiento = False
            juego(ia=True)
        elif seleccion == 'como_jugar':
            mostrar_instrucciones()

def juego(ia):
    global pelota_en_movimiento, puntos_izquierda, puntos_derecha, velocidad_pelota_x, velocidad_pelota_y
    reloj = pygame.time.Clock()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pelota_en_movimiento = True
        
        # Movimiento de las palas
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_a] and pala_izquierda.top > 0:
            pala_izquierda.y -= velocidad_pala
        if teclas[pygame.K_d] and pala_izquierda.bottom < alto_pantalla:
            pala_izquierda.y += velocidad_pala
        if not ia:
            if teclas[pygame.K_LEFT] and pala_derecha.top > 0:
                pala_derecha.y -= velocidad_pala
            if teclas[pygame.K_RIGHT] and pala_derecha.bottom < alto_pantalla:
                pala_derecha.y += velocidad_pala
        else:
            # Movimiento de la IA con errores
            if pala_derecha.centery < pelota.centery and pala_derecha.bottom < alto_pantalla:
                pala_derecha.y += velocidad_pala_ia
            if pala_derecha.centery > pelota.centery and pala_derecha.top > 0:
                pala_derecha.y -= velocidad_pala_ia
            # Aumentar el error de la IA
            if random.randint(0, 20) < 5:  # Mayor probabilidad de error
                if pala_derecha.centery < pelota.centery and pala_derecha.bottom < alto_pantalla:
                    pala_derecha.y += velocidad_pala_ia // 2
                if pala_derecha.centery > pelota.centery and pala_derecha.top > 0:
                    pala_derecha.y -= velocidad_pala_ia // 2

        # Movimiento de la pelota
        if pelota_en_movimiento:
            pelota.x += velocidad_pelota_x
            pelota.y += velocidad_pelota_y

        # Colisiones con las paredes
        if pelota.top <= 0 or pelota.bottom >= alto_pantalla:
            velocidad_pelota_y = -velocidad_pelota_y
        if pelota.left <= 0:
            puntos_derecha += 1
            pelota.x, pelota.y = ancho_pantalla // 2 - radio_pelota, alto_pantalla // 2 - radio_pelota
            pelota_en_movimiento = False
        if pelota.right >= ancho_pantalla:
            puntos_izquierda += 1
            pelota.x, pelota.y = ancho_pantalla // 2 - radio_pelota, alto_pantalla // 2 - radio_pelota
            pelota_en_movimiento = False

        # Colisiones con las palas
        if pelota.colliderect(pala_izquierda) or pelota.colliderect(pala_derecha):
            velocidad_pelota_x = -velocidad_pelota_x

        dibujar(pantalla, pelota, pala_izquierda, pala_derecha, puntos_izquierda, puntos_derecha)
        reloj.tick(60)

if __name__ == "__main__":
    main()
