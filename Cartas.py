import pygame

class Carta:
    def __init__(self, numero, palo, ruta_imagen):
        self.numero = numero
        self.palo = palo
        try:
            self.imagen = pygame.image.load(ruta_imagen)
            self.imagen = pygame.transform.scale(self.imagen, (100, 150))
        except:
            self.imagen = None
            print(f"Error: No se encontró la imagen en {ruta_imagen}")

    def obtener_jerarquia(self):
        pass

    def dibujar(self, pantalla, x, y):
        if self.imagen:
            pantalla.blit(self.imagen, (x, y))