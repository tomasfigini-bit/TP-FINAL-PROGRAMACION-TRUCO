class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class PilaMazo:
    def __init__(self):
        self.tope = None
        self.tamaño = 0

    def apilar(self, carta):
        nuevo_nodo = Nodo(carta)
        nuevo_nodo.siguiente = self.tope
        self.tope = nuevo_nodo
        self.tamaño += 1

    def desapilar(self):
        if self.esta_vacia():
            return None
        carta = self.tope.dato
        self.tope = self.tope.siguiente
        self.tamaño -= 1
        return carta

    def esta_vacia(self):
        return self.tope is None