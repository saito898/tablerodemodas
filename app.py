import base64
import io
import math

import numpy as np
import streamlit as st
from PIL import Image, ImageDraw, ImageFilter
from streamlit_drawable_canvas import st_canvas

st.set_page_config(
    page_title="Costurero Digital - Diseño de Modas",
    page_icon="🧵",
    layout="wide",
)

# =========================================================
# CSS: ambiente de costurero morado + fondo con patrones de hilo/aguja
# =========================================================
st.markdown("""
<style>
    /* Fondo base morado con textura de tela */
    .stApp {
        background-color: #2d1b4e;
        background-image:
            radial-gradient(circle at 20% 30%, rgba(168, 85, 247, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 70%, rgba(139, 92, 246, 0.12) 0%, transparent 50%),
            repeating-linear-gradient(45deg, transparent, transparent 10px, rgba(255,255,255,0.03) 10px, rgba(255,255,255,0.03) 20px),
            repeating-linear-gradient(-45deg, transparent, transparent 10px, rgba(255,255,255,0.03) 10px, rgba(255,255,255,0.03) 20px);
    }

    /* Título con estilo de letrero de costura */
    h1 {
        font-family: 'Georgia', serif;
        color: #e9d5ff;
        text-align: center;
        text-shadow: 0 0 20px rgba(168, 85, 247, 0.6), 2px 2px 4px rgba(0,0,0,0.5);
        border-bottom: 3px dashed #a855f7;
        padding-bottom: 10px;
        letter-spacing: 2px;
    }
    h2, h3 {
        font-family: 'Georgia', serif;
        color: #d8b4fe;
    }

    /* Sidebar oscura morada */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1233 0%, #2d1b4e 100%);
        border-right: 3px dashed #7e22ce;
    }
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span {
        color: #e9d5ff !important;
    }
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stSlider label,
    section[data-testid="stSidebar"] .stRadio label {
        color: #d8b4fe !important;
    }

    /* Botones */
    .stButton > button {
        background-color: #7e22ce;
        color: white;
        border-radius: 20px;
        border: 2px solid #a855f7;
        font-weight: bold;
        padding: 0.5em 1.5em;
        box-shadow: 0 0 10px rgba(168, 85, 247, 0.4);
    }
    .stButton > button:hover {
        background-color: #9333ea;
        color: #faf5ff;
        box-shadow: 0 0 20px rgba(168, 85, 247, 0.8);
    }

    /* Lienzo con marco de costurero */
    div[data-testid="stCanvas"] {
        border: 4px solid #a855f7;
        border-radius: 12px;
        box-shadow: 0 0 30px rgba(168, 85, 247, 0.5), inset 0 0 20px rgba(0,0,0,0.3);
        background: #1a0f2e;
        padding: 8px;
    }

    /* Caja descriptiva */
    .descripcion {
        background: linear-gradient(135deg, rgba(45, 27, 78, 0.9), rgba(30, 18, 51, 0.95));
        border-left: 5px solid #a855f7;
        padding: 12px 18px;
        border-radius: 8px;
        font-family: 'Georgia', serif;
        color: #e9d5ff;
        box-shadow: 0 0 15px rgba(168, 85, 247, 0.2);
    }
    .descripcion b { color: #c084fc; }

    /* Pie de página */
    .footer {
        text-align: center;
        color: #a78bfa;
        font-family: 'Georgia', serif;
        font-style: italic;
        padding: 10px;
        border-top: 2px dashed #7e22ce;
        margin-top: 20px;
    }

    /* Separadores decorativos con hilo */
    hr {
        border: none;
        border-top: 2px dashed #7e22ce;
    }
</style>
""", unsafe_allow_html=True)

st.title("🧵 Costurero Digital")
st.markdown(
    '<div class="descripcion">✂️ Tu taller de diseño. Elige una silueta realista, '
    'selecciona tu tela, ajusta el pincel y crea tu próximo boceto de moda.</div>',
    unsafe_allow_html=True,
)
st.write("")


# =========================================================
# SILUETA REALISTA (maniquí de modas, no palitos)
# =========================================================
def crear_maniqui(tipo: str, talla: str) -> Image.Image:
    """
    Genera una silueta de maniquí de modas realista usando curvas suaves
    y proporciones anatómicas. Sin palitos ni bolitas.
    """
    W, H = 600, 900
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    escala = {"Pequeña": 0.88, "Mediana": 1.0, "Grande": 1.12, "Extra Grande": 1.25}[talla]
    cx = W / 2
    color = (180, 150, 210, 255)  # morado claro para la silueta
    color_suave = (200, 175, 230, 180)

    def s(v):
        return v * escala

    # ---- CABEZA (óvalo más realista) ----
    cabeza_ancho, cabeza_alto = s(38), s(52)
    cabeza_y = s(55)
    draw.ellipse(
        [cx - cabeza_ancho, cabeza_y, cx + cabeza_ancho, cabeza_y + cabeza_alto],
        outline=color, width=3,
    )
    # Cuello suave
    cuello_y1 = cabeza_y + cabeza_alto
    cuello_y2 = cuello_y1 + s(35)
    draw.polygon(
        [
            (cx - s(14), cuello_y1), (cx + s(14), cuello_y1),
            (cx + s(18), cuello_y2), (cx - s(18), cuello_y2),
        ],
        outline=color, width=3,
    )

    # ---- HOMBROS Y TORSO (curvas Bézier aproximadas con polígonos suaves) ----
    hombro_y = cuello_y2 + s(5)
    if tipo == "Mujer":
        hombro_ancho = s(110)
        busto_y = hombro_y + s(60)
        busto_ancho = s(120)
        cintura_y = busto_y + s(80)
        cintura_ancho = s(75)
        cadera_y = cintura_y + s(70)
        cadera_ancho = s(125)
    else:
        hombro_ancho = s(145)
        busto_y = hombro_y + s(65)
        busto_ancho = s(135)
        cintura_y = busto_y + s(85)
        cintura_ancho = s(105)
        cadera_y = cintura_y + s(60)
        cadera_ancho = s(115)

    # Torso: puntos que forman una silueta suave
    torso_pts = [
        (cx - hombro_ancho, hombro_y),
        (cx - busto_ancho, busto_y),
        (cx - cintura_ancho, cintura_y),
        (cx - cadera_ancho * 0.9, cadera_y),
        (cx + cadera_ancho * 0.9, cadera_y),
        (cx + cintura_ancho, cintura_y),
        (cx + busto_ancho, busto_y),
        (cx + hombro_ancho, hombro_y),
    ]
    draw.polygon(torso_pts, outline=color, width=3)

    # Pecho femenino (dos curvas sutiles)
    if tipo == "Mujer":
        pecho_r = s(28)
        pecho_y = busto_y - s(10)
        draw.arc(
            [cx - s(55), pecho_y - pecho_r, cx - s(10), pecho_y + pecho_r],
            start=200, end=340, fill=color_suave, width=2,
        )
        draw.arc(
            [cx + s(10), pecho_y - pecho_r, cx + s(55), pecho_y + pecho_r],
            start=200, end=340, fill=color_suave, width=2,
        )

    # ---- BRAZOS (con forma, no líneas) ----
    # Brazo izquierdo: del hombro a la cadera
    brazo_ancho_sup = s(22)
    brazo_ancho_inf = s(14)
    codo_y = hombro_y + s(150)
    muneca_y = codo_y + s(140)

    # Brazo izquierdo
    brazo_izq_pts = [
        (cx - hombro_ancho + s(5), hombro_y + s(5)),
        (cx - hombro_ancho - s(15), hombro_y + s(20)),
        (cx - hombro_ancho - s(25), codo_y),
        (cx - hombro_ancho - s(10), muneca_y),
        (cx - hombro_ancho + s(5), muneca_y),
        (cx - hombro_ancho + s(10), codo_y),
        (cx - hombro_ancho + s(15), hombro_y + s(20)),
    ]
    draw.polygon(brazo_izq_pts, outline=color, width=2)

    # Brazo derecho (simétrico)
    brazo_der_pts = [
        (cx + hombro_ancho - s(5), hombro_y + s(5)),
        (cx + hombro_ancho + s(15), hombro_y + s(20)),
        (cx + hombro_ancho + s(25), codo_y),
        (cx + hombro_ancho + s(10), muneca_y),
        (cx + hombro_ancho - s(5), muneca_y),
        (cx + hombro_ancho - s(10), codo_y),
        (cx + hombro_ancho - s(15), hombro_y + s(20)),
    ]
    draw.polygon(brazo_der_pts, outline=color, width=2)

    # ---- PIERNAS (con muslo y pantorrilla) ----
    entrepierna_y = cadera_y + s(5)
    rodilla_y = entrepierna_y + s(180)
    tobillo_y = rodilla_y + s(200)

    # Pierna izquierda
    muslo_ancho = s(55)
    rodilla_ancho = s(30)
    tobillo_ancho = s(18)
    pierna_izq_pts = [
        (cx - cadera_ancho * 0.85, cadera_y),
        (cx - muslo_ancho, entrepierna_y + s(40)),
        (cx - muslo_ancho * 0.8, rodilla_y),
        (cx - tobillo_ancho, tobillo_y),
        (cx - tobillo_ancho + s(5), tobillo_y),
        (cx - rodilla_ancho, rodilla_y),
        (cx - muslo_ancho * 0.5, entrepierna_y + s(20)),
        (cx - s(15), entrepierna_y),
    ]
    draw.polygon(pierna_izq_pts, outline=color, width=2)

    # Pierna derecha
    pierna_der_pts = [
        (cx + cadera_ancho * 0.85, cadera_y),
        (cx + muslo_ancho, entrepierna_y + s(40)),
        (cx + muslo_ancho * 0.8, rodilla_y),
        (cx + tobillo_ancho, tobillo_y),
        (cx + tobillo_ancho - s(5), tobillo_y),
        (cx + rodilla_ancho, rodilla_y),
        (cx + muslo_ancho * 0.5, entrepierna_y + s(20)),
        (cx + s(15), entrepierna_y),
    ]
    draw.polygon(pierna_der_pts, outline=color, width=2)

    # Pies
    pie_y = tobillo_y
    draw.ellipse([cx - s(40), pie_y, cx - s(5), pie_y + s(20)], outline=color, width=2)
    draw.ellipse([cx + s(5), pie_y, cx + s(40), pie_y + s(20)], outline=color, width=2)

    return img


def pil_a_data_uri(img: Image.Image) -> str:
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    encoded = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{encoded}"


# =========================================================
# FONDO DEL COSTURERO CON HILOS Y AGUJAS (decorativo)
# =========================================================
def crear_fondo_costurero(ancho: int, alto: int, color_base: str) -> Image.Image:
    """Genera un fondo con patrón de hilos y agujas sutiles."""
    img = Image.new("RGBA", (ancho, alto), color_base)
    draw = ImageDraw.Draw(img)

    # Líneas de hilo diagonales suaves (color morado tenue)
    color_hilo = (168, 85, 247, 25)
    for i in range(-alto, ancho, 80):
        draw.line([(i, 0), (i + alto, alto)], fill=color_hilo, width=1)
    for i in range(-alto, ancho, 80):
        draw.line([(i + alto, 0), (i, alto)], fill=color_hilo, width=1)

    # Pequeñas "agujas" decorativas en las esquinas
    color_aguja = (168, 85, 247, 40)
    # Aguja superior izquierda
    draw.line([(30, 30), (80, 100)], fill=color_aguja, width=2)
    draw.ellipse([75, 95, 85, 105], outline=color_aguja, width=1)
    # Aguja inferior derecha
    draw.line([(ancho - 80, alto - 100), (ancho - 30, alto - 30)], fill=color_aguja, width=2)
    draw.ellipse([ancho - 85, alto - 105, ancho - 75, alto - 95], outline=color_aguja, width=1)

    # Botones decorativos dispersos (círculos con 4 huecos)
    posiciones_botones = [(60, alto - 80), (ancho - 70, 70), (ancho // 2, 40)]
    for bx, by in posiciones_botones:
        r = 12
        draw.ellipse([bx - r, by - r, bx + r, by + r], outline=(168, 85, 247, 50), width=2)
        for dx, dy in [(-4, -4), (4, -4), (-4, 4), (4, 4)]:
            draw.ellipse([bx + dx - 2, by + dy - 2, bx + dx + 2, by + dy + 2], fill=(168, 85, 247, 40))

    # Aplicar desenfoque suave para que no compita con el dibujo
    img = img.filter(ImageFilter.GaussianBlur(radius=0.8))
    return img


# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.header("🧵 Panel del Costurero")
    st.markdown("---")

    st.subheader("👗 Silueta")
    tipo_cuerpo = st.radio("Tipo de cuerpo:", ["Mujer", "Hombre"], horizontal=True)
    talla = st.select_slider(
        "Tallaje:",
        options=["Pequeña", "Mediana", "Grande", "Extra Grande"],
        value="Mediana",
    )
    mostrar_silueta = st.checkbox("Mostrar maniquí de fondo", value=True)

    st.markdown("---")
    st.subheader("✏️ Pincel")
    drawing_mode = st.selectbox(
        "Modo de dibujo:",
        ["freedraw", "line", "rect", "circle", "transform"],
        format_func=lambda x: {
            "freedraw": "✍️ Trazo libre",
            "line": "📏 Línea",
            "rect": "⬛ Rectángulo",
            "circle": "⭕ Círculo",
            "transform": "🖐️ Mover",
        }[x],
    )
    stroke_width = st.slider("Grosor del trazo:", 1, 30, 4)
    stroke_color = st.color_picker("Color del trazo:", "#d8b4fe")

    st.markdown("---")
    st.subheader("🧶 Telas")
    telas = {
        "Papel de boceto": {"bg": "#FFFFFF", "color": "#4c1d95", "nombre": "📄 Papel"},
        "Lavanda": {"bg": "#E6E6FA", "color": "#6b21a8", "nombre": "💜 Lavanda"},
        "Amatista": {"bg": "#9966CC", "color": "#FFFFFF", "nombre": "🔮 Amatista"},
        "Malva": {"bg": "#E0B0FF", "color": "#4c1d95", "nombre": "🌸 Malva"},
        "Uva oscura": {"bg": "#4A1A6B", "color": "#E9D5FF", "nombre": "🍇 Uva"},
        "Orquídea": {"bg": "#DA70D6", "color": "#FFFFFF", "nombre": "🌺 Orquídea"},
        "Ciruela": {"bg": "#8E4585", "color": "#FDF4FF", "nombre": "🫐 Ciruela"},
        "Lila suave": {"bg": "#F3E8FF", "color": "#7e22ce", "nombre": "🪻 Lila"},
    }

    tela_sel = st.selectbox(
        "Selecciona tu tela:",
        options=list(telas.keys()),
        format_func=lambda x: telas[x]["nombre"],
    )
    usar_color_tela = st.checkbox("Usar color de tela como trazo", value=False)
    if usar_color_tela:
        stroke_color = telas[tela_sel]["color"]
    bg_color = telas[tela_sel]["bg"]

    st.markdown("---")
    st.subheader("📐 Acciones")
    if st.button("🗑️ Limpiar lienzo", use_container_width=True):
        st.session_state["canvas_key"] = st.session_state.get("canvas_key", 0) + 1
        st.rerun()

    st.markdown("---")
    st.info("💡 **Tip:** Dibuja sobre el maniquí. Cambia de tela para inspirarte.")


# =========================================================
# LIENZO
# =========================================================
ancho_canvas, alto_canvas = 600, 850

# Fondo base: color de tela + patrón de costurero
fondo = crear_fondo_costurero(ancho_canvas, alto_canvas, bg_color)

# Superponer maniquí si está activado
if mostrar_silueta:
    maniqui = crear_maniqui(tipo_cuerpo, talla)
    maniqui = maniqui.resize((ancho_canvas, alto_canvas), Image.LANCZOS)
    fondo = Image.alpha_composite(fondo, maniqui)

fondo_uri = pil_a_data_uri(fondo)

if "canvas_key" not in st.session_state:
    st.session_state["canvas_key"] = 0

col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    canvas_result = st_canvas(
        fill_color="rgba(168, 85, 247, 0.15)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        background_image=fondo_uri,
        height=alto_canvas,
        width=ancho_canvas,
        drawing_mode=drawing_mode,
        update_streamlit=True,
        return_image_data=True,  # <-- CRÍTICO para evitar el RuntimeError
        key=f"canvas_{st.session_state['canvas_key']}",
    )

st.write("")
st.markdown(
    f'<div class="descripcion">🧵 <b>Tela:</b> {telas[tela_sel]["nombre"]} | '
    f'<b>Silueta:</b> {tipo_cuerpo} — Talla {talla} | '
    f'<b>Modo:</b> {drawing_mode}</div>',
    unsafe_allow_html=True,
)

# =========================================================
# DESCARGA
# =========================================================
if canvas_result.image_data is not None:
    st.write("")
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        arr = np.array(canvas_result.image_data).astype("uint8")
        dibujo = Image.fromarray(arr, "RGBA")
        resultado = Image.alpha_composite(fondo.copy(), dibujo)

        buf = io.BytesIO()
        resultado.save(buf, format="PNG")
        st.download_button(
            label="💾 Descargar mi diseño",
            data=buf.getvalue(),
            file_name=f"diseno_{tipo_cuerpo}_{talla}.png",
            mime="image/png",
            use_container_width=True,
        )

st.markdown('<div class="footer">✂️ Costurero Digital — Donde tu creatividad cobra vida</div>', unsafe_allow_html=True)
