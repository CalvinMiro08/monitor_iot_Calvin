"""Pruebas del reproductor de alertas sin audio del sistema."""
# LABORATORIO: dependencias para simular salida, tiempo e integracion.
import unittest
from unittest.mock import patch

import config
from alertas.reproductor import Reproductor
import nucleo


# LABORATORIO: el emisor y el reloj simulados mantienen las pruebas deterministas.
class TestReproductor(unittest.TestCase):
    def setUp(self):
        self.ahora = config.DURACION_PASO_SONORO
        self.emitidos = []
        self.reproductor = Reproductor(
            emitir=self.emitidos.append,
            reloj=lambda: self.ahora,
        )

    def test_procesa_un_sonido_por_intervalo_sin_bloquear(self):
        patron = config.SONIDOS_ALERTA["cpu_alta"]
        self.reproductor.notificar("cpu_alta")

        self.assertEqual(self.emitidos, [])
        self.reproductor.procesar()
        self.assertEqual(self.emitidos, [patron[0]])
        self.reproductor.procesar()
        self.assertEqual(self.emitidos, [patron[0]])

        for sonido in patron[1:]:
            self.ahora += config.DURACION_PASO_SONORO
            self.reproductor.procesar()

        self.assertEqual(self.emitidos, list(patron))

    def test_evento_sin_patron_no_emite_sonido(self):
        self.reproductor.notificar("evento_sin_alerta")
        self.reproductor.procesar()
        self.assertEqual(self.emitidos, [])

    def test_reiniciar_descarta_sonidos_pendientes(self):
        self.reproductor.notificar("cpu_alta")
        self.reproductor.reiniciar()
        self.reproductor.procesar()
        self.assertEqual(self.emitidos, [])

    @patch("nucleo.alertas.notificar")
    @patch("nucleo.eventos.atender")
    def test_nucleo_encola_el_sonido_del_evento(
        self, atender, notificar
    ):
        evento = object()
        atender.return_value = evento

        resultado = nucleo._atender("cpu_alta", {})

        self.assertIs(resultado, evento)
        atender.assert_called_once_with("cpu_alta", {})
        notificar.assert_called_once_with("cpu_alta")


# LABORATORIO: permite ejecutar este archivo directamente con unittest.
if __name__ == "__main__":
    unittest.main()