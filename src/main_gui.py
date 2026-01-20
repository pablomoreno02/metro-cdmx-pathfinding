import tkinter as tk
from tkinter import ttk
import math

# Importamos los datos y lógica del backend
from metro_graph import coordenadas, conexiones, posiciones_dibujo, calcular_ruta,accesibilidad_mec,accesibilidad_asc

# ==========================================
# CONFIGURACIÓN VISUAL
# ==========================================
MARGEN = 40
FONDO_MAPA = "#D1D1D1"
COLOR_ESTACIONES = "#FFFFFF"
COLOR_TEXTO = "black"
COLOR_TRANSBORDO = "#888888"
COLOR_RUTA = "#0400FF"
RADIO_CURSOR = 6

# Escala y Desplazamiento del dibujo
ESCALA_X = 125
ESCALA_Y = 40
OFFSET_X = -90
OFFSET_Y = 0


COLOR_LINEA = {
    "L1": "#E71D73", "L3": "#A4C639", "L7": "#F5A623",
    "L9": "#8B5A2B", "L12": "#C9A100"
}

# Variables Globales de Estado
station_ids = {}  
stations_oid = {}# Relaciona el ID del canvas con el nombre de la estación
stations_color = {}
current_origin = None
current_dest = None
animacion_activa = False
modo_accesible = False

# ==========================================
# 1. FUNCIONES DE AYUDA (COORDENADAS Y NOMBRES)
# ==========================================
def obtener_nombre_base(nodo):
    return nodo.split("_")[0]

def obtener_linea(nodo):
    return nodo.split("_")[1]

def grid_a_pixeles(gx, gy):
    """Convierte coordenadas de la cuadrícula a píxeles en pantalla."""
    x = (gx * ESCALA_X) + OFFSET_X
    y = (gy * ESCALA_Y) + OFFSET_Y
    return x, y

def es_transbordo(nodo1, nodo2):
    return (obtener_nombre_base(nodo1) == obtener_nombre_base(nodo2) and 
            obtener_linea(nodo1) != obtener_linea(nodo2))

# ==========================================
# 2. DIBUJO DEL MAPA
# ==========================================
def dibujar_mapa(canvas):
    
    global station_ids, stations_oid,stations_color
    station_ids = {}
    stations_color={}
    stations_oid = {}
    canvas.delete("all")
    
    h= canvas.winfo_height()
    w = canvas.winfo_width()
    
    canvas.create_rectangle(0,0,w,h,fill=FONDO_MAPA,outline=FONDO_MAPA)
    for a,b,_ in conexiones:
      if(a in posiciones_dibujo and b in posiciones_dibujo):
        nombre_a = obtener_nombre_base(a)
        linea_a = obtener_linea(a)
        nombre_b = obtener_nombre_base(b)
        gx,gy = posiciones_dibujo.get(a)
        gbx,gby = posiciones_dibujo.get(b)
        ax,ay = grid_a_pixeles(gx,gy)
        bx,by = grid_a_pixeles(gbx,gby)
        
        if(es_transbordo(a,b)):
            canvas.create_line(ax,ay,bx,by,fill=COLOR_TRANSBORDO,width=2)
        else:
            canvas.create_line(ax,ay,bx,by,fill=COLOR_LINEA.get(linea_a, "#B0B0B0"),width=5)
    for nodo,(gx,gy) in posiciones_dibujo.items():
        x,y = grid_a_pixeles(gx,gy)
        oid = canvas.create_oval(x-6,y-6,x+6,y+6,fill=COLOR_ESTACIONES,width=2)
        tid = canvas.create_text(x+10,y-10,text=obtener_nombre_base(nodo), anchor="w", font=("Segoe UI", 8, "bold"), fill=COLOR_TEXTO)
        
        station_ids[oid] = obtener_nombre_base(nodo)
        stations_oid[station_ids[oid]] = oid
    
    resaltar_seleccion(canvas)
    dibujar_leyenda_lineas(canvas)
    dibujar_leyenda_accesibilidad(canvas)



def dibujar_leyenda_lineas(canvas):
    # Borrar la antigua leyenda si existe
    canvas.delete("leyenda_lineas")

    w = canvas.winfo_width()
    h = canvas.winfo_height()

    # Localización: esquina inferior derecha
    x0 = w - 180
    y0 = h - 160

    # Fondo
    canvas.create_rectangle( x0 - 10, y0 - 20, x0 + 150, y0 + (len(COLOR_LINEA) * 18) + 20, fill="#FFFFFF", outline="black", width=1, tags="leyenda_lineas"
    )

    # Título
    canvas.create_text(x0, y0 - 10, text="Líneas del Metro:", anchor="w", font=("Segoe UI", 10, "bold"), fill="black", tags="leyenda_lineas"
    )
    y0 += 12
    # Dibujar cada línea
    for linea, color in COLOR_LINEA.items():
        canvas.create_line(
            x0, y0, x0 + 30, y0,
            width=5, fill=color, tags="leyenda_lineas"
        )
        canvas.create_text(
            x0 + 40, y0,
            text=linea, anchor="w",
            font=("Segoe UI", 9, "bold"),
            fill="black", tags="leyenda_lineas"
        )
        y0 += 18

        
def resaltar_seleccion(canvas):
    """Pinta de color azul el origen y verde el destino."""
    # Primero ponemos todas en blanco
    canvas.itemconfig("estacion", fill="white")
    if(modo_accesible):
        canvas.itemconfig("Escaleras_mec",fill="blue")
        canvas.itemconfig("Ascensor",fill="green")
    
    # Buscamos los IDs correspondientes a los nombres seleccionados
    # (Iteramos items del canvas para encontrar coincidencias)
    all_items = set()

    all_items = station_ids.keys()
    for item in all_items:
        nombre = station_ids.get(item)
        if nombre == current_origin:
            canvas.itemconfig(item, fill="#7DFBFB") # Azul
        elif nombre == current_dest:
            canvas.itemconfig(item, fill="#A02B16") # Verde
def dibujar_leyenda_accesibilidad(canvas):
    # Borrar leyenda anterior si existe
    canvas.delete("leyenda_acc")

    if not modo_accesible:
        return  # No dibujar si accesibilidad está OFF

    w = canvas.winfo_width()
    h = canvas.winfo_height()

    x0 = 20
    y0 = h - 150  # Esquina inferior izquierda

    # Fondo de la leyenda
    rect = canvas.create_rectangle(
        x0 - 10, y0 - 20, x0 + 200, y0 + 60,
        fill="#FFFFFF", outline="black", width=1,
        tags="leyenda_acc"
    )

    # Título
    canvas.create_text(x0, y0 - 10, text="Accesibilidad:", anchor="w", fill="black", font=("Segoe UI", 10, "bold"), tags="leyenda_acc")

    # Escaleras mecánicas
    canvas.create_oval(x0, y0, x0+12, y0+12, fill="blue", outline="black", tags="leyenda_acc")
    canvas.create_text(x0+20, y0+6, text="Escalera Mecánica", anchor="w", fill="black", font=("Segoe UI", 8), tags="leyenda_acc")

    y0 += 18

    # Ascensores
    canvas.create_oval(x0, y0, x0+12, y0+12, fill="green", outline="black", tags="leyenda_acc")
    canvas.create_text(x0+20, y0+6,text="Ascensor y Escalera Mecánica", anchor="w", fill="black", font=("Segoe UI", 8),tags="leyenda_acc")
    y0 += 18

# ==========================================
# 3. ANIMACIÓN SIMPLIFICADA
# ==========================================
def animar_ruta(canvas, puntos, idx=0, t=0.0, cursor_id=None):
    """Mueve un punto azul a lo largo de la lista de coordenadas."""
    global animacion_activa
    
    # Si el usuario canceló, detenemos
    if not animacion_activa:
        return

    # Si llegamos al final de la lista de puntos
    if idx >= len(puntos) - 1:
        animacion_activa = False
        canvas.delete(cursor_id) # Opcional: borrar cursor al final
        return

    # Coordenadas actuales (A) y siguientes (B)
    x1, y1 = puntos[idx]
    x2, y2 = puntos[idx+1]

    # Interpolación lineal (Matemáticas para mover suavemente de A a B)
    x = x1 + (x2 - x1) * t
    y = y1 + (y2 - y1) * t

    # Dibujar o mover el cursor
    if cursor_id is None:
        cursor_id = canvas.create_oval(x-RADIO_CURSOR, y-RADIO_CURSOR, x+RADIO_CURSOR, y+RADIO_CURSOR, fill=COLOR_RUTA, outline="white", width=2)
    else:
        canvas.coords(cursor_id, x-RADIO_CURSOR, y-RADIO_CURSOR, x+RADIO_CURSOR, y+RADIO_CURSOR)

    # Dibujar rastro sólido al completar un tramo
    if t >= 1.0:
        canvas.create_line(x1, y1, x2, y2, fill=COLOR_RUTA, width=4)
        # Siguiente tramo
        idx += 1
        t = 0.0
    else:
        # Avanzar tiempo (velocidad)
        t += 0.05 

    # Llamar a esta misma función en 30 milisegundos (Loop)
    canvas.after(30, lambda: animar_ruta(canvas, puntos, idx, t, cursor_id))

# ==========================================
# 4. INTERACCIÓN (ZOOM, PAN, CLIC)
# ==========================================
def configurar_eventos(canvas, combo_origen, combo_destino):
    
    # --- Zoom con Rueda ---
    def zoom(event):
        scale = 1.1 if event.delta > 0 else 0.9
        canvas.scale("all", event.x, event.y, scale, scale)

    # --- Mover mapa (Pan) ---
    canvas.bind("<ButtonPress-2>", lambda e: canvas.scan_mark(e.x, e.y))
    canvas.bind("<B2-Motion>", lambda e: canvas.scan_dragto(e.x, e.y, gain=1))
    canvas.bind("<ButtonPress-3>", lambda e: canvas.scan_mark(e.x, e.y)) # Click derecho
    canvas.bind("<B3-Motion>", lambda e: canvas.scan_dragto(e.x, e.y, gain=1))
    canvas.bind("<MouseWheel>", zoom)

    # --- Selección de estación con Clic Izquierdo ---
    def clic_izquierdo(event):
        global current_origin, current_dest
        
        # Buscar objeto cercano al clic
        item = canvas.find_closest(canvas.canvasx(event.x), canvas.canvasy(event.y))[0]
        nombre = station_ids.get(item)

        if nombre:
            if current_origin is None:
                current_origin = nombre
            elif current_dest is None:
                current_dest = nombre
            else:
                # Reiniciar si ya había dos
                current_origin = nombre
                current_dest = None
            
            # Actualizar visuales y combobox
            resaltar_seleccion(canvas)
            combo_origen.set(current_origin if current_origin else "")
            combo_destino.set(current_dest if current_dest else "")

    canvas.bind("<ButtonPress-1>", clic_izquierdo)

# ==========================================
# 5. INTERFAZ PRINCIPAL
# ==========================================
def interfaz():
    global animacion_activa, current_origin, current_dest, modo_accesible

    root = tk.Tk()
    root.title("Metro CDMX - A* Simple")
    root.geometry("1400x800")

    # --- Panel de Controles ---
    panel = tk.Frame(root, bg="#DDD", pady=5)
    panel.pack(side="top", fill="x")

    estaciones = sorted(list(set([obtener_nombre_base(k) for k in coordenadas.keys()])))

    # Comboboxes
    tk.Label(panel, text="Origen:", bg="#DDD").pack(side="left", padx=5)
    cb_origen = ttk.Combobox(panel, values=estaciones)
    cb_origen.pack(side="left")

    tk.Label(panel, text="Destino:", bg="#DDD").pack(side="left", padx=5)
    cb_destino = ttk.Combobox(panel, values=estaciones)
    cb_destino.pack(side="left")

    # Botones
    def accion_calcular():
        global animacion_activa, current_origin, current_dest
        
        # Obtener valores
        current_origin = cb_origen.get()
        current_dest = cb_destino.get()

        if not current_origin or not current_dest:
            return

        # Limpiar mapa previo
        animacion_activa = False # Detener animación anterior si la hay
        dibujar_mapa(canvas) 
        
        # Calcular Ruta (Backend)
        camino = calcular_ruta(current_origin, current_dest)
        
        if camino:
            # Convertir nombres de nodos a coordenadas de pantalla (puntos)
            puntos_pantalla = []
            for nodo in camino:
                if nodo in posiciones_dibujo:
                    gx, gy = posiciones_dibujo[nodo]
                    # Necesitamos convertir las coordenadas GRID a las coordenadas actuales del CANVAS (por si hubo zoom)
                    # Truco simple: Usamos la función base y no soportamos zoom *durante* la animación en esta versión simple
                    px, py = grid_a_pixeles(gx, gy)
                    puntos_pantalla.append((px, py))
            
            animacion_activa = True
            animar_ruta(canvas, puntos_pantalla)
        else:
            print("No se encontró ruta")

    def accion_limpiar():
        global current_origin, current_dest, animacion_activa
        animacion_activa = False
        current_origin = None
        current_dest = None
        cb_origen.set("")
        cb_destino.set("")
        dibujar_mapa(canvas)

    def toggle_accesibilidad():
        global modo_accesible,btn_acc
        modo_accesible = not modo_accesible
        if (modo_accesible):
          btn_acc.config(text ="Accesibilidad: ON",bg="green", fg="white")
          for esta in accesibilidad_mec.keys():
              if(stations_oid[esta]):
                canvas.itemconfig(stations_oid[esta],fill="blue")
                canvas.addtag_withtag("Escaleras_mec", stations_oid[esta])
                canvas.dtag(stations_oid[esta],"estacion")
          for est in accesibilidad_asc:
              if(stations_oid[est]):
                  canvas.itemconfig(stations_oid[est],fill="green")
                  canvas.addtag_withtag("Ascensor", stations_oid[est])
                  canvas.dtag(stations_oid[esta],"estacion")
        else:
          btn_acc.config(text = "Accesibilidad: OFF",bg="#DDD",fg="black")
          for estac in accesibilidad_mec.keys():
           if(stations_oid[estac]):
             canvas.itemconfig(stations_oid[estac],fill="white")
             canvas.dtag(stations_oid[estac],"Escaleras_mec")
             canvas.addtag_withtag("estacion",stations_oid[estac])
          for es in accesibilidad_asc:
              if(stations_oid[es]):
                  canvas.itemconfig(stations_oid[es],fill="white")
                  canvas.dtag(stations_oid[es],"Ascensor")
                  canvas.addtag_withtag("estacion",stations_oid[estac])
        dibujar_leyenda_accesibilidad(canvas)

    tk.Button(panel, text="Calcular", command=accion_calcular, bg="#4CAF50", fg="white").pack(side="left", padx=10)
    tk.Button(panel, text="Limpiar", command=accion_limpiar).pack(side="left")
    
    global btn_acc
    btn_acc = tk.Button(panel, text="Accesibilidad: OFF", command=toggle_accesibilidad)
    btn_acc.pack(side="right", padx=10)

    # --- Canvas (Mapa) ---
    canvas = tk.Canvas(root, bg=FONDO_MAPA)
    canvas.pack(fill="both", expand=True)

    # Inicializar
    dibujar_mapa(canvas)
    configurar_eventos(canvas, cb_origen, cb_destino)
    root.after(100, lambda: (dibujar_leyenda_lineas(canvas), dibujar_leyenda_accesibilidad(canvas)))

    root.mainloop()

if __name__ == "__main__":
    interfaz()