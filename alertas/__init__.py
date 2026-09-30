"""Paquete para reaccionar sonoramente a eventos del monitor."""
# LABORATORIO: API compartida por el ciclo de monitoreo.
from .reproductor import Reproductor


# LABORATORIO: instancia compartida por el ciclo de monitoreo.
_reproductor = Reproductor()


# LABORATORIO: funciones publicas para encolar, avanzar y limpiar sonidos.
def notificar(evento):
    _reproductor.notificar(evento)


def procesar():
    _reproductor.procesar()


def reiniciar():
    _reproductor.reiniciar()