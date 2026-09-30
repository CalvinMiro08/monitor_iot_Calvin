"""
dashboard/ventana.py
Interfaz grafica principal con Tkinter.

Muestra las metricas en vivo y los eventos con sus colores de severidad.
Usa `.after()` para coordinar el bucle de monitoreo con el bucle de
eventos de Tkinter sin bloquear la pantalla.
"""
import tkinter as tk
from tkinter import ttk, scrolledtext
import nucleo
import config

COLORES_NIVEL = {
    "INFO": "#2e7d32",     # Verde
    "AVISO": "#f57f17",    # Amarillo / Naranja
    "ALERTA": "#c62828",   # Rojo
    "FALLA": "#6a1b9a",    # Morado
}

class DashboardVentana:
    def __init__(self, root):
        self.root = root
        self.root.title(f"Monitor IoT - Nodo: {config.NODO}")
        self.root.geometry("650x500")

        nucleo.iniciar()

        # Contenedor de metricas
        frame_metricas = ttk.LabelFrame(root, text=" Metricas en tiempo real ")
        frame_metricas.pack(fill="x", padx=10, pady=5)

        self.labels_metricas = {}
        activos = nucleo.activos()

        for i, clave in enumerate(activos):
            row = i // 2
            col = (i % 2) * 2
            ttk.Label(frame_metricas, text=f"{clave.upper()}:", font=("Consolas", 10, "bold")).grid(
                row=row, column=col, sticky="w", padx=10, pady=4
            )
            lbl_val = ttk.Label(frame_metricas, text="---", font=("Consolas", 10))
            lbl_val.grid(row=row, column=col + 1, sticky="w", padx=10, pady=4)
            self.labels_metricas[clave] = lbl_val

        # Contenedor de eventos
        frame_eventos = ttk.LabelFrame(root, text=" Bitacora de eventos ")
        frame_eventos.pack(fill="both", expand=True, padx=10, pady=5)

        self.txt_eventos = scrolledtext.ScrolledText(
            frame_eventos, wrap=tk.WORD, font=("Consolas", 9), state="disabled"
        )
        self.txt_eventos.pack(fill="both", expand=True, padx=5, pady=5)

        # Configurar etiquetas de color para el texto
        for nivel, color in COLORES_NIVEL.items():
            self.txt_eventos.tag_config(nivel, foreground=color)

        # Iniciar refresco periodico
        self.actualizar()

    def actualizar(self):
        """Metodo recursivo no bloqueante llamado por tkinter."""
        res = nucleo.ciclo()
        lecturas = res["lecturas"]
        nuevos_eventos = res["eventos"]

        # Actualizar valores numéricos
        for clave, lbl in self.labels_metricas.items():
            if clave in lecturas and lecturas[clave]:
                val = lecturas[clave]["valor"]
                lbl.config(text=f"{val:.1f}")

        # Insertar nuevos eventos
        if nuevos_eventos:
            self.txt_eventos.config(state="normal")
            for e in nuevos_eventos:
                nivel = e["nivel"]
                linea = f"{e['hora']} [{nivel:<6}] {e['mensaje']}\n"
                self.txt_eventos.insert("1.0", linea, nivel)
            self.txt_eventos.config(state="disabled")

        # Reagendar siguiente ciclo (1000 ms = 1 seg)
        intervalo_ms = int(getattr(config, "PERIODO_GRAFICO", 1.0) * 1000)
        self.root.after(intervalo_ms, self.actualizar)

def ejecutar():
    root = tk.Tk()
    app = DashboardVentana(root)
    root.mainloop()

if __name__ == "__main__":
    ejecutar()