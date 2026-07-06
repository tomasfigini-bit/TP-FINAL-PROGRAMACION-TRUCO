import pygame
import sys
from Juego import PartidaTruco
from Tads import ListaEnlazada
from JuegoBlackjack import PartidaBlackjack

class Boton:
    def __init__(self, x, y, ancho, alto, texto, color_fondo):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.fuente = pygame.font.SysFont("Arial", 18, bold=True)
        self.configurar(texto, color_fondo)

    def configurar(self, nuevo_texto, nuevo_color):
        self.texto = nuevo_texto
        self.color_fondo = nuevo_color
        self.color_hover = tuple(min(255, int(c * 1.25)) for c in nuevo_color)
        self.color_borde = tuple(max(0, int(c * 0.7)) for c in nuevo_color)

    def dibujar(self, pantalla):
        pos_mouse = pygame.mouse.get_pos()
        es_hover = self.rect.collidepoint(pos_mouse)
        color_actual = self.color_hover if es_hover else self.color_fondo
        rect_sombra = self.rect.move(0, 3)
        pygame.draw.rect(pantalla, (18, 70, 18), rect_sombra, border_radius=10)
        pygame.draw.rect(pantalla, color_actual, self.rect, border_radius=10)
        if es_hover:
            pygame.draw.rect(pantalla, (255, 255, 255), self.rect, 2, border_radius=10)
        else:
            pygame.draw.rect(pantalla, self.color_borde, self.rect, 1, border_radius=10)
        
        superficie_texto = self.fuente.render(self.texto, True, (255, 255, 255))
        rect_texto = superficie_texto.get_rect(center=self.rect.center)
        pantalla.blit(superficie_texto, rect_texto)

    def clic(self, pos_mouse):
        return self.rect.collidepoint(pos_mouse)


class GameManager:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.ANCHO = 800
        self.ALTO = 600
        self.FPS = 60
        self.pantalla = pygame.display.set_mode((self.ANCHO, self.ALTO))
        pygame.display.set_caption("TP Final - Sistema Multi-Juegos")
        self.reloj = pygame.time.Clock()

        # --- SISTEMA DE ESTADOS ---
        self.estado = "MENU" # "MENU", "TRUCO", "BLACKJACK"

        # --- BOTONES DEL MENÚ ---
        self.btn_menu_truco = Boton(250, 250, 300, 60, "JUGAR TRUCO", (41, 128, 185))
        self.btn_menu_bj = Boton(250, 340, 300, 60, "JUGAR BLACKJACK", (39, 174, 96))
        self.btn_volver = Boton(20, 540, 150, 40, "Volver al Menú", (100, 50, 50))

        # --- VARIABLES DEL TRUCO ---
        self.juego = PartidaTruco()
        self.juego.repartir()
        self.cartas_mesa_j1 = ListaEnlazada()
        self.cartas_mesa_j2 = ListaEnlazada()
        self.manos_ganadas_j1 = 0
        self.manos_ganadas_j2 = 0
        self.historial_manos = ListaEnlazada()
        self.esperando_nueva_ronda = False
        self.quien_es_mano = "J1"      
        self.turno_actual = "J1"       
        self.lider_mano_actual = "J1"  
        self.valor_truco_actual = 1  
        self.estado_truco = "nada"   
        self.envido_jugado = False   
        self.bot_canto = None          
        
        self.log_mensajes = ListaEnlazada()
        self.agregar_log("Bienvenido al Truco Argentino")

        try:
            self.sonido_carta = pygame.mixer.Sound("assets/cartas/sonido_carta.wav")
            self.sonido_carta.set_volume(0.6)
        except:
            self.sonido_carta = None

        try:
            self.img_reverso = pygame.image.load("assets/cartas/reverso_2.jpg")
            self.img_reverso = pygame.transform.scale(self.img_reverso, (100, 150))
        except:
            self.img_reverso = None

        try:
            # Buscamos el archivo con su nombre real completo '.png.jpg'
            self.reverso_bj = pygame.image.load("assets/cartas_bj/reverso_bj.png").convert_alpha()
            self.reverso_bj = pygame.transform.scale(self.reverso_bj, (80, 115)) 
        except:
            self.reverso_bj = None

        try:
            # Cargamos el back.png para usarlo de base en las cartas transparentes
            self.fondo_carta_bj = pygame.image.load("assets/cartas_bj/back.png").convert_alpha()
            self.fondo_carta_bj = pygame.transform.scale(self.fondo_carta_bj, (80, 115))
        except:
            self.fondo_carta_bj = None

        self.btn_envido = Boton(650, 400, 130, 42, "Envido", (41, 128, 185))
        self.btn_truco = Boton(650, 455, 130, 42, "Truco", (192, 57, 43))
        self.btn_mazo = Boton(650, 510, 130, 42, "Ir al Mazo", (127, 130, 131))

        # --- VARIABLES DEL BLACKJACK ---
        self.bj_juego = PartidaBlackjack()
        self.bj_estado_ronda = "FASE_APUESTAS" # Ahora empezamos apostando
        self.bj_mensaje_final = ""
        
        # Sistema de Billetera
        self.bj_saldo = 1000
        self.bj_apuesta_actual = 0
        
        # Botones de Juego
        self.btn_bj_pedir = Boton(250, 500, 140, 45, "Pedir Carta", (41, 128, 185))
        self.btn_bj_plantarse = Boton(410, 500, 140, 45, "Plantarse", (192, 57, 43))
        self.btn_bj_nueva = Boton(330, 500, 140, 45, "Nueva Ronda", (39, 174, 96))
        
        # Botones de Apuesta (Fichas)
        self.btn_bj_ficha_10 = Boton(200, 320, 100, 45, "+ $10", (52, 152, 219))
        self.btn_bj_ficha_50 = Boton(350, 320, 100, 45, "+ $50", (155, 89, 182))
        self.btn_bj_ficha_100 = Boton(500, 320, 100, 45, "+ $100", (241, 196, 15))
        self.btn_bj_limpiar = Boton(270, 390, 120, 40, "Limpiar", (149, 165, 166))
        self.btn_bj_repartir = Boton(410, 390, 120, 40, "¡Repartir!", (46, 204, 113))

    def agregar_log(self, texto):
        self.log_mensajes.insertar_al_final(texto)
        if len(self.log_mensajes) > 5:
            primer_nodo = None
            for m in self.log_mensajes:
                primer_nodo = m
                break
            self.log_mensajes.eliminar(primer_nodo)

    def verificar_ganador_mano(self):
        carta_j1 = None
        for c in self.cartas_mesa_j1: carta_j1 = c
        carta_j2 = None
        for c in self.cartas_mesa_j2: carta_j2 = c

        if carta_j1 and carta_j2:
            if carta_j1 > carta_j2:
                self.manos_ganadas_j1 += 1
                self.historial_manos.insertar_al_final("J1")
                self.turno_actual = "J1"  
                self.agregar_log(f"Ganaste con {carta_j1}")
            elif carta_j1 < carta_j2:
                self.manos_ganadas_j2 += 1
                self.historial_manos.insertar_al_final("J2")
                self.turno_actual = "J2"  
                self.agregar_log(f"Rival ganó con {carta_j2}")
            else:
                self.manos_ganadas_j1 += 1
                self.manos_ganadas_j2 += 1
                self.historial_manos.insertar_al_final("Empate")
                self.turno_actual = self.lider_mano_actual
                self.agregar_log("Empate en la mesa")

        ronda_terminada = False
        ganador_ronda = None

        if self.manos_ganadas_j1 == 2 and self.manos_ganadas_j2 < 2:
            ganador_ronda = "J1"
            ronda_terminada = True
        elif self.manos_ganadas_j2 == 2 and self.manos_ganadas_j1 < 2:
            ganador_ronda = "J2"
            ronda_terminada = True
        elif len(self.cartas_mesa_j1) == 3:
            ronda_terminada = True
            primera, segunda, tercera = None, None, None
            for i, resultado in enumerate(self.historial_manos):
                if i == 0: primera = resultado
                elif i == 1: segunda = resultado
                elif i == 2: tercera = resultado
            if self.manos_ganadas_j1 > self.manos_ganadas_j2: ganador_ronda = "J1"
            elif self.manos_ganadas_j2 > self.manos_ganadas_j1: ganador_ronda = "J2"
            else:
                if primera == "J1": ganador_ronda = "J1"
                elif primera == "J2": ganador_ronda = "J2"
                elif segunda == "J1": ganador_ronda = "J1"
                elif segunda == "J2": ganador_ronda = "J2"
                else: ganador_ronda = "Empate"

        if ronda_terminada:
            if ganador_ronda == "J1":
                self.juego.puntos_j1 += self.valor_truco_actual
                self.agregar_log(f"¡GANASTE VOS! (+{self.valor_truco_actual})")
            elif ganador_ronda == "J2":
                self.juego.puntos_j2 += self.valor_truco_actual
                self.agregar_log(f"GANO EL RIVAL (+{self.valor_truco_actual})")
            else:
                self.juego.puntos_j1 += 1
                self.juego.puntos_j2 += 1
                self.agregar_log("Ronda empatada")
            self.esperando_nueva_ronda = True
        else:
            self.lider_mano_actual = self.turno_actual

    def revisar_cantos_bot(self):
        if self.bot_canto is not None: return
        envido_bot = self.juego.calcular_envido(self.juego.mano_j2)
        poder_bot = 0
        for c in self.juego.mano_j2: poder_bot += c.obtener_jerarquia()
        if len(self.cartas_mesa_j2) == 0 and len(self.cartas_mesa_j1) <= 1 and not self.envido_jugado and self.estado_truco == "nada":
            if envido_bot >= 26:
                self.agregar_log("Rival canta: ¡ENVIDO!")
                self.bot_canto = "envido"
                self.btn_envido.configurar("Quiero", (39, 174, 96))
                self.btn_truco.configurar("No Quiero", (211, 84, 0))
                return
        if self.estado_truco == "nada" and poder_bot >= 18:
            self.agregar_log("Rival canta: ¡TRUCO!")
            self.bot_canto = "truco"
            self.btn_envido.configurar("Quiero", (39, 174, 96))
            self.btn_truco.configurar("No Quiero", (211, 84, 0))
            return

    def procesar_respuesta_jugador_envido(self, quiso):
        envido_bot = self.juego.calcular_envido(self.juego.mano_j2)
        envido_jugador = self.juego.calcular_envido(self.juego.mano_j1)
        if quiso:
            self.agregar_log("Vos: ¡Quiero el Envido!")
            self.agregar_log(f"Rival tiene {envido_bot}")
            self.agregar_log(f"Vos tenés {envido_jugador}")
            if envido_jugador >= envido_bot:
                self.agregar_log("Ganaste el Envido (+2)")
                self.juego.puntos_j1 += 2
            else:
                self.agregar_log("Rival gana el Envido (+2)")
                self.juego.puntos_j2 += 2
        else:
            self.agregar_log("Vos: No quiero Envido.")
            self.juego.puntos_j2 += 1
        self.envido_jugado = True
        self.bot_canto = None
        self.btn_envido.configurar("Envido", (41, 128, 185))
        self.btn_truco.configurar("Truco", (192, 57, 43))

    def procesar_respuesta_jugador_truco(self, quiso):
        if quiso:
            self.agregar_log("Vos: ¡Quiero el Truco!")
            self.valor_truco_actual = 2
            self.estado_truco = "truco"
            self.bot_canto = None
            self.btn_envido.configurar("Envido", (41, 128, 185))
            self.btn_truco.configurar("Retruco", (192, 57, 43))
        else:
            self.agregar_log("Vos: No quiero Truco.")
            self.juego.puntos_j2 += 1
            self.bot_canto = None
            self.btn_envido.configurar("Envido", (41, 128, 185))
            self.btn_truco.configurar("Truco", (192, 57, 43))
            self.esperando_nueva_ronda = True

    def procesar_canto_envido(self):
        if len(self.cartas_mesa_j1) > 0 or self.envido_jugado or self.estado_truco != "nada":
            self.agregar_log("Ya no podes cantar el envido.")
            return
        envido_bot = self.juego.calcular_envido(self.juego.mano_j2)
        envido_jugador = self.juego.calcular_envido(self.juego.mano_j1)
        if self.btn_envido.texto == "Envido":
            self.agregar_log("Vos cantás: ¡ENVIDO!")
            if envido_bot >= 22:
                self.agregar_log(f"Rival: ¡Quiero! ({envido_bot})")
                if envido_jugador >= envido_bot:
                    self.agregar_log("Ganaste el Envido (+2)")
                    self.juego.puntos_j1 += 2
                else:
                    self.agregar_log("Rival gana el Envido (+2)")
                    self.juego.puntos_j2 += 2
                self.envido_jugado = True
            else:
                if envido_bot >= 28:
                    self.agregar_log("Rival canta: REAL ENVIDO")
                    self.btn_envido.configurar("Real Envido", (41, 128, 185))
                else:
                    self.agregar_log("Rival: No quiero Envido.")
                    self.juego.puntos_j1 += 1
                    self.envido_jugado = True
            if not self.envido_jugado and self.btn_envido.texto == "Envido":
                self.btn_envido.configurar("Real Envido", (41, 128, 185))
        elif self.btn_envido.texto == "Real Envido":
            self.agregar_log("Vos cantás: REAL ENVIDO")
            if envido_bot >= 25:
                self.agregar_log(f"Rival: ¡Quiero! ({envido_bot})")
                if envido_jugador >= envido_bot:
                    self.agregar_log("Ganaste Real Envido (+3)")
                    self.juego.puntos_j1 += 3
                else:
                    self.agregar_log("Rival gana Real Envido (+3)")
                    self.juego.puntos_j2 += 3
            else:
                self.agregar_log("Rival: No quiero.")
                self.juego.puntos_j1 += 1
            self.envido_jugado = True
            self.btn_envido.configurar("Falta Envido", (41, 128, 185))
        elif self.btn_envido.texto == "Falta Envido":
            self.agregar_log("Vos cantás: FALTA ENVIDO")
            if envido_bot >= 29:
                self.agregar_log("Rival: ¡Quiero!")
                puntos_faltantes = 30 - max(self.juego.puntos_j1, self.juego.puntos_j2)
                if puntos_faltantes <= 0: puntos_faltantes = 15
                if envido_jugador >= envido_bot:
                    self.agregar_log(f"¡Ganaste la Falta! (+{puntos_faltantes})")
                    self.juego.puntos_j1 += puntos_faltantes
                else:
                    self.agregar_log(f"¡Rival gana la Falta! (+{puntos_faltantes})")
                    self.juego.puntos_j2 += puntos_faltantes
            else:
                self.agregar_log("Rival: No quiero.")
                self.juego.puntos_j1 += 1
            self.envido_jugado = True

    def procesar_canto_truco(self):
        poder_bot = 0
        for c in self.juego.mano_j2: poder_bot += c.obtener_jerarquia()
        if self.estado_truco == "nada":
            self.agregar_log("Vos cantás: ¡TRUCO!")
            if poder_bot >= 12:
                self.agregar_log("Rival dice: ¡Quiero!")
                self.valor_truco_actual = 2
                self.estado_truco = "truco"
                self.btn_truco.configurar("Retruco", (192, 57, 43))
            else:
                self.agregar_log("Rival dice: No quiero.")
                self.juego.puntos_j1 += 1  
                self.esperando_nueva_ronda = True
        elif self.estado_truco == "truco":
            self.agregar_log("Vos cantás: ¡RETRUCO!")
            if poder_bot >= 18:
                self.agregar_log("Rival dice: ¡Quiero!")
                self.valor_truco_actual = 3
                self.estado_truco = "retruco"
                self.btn_truco.configurar("Vale 4", (192, 57, 43))
            else:
                self.agregar_log("Rival dice: No quiero.")
                self.juego.puntos_j1 += 2  
                self.esperando_nueva_ronda = True
        elif self.estado_truco == "retruco":
            self.agregar_log("Vos cantás: ¡VALE 4!")
            if poder_bot >= 25:
                self.agregar_log("Rival dice: ¡Quiero!")
                self.valor_truco_actual = 4
                self.estado_truco = "vale4"
            else:
                self.agregar_log("Rival dice: No quiero.")
                self.juego.puntos_j1 += 3  
                self.esperando_nueva_ronda = True

    def procesar_irse_al_mazo(self):
        puntos_entregados = self.valor_truco_actual if self.estado_truco != "nada" else 1
        self.agregar_log(f"Te fuiste al mazo. Rival +{puntos_entregados}")
        self.juego.puntos_j2 += puntos_entregados
        self.esperando_nueva_ronda = True

    # --- FUNCIONES DE DIBUJO ---

    def dibujar_carta_bj(self, pantalla, carta, x, y, oculta=False):
        if oculta:
            # Si la carta está dada vuelta, usa el reverso rojo original
            if self.reverso_bj:
                pantalla.blit(self.reverso_bj, (x, y))
            else:
                pygame.draw.rect(pantalla, (150, 0, 0), (x, y, 80, 115), border_radius=8)
                pygame.draw.rect(pantalla, (255, 255, 255), (x, y, 80, 115), 2, border_radius=8)
        else:
            # 1. PRIMERO DIBUJAMOS EL FONDO (Evita que la carta se vea transparente)
            if self.fondo_carta_bj:
                pantalla.blit(self.fondo_carta_bj, (x, y))
            else:
                pygame.draw.rect(pantalla, (255, 255, 255), (x, y, 80, 115), border_radius=8)

            # 2. SEGUNDO ESTAMPAMOS EL CASILLERO DE LA CARTA EN CUESTIÓN
            nombre_archivo = f"assets/cartas_bj/{carta.valor}_of_{carta.palo}.png"
            try:
                img_carta = pygame.image.load(nombre_archivo).convert_alpha()
                img_carta = pygame.transform.scale(img_carta, (80, 115))
                pantalla.blit(img_carta, (x, y))
            except:
                # Plan de emergencia con texto si falta el archivo numérico
                pygame.draw.rect(pantalla, (0, 0, 0), (x, y, 80, 115), 1, border_radius=8)
                color_texto = (200, 0, 0) if carta.palo in ["hearts", "diamonds"] else (20, 20, 20)
                fuente_val = pygame.font.SysFont("Arial", 22, bold=True)
                texto_str = str(carta.valor).upper()[0] if carta.valor != "10" else "10"
                surf_val = fuente_val.render(texto_str, True, color_texto)
                pantalla.blit(surf_val, (x + 8, y + 8))

    def dibujar_menu_principal(self):
        self.pantalla.fill((25, 25, 30))
        fuente_titulo = pygame.font.SysFont("Arial", 48, bold=True)
        texto_titulo = fuente_titulo.render("TRUCO Y BLACKJACK", True, (255, 255, 255))
        rect_titulo = texto_titulo.get_rect(center=(self.ANCHO//2, 120))
        self.pantalla.blit(texto_titulo, rect_titulo)

        self.btn_menu_truco.dibujar(self.pantalla)
        self.btn_menu_bj.dibujar(self.pantalla)

    def iniciar_partida(self):
        corriendo = True
        fuente_pts = pygame.font.SysFont("Arial", 26, bold=True)
        fuente_log = pygame.font.SysFont("Arial", 16, bold=True)

        while corriendo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT: 
                    corriendo = False
                
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    pos_mouse = pygame.mouse.get_pos()
                    
                    # --- CONTROLES DEL MENÚ ---
                    if self.estado == "MENU":
                        if self.btn_menu_truco.clic(pos_mouse):
                            self.estado = "TRUCO"
                        elif self.btn_menu_bj.clic(pos_mouse):
                            self.estado = "BLACKJACK"

                    # --- CONTROLES DEL TRUCO ---
                    elif self.estado == "TRUCO" and not self.esperando_nueva_ronda:
                        if self.btn_volver.clic(pos_mouse):
                            self.estado = "MENU"
                        elif self.btn_envido.clic(pos_mouse):
                            if self.bot_canto == "envido": self.procesar_respuesta_jugador_envido(True)
                            elif self.bot_canto == "truco": self.procesar_respuesta_jugador_truco(True)
                            else: self.procesar_canto_envido()
                        elif self.btn_truco.clic(pos_mouse):
                            if self.bot_canto == "envido": self.procesar_respuesta_jugador_envido(False)
                            elif self.bot_canto == "truco": self.procesar_respuesta_jugador_truco(False)
                            else: self.procesar_canto_truco()
                        elif self.btn_mazo.clic(pos_mouse): 
                            self.procesar_irse_al_mazo()
                        elif self.turno_actual == "J1" and self.bot_canto is None:
                            x_inicial = 300
                            for i, carta in enumerate(self.juego.mano_j1):
                                rect_carta = pygame.Rect(x_inicial + (i * 110), 450, 100, 150)
                                if rect_carta.collidepoint(pos_mouse):
                                    if self.sonido_carta: self.sonido_carta.play()
                                    self.cartas_mesa_j1.insertar_al_final(carta)
                                    self.juego.mano_j1.eliminar(carta)
                                    if len(self.cartas_mesa_j2) < len(self.cartas_mesa_j1): self.turno_actual = "J2"
                                    else: self.verificar_ganador_mano()
                                    break

                    # --- CONTROLES DEL BLACKJACK ---
                    elif self.estado == "BLACKJACK":
                        if self.btn_volver.clic(pos_mouse):
                            self.estado = "MENU"
                            
                        elif self.bj_estado_ronda == "FASE_APUESTAS":
                            if self.btn_bj_ficha_10.clic(pos_mouse) and self.bj_saldo >= 10:
                                self.bj_saldo -= 10
                                self.bj_apuesta_actual += 10
                            elif self.btn_bj_ficha_50.clic(pos_mouse) and self.bj_saldo >= 50:
                                self.bj_saldo -= 50
                                self.bj_apuesta_actual += 50
                            elif self.btn_bj_ficha_100.clic(pos_mouse) and self.bj_saldo >= 100:
                                self.bj_saldo -= 100
                                self.bj_apuesta_actual += 100
                            elif self.btn_bj_limpiar.clic(pos_mouse):
                                self.bj_saldo += self.bj_apuesta_actual # Devolvemos la plata a la billetera
                                self.bj_apuesta_actual = 0
                            elif self.btn_bj_repartir.clic(pos_mouse) and self.bj_apuesta_actual > 0:
                                self.bj_juego.reiniciar_ronda() # Recién acá repartimos las cartas
                                self.bj_estado_ronda = "TURNO_JUGADOR"
                                
                        elif self.bj_estado_ronda == "TURNO_JUGADOR":
                            if self.btn_bj_pedir.clic(pos_mouse):
                                self.bj_juego.pedir_carta(self.bj_juego.mano_jugador)
                                if self.bj_juego.calcular_puntaje(self.bj_juego.mano_jugador) > 21:
                                    self.bj_estado_ronda = "FIN_RONDA"
                                    self.bj_mensaje_final = "¡Te pasaste! Gana el Crupier."
                                    # La plata ya se descontó, así que simplemente la pierde
                            elif self.btn_bj_plantarse.clic(pos_mouse):
                                self.bj_estado_ronda = "TURNO_CRUPIER"
                                
                        elif self.bj_estado_ronda == "FIN_RONDA":
                            if self.btn_bj_nueva.clic(pos_mouse):
                                self.bj_estado_ronda = "FASE_APUESTAS" # Volvemos a apostar
                                self.bj_apuesta_actual = 0
                                self.bj_mensaje_final = ""

            # --- LÓGICA DEL BOT (TRUCO) ---
            if self.estado == "TRUCO":
                if self.turno_actual == "J2" and not self.esperando_nueva_ronda and self.bot_canto is None:
                    self.revisar_cantos_bot()
                if self.turno_actual == "J2" and not self.esperando_nueva_ronda and self.bot_canto is None:
                    carta_bot = None
                    for c in self.juego.mano_j2:
                        carta_bot = c
                        break
                    if carta_bot:
                        if self.sonido_carta: self.sonido_carta.play()
                        self.cartas_mesa_j2.insertar_al_final(carta_bot)
                        self.juego.mano_j2.eliminar(carta_bot)
                        if len(self.cartas_mesa_j1) < len(self.cartas_mesa_j2): self.turno_actual = "J1"
                        else: self.verificar_ganador_mano()

            # --- LÓGICA DEL CRUPIER (BLACKJACK) ---
            if self.estado == "BLACKJACK" and self.bj_estado_ronda == "TURNO_CRUPIER":
                puntos_crupier = self.bj_juego.calcular_puntaje(self.bj_juego.mano_crupier)
                if puntos_crupier < 17:
                    pygame.time.wait(800)
                    self.bj_juego.pedir_carta(self.bj_juego.mano_crupier)
                else:
                    puntos_jugador = self.bj_juego.calcular_puntaje(self.bj_juego.mano_jugador)
                    if puntos_crupier > 21:
                        self.bj_mensaje_final = "El Crupier se pasó. ¡GANASTE!"
                        self.bj_saldo += self.bj_apuesta_actual * 2
                    elif puntos_jugador > puntos_crupier:
                        self.bj_mensaje_final = "¡GANASTE!"
                        self.bj_saldo += self.bj_apuesta_actual * 2
                    elif puntos_crupier > puntos_jugador:
                        self.bj_mensaje_final = "Gana el Crupier."
                    else:
                        self.bj_mensaje_final = "Empate."
                        self.bj_saldo += self.bj_apuesta_actual # Te devuelve la apuesta
                    self.bj_estado_ronda = "FIN_RONDA"

            # --- RENDERIZADO SEGÚN EL ESTADO ACTUAL ---
            if self.estado == "MENU":
                self.dibujar_menu_principal()

            elif self.estado == "TRUCO":
                self.pantalla.fill((34, 139, 34))
                
                # --- Marcador Truco (Restaurado recuadro premium) ---
                texto_pts = f"TU: {self.juego.puntos_j1}   |   RIVAL: {self.juego.puntos_j2}"
                surf_pts = fuente_pts.render(texto_pts, True, (255, 255, 255))
                fondo_pts = pygame.Surface((surf_pts.get_width() + 40, 50), pygame.SRCALPHA)
                pygame.draw.rect(fondo_pts, (0, 0, 0, 180), fondo_pts.get_rect(), border_radius=15)
                self.pantalla.blit(fondo_pts, (15, 15))
                self.pantalla.blit(surf_pts, (35, 23))

                # --- Bitácora Clásica Original (Ajustada para no pisar cartas) ---
                ancho_chat = 220 # Ahora mide 220 para que no choque con la carta en X=250
                alto_chat = 130
                pygame.draw.rect(self.pantalla, (18, 70, 18), (15, 80, ancho_chat, alto_chat))
                pygame.draw.rect(self.pantalla, (255, 255, 255), (15, 80, ancho_chat, alto_chat), 2)
                
                for idx, mensaje in enumerate(self.log_mensajes):
                    surf_msg = fuente_log.render(mensaje, True, (255, 255, 255))
                    self.pantalla.blit(surf_msg, (25, 90 + (idx * 22)))

                # Dibujar Cartas Truco
                x_inicial = 300
                for i, carta in enumerate(self.juego.mano_j1):
                    carta.dibujar(self.pantalla, x_inicial + (i * 110), 450)
                for i, carta in enumerate(self.juego.mano_j2):
                    x_c = x_inicial + (i * 110)
                    if self.img_reverso: self.pantalla.blit(self.img_reverso, (x_c, 0))
                    else: pygame.draw.rect(self.pantalla, (255, 255, 255), (x_c, 0, 100, 150), border_radius=6)
                
                x_mesa = 250
                for i, carta in enumerate(self.cartas_mesa_j2): carta.dibujar(self.pantalla, x_mesa + (i * 145), 145)
                for i, carta in enumerate(self.cartas_mesa_j1): carta.dibujar(self.pantalla, x_mesa + (i * 145), 300)

                # Botones Truco
                self.btn_envido.dibujar(self.pantalla)
                self.btn_truco.dibujar(self.pantalla)
                self.btn_mazo.dibujar(self.pantalla)
                self.btn_volver.dibujar(self.pantalla)

                # Reinicio de ronda
                if self.esperando_nueva_ronda:
                    pygame.display.flip()
                    pygame.time.wait(2500)
                    p1, p2 = self.juego.puntos_j1, self.juego.puntos_j2
                    self.juego = PartidaTruco()
                    self.juego.puntos_j1, self.juego.puntos_j2 = p1, p2
                    self.cartas_mesa_j1, self.cartas_mesa_j2 = ListaEnlazada(), ListaEnlazada()
                    self.manos_ganadas_j1, self.manos_ganadas_j2, self.historial_manos = 0, 0, ListaEnlazada()
                    self.valor_truco_actual, self.estado_truco, self.envido_jugado, self.bot_canto = 1, "nada", False, None
                    self.btn_envido.configurar("Envido", (41, 128, 185))
                    self.btn_truco.configurar("Truco", (192, 57, 43))
                    self.quien_es_mano = "J2" if self.quien_es_mano == "J1" else "J1"
                    self.turno_actual = self.quien_es_mano
                    self.lider_mano_actual = self.quien_es_mano
                    self.agregar_log("NUEVA RONDA")
                    self.juego.repartir()
                    self.esperando_nueva_ronda = False

            elif self.estado == "BLACKJACK":
                self.pantalla.fill((20, 80, 20)) 
                fuente_bj = pygame.font.SysFont("Arial", 28, bold=True)
                
                # Billetera y Apuesta actual (siempre visibles)
                surf_saldo = fuente_bj.render(f"Saldo: ${self.bj_saldo}", True, (241, 196, 15))
                surf_apuesta = fuente_bj.render(f"En Mesa: ${self.bj_apuesta_actual}", True, (255, 255, 255))
                self.pantalla.blit(surf_saldo, (20, 20))
                self.pantalla.blit(surf_apuesta, (20, 60))

                if self.bj_estado_ronda == "FASE_APUESTAS":
                    surf_titulo = fuente_bj.render("Hacé tu apuesta", True, (255, 255, 255))
                    self.pantalla.blit(surf_titulo, (300, 250))
                    
                    self.btn_bj_ficha_10.dibujar(self.pantalla)
                    self.btn_bj_ficha_50.dibujar(self.pantalla)
                    self.btn_bj_ficha_100.dibujar(self.pantalla)
                    self.btn_bj_limpiar.dibujar(self.pantalla)
                    self.btn_bj_repartir.dibujar(self.pantalla)
                
                else:
                    # Textos de puntaje
                    puntos_jugador = self.bj_juego.calcular_puntaje(self.bj_juego.mano_jugador)
                    surf_pj = fuente_bj.render(f"Tus Puntos: {puntos_jugador}", True, (255, 255, 255))
                    self.pantalla.blit(surf_pj, (320, 440))
                    
                    if self.bj_estado_ronda == "TURNO_JUGADOR":
                        puntos_visibles_c = self.bj_juego.mano_crupier[0].obtener_puntos() if self.bj_juego.mano_crupier[0].valor != "A" else 11
                        surf_pc = fuente_bj.render(f"Crupier: {puntos_visibles_c} + ?", True, (255, 255, 255))
                    else:
                        puntos_crupier = self.bj_juego.calcular_puntaje(self.bj_juego.mano_crupier)
                        surf_pc = fuente_bj.render(f"Crupier: {puntos_crupier}", True, (255, 255, 255))
                    self.pantalla.blit(surf_pc, (320, 40))
                    
                    # Dibujar Cartas
                    x_crupier = 400 - (len(self.bj_juego.mano_crupier) * 45) 
                    for i, carta in enumerate(self.bj_juego.mano_crupier):
                        oculta = (i == 1 and self.bj_estado_ronda == "TURNO_JUGADOR")
                        self.dibujar_carta_bj(self.pantalla, carta, x_crupier + (i * 90), 90, oculta)
                        
                    x_jugador = 400 - (len(self.bj_juego.mano_jugador) * 45)
                    for i, carta in enumerate(self.bj_juego.mano_jugador):
                        self.dibujar_carta_bj(self.pantalla, carta, x_jugador + (i * 90), 300)

                    # Botones de juego
                    if self.bj_estado_ronda == "FIN_RONDA":
                        surf_msg = fuente_bj.render(self.bj_mensaje_final, True, (255, 215, 0))
                        rect_msg = surf_msg.get_rect(center=(400, 250))
                        # Le ponemos un fondito negro al mensaje para que se lea mejor sobre las cartas
                        pygame.draw.rect(self.pantalla, (0, 0, 0), rect_msg.inflate(20, 10))
                        self.pantalla.blit(surf_msg, rect_msg)
                        self.btn_bj_nueva.dibujar(self.pantalla)
                    else:
                        self.btn_bj_pedir.dibujar(self.pantalla)
                        self.btn_bj_plantarse.dibujar(self.pantalla)
                        
                self.btn_volver.dibujar(self.pantalla)

            pygame.display.flip()
            self.reloj.tick(self.FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    manager = GameManager()
    manager.iniciar_partida()