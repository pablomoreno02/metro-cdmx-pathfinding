# CDMX Metro Pathfinding AI

## Descripción
Herramienta interactiva desarrollada en Python para calcular y visualizar la ruta óptima entre estaciones del Metro de Ciudad de México.

El sistema implementa el algoritmo **A*** utilizando la **fórmula de Haversine** como heurística, garantizando la ruta más eficiente basada en distancias geográficas reales y no solo en el número de paradas. Incluye gestión de accesibilidad para personas con movilidad reducida.

## Características Principales
* **Algoritmo de Búsqueda Informada:** Implementación propia de A* sobre un grafo ponderado (`NetworkX`).
* **Heurística Real:** Cálculo de costes basado en geolocalización (latitud/longitud) real de las estaciones.
* **Interfaz Gráfica (GUI):** Mapa interactivo construido con `Tkinter` que permite zoom, paneo y selección visual.
* **Animación:** Visualización dinámica del recorrido del usuario.
* **Accesibilidad:** Filtrado y visualización de rutas adaptadas (ascensores/escaleras mecánicas).

## Tecnologías Utilizadas
* **Lenguaje:** Python 3
* **Lógica y Grafos:** `NetworkX`
* **Interfaz:** `Tkinter`
* **Algoritmos:** A*, Haversine Distance

## Instalación y Ejecución

1. Clonar el repositorio:
   ```bash
   git clone [https://github.com/pablomoreno02/metro-cdmx-pathfinding.git](https://github.com/pablomoreno02/metro-cdmx-pathfinding.git)
2. Instalar dependencias: pip install -r requirements.txt
3. Ejecutar: python src/main_gui.py

## Sobre el Proyecto
Este proyecto fue desarrollado en grupo como parte de la asignatura de Inteligencia Artificial en el Grado de Ingeniería Informática (UPM).