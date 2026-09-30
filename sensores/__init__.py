"""
Paquete sensores

Cada modulo de este paquete representa UN sensor del nodo y cumple
siempre la misma estructura, de modo que el resto del programa pueda
tratarlos a todos por igual sin saber que miden:

ETIQUETA       -> texto que se muestra en el dashboard
disponible()   -> True si esta metrica existe en este equipo
leer()         -> diccionario con la lectura, o None si fallo

El diccionario que devuelve leer() siempre tiene estas claves:
valor, unidad, porcentaje, detalle, extra.

Agregar una metrica nueva al sistema consiste en escribir un modulo
que cumpla esta estructura y anadirlo al diccionario LECTORES.
"""

from . import cpu, memoria, disco, red, procesos, bateria

# El orden de este diccionario es el orden en que aparecen las tarjetas.
LECTORES = {
    "cpu": cpu,
    "memoria": memoria,
    "disco": disco,
    "red": red,
    "procesos": procesos,
    "bateria": bateria,
}


def disponibles():
    """Devuelve la lista de claves de los sensores presentes en el equipo."""
    return [clave for clave, modulo in LECTORES.items() if modulo.disponible()]


def leer(clave):
    """Lee un sensor por su clave. Devuelve None si no esta disponible."""
    modulo = LECTORES.get(clave)
    if modulo is None or not modulo.disponible():
        return None
    return modulo.leer()


def etiqueta(clave):
    """Nombre legible de un sensor, para mostrarlo en pantalla."""
    modulo = LECTORES.get(clave)
    return modulo.ETIQUETA if modulo else clave