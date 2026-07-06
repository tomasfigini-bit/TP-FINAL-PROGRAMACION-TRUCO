class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class PilaMazo:
    """
    TAD Pila implementado utilizando internamente el TAD ListaEnlazada.
    """
    def __init__(self):
        # PRE: Ninguna
        # POST: Crea una pila vacía apoyándose en ListaEnlazada.
        self.elementos = ListaEnlazada()

    def push(self, carta):
        # PRE: 'carta' debe ser válida.
        # POST: Apila el elemento en el tope (inicio de la lista).
        self.elementos.insertar_al_inicio(carta)

    def pop(self):
        # PRE: La pila no debe estar vacía.
        # POST: Desapila y devuelve el elemento del tope.
        if self.is_empty():
            return None
        # Tomamos el dato del tope (cabeza) y lo eliminamos
        carta_tope = self.elementos.cabeza.dato
        self.elementos.eliminar(carta_tope)
        return carta_tope

    def peek(self):
        # PRE: La pila no debe estar vacía.
        # POST: Devuelve el elemento del tope sin eliminarlo.
        if self.is_empty():
            return None
        return self.elementos.cabeza.dato

    def is_empty(self):
        # POST: Devuelve True si está vacía, False si tiene elementos.
        return self.elementos.esta_vacia()

    def __str__(self):
        return str(self.elementos)
    
class ListaEnlazada:
    """
    TAD Lista Enlazada
    Invariante de clase:
    - self.cabeza siempre apunta al primer Nodo de la lista, o a None si está vacía.
    - self.tamano siempre es un entero >= 0 que representa la cantidad exacta de nodos.
    """
    def __init__(self):
        # PRE: Ninguna
        # POST: Crea una lista vacía.
        self.cabeza = None
        self.tamano = 0

    def esta_vacia(self):
        # PRE: Ninguna
        # POST: Devuelve True si la lista está vacía, False en caso contrario.
        return self.cabeza is None

    def obtener_longitud(self):
        # PRE: Ninguna
        # POST: Devuelve un entero con la cantidad de elementos en la lista.
        return self.tamano

    def insertar_al_inicio(self, dato):
        # PRE: 'dato' debe ser un elemento válido.
        # POST: El dato se inserta como primer elemento. El tamaño aumenta en 1.
        nuevo_nodo = Nodo(dato)
        nuevo_nodo.siguiente = self.cabeza
        self.cabeza = nuevo_nodo
        self.tamano += 1

    def insertar_al_final(self, dato):
        # PRE: 'dato' debe ser un elemento válido.
        # POST: El dato se inserta como último elemento. El tamaño aumenta en 1.
        nuevo_nodo = Nodo(dato)
        if self.esta_vacia():
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
        self.tamano += 1

    def eliminar(self, dato):
        # PRE: Ninguna.
        # POST: Si el dato existe, elimina su primera aparición y devuelve True. 
        #       Si no existe, devuelve False. El tamaño se actualiza.
        if self.esta_vacia():
            return False
        
        # Caso especial: eliminar el primer elemento
        if self.cabeza.dato == dato:
            self.cabeza = self.cabeza.siguiente
            self.tamano -= 1
            return True
            
        actual = self.cabeza
        while actual.siguiente is not None:
            if actual.siguiente.dato == dato:
                actual.siguiente = actual.siguiente.siguiente
                self.tamano -= 1
                return True
            actual = actual.siguiente
        return False

    def buscar(self, dato):
        # PRE: Ninguna.
        # POST: Devuelve True si el dato está en la lista, False si no está.
        actual = self.cabeza
        while actual is not None:
            if actual.dato == dato:
                return True
            actual = actual.siguiente
        return False

    # --- Métodos Mágicos Obligatorios ---
    def __len__(self):
        return self.tamano

    def __str__(self):
        elementos = []
        actual = self.cabeza
        while actual is not None:
            elementos.append(str(actual.dato))
            actual = actual.siguiente
        return " -> ".join(elementos)

    def __iter__(self):
        # POST: Permite iterar secuencialmente sobre los elementos de la lista.
        # Esto reemplaza el comportamiento de las listas de Python nativas.
        actual = self.cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente