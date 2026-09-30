"""
dashboard/consola.py
Interfaz grafica de texto (fallback).

Si el sistema corre en un servidor sin pantalla grafica o falla
tkinter, esta vista permite monitorear el nodo desde la terminal.
Usa codigos ANSI para limpiar pantalla y colorear los eventos.
"""
import os
import sys
import time
import nucleo
import config

# Codigos de escape ANSI para colores en la terminal
COLORES = {
    "INFO": "\033[32m",    # Verde
    "AVISO": "\033[33m",   # Amarillo
    "ALERTA": "\033[31m",  # Rojo
    "FALLA": "\033[35m",   # Magenta
    "RESET": "\033[0m",
}

def limpiar_pantalla():
    """Limpia la terminal segun el sistema operativo."""
    os.system("cls" if os.name == "nt" else "clear")

def ejecutar():
    """Bucle principal de la consola."""
    print("Iniciando monitor IoT en modo consola...")
    nucleo.iniciar()
    historial_eventos = []

    try:
        while True:
            res = nucleo.ciclo()
            lecturas = res["lecturas"]
            nuevos = res["eventos"]

            for e in nuevos:
                historial_eventos.insert(0, e)
            
            # Mantener solo los ultimos 10 eventos en pantalla
            historial_eventos = historial_eventos[:10]

            limpiar_pantalla()
            print("=" * 60)
            print(f" MONITOR IOT - NODO: {config.NODO} (PRESIONA CTRL+C PARA SALIR)")
            print("=" * 60)
            
            print("\n--- METRICAS EN TIEMPO REAL ---")
            for clave, datos in lecturas.items():
                if datos:
                    val = datos.get("valor", 0)
                    etiq = datos.get("etiqueta", clave)
                    print(f" -> {etiq:<20}: {val:>6.1f}")

            print("\n--- ULTIMOS EVENTOS DETECTADOS ---")
            if not historial_eventos:
                print(" Sin eventos registrados aun...")
            else:
                for e in historial_eventos:
                    col = COLORES.get(e["nivel"], COLORES["RESET"])
                    resets = COLORES["RESET"]
                    print(f"{e['hora']} [{col}{e['nivel']:<6}{resets}] {e['mensaje']}")

            print("\n" + "=" * 60)
            time.sleep(config.PERIODO_RAPIDO)

    except KeyboardInterrupt:
        print("\nMonitor detenido por el usuario.")
        sys.exit(0)

if __name__ == "__main__":
    ejecutar()