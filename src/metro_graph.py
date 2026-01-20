import networkx as nx
import math

# ==========================================
# CONFIGURACIÓN GENERAL
# ==========================================
COSTO_TRANSBORDO = 150  # Penalización en metros (costo de cambiar de andén)

# ==========================================
# 1. COORDENADAS GEOGRÁFICAS (LATITUD, LONGITUD)
# Usadas por el Algoritmo A* para la Heurística (Distancia Real)
# ==========================================
coordenadas = {
    # --- LÍNEA 1 (Rosa) ---
    "Observatorio_L1": (19.398237, -99.200363),
    "Tacubaya_L1": (19.403439, -99.187102),
    "Juanacatlán_L1": (19.41289, -99.182167),
    "Chapultepec_L1": (19.420783, -99.176288),
    "Sevilla_L1": (19.421916, -99.17058),
    "Insurgentes_L1": (19.423292, -99.163177),
    "Cuauhtémoc_L1": (19.425862, -99.154701),
    "Balderas_L1": (19.42744, -99.149036),

    # --- LÍNEA 3 (Verde Olivo) ---
    "Universidad_L3": (19.324427, -99.17397),
    "Copilco_L3": (19.335887, -99.176652),
    "M. A. de Quevedo_L3": (19.346395, -99.18103),
    "Viveros_L3": (19.353724, -99.176052),
    "Coyoacán_L3": (19.361417, -99.170709),
    "Zapata_L3": (19.370952, -99.164937),
    "División del Norte_L3": (19.380021, -99.158885),
    "Eugenia_L3": (19.385466, -99.157469),
    "Etiopía_L3": (19.395586, -99.156268),
    "Centro Médico_L3": (19.406637, -99.155753),
    "Hospital General_L3": (19.413578, -99.153886),
    "Niños Héroes_L3": (19.419508, -99.150581),
    "Balderas_L3": (19.42744, -99.149036),
    "Juárez_L3": (19.433167, -99.147792),

    # --- LÍNEA 7 (Naranja) ---
    "Barranca del Muerto_L7": (19.360648, -99.19014),
    "Mixcoac_L7": (19.375891, -99.187531),
    "San Antonio_L7": (19.384757, -99.186308),
    "San Pedro de los Pinos_L7": (19.391275, -99.186051),
    "Tacubaya_L7": (19.403439, -99.187102),
    "Constituyentes_L7": (19.411858, -99.191265),
    "Auditorio_L7": (19.425498, -99.191995),
    "Polanco_L7": (19.433511, -99.191029),

    # --- LÍNEA 9 (Café) ---
    "Tacubaya_L9": (19.403439, -99.187102),
    "Patriotismo_L9": (19.4062, -99.1789),
    "Chilpancingo_L9": (19.4059, -99.1686),
    "Centro Médico_L9": (19.406637, -99.155753),
    "Lázaro Cárdenas_L9": (19.40696, -99.144874),

    # --- LÍNEA 12 (Dorada) ---
    "Mixcoac_L12": (19.375891, -99.187531),
    "Insurgentes Sur_L12": (19.3736, -99.1788),
    "Hospital 20 de Noviembre_L12": (19.372, -99.171),
    "Zapata_L12": (19.370952, -99.164937),
    "Parque de los Venados_L12": (19.3707, -99.1587),
    "Eje Central_L12": (19.3614, -99.1514)
}

# ==========================================
# 2. POSICIONES DE DIBUJO (GRID X, Y)
# Usadas por tkin.py para dibujar el mapa "recto" (Estilo Diagrama)
# ==========================================
posiciones_dibujo = {
    # --- LÍNEA 1 (Horizontal Superior: Y=4) ---
    "Observatorio_L1": (1, 4),
    "Tacubaya_L1": (2, 4),       # Nodo Cruce L1/L7/L9
    "Juanacatlán_L1": (3, 4),
    "Chapultepec_L1": (4, 4),
    "Sevilla_L1": (5, 4),
    "Insurgentes_L1": (6, 4),
    "Cuauhtémoc_L1": (7, 4),
    "Balderas_L1": (8, 4),       # Nodo Cruce L1/L3

    # --- LÍNEA 3 (Vertical Derecha: X=8) ---
    "Juárez_L3": (8, 3),
    "Balderas_L3": (8, 4),       # Nodo Cruce
    "Niños Héroes_L3": (8, 5),
    "Hospital General_L3": (8, 6),
    "Centro Médico_L3": (8, 7),  # Nodo Cruce L3/L9
    "Etiopía_L3": (8, 8),
    "Eugenia_L3": (8, 9),
    "División del Norte_L3": (8, 10),
    "Zapata_L3": (8, 11),        # Nodo Cruce L3/L12
    "Coyoacán_L3": (8, 12),
    "Viveros_L3": (8, 13),
    "M. A. de Quevedo_L3": (8, 14),
    "Copilco_L3": (8, 15),
    "Universidad_L3": (8, 16),

    # --- LÍNEA 7 (Vertical Izquierda: X=2) ---
    "Polanco_L7": (2, 1),
    "Auditorio_L7": (2, 2),
    "Constituyentes_L7": (2, 3),
    "Tacubaya_L7": (2, 4),       # Nodo Cruce
    "San Pedro de los Pinos_L7": (2, 8),
    "San Antonio_L7": (2, 9),
    "Mixcoac_L7": (2, 11),       # Nodo Cruce L7/L12
    "Barranca del Muerto_L7": (2, 12),

    # --- LÍNEA 9 (Horizontal Medio: Y=7) ---
    "Tacubaya_L9": (2, 4),       # Nodo Cruce
    "Patriotismo_L9": (4, 7),
    "Chilpancingo_L9": (6, 7),
    "Centro Médico_L9": (8, 7),  # Nodo Cruce
    "Lázaro Cárdenas_L9": (10, 7),

    # --- LÍNEA 12 (Horizontal Inferior: Y=11) ---
    "Mixcoac_L12": (2, 11),      # Nodo Cruce
    "Insurgentes Sur_L12": (4, 11),
    "Hospital 20 de Noviembre_L12": (6, 11),
    "Zapata_L12": (8, 11),       # Nodo Cruce
    "Parque de los Venados_L12": (10, 11),
    "Eje Central_L12": (11, 11)
}

# ==========================================
# 3. CONSTRUCCIÓN DEL GRAFO (CONEXIONES Y PESOS)
# ==========================================
G = nx.Graph()

conexiones = [
    # L1
    ("Observatorio_L1", "Tacubaya_L1", 1262), ("Tacubaya_L1", "Juanacatlán_L1", 1158),
    ("Juanacatlán_L1", "Chapultepec_L1", 973), ("Chapultepec_L1", "Sevilla_L1", 501),
    ("Sevilla_L1", "Insurgentes_L1", 645), ("Insurgentes_L1", "Cuauhtémoc_L1", 793),
    ("Cuauhtémoc_L1", "Balderas_L1", 409),
    # L3
    ("Universidad_L3", "Copilco_L3", 1306), ("Copilco_L3", "M. A. de Quevedo_L3", 1295),
    ("M. A. de Quevedo_L3", "Viveros_L3", 824), ("Viveros_L3", "Coyoacán_L3", 908),
    ("Coyoacán_L3", "Zapata_L3", 1153), ("Zapata_L3", "División del Norte_L3", 794),
    ("División del Norte_L3", "Eugenia_L3", 715), ("Eugenia_L3", "Etiopía_L3", 950),
    ("Etiopía_L3", "Centro Médico_L3", 1119), ("Centro Médico_L3", "Hospital General_L3", 653),
    ("Hospital General_L3", "Niños Héroes_L3", 559), ("Niños Héroes_L3", "Balderas_L3", 665),
    ("Balderas_L3", "Juárez_L3", 659),
    # L7
    ("Barranca del Muerto_L7", "Mixcoac_L7", 1476), ("Mixcoac_L7", "San Antonio_L7", 788),
    ("San Antonio_L7", "San Pedro de los Pinos_L7", 606), ("San Pedro de los Pinos_L7", "Tacubaya_L7", 1084),
    ("Tacubaya_L7", "Constituyentes_L7", 1005), ("Constituyentes_L7", "Auditorio_L7", 1430),
    ("Auditorio_L7", "Polanco_L7", 812),
    # L9
    ("Tacubaya_L9", "Patriotismo_L9", 1133), ("Patriotismo_L9", "Chilpancingo_L9", 955),
    ("Chilpancingo_L9", "Centro Médico_L9", 1152), ("Centro Médico_L9", "Lázaro Cárdenas_L9", 1059),
    # L12
    ("Mixcoac_L12", "Insurgentes Sur_L12", 651), ("Insurgentes Sur_L12", "Hospital 20 de Noviembre_L12", 725),
    ("Hospital 20 de Noviembre_L12", "Zapata_L12", 450), ("Zapata_L12", "Parque de los Venados_L12", 563),
    ("Parque de los Venados_L12", "Eje Central_L12", 1280),
    # TRANSBORDOS (Conexiones entre líneas)
    ("Tacubaya_L1", "Tacubaya_L7", COSTO_TRANSBORDO), ("Tacubaya_L1", "Tacubaya_L9", COSTO_TRANSBORDO),
    ("Tacubaya_L7", "Tacubaya_L9", COSTO_TRANSBORDO), ("Balderas_L1", "Balderas_L3", COSTO_TRANSBORDO),
    ("Centro Médico_L3", "Centro Médico_L9", COSTO_TRANSBORDO), ("Zapata_L3", "Zapata_L12", COSTO_TRANSBORDO),
    ("Mixcoac_L7", "Mixcoac_L12", COSTO_TRANSBORDO)
]

accesibilidad_mec = {
    # Línea 1
    "Observatorio": True,
    "Tacubaya": True,
    "Chapultepec": True,
    "Sevilla": True,
    "Insurgentes": True,
    "Cuauhtémoc": True,
    "Balderas": True,

    # Línea 7
    "San Pedro de los Pinos": True,
    "San Antonio": True,
    "Mixcoac": True,
    "Barranca del Muerto": True,

    # Línea 9
    "Tacubaya": True,
    "Patriotismo": True,
    "Chilpancingo": True,
    "Centro Médico": True,
    "Lázaro Cárdenas": True,

    # Línea 3
    "Zapata": True,
    "División del Norte": True,
    "Eugenia": True,
    "Centro Médico": True,
    "Niños Héroes": True,
    "Hospital General": True,
    "Juárez": True,

    # Línea 12
    "Mixcoac": True,
    "Hospital 20 de Noviembre": True,
    "Parque de los Venados": True,
    "Eje Central": True,
    "Copilco" : True,
    "Viveros" : True,
    "M. A. de Quevedo":True
}

accesibilidad_asc = {
    "Centro Médico": True,
    "Hospital 20 de Noviembre":True,
    "Insurgentes Sur":True,
    "Mixcoac":True,
    "Parque de los Venados":True,
    "Eje Central":True,
    "Universidad":True,
    "Balderas":True,
    "Copilco":True,
    "M. A. de Quevedo":True,
    "Juárez": True,
    "Universidad": True,
    "Etiopía": True,
    "Zapata": True,
    "Insurgentes": True,
    "Sevilla": True,
    "Cuauhtémoc": True,
    "Observatorio": True
}


G.add_weighted_edges_from(conexiones)

# ==========================================
# 4. FUNCIÓN HEURÍSTICA (FÓRMULA HAVERSINE)
# ==========================================
def dist_haversine(nodo1, nodo2):
    R = 6371000  # Radio Tierra en metros
    lat1, lon1 = coordenadas[nodo1]
    lat2, lon2 = coordenadas[nodo2]

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    # Fórmula completa
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    a = max(0, min(1, a))  # Clampeo para evitar errores de dominio (sqrt negativos)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

# ==========================================
# 5. FUNCIÓN DE CÁLCULO DE RUTA
# ==========================================

def calcular_ruta(origen_usuario, destino_usuario):

    # 1. Filtrar nodos equivalentes (por nombre sin línea)
    candidatos_origen = [n for n in coordenadas if n.split('_')[0] == origen_usuario]
    candidatos_destino = [n for n in coordenadas if n.split('_')[0] == destino_usuario]

    if not candidatos_origen or not candidatos_destino:
        return None

    mejor_camino = None
    menor_costo = float('inf')

    # 2. Elegir función de peso según modo accesible
    def peso(u, v, datos):
        return datos["weight"]

    # 3. Probar todas las combinaciones origen–destino
    for inicio in candidatos_origen:
        for fin in candidatos_destino:
            try:
                costo = nx.astar_path_length(
                    G,
                    source=inicio,
                    target=fin,
                    heuristic=dist_haversine,
                    weight=peso
                )

                if costo < menor_costo:
                    menor_costo = costo
                    mejor_camino = nx.astar_path(
                        G,
                        source=inicio,
                        target=fin,
                        heuristic=dist_haversine,
                        weight=peso
                    )

            except nx.NetworkXNoPath:
                continue

    return mejor_camino


# Exportar variables para que tkin.py las pueda importar
__all__ = ["coordenadas", "conexiones", "dist_haversine", "G", "calcular_ruta", "posiciones_dibujo"]

# ==============================================================================
# BLOQUE DE EJECUCIÓN PRINCIPAL (SOLO SE EJECUTA SI ABRES ESTE ARCHIVO DIRECTO)
# ==============================================================================
if __name__ == "__main__":
    print("--- MODO PRUEBA DE METROMEXICO.PY ---")
    
    # Prueba simple
    origen = "Polanco"
    destino = "Zapata"
    
    ruta = calcular_ruta(origen, destino)
    
    if ruta:
        print(f"Ruta encontrada de {origen} a {destino}:")
        print(ruta)
    else:
        print("No se encontró ruta o estación inválida.")