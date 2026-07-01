import pygame
import sys
from Juego import PartidaTruco

# Configuración inicial
ANCHO = 800
ALTO = 600
FPS = 60

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("TP Final - Truco Argentino")
    reloj = pygame.time.Clock()

    # Inicializamos la lógica del juego
    juego = PartidaTruco()
    juego.repartir()

    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        # Fondo verde de mesa de cartas
        pantalla.fill((34, 139, 34))

        # Dibujar cartas del Jugador 1 (abajo)
        x_inicial = 250
        for i, carta in enumerate(juego.mano_j1):
            if carta:
                carta.dibujar(pantalla, x_inicial + (i * 110), 400)

        pygame.display.flip()
        reloj.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
