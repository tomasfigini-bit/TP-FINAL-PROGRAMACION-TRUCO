import pygame

class Carta:
    def __init__(self, numero, palo, ruta_imagen):
        # PRE: numero y palo deben ser válidos.
        # POST: Inicializa la carta y carga su imagen.
        self.numero = numero
        self.palo = palo
        try:
            self.imagen = pygame.image.load(ruta_imagen)
            self.imagen = pygame.transform.scale(self.imagen, (100, 150))
        except:
            self.imagen = None
            print(f"Error: No se encontró la imagen en {ruta_imagen}")

    def obtener_jerarquia(self):
        # POST: Devuelve un valor numérico de poder para el Truco.
        if self.numero == 1 and self.palo == "espada": return 14
        if self.numero == 1 and self.palo == "basto": return 13
        if self.numero == 7 and self.palo == "espada": return 12
        if self.numero == 7 and self.palo == "oro": return 11
        if self.numero == 3: return 10
        if self.numero == 2: return 9
        if self.numero == 1 and self.palo in ["copa", "oro"]: return 8
        if self.numero == 12: return 7
        if self.numero == 11: return 6
        if self.numero == 10: return 5
        if self.numero == 7 and self.palo in ["copa", "basto"]: return 4
        if self.numero == 6: return 3
        if self.numero == 5: return 2
        if self.numero == 4: return 1
        return 0

    # --- MÉTODOS MÁGICOS REQUERIDOS (Parte 2 del TP) ---
    def __str__(self):
        return f"{self.numero} de {self.palo}"

    def __eq__(self, otra_carta):
        if isinstance(otra_carta, Carta):
            return self.obtener_jerarquia() == otra_carta.obtener_jerarquia()
        return False

    def __lt__(self, otra_carta):
        if isinstance(otra_carta, Carta):
            return self.obtener_jerarquia() < otra_carta.obtener_jerarquia()
        return NotImplemented

    def __gt__(self, otra_carta):
        if isinstance(otra_carta, Carta):
            return self.obtener_jerarquia() > otra_carta.obtener_jerarquia()
        return NotImplemented

    def dibujar(self, pantalla, x, y):
        if self.imagen:
            pantalla.blit(self.imagen, (x, y))