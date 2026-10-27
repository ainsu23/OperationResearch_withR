"""Dibuja la red de turnos de Siigo (versión conceptual) en SVG y draw.io.

Una sola lista de nodos y arcos alimenta los dos formatos. Para corregir el
diagrama, edita las listas y vuelve a correr: python diagramas/generar_red_siigo.py
"""
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

SALIDA = Path(__file__).parent
W, H = 1820, 1270

ESTILO = {  # tipo: (relleno, borde, texto)
    "trabajo": ("#dbeafe", "#2563eb", "#1e3a8a"),
    "descanso": ("#dcfce7", "#16a34a", "#14532d"),
    "almuerzo": ("#ffedd5", "#ea580c", "#7c2d12"),
    "libre": ("#f3f4f6", "#6b7280", "#111827"),
    "borde": ("#1f2937", "#1f2937", "#ffffff"),
    "red": ("#eff6ff", "#2563eb", "#1e3a8a"),
}

nodos = {}   # id: (cx, cy, ancho, alto, texto, tipo)
arcos = []   # (origen, destino, etiqueta, punteado)
textos = []  # (x, y, texto, tamaño, negrita, ancla)


def hora(i):
    minutos = 7 * 60 + 30 * i
    return f"{minutos // 60:02d}:{minutos % 60:02d}"


def x(i):
    return 210 + i * 70


# ---------- A. Un día ----------
# Una fila por etapa del día. Solo se baja de etapa pasando por un descanso o
# por el almuerzo: así son obligatorios y el almuerzo dura exactamente 1 hora.
ENTRADA = (0, 1, 2, 3)            # 07:00, 07:30, 08:00, 08:30
DESCANSO1 = (3, 4, 5, 6)          # ventana de ejemplo: 08:30–10:00
ALMUERZO = (10, 11, 12, 13)       # empieza 12:00, 12:30, 13:00 o 13:30
DESCANSO2 = (14, 15, 16, 17, 18)  # ventana de ejemplo: 14:00–16:00
SALIDA_ULTIMO_BLOQUE = (18, 19, 20, 21)  # último bloque 16:00–17:30 → sale 16:30–18:00
ETAPAS = {  # prefijo: (filas de tiempo, y, nombre)
    "S0": (range(0, 6), 200, "Trabaja · antes de Descanso1"),
    "S1": (range(4, 13), 310, "Trabaja · entre Descanso1 y almuerzo"),
    "S2": (range(12, 18), 480, "Trabaja · entre almuerzo y Descanso2"),
    "S3": (range(15, 22), 590, "Trabaja · después de Descanso2"),
}
Y_D1, Y_A1, Y_A2, Y_D2 = 255, 370, 420, 535

textos += [
    (20, 30, "A. Un día de Andrés (lun 26 oct), bloques de 30 min", 18, True, "start"),
    (20, 54, "«inicio» existe una sola vez por persona. Entrada a las 07:00, 07:30, 08:00 u 08:30. Cada fila "
             "«Trabaja» es una etapa del día: solo se baja de etapa por un descanso o por el almuerzo (confirmado).",
     13, False, "start"),
    (x(4.5), 172, ETAPAS["S0"][2], 12, True, "middle"),
    (x(3) - 40, Y_D1, "Descanso1 · 15 min: 2 opciones por bloque", 12, True, "end"),
    (x(4) - 32, ETAPAS["S1"][1], ETAPAS["S1"][2], 12, True, "end"),
    (x(10) - 32, Y_A1, "Almuerzo · 1ª media hora (4 opciones)", 12, True, "end"),
    (x(11) - 32, Y_A2, "Almuerzo · 2ª media hora", 12, True, "end"),
    (x(12) - 32, ETAPAS["S2"][1], ETAPAS["S2"][2], 12, True, "end"),
    (x(14) - 40, Y_D2, "Descanso2 · 15 min: 2 opciones por bloque", 12, True, "end"),
    (x(15) - 32, ETAPAS["S3"][1], ETAPAS["S3"][2], 12, True, "end"),
]
textos += [(x(i), 92, hora(i), 11, False, "middle") for i in range(22)]

nodos["inicio"] = (x(1.5), 140, 72, 30, "inicio", "borde")  # encima de las 4 horas de entrada
nodos["siguiente"] = (1600, 665, 140, 34, "mar 27 (ver B)", "red")
for prefijo, (filas, y, _) in ETAPAS.items():
    for i in filas:
        nodos[f"{prefijo}_{i}"] = (x(i), y, 50, 28, hora(i), "trabajo")
    for a in filas:
        if a + 1 in filas:
            arcos.append((f"{prefijo}_{a}", f"{prefijo}_{a + 1}", "", False))
def descansos(nombre, bloques, y, antes, despues):
    """Cada bloque de 30 min tiene 2 descansos posibles de 15 min (p. ej. 08:30_30 y 08:30_45).
    Para la demanda, el bloque entero cuenta como no disponible."""
    for i in bloques:
        base = int(hora(i)[-2:])
        for k in (0, 1):
            nid = f"{nombre}_{i}_{k}"
            nodos[nid] = (x(i) - 17 + 34 * k, y, 30, 28, f":{base + 15 * k:02d}", "descanso")
            arcos.extend([(f"{antes}_{i - 1}", nid, "", False), (nid, f"{despues}_{i + 1}", "", False)])


descansos("D1", DESCANSO1, Y_D1, "S0", "S1")
for i in ALMUERZO:  # cada opción tiene sus 2 nodos: 1ª y 2ª media hora
    nodos[f"A1_{i}"] = (x(i), Y_A1, 50, 28, hora(i), "almuerzo")
    nodos[f"A2_{i + 1}"] = (x(i + 1), Y_A2, 50, 28, hora(i + 1), "almuerzo")
    arcos += [(f"S1_{i - 1}", f"A1_{i}", "", False), (f"A1_{i}", f"A2_{i + 1}", "", False),
              (f"A2_{i + 1}", f"S2_{i + 2}", "", False)]
descansos("D2", DESCANSO2, Y_D2, "S2", "S3")
arcos += [("inicio", f"S0_{i}", "", False) for i in ENTRADA]
arcos += [(f"S3_{i}", "siguiente", "", False) for i in SALIDA_ULTIMO_BLOQUE]

# leyenda
YL = 700
nodos["leg_t"] = (95, YL, 150, 26, "Trabaja (30 min)", "trabajo")
nodos["leg_d"] = (300, YL, 230, 26, "Descanso (15 min en bloque de 30)", "descanso")
nodos["leg_a"] = (530, YL, 200, 26, "Almuerzo (2 × 30 min)", "almuerzo")
nodos["leg_l"] = (720, YL, 160, 26, "Libre / medio día", "libre")
nodos["leg_b"] = (870, YL, 110, 26, "inicio / Fin", "borde")
textos.append((950, YL, "Arco Trabaja → Trabaja: costo 0,5. Arco hacia o desde Libre: costo 4. "
                        "Punteado = por confirmar.", 12, False, "start"))

# ---------- B. Unión entre dos días ----------
textos += [
    (20, 770, "B. Unión entre dos días: no hay inicio ni Fin por día", 18, True, "start"),
    (20, 794, "Los nodos donde termina el lunes se conectan directamente con los nodos donde empieza el martes.",
     13, False, "start"),
    (360, 828, "termina lun 26", 13, True, "middle"),
    (1100, 828, "empieza mar 27", 13, True, "middle"),
    (1260, 885, "Arcos que tocan Libre: costo 4 (sólidos).", 13, False, "start"),
    (1260, 910, "Arcos sin Libre: costo por confirmar (punteados).", 13, False, "start"),
    (1260, 935, "Mañana_libre y Tarde_libre: horario por confirmar.", 13, False, "start"),
]
izquierda = {"Ltrab": "Trabaja (último bloque)", "Llib": "Libre", "Ltarde": "Tarde_libre"}
derecha = {"Mtrab": "Trabaja (primer bloque)", "Mlib": "Libre", "Mman": "Mañana_libre"}
for k, (nid, texto) in enumerate(izquierda.items()):
    nodos[nid] = (360, 860 + 50 * k, 180, 30, texto, "trabajo" if k == 0 else "libre")
for k, (nid, texto) in enumerate(derecha.items()):
    nodos[nid] = (1100, 860 + 50 * k, 180, 30, texto, "trabajo" if k == 0 else "libre")
for o in izquierda:
    for d in derecha:
        arcos.append((o, d, "", "lib" not in o and "lib" not in d))

# ---------- C. La semana ----------
YC = 1095
textos += [
    (20, 1025, "C. La semana de cada persona: un solo inicio y un solo Fin", 18, True, "start"),
    (20, 1049, "La misma red se copia para cada persona (Andrés, Klaudia, Oliver…). Si ya se sabe que un día es "
               "libre, ese día solo tiene su nodo Libre: no se crean nodos ni arcos de trabajo.", 13, False, "start"),
]
nodos["c_inicio"] = (80, YC, 72, 34, "inicio", "borde")
nodos["c_lun"] = (270, YC, 180, 34, "lun 26: red del día", "red")
nodos["c_mar"] = (530, YC, 180, 34, "mar 27: red del día", "red")
nodos["c_mie"] = (790, YC, 180, 34, "mié 28: solo Libre", "libre")
nodos["c_jue"] = (1050, YC, 180, 34, "jue 29: red del día", "red")
nodos["c_dom"] = (1340, YC, 180, 34, "dom 1: red del día", "red")
nodos["c_fin"] = (1550, YC, 72, 34, "Fin", "borde")
arcos += [
    ("c_inicio", "c_lun", "", False), ("c_lun", "c_mar", "", False),
    ("c_mar", "c_mie", "4", False), ("c_mie", "c_jue", "4", False),
    ("c_jue", "c_dom", "vie, sáb", False), ("c_dom", "c_fin", "", False),
]

# ---------- D. Reglas que no se ven en el dibujo ----------
textos += [
    (20, 1170, "D. Reglas fuera del dibujo", 16, True, "start"),
    (20, 1195, "Cobertura, en cada bloque de 30 min: Σ personas en «Trabaja» + demanda no atendida ≥ demanda. La demanda "
               "no atendida se penaliza y sirve para planear contrataciones. Quien está en descanso no cuenta.", 13, False, "start"),
    (20, 1220, "Los costos son horas y cada día suma un total fijo: 8 h de trabajo + 1 h de almuerzo + 30 min de "
               "descanso = 9,5 h (libre: 4 + 4). Por eso la salida queda fija: entrada 07:00 → 16:30; 08:30 → 18:00.",
     13, False, "start"),
    (20, 1245, "Por confirmar: horas exactas de las ventanas de descanso, costo de los arcos de descanso (¿0,25?), "
               "de almuerzo y entre días, y horario del medio día libre.", 13, False, "start"),
]


def punto_borde(n, hacia):
    """Punto donde la recta desde el centro de n hacia `hacia` cruza el borde de n."""
    cx, cy, w, h = nodos[n][:4]
    dx, dy = hacia[0] - cx, hacia[1] - cy
    t = min((w / 2) / abs(dx) if dx else float("inf"), (h / 2) / abs(dy) if dy else float("inf"))
    return cx + dx * t, cy + dy * t


def generar_svg():
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         'font-family="Helvetica, Arial, sans-serif">',
         '<defs><marker id="flecha" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="7" markerHeight="7" '
         'orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#374151"/></marker></defs>',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>']
    for y in (740, 995, 1140):
        s.append(f'<line x1="20" y1="{y}" x2="{W - 20}" y2="{y}" stroke="#e5e7eb" stroke-width="2"/>')
    for o, d, etiqueta, punteado in arcos:
        x1, y1 = punto_borde(o, nodos[d][:2])
        x2, y2 = punto_borde(d, nodos[o][:2])
        guion = ' stroke-dasharray="6 4"' if punteado else ""
        s.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#374151" '
                 f'stroke-width="1.4"{guion} marker-end="url(#flecha)"/>')
        if etiqueta:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            largo = max(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5, 1)
            if abs(y2 - y1) < 2:
                ox, oy = 0, -7
            else:
                ox, oy = -(y2 - y1) / largo * 10, (x2 - x1) / largo * 10
            s.append(f'<text x="{mx + ox:.1f}" y="{my + oy:.1f}" font-size="11" text-anchor="middle" '
                     f'fill="#111827" stroke="#ffffff" stroke-width="3" paint-order="stroke">{escape(etiqueta)}</text>')
    for cx, cy, w, h, texto, tipo in nodos.values():
        relleno, borde, letra = ESTILO[tipo]
        tam = 11 if w <= 60 else 12
        s.append(f'<rect x="{cx - w / 2:.1f}" y="{cy - h / 2:.1f}" width="{w}" height="{h}" rx="6" '
                 f'fill="{relleno}" stroke="{borde}" stroke-width="1.5"/>')
        s.append(f'<text x="{cx}" y="{cy + 4}" font-size="{tam}" text-anchor="middle" fill="{letra}">'
                 f'{escape(texto)}</text>')
    for tx, ty, texto, tam, negrita, ancla in textos:
        peso = ' font-weight="bold"' if negrita else ""
        s.append(f'<text x="{tx}" y="{ty + 4}" font-size="{tam}"{peso} text-anchor="{ancla}" fill="#111827">'
                 f'{escape(texto)}</text>')
    s.append("</svg>")
    return "\n".join(s)


def generar_drawio():
    c = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']
    for nid, (cx, cy, w, h, texto, tipo) in nodos.items():
        relleno, borde, letra = ESTILO[tipo]
        estilo = (f"rounded=1;whiteSpace=wrap;html=1;fillColor={relleno};strokeColor={borde};"
                  f"fontColor={letra};fontSize={11 if w <= 60 else 12};")
        c.append(f'<mxCell id="{nid}" value={quoteattr(texto)} style="{estilo}" vertex="1" parent="1">'
                 f'<mxGeometry x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" as="geometry"/></mxCell>')
    for k, (o, d, etiqueta, punteado) in enumerate(arcos):
        estilo = ("endArrow=block;endFill=1;html=1;rounded=0;strokeColor=#374151;fontSize=11;"
                  "labelBackgroundColor=#ffffff;")
        estilo += "dashed=1;" if punteado else ""
        c.append(f'<mxCell id="e{k}" value={quoteattr(etiqueta)} style="{estilo}" edge="1" parent="1" '
                 f'source="{o}" target="{d}"><mxGeometry relative="1" as="geometry"/></mxCell>')
    for k, (tx, ty, texto, tam, negrita, ancla) in enumerate(textos):
        ancho = W - 60 if ancla == "start" else 320
        gx = {"start": tx, "middle": tx - ancho / 2, "end": tx - ancho}[ancla]
        alinear = {"start": "left", "middle": "center", "end": "right"}[ancla]
        estilo = (f"text;html=1;align={alinear};verticalAlign=middle;fontSize={tam};"
                  + ("fontStyle=1;" if negrita else ""))
        c.append(f'<mxCell id="t{k}" value={quoteattr(texto)} style="{estilo}" vertex="1" parent="1">'
                 f'<mxGeometry x="{gx}" y="{ty - 12}" width="{ancho}" height="24" as="geometry"/></mxCell>')
    return ('<mxfile host="app.diagrams.net"><diagram name="Red de turnos Siigo" id="red-siigo">'
            f'<mxGraphModel dx="{W}" dy="{H}" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" '
            f'arrows="1" fold="1" page="1" pageScale="1" pageWidth="{W}" pageHeight="{H}" math="0" shadow="0">'
            "<root>" + "".join(c) + "</root></mxGraphModel></diagram></mxfile>")


(SALIDA / "red_turnos_siigo.svg").write_text(generar_svg(), encoding="utf-8")
(SALIDA / "red_turnos_siigo.drawio").write_text(generar_drawio(), encoding="utf-8")
print(f"{len(nodos)} nodos, {len(arcos)} arcos → red_turnos_siigo.svg y red_turnos_siigo.drawio")
