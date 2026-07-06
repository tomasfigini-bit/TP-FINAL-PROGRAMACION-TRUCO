import random
from Cartas import Carta
from Tads import PilaMazo, ListaEnlazada

class PartidaTruco:
    def __init__(self):
        # PRE: Ninguna
        # POST: Inicializa la partida, crea el mazo y las manos vacías.
        self.puntos_j1 = 0
        self.puntos_j2 = 0
        self.mazo = PilaMazo()
        self.mano_j1 = ListaEnlazada()
        self.mano_j2 = ListaEnlazada()
        self.inicializar_mazo()

    def inicializar_mazo(self):
        # POST: Llena la pila del mazo con las 40 cartas españolas barajadas.
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
            self.mazo.push(c) # Usamos push en lugar de apilar (Regla del profesor)

    def repartir(self):
        # POST: Reparte 3 cartas de la pila mazo a cada jugador usando ListaEnlazada.
        self.mano_j1 = ListaEnlazada()
        self.mano_j2 = ListaEnlazada()
        
        for _ in range(3):
            carta_j1 = self.mazo.pop() # Usamos pop en lugar de desapilar
            carta_j2 = self.mazo.pop()
            
            if carta_j1:
                self.mano_j1.insertar_al_final(carta_j1)
            if carta_j2:
                self.mano_j2.insertar_al_final(carta_j2)

    def calcular_envido(self, mano):
        # PRE: 'mano' es un objeto ListaEnlazada con 3 cartas.
        # POST: Devuelve un entero con el puntaje de envido de esa mano (0 a 33).
        cartas = []
        for carta in mano:
            cartas.append(carta)
            
        # Agrupamos los valores por palo
        palos = {"espada": [], "basto": [], "oro": [], "copa": []}
        for c in cartas:
            # Para el envido, 10, 11 y 12 valen 0
            valor = 0 if c.numero >= 10 else c.numero
            palos[c.palo].append(valor)
            
        max_envido = 0
        for palo, valores in palos.items():
            if len(valores) == 2:
                # Dos del mismo palo: 20 + la suma de ambos
                envido_actual = 20 + sum(valores)
                if envido_actual > max_envido: max_envido = envido_actual
            elif len(valores) == 3:
                # Tres del mismo palo (flor o envido con la pieza más alta): 20 + los dos mayores
                valores.sort(reverse=True)
                envido_actual = 20 + valores[0] + valores[1]
                if envido_actual > max_envido: max_envido = envido_actual
                
        # Si no tiene cartas del mismo palo, es el valor de la carta más alta
        if max_envido == 0:
            for c in cartas:
                valor = 0 if c.numero >= 10 else c.numero
                if valor > max_envido: max_envido = valor
                
        return max_envido