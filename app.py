
import io
import math

import numpy as np
import streamlit as st
from PIL import Image, ImageDraw
from streamlit_drawable_canvas import st_canvas

st.set_page_config(
    page_title="Atelier | Costurero Digital",
    page_icon="🧵",
    layout="wide",
)

# ==========================================================
# PALETA Y ESTILO DEL ATELIER
# ==========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@500;600;700&display=swap');

:root {
    --cream: #f7f1e8;
    --paper: #fffdf8;
    --ink: #3d332f;
    --muted: #8a7970;
    --rose: #c47d83;
    --rose-dark: #9f5e67;
    --sage: #899985;
    --wood: #a77755;
    --line: #e5d8ca;
}

.stApp {
    background:
        radial-gradient(ellipse at top left, #fffaf3 0%, transparent 50%),
        linear-gradient(135deg, #f7f1e8 0%, #eee3d7 100%);
    color: var(--ink);
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1500px;
    padding-top: 1.6rem;
    padding-bottom: 3rem;
}

#MainMenu, footer {
    visibility: hidden;
}

h1, h2, h3 {
    color: var(--ink);
}

h1 {
    font-family: 'Playfair Display', serif;
    letter-spacing: -1px;
}

h2, h3 {
    font-family: 'Playfair Display', serif;
}

section[data-testid="stSidebar"] {
    background: #eee3d7;
    border-right: 1px solid #ddcabb;
}

section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p {
    color: #51423b;
}

.atelier-header {
    background: #fffaf3;
    border: 1px solid #e3d4c4;
    border-radius: 18px;
    padding: 27px 32px;
    margin-bottom: 22px;
    box-shadow: 0 6px 20px rgba(90, 63, 45, .06);
    position: relative;
    overflow: hidden;
}

.atelier-header:after {
    content: "✂";
    position: absolute;
    right: 30px;
    top: 12px;
    font-size: 74px;
    color: #ead8d0;
    transform: rotate(-18deg);
}

.brand-eyebrow {
    text-transform: uppercase;
    letter-spacing: 4px;
    font-size: 10px;
    font-weight: 800;
    color: var(--rose-dark);
    margin-bottom: 7px;
}

.brand-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(35px, 4vw, 52px);
    font-weight: 600;
    color: #47362f;
    line-height: 1.15;
}

.brand-subtitle {
    margin-top: 8px;
    color: #88766a;
    font-size: 14px;
    max-width: 680px;
}

.atelier-label {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #9f6b68;
    margin-bottom: 8px;
}

.work-card {
    background: #fffdf8;
    border: 1px solid #e3d6c8;
    border-radius: 15px;
    padding: 17px;
    box-shadow: 0 5px 15px rgba(80, 57, 41, .045);
    margin-bottom: 15px;
}

.work-title {
    font-family: 'Playfair Display', serif;
    font-size: 20px;
    font-weight: 600;
    color: #483832;
    margin-bottom: 4px;
}

.work-subtitle {
    color: #938176;
    font-size: 12px;
    margin-bottom: 10px;
}

.fabric-board {
    background: #fffaf3;
    border: 1px solid #e2d2c1;
    border-radius: 15px;
    padding: 17px;
    margin-bottom: 16px;
}

.fabric-heading {
    font-family: 'Playfair Display', serif;
    font-size: 21px;
    font-weight: 600;
    color: #493a33;
    margin-bottom: 4px;
}

.fabric-caption {
    color: #8c7a6d;
    font-size: 12px;
    margin-bottom: 14px;
}

.tool-note {
    background: #f0e6dc;
    border-left: 4px solid #c47d83;
    border-radius: 6px;
    padding: 12px 14px;
    color: #655148;
    font-size: 13px;
    line-height: 1.6;
    margin: 10px 0 17px;
}

.measure-card {
    background: #f8f1e8;
    border: 1px dashed #cbb4a3;
    border-radius: 10px;
    padding: 12px;
    text-align: center;
}

.measure-number {
    font-family: 'Playfair Display', serif;
    font-size: 23px;
    color: #9f5e67;
    font-weight: 700;
}

.measure-label {
    font-size: 10px;
    color: #89766b;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.stButton > button {
    background: #fffaf3;
    border: 1px solid #d9c5b5;
    color: #58443a;
    border-radius: 10px;
    font-weight: 700;
    min-height: 42px;
    transition: .18s ease;
}

.stButton > button:hover {
    background: #f3e4dd;
    border-color: #c47d83;
    color: #70484a;
}

.stButton > button[kind="primary"] {
    background: #ad6d73;
    color: white;
    border-color: #ad6d73;
}

.stButton > button[kind="primary"]:hover {
    background: #95575f;
    color: white;
}

[data-testid="stMetric"] {
    background: #fffaf3;
    border: 1px solid #e3d6c8;
    border-radius: 12px;
    padding: 12px;
}

[data-testid="stMetricValue"] {
    color: #9f5e67;
}

[data-testid="stExpander"] {
    background: #fffaf3;
    border: 1px solid #e3d6c8;
    border-radius: 10px;
}

hr {
    border-color: #e0d0c2;
}

.atelier-footer {
    text-align: center;
    color: #9a8274;
    font-family: 'Playfair Display', serif;
    font-style: italic;
    border-top: 1px solid #ddcabb;
    margin-top: 30px;
    padding-top: 20px;
}

div[data-testid="stCanvas"] {
    border: 1px solid #d9c8b8;
    border-radius: 5px;
    box-shadow: 0 7px 18px rgba(76, 52, 38, .13);
}

@media(max-width: 800px) {
    .atelier-header {
        padding: 20px;
    }

    .atelier-header:after {
        font-size: 45px;
        right: 15px;
    }
}
</style>
""", unsafe_allow_html=True)


# ==========================================================
# CABECERA
# ==========================================================

st.markdown("""
<div class="atelier-header">
    <div class="brand-eyebrow">Estudio de diseño · Patronaje · Textiles</div>
    <div class="brand-title">Atelier</div>
    <div class="brand-subtitle">
        Tu costurero digital. Explora siluetas, combina tejidos y dibuja
        tus ideas de moda en tu propio estudio de diseño.
    </div>
</div>
""", unsafe_allow_html=True)


# ==========================================================
# FUNCIONES DE DIBUJO DEL FIGURÍN
# ==========================================================

CANVAS_W = 600
CANVAS_H = 820


def curva_bezier(p0, p1, p2, p3, pasos=24):
    """Devuelve puntos de una curva Bézier cúbica."""
    puntos = []
    for i in range(pasos + 1):
        t = i / pasos
        u = 1 - t
        x = (
            u**3 * p0[0]
            + 3 * u**2 * t * p1[0]
            + 3 * u * t**2 * p2[0]
            + t**3 * p3[0]
        )
        y = (
            u**3 * p0[1]
            + 3 * u**2 * t * p1[1]
            + 3 * u * t**2 * p2[1]
            + t**3 * p3[1]
        )
        puntos.append((x, y))
    return puntos


def dibujar_curva(draw, puntos, fill, width=2):
    draw.line(puntos, fill=fill, width=width, joint="curve")


def crear_figurin(complexion="Media", tipo="Mujer"):
    """
    Crea un figurín de moda de tamaño constante.
    La complexión cambia las proporciones corporales, no la escala total.
    """
    img = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    tinta = (104, 87, 78, 225)
    tinta_suave = (165, 140, 125, 155)
    guia = (191, 170, 153, 95)

    cx = CANVAS_W // 2

    # Las proporciones cambian, pero la altura y posición general no.
    proporciones = {
        "Delgada": {
            "hombro": 61, "busto": 48, "cintura": 31, "cadera": 48,
            "brazo": 13, "muslo": 25
        },
        "Media": {
            "hombro": 66, "busto": 55, "cintura": 39, "cadera": 57,
            "brazo": 16, "muslo": 30
        },
        "Robusta": {
            "hombro": 72, "busto": 66, "cintura": 54, "cadera": 69,
            "brazo": 20, "muslo": 37
        }
    }

    p = proporciones[complexion]

    # Línea central de referencia.
    draw.line((cx, 65, cx, 760), fill=guia, width=1)

    # Cabeza: óvalo elegante de figurín.
    head_box = (cx - 22, 48, cx + 22, 104)
    draw.ellipse(head_box, outline=tinta, width=2)

    # Rasgos mínimos, estilo ilustración de moda.
    draw.arc(
        (cx - 13, 65, cx + 13, 92),
        start=205, end=335, fill=tinta_suave, width=1
    )

    # Cuello.
    draw.line((cx - 10, 104, cx - 13, 126), fill=tinta, width=2)
    draw.line((cx + 10, 104, cx + 13, 126), fill=tinta, width=2)

    # Hombros.
    shoulder_y = 135
    shoulder_l = cx - p["hombro"]
    shoulder_r = cx + p["hombro"]

    # Torso con curvas anatómicas.
    if tipo == "Mujer":
        left_torso = []
        left_torso += curva_bezier(
            (cx - 13, 124), (cx - 33, 123),
            (shoulder_l - 7, 127), (shoulder_l, 147)
        )
        left_torso += curva_bezier(
            (shoulder_l, 147), (cx - p["busto"] - 9, 169),
            (cx - p["busto"] - 7, 190), (cx - p["busto"], 210)
        )
        left_torso += curva_bezier(
            (cx - p["busto"], 210), (cx - p["cintura"] - 8, 235),
            (cx - p["cintura"] - 5, 257), (cx - p["cintura"], 280)
        )
        left_torso += curva_bezier(
            (cx - p["cintura"], 280), (cx - p["cintura"] - 3, 300),
            (cx - p["cadera"] - 3, 315), (cx - p["cadera"], 336)
        )

        right_torso = []
        right_torso += curva_bezier(
            (cx + p["cadera"], 336), (cx + p["cadera"] + 3, 315),
            (cx + p["cintura"] + 3, 300), (cx + p["cintura"], 280)
        )
        right_torso += curva_bezier(
            (cx + p["cintura"], 280), (cx + p["cintura"] + 5, 257),
            (cx + p["cintura"] + 8, 235), (cx + p["busto"], 210)
        )
        right_torso += curva_bezier(
            (cx + p["busto"], 210), (cx + p["busto"] + 7, 190),
            (cx + p["busto"] + 9, 169), (shoulder_r, 147)
        )
        right_torso += curva_bezier(
            (shoulder_r, 147), (shoulder_r + 7, 127),
            (cx + 33, 123), (cx + 13, 124)
        )

    else:
        left_torso = []
        left_torso += curva_bezier(
            (cx - 13, 124), (cx - 35, 124),
            (shoulder_l - 6, 128), (shoulder_l, 148)
        )
        left_torso += curva_bezier(
            (shoulder_l, 148), (cx - p["busto"], 172),
            (cx - p["busto"] + 3, 200), (cx - p["cintura"], 255)
        )
        left_torso += curva_bezier(
            (cx - p["cintura"], 255), (cx - p["cintura"], 278),
            (cx - p["cadera"], 308), (cx - p["cadera"], 330)
        )

        right_torso = []
        right_torso += curva_bezier(
            (cx + p["cadera"], 330), (cx + p["cadera"], 308),
            (cx + p["cintura"], 278), (cx + p["cintura"], 255)
        )
        right_torso += curva_bezier(
            (cx + p["cintura"], 255), (cx + p["busto"] - 3, 200),
            (cx + p["busto"], 172), (shoulder_r, 148)
        )
        right_torso += curva_bezier(
            (shoulder_r, 148), (shoulder_r + 6, 128),
            (cx + 35, 124), (cx + 13, 124)
        )

    # Línea del cuerpo.
    dibujar_curva(draw, left_torso, tinta, 2)
    dibujar_curva(draw, right_torso, tinta, 2)

    # Líneas guía de hombros, pecho, cintura y cadera.
    draw.line((cx - p["busto"], 207, cx + p["busto"], 207), fill=guia, width=1)
    draw.line((cx - p["cintura"], 280, cx + p["cintura"], 280), fill=guia, width=1)
    draw.line((cx - p["cadera"], 336, cx + p["cadera"], 336), fill=guia, width=1)

    # Brazos: contornos curvos, no líneas rectas.
    arm_outer_l = curva_bezier(
        (shoulder_l + 5, 145),
        (shoulder_l - 24, 165),
        (cx - p["hombro"] - 28, 217),
        (cx - p["hombro"] - 22, 263)
    )
    arm_outer_l += curva_bezier(
        (cx - p["hombro"] - 22, 263),
        (cx - p["hombro"] - 17, 282),
        (cx - p["hombro"] - 12, 299),
        (cx - p["hombro"] - 5, 312)
    )
    arm_inner_l = curva_bezier(
        (cx - p["hombro"] - 5, 312),
        (cx - p["hombro"] + 3, 296),
        (cx - p["hombro"] - 1, 277),
        (cx - p["hombro"] - 6, 258)
    )
    arm_inner_l += curva_bezier(
        (cx - p["hombro"] - 6, 258),
        (cx - p["hombro"] - 7, 220),
        (shoulder_l + 17, 177),
        (shoulder_l + 14, 153)
    )
    dibujar_curva(draw, arm_outer_l, tinta, 2)
    dibujar_curva(draw, arm_inner_l, tinta, 2)

    # Brazo derecho simétrico.
    def espejo(puntos):
        return [(2 * cx - x, y) for x, y in puntos]

    dibujar_curva(draw, espejo(arm_outer_l), tinta, 2)
    dibujar_curva(draw, espejo(arm_inner_l), tinta, 2)

    # Piernas con rodillas, pantorrillas y tobillos.
    crotch_y = 340
    knee_y = 530
    ankle_y = 714
    thigh = p["muslo"]

    # Pierna izquierda.
    leg_l = []
    leg_l += curva_bezier(
        (cx - p["cadera"], 336),
        (cx - p["cadera"] - 3, 372),
        (cx - thigh - 7, 400),
        (cx - thigh, 433)
    )
    leg_l += curva_bezier(
        (cx - thigh, 433),
        (cx - thigh + 2, 465),
        (cx - thigh + 4, 499),
        (cx - thigh + 1, knee_y)
    )
    leg_l += curva_bezier(
        (cx - thigh + 1, knee_y),
        (cx - thigh + 8, 585),
        (cx - 24, 648),
        (cx - 20, ankle_y)
    )

    leg_r = []
    leg_r += curva_bezier(
        (cx - 20, ankle_y),
        (cx - 16, 648),
        (cx - 10, 585),
        (cx - 12, knee_y)
    )
    leg_r += curva_bezier(
        (cx - 12, knee_y),
        (cx - 13, 499),
        (cx - 12, 465),
        (cx - 14, 433)
    )
    leg_r += curva_bezier(
        (cx - 14, 433),
        (cx - 17, 400),
        (cx - 8, 367),
        (cx, crotch_y)
    )

    dibujar_curva(draw, leg_l, tinta, 2)
    dibujar_curva(draw, leg_r, tinta, 2)

    # Pierna derecha.
    dibujar_curva(draw, espejo(leg_l), tinta, 2)
    dibujar_curva(draw, espejo(leg_r), tinta, 2)

    # Línea de rodilla y tobillo para facilitar el dibujo de prendas.
    draw.line((cx - thigh + 4, knee_y, cx - 12, knee_y), fill=guia, width=1)
    draw.line((cx + 12, knee_y, cx + thigh - 4, knee_y), fill=guia, width=1)
    draw.line((cx - 22, ankle_y, cx + 22, ankle_y), fill=guia, width=1)

    # Pies estilizados.
    draw.line((cx - 20, ankle_y, cx - 32, 728, cx - 10, 732), fill=tinta, width=2)
    draw.line((cx + 20, ankle_y, cx + 32, 728, cx + 10, 732), fill=tinta, width=2)

    # Referencias pequeñas de patronaje.
    draw.line((cx - 115, 145, cx - 80, 145), fill=guia, width=1)
    draw.line((cx + 80, 145, cx + 115, 145), fill=guia, width=1)

    return img


# ==========================================================
# PAPEL DE PATRONAJE
# ==========================================================

def crear_papel():
    img = Image.new("RGBA", (CANVAS_W, CANVAS_H), (255, 253, 248, 255))
    draw = ImageDraw.Draw(img)

    # Cuadrícula sutil.
    for x in range(0, CANVAS_W, 25):
        draw.line((x, 0, x, CANVAS_H), fill=(224, 211, 196, 100), width=1)

    for y in range(0, CANVAS_H, 25):
        draw.line((0, y, CANVAS_W, y), fill=(224, 211, 196, 100), width=1)

    # Borde interior de hoja.
    draw.rectangle(
        (12, 12, CANVAS_W - 13, CANVAS_H - 13),
        outline=(209, 190, 171, 180),
        width=1
    )
    return img


# ==========================================================
# MUESTRAS DE TELAS
# ==========================================================

telas = {
    "Rosa empolvado": {"color": "#C98791", "emoji": "🌸", "textura": "Sarga suave"},
    "Verde salvia": {"color": "#849780", "emoji": "🌿", "textura": "Lino"},
    "Azul noche": {"color": "#344A67", "emoji": "🌌", "textura": "Denim"},
    "Lavanda": {"color": "#B4A0CC", "emoji": "🪻", "textura": "Satén"},
    "Terracota": {"color": "#BD765B", "emoji": "🧶", "textura": "Algodón"},
    "Amarillo mantequilla": {"color": "#E9CE86", "emoji": "🌼", "textura": "Popelina"},
    "Chocolate": {"color": "#705044", "emoji": "🤎", "textura": "Paño"},
    "Negro": {"color": "#302E32", "emoji": "🖤", "textura": "Crepé"},
    "Blanco": {"color": "#F6F1E8", "emoji": "🤍", "textura": "Muselina"},
    "Rojo cereza": {"color": "#A94252", "emoji": "🍒", "textura": "Terciopelo"},
    "Lila": {"color": "#D1B6D9", "emoji": "💜", "textura": "Gasa"},
    "Caramelo": {"color": "#C28D57", "emoji": "🧵", "textura": "Lona"},
}


# ==========================================================
# SIDEBAR: HERRAMIENTAS
# ==========================================================

with st.sidebar:
    st.markdown("## 🧵 Mesa de trabajo")
    st.caption("Personaliza tu figurín y prepara tus materiales.")
    st.divider()

    st.markdown("### 👗 Figurín")

    tipo_cuerpo = st.radio(
        "Plantilla",
        ["Mujer", "Hombre"],
        horizontal=True
    )

    complexion = st.select_slider(
        "Complexión corporal",
        options=["Delgada", "Media", "Robusta"],
        value="Media"
    )

    st.caption(
        "La complexión modifica las proporciones del cuerpo, "
        "manteniendo el figurín en la misma escala."
    )

    st.divider()
    st.markdown("### ✏️ Herramientas de diseño")

    drawing_mode = st.selectbox(
        "Herramienta",
        ["freedraw", "line", "rect", "circle"],
        format_func=lambda x: {
            "freedraw": "✍️ Lápiz / pincel",
            "line": "📏 Línea",
            "rect": "▰ Rectángulo",
            "circle": "⭕ Elipse",
        }[x]
    )

    stroke_width = st.slider(
        "Grosor del trazo",
        min_value=1,
        max_value=24,
        value=4
    )

    color_manual = st.color_picker(
        "Color personalizado",
        "#C98791"
    )

    usar_tela = st.checkbox(
        "Dibujar con la tela seleccionada",
        value=True
    )

    st.divider()
    st.markdown("### 📐 Referencias de medidas")

    altura_cm = st.number_input(
        "Altura de referencia (cm)",
        min_value=130,
        max_value=220,
        value=168,
        step=1
    )

    # Valores orientativos de referencia, no mediciones corporales reales.
    datos_medidas = {
        "Delgada": {"Busto": 82, "Cintura": 64, "Cadera": 88},
        "Media": {"Busto": 92, "Cintura": 76, "Cadera": 100},
        "Robusta": {"Busto": 108, "Cintura": 94, "Cadera": 114},
    }

    medidas = datos_medidas[complexion]

    st.markdown(
        f"""
        <div class="measure-card">
            <div class="measure-label">Medidas orientativas</div>
            <div class="measure-number">{medidas["Busto"]} cm</div>
            <div class="measure-label">Busto</div>
            <hr>
            <div class="measure-number">{medidas["Cintura"]} cm</div>
            <div class="measure-label">Cintura</div>
            <hr>
            <div class="measure-number">{medidas["Cadera"]} cm</div>
            <div class="measure-label">Cadera</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption(
        "Son referencias ilustrativas según la complexión elegida, "
        "no medidas tomadas de una persona."
    )

    st.divider()

    if st.button("🗑️ Nuevo diseño", use_container_width=True):
        st.session_state["design_version"] = (
            st.session_state.get("design_version", 0) + 1
        )
        st.rerun()


# ==========================================================
# ÁREA PRINCIPAL
# ==========================================================

if "design_version" not in st.session_state:
    st.session_state["design_version"] = 0

col_editor, col_tools = st.columns([1.65, 1], gap="large")


# ==========================================================
# EDITOR DE FIGURÍN
# ==========================================================

with col_editor:
    st.markdown("""
    <div class="work-card">
        <div class="atelier-label">01 · Mesa de patronaje</div>
        <div class="work-title">Tu figurín de moda</div>
        <div class="work-subtitle">
            Dibuja sobre el papel, crea siluetas de prendas y prueba combinaciones de color.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # El fondo siempre es papel, nunca cambia al elegir otra tela.
    papel = crear_papel()

    figurin = crear_figurin(
        complexion=complexion,
        tipo=tipo_cuerpo
    )

    fondo_editor = Image.alpha_composite(papel, figurin)

    # La muestra textil solo modifica el color del pincel.
    tela_nombre = st.session_state.get("tela_seleccionada", "Rosa empolvado")
    color_tela = telas[tela_nombre]["color"]
    color_trazo = color_tela if usar_tela else color_manual

    # El componente acepta una imagen PIL como fondo.
    canvas_result = st_canvas(
        fill_color=color_trazo + "26",
        stroke_width=stroke_width,
        stroke_color=color_trazo,
        background_image=fondo_editor.convert("RGB"),
        width=CANVAS_W,
        height=CANVAS_H,
        drawing_mode=drawing_mode,
        update_streamlit=True,
        key=f"atelier_canvas_{st.session_state['design_version']}",
    )

    st.markdown(
        f"""
        <div class="tool-note">
            <b>Material activo:</b> {tela_nombre} · {telas[tela_nombre]["textura"]}<br>
            <b>Complexión:</b> {complexion} · <b>Altura de referencia:</b> {altura_cm} cm<br>
            El papel permanece fijo. La muestra seleccionada cambia el color de tus trazos.
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# MUESTRARIO TEXTIL
# ==========================================================

with col_tools:
    st.markdown("""
    <div class="fabric-board">
        <div class="atelier-label">02 · Biblioteca de materiales</div>
        <div class="fabric-heading">Muestrario textil</div>
        <div class="fabric-caption">
            Selecciona una tela para utilizar su color en tu diseño.
        </div>
    </div>
    """, unsafe_allow_html=True)

    nombres_telas = list(telas.keys())
    filas = [nombres_telas[i:i + 2] for i in range(0, len(nombres_telas), 2)]

    for fila in filas:
        swatch_cols = st.columns(2)

        for col, nombre in zip(swatch_cols, fila):
            with col:
                color = telas[nombre]["color"]
                activo = (
                    st.session_state.get("tela_seleccionada", "Rosa empolvado")
                    == nombre
                )

                borde = "#9f5e67" if activo else "#dfcfc0"
                grosor = "3px" if activo else "1px"

                st.markdown(
                    f"""
                    <div style="
                        background:#fffaf3;
                        border:1px solid #e3d6c8;
                        border-radius:12px;
                        padding:8px;
                        margin-bottom:5px;
                    ">
                        <div style="
                            height:55px;
                            background-color:{color};
                            border:{grosor} solid {borde};
                            border-radius:7px;
                            background-image:
                                repeating-linear-gradient(
                                    45deg,
                                    rgba(255,255,255,.09) 0px,
                                    rgba(255,255,255,.09) 2px,
                                    transparent 2px,
                                    transparent 7px
                                );
                        "></div>
                        <div style="
                            font-size:12px;
                            font-weight:800;
                            color:#51423b;
                            margin-top:7px;
                        ">{nombre}</div>
                        <div style="
                            font-size:10px;
                            color:#9b887b;
                        ">{telas[nombre]["textura"]}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if st.button(
                    "Seleccionar" if not activo else "✓ Seleccionada",
                    key=f"tela_{nombre}",
                    use_container_width=True
                ):
                    st.session_state["tela_seleccionada"] = nombre
                    st.rerun()

    st.markdown("""
    <div class="work-card">
        <div class="atelier-label">03 · Herramientas del taller</div>
        <div class="work-title">Consejos de diseño</div>
        <div class="work-subtitle">
            Empieza por el contorno de la prenda y después añade detalles,
            costuras, mangas, cuellos y accesorios.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="tool-note">
        <b>✂️ Consejo:</b> usa un trazo fino para los detalles y uno más grueso
        para definir los bordes de la prenda. Puedes cambiar de tela entre trazos
        para combinar colores.
    </div>
    """, unsafe_allow_html=True)


# ==========================================================
# DESCARGA DEL DISEÑO
# ==========================================================

st.divider()

st.markdown("""
<div class="work-card">
    <div class="atelier-label">04 · Colección personal</div>
    <div class="work-title">Guarda tu creación</div>
    <div class="work-subtitle">
        Descarga tu figurín con el papel de patronaje y los trazos realizados.
    </div>
</div>
""", unsafe_allow_html=True)

if canvas_result.image_data is not None:
    arr = np.asarray(canvas_result.image_data).astype("uint8")
    resultado = Image.fromarray(arr)

    # Garantizar modo compatible para exportación.
    if resultado.mode not in ("RGB", "RGBA"):
        resultado = resultado.convert("RGBA")

    buf = io.BytesIO()
    resultado.save(buf, format="PNG")

    col_blank, col_download, col_blank2 = st.columns([1, 2, 1])

    with col_download:
        st.download_button(
            label="💾 Descargar diseño en PNG",
            data=buf.getvalue(),
            file_name=f"atelier_{tipo_cuerpo}_{complexion.lower()}.png",
            mime="image/png",
            use_container_width=True,
            type="primary"
        )
else:
    st.info("Empieza a dibujar para preparar tu primer diseño descargable.")


# ==========================================================
# PIE DE PÁGINA
# ==========================================================

st.markdown("""
<div class="atelier-footer">
    Atelier · Diseña, combina, crea.
    <div style="font-family:'DM Sans',sans-serif;font-size:11px;margin-top:6px;">
        Tu creatividad es el patrón de cada nueva idea.
    </div>
</div>
""", unsafe_allow_html=True)
