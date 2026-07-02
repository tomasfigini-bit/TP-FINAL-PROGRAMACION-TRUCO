import random
from Cartas import Carta
from Tads import PilaMazo

class PartidaTruco:
    def __init__(self):
        self.puntos_j1 = 0
        self.puntos_j2 = 0
        self.mazo = PilaMazo()
        self.mano_j1 = []
        self.mano_j2 = []
        self.inicializar_mazo()

    def inicializar_mazo(self):
        palos = ["espada", "basto", "oro", "copa"]
        numeros = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]
        cartas_temporales = []
        
        for palo in palos:
            for numero in numeros:
                ruta = f"assets/cartas/{numero} de {palo}.jpg"
                nueva_carta = Carta(numero, palo, ruta)
                cartas_temporales.append(nueva_carta)
        
        random.shuffle(cartas_temporales)
        for c in cartas_temporales:
            self.mazo.apilar(c)

    def repartir(self):
        self.mano_j1 = [self.mazo.desapilar() for _ in range(3)]
        self.mano_j2 = [self.mazo.desapilar() for _ in range(3)]
