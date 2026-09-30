# Monitor IoT

Nodo de telemetría desarrollado en Python. Monitorea recursos del equipo, muestra eventos en un dashboard y reproduce alertas sonoras sin detener el ciclo de monitoreo.

## Funcionalidades

- Monitoreo en tiempo real (CPU, RAM, disco, red, procesos, batería).
- Dashboard gráfico (GUI) y modo consola.
- Detección de pérdida/recuperación de red con recordatorios temporizados.
- Alertas sonoras no bloqueantes mediante cola deque.
- Registro histórico en bitacora.json.
- Pruebas unitarias con unittest.

## Requisitos e Instalación

- Python 3
- Dependencias descritas en requirements.txt (psutil)

Configuración del entorno en PowerShell:

python -m venv entorno
.\entorno\Scripts\Activate.ps1
pip install -r requirements.txt

Nota: Si PowerShell bloquea la ejecución de scripts, habilítala temporalmente ejecutando:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned

## Uso

Modo Gráfico (Dashboard):
python main.py

Modo Consola:
python main.py --consola

Ejecutar Pruebas:
python -m unittest discover -s tests -v

## Estructura del Proyecto

├── sensores/       # Lectura de métricas del equipo
├── eventos/        # Detección y manejo de eventos
├── alertas/        # Cola y reproducción no bloqueante de sonidos
├── dashboard/      # Interfaz gráfica y consola
├── almacenamiento/ # Persistencia de métricas y bitácora
├── tests/          # Pruebas unitarias
├── config.py       # Parámetros, umbrales e intervalos
├── nucleo.py       # Ciclo principal de monitoreo
└── main.py         # Punto de entrada de la aplicación

## Autoría

- Nombre: Calvin Miro
- Asignatura: Desarrollo de Software VIII
- Grupo: 134
- Institución: Universidad Tecnológica de Panamá
