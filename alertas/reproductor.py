"""Reproductor de alertas que nunca espera a que termine un sonido."""
# LABORATORIO: cola, reloj y salida de audio para patrones de alerta.
from collections import deque
import sys
import time

import config

try:
    import winsound
except ImportError:
    winsound = None


# LABORATORIO: deque y reloj inyectable para procesar un solo paso por ciclo.
class Reproductor:
    def __init__(self, emitir=None, reloj=time.monotonic):
        self._cola = deque(maxlen=config.MAX_ALERTAS_PENDIENTES)
        self._reloj = reloj
        self._emitir = emitir or self._emitir_sonido
        self._disponible_desde = self._reloj()

    def notificar(self, evento):
        self._cola.extend(config.SONIDOS_ALERTA.get(evento, ()))

    def procesar(self):
        ahora = self._reloj()
        if ahora < self._disponible_desde or not self._cola:
            return

        sonido = self._cola.popleft()
        self._emitir(sonido)
        self._disponible_desde = ahora + config.DURACION_PASO_SONORO

    def reiniciar(self):
        self._cola.clear()
        self._disponible_desde = self._reloj()

    @staticmethod
    def _emitir_sonido(sonido):
        if winsound is None:
            sys.stdout.write("\a")
            sys.stdout.flush()
            return
        winsound.PlaySound(
            sonido, winsound.SND_ALIAS | winsound.SND_ASYNC
        )