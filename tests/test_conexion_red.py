"""Pruebas del detector de conectividad de red."""
# LABORATORIO: dependencias para las pruebas de conectividad.
import unittest

import config
from eventos.conexion_red import DetectorConexionRed
from eventos import eventos_conocidos


# LABORATORIO: reloj y proveedor simulados para no depender de la red real.
class TestDetectorConexionRed(unittest.TestCase):
    def setUp(self):
        self.ahora = config.PERIODO_ESTADO_RED

    def crear_detector(self, estados):
        secuencia = iter(estados)
        return DetectorConexionRed(
            proveedor=lambda: next(secuencia),
            reloj=lambda: self.ahora,
        )

    def avanzar(self, periodo=config.PERIODO_ESTADO_RED):
        self.ahora += periodo

    def test_emite_eventos_al_perder_y_recuperar_conexion(self):
        detector = self.crear_detector((True, False, True))

        self.assertEqual(detector.revisar(), [])
        self.avanzar()
        self.assertEqual(
            detector.revisar(), [("red_desconectada", {})]
        )
        self.avanzar()
        self.assertEqual(detector.revisar(), [("red_conectada", {})])

    def test_emite_recordatorio_despues_del_intervalo_configurado(self):
        detector = self.crear_detector((False, False))

        self.assertEqual(detector.revisar(), [("red_desconectada", {})])
        self.avanzar(config.RECORDATORIO_RED_DESCONECTADA)
        self.assertEqual(
            detector.revisar(), [("red_sigue_desconectada", {})]
        )

    def test_no_consulta_antes_del_periodo_configurado(self):
        detector = self.crear_detector((True, False))

        self.assertEqual(detector.revisar(), [])
        self.assertEqual(detector.revisar(), [])
        self.avanzar()
        self.assertEqual(
            detector.revisar(), [("red_desconectada", {})]
        )

    def test_eventos_de_conectividad_estan_registrados(self):
        conocidos = eventos_conocidos()
        self.assertIn("red_desconectada", conocidos)
        self.assertIn("red_conectada", conocidos)
        self.assertIn("red_sigue_desconectada", conocidos)


# LABORATORIO: permite ejecutar este archivo directamente con unittest.
if __name__ == "__main__":
    unittest.main()