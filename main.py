"""
main.py
Punto de entrada principal del Monitor IoT.

Permite elegir el modo de ejecucion (grafico o consola) mediante
argumentos de linea de comandos.
"""
import sys
import dashboard

def main():
    # Si se pasa el argumento --consola o -c, arranca la terminal
    if len(sys.argv) > 1 and sys.argv[1] in ("--consola", "-c"):
        dashboard.consola()
    else:
        # Por defecto abre la ventana grafica con Tkinter
        try:
            dashboard.ventana()
        except Exception as e:
            print(f"No se pudo iniciar la interfaz grafica ({e}).")
            print("Iniciando modo consola como respaldo...")
            dashboard.consola()

if __name__ == "__main__":
    main()