import random
import pygame  # Importamos pygame para poder cargar y dibujar las imágenes

class CartaBJ:
    def __init__(self, palo, valor):
        self.palo = palo
        self.valor = valor # "2", "3", ..., "jack", "queen", "king", "ace"

        # Cargar la imagen frontal directo usando el valor y el palo (Ruta limpia como en el Truco)
        try:
            self.imagen = pygame.image.load(f"assets/cartas_bj/{self.valor}_of_{self.palo}.png").convert_alpha()
            # Si necesitás achicar o agrandar las cartas descomentá la línea de abajo:
            # self.imagen = pygame.transform.scale(self.imagen, (100, 150))
        except:
            self.imagen = None # Plan B por si el archivo no existe

        # Cargar el reverso directo
        try:
            self.img_reverso = pygame.image.load("assets/cartas_bj/reverso_bj.png").convert_alpha()
            # self.img_reverso = pygame.transform.scale(self.img_reverso, (100, 150))
        except:
            self.img_reverso = None

    def obtener_puntos(self):
        # Adaptado para que reconozca los nombres de tus archivos en inglés
        if self.valor in ["jack", "queen", "king"]:
            return 10
        elif self.valor == "ace":
            return 11 
        else:
            return int(self.valor)

    def dibujar(self, pantalla, x, y, oculta=False):
        """ 
        Método igual al del Truco para dibujar la carta en la pantalla.
        Si 'oculta' es True, dibuja la parte de atrás (reverso).
        """
        if oculta:
            if self.img_reverso:
                pantalla.blit(self.img_reverso, (x, y))
            else:
                # Rectángulo rojo de emergencia si no encuentra el reverso
                pygame.draw.rect(pantalla, (150, 0, 0), (x, y, 100, 150), border_radius=6)
        else:
            if self.imagen:
                pantalla.blit(self.imagen, (x, y))
            else:
                # Rectángulo blanco de emergencia si no encuentra la imagen de la carta
                pygame.draw.rect(pantalla, (255, 255, 255), (x, y, 100, 150), border_radius=6)
                fuente = pygame.font.SysFont("Arial", 24, bold=True)
                texto = fuente.render(self.valor.upper()[0], True, (0, 0, 0))
                pantalla.blit(texto, (x + 10, y + 10))

    def __str__(self):
        return f"{self.valor} de {self.palo}"


class PartidaBlackjack:
    def __init__(self):
        # Cambiamos los nombres para que coincidan EXACTAMENTE con tus archivos de la carpeta cartas_bj
        self.palos = ["clubs", "diamonds", "hearts", "spades"]
        self.valores = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace"]
        self.mazo = []
        self.mano_jugador = []
        self.mano_crupier = []
        self.reiniciar_ronda()

    def crear_mazo_y_mezclar(self):
        # Crea las cartas pasando el palo primero y el valor después según tu init original
        self.mazo = [CartaBJ(p, v) for p in self.palos for v in self.valores]
        random.shuffle(self.mazo)

    def reiniciar_ronda(self):
        self.crear_mazo_y_mezclar()
        self.mano_jugador = []
        self.mano_crupier = []
        
        # Repartimos 2 cartas a cada uno
        self.pedir_carta(self.mano_jugador)
        self.pedir_carta(self.mano_jugador)
        self.pedir_carta(self.mano_crupier)
        self.pedir_carta(self.mano_crupier)

    def pedir_carta(self, mano):
        if self.mazo:
            mano.append(self.mazo.pop())

    def calcular_puntaje(self, mano):
        puntos = 0
        ases = 0
        
        for carta in mano:
            puntos += carta.obtener_puntos()
            if carta.valor == "ace":
                ases += 1
                
        # Si nos pasamos de 21 y tenemos Ases, los hacemos valer 1 en vez de 11
        while puntos > 21 and ases > 0:
            puntos -= 10
            ases -= 1
            
        return puntos