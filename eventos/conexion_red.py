# LABORATORIO: deteccion de conectividad independiente del sensor de trafico.
"""Deteccion de conectividad independiente del sensor de trafico."""
# LABORATORIO: usar estado de interfaces y direcciones locales.
import ipaddress
import socket
import time

import psutil

import config


# LABORATORIO: usa el estado local de interfaces; no realiza conexiones bloqueantes.
def estado_conexion():
    """Devuelve True/False o None si no fue posible consultar las interfaces."""
    try:
        estados = psutil.net_if_stats()
        direcciones = psutil.net_if_addrs()
    except Exception:
        return None

    for nombre, estado in estados.items():
        if not estado.isup:
            continue
        for direccion in direcciones.get(nombre, ()):
            if direccion.family not in (socket.AF_INET, socket.AF_INET6):
                continue
            try:
                ip = ipaddress.ip_address(direccion.address.split("%", 1)[0])
            except ValueError:
                continue
            if not (ip.is_loopback or ip.is_link_local or ip.is_unspecified):
                return True
    return False


# LABORATORIO: genera eventos por flanco y recordatorios con marcas de tiempo.
class DetectorConexionRed:
    def __init__(self, proveedor=estado_conexion, reloj=time.monotonic):
        self._proveedor = proveedor
        self._reloj = reloj
        self.reiniciar()

    def reiniciar(self):
        self._conectada = None
        self._ultima_revision = None
        self._ultima_desconexion = None

    def revisar(self):
        ahora = self._reloj()
        if (
            self._ultima_revision is not None
            and ahora - self._ultima_revision < config.PERIODO_ESTADO_RED
        ):
            return []

        self._ultima_revision = ahora
        conectada = self._proveedor()
        if conectada is None:
            return []

        if self._conectada is None:
            self._conectada = conectada
            if conectada:
                return []
            self._ultima_desconexion = ahora
            return [("red_desconectada", {})]

        if conectada != self._conectada:
            self._conectada = conectada
            if conectada:
                self._ultima_desconexion = None
                return [("red_conectada", {})]
            self._ultima_desconexion = ahora
            return [("red_desconectada", {})]

        if (
            not conectada
            and ahora - self._ultima_desconexion
            >= config.RECORDATORIO_RED_DESCONECTADA
        ):
            self._ultima_desconexion = ahora
            return [("red_sigue_desconectada", {})]
        return []