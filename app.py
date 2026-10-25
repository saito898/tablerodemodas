import base64
import io

import numpy as np
import streamlit as st
from PIL import Image, ImageDraw
from streamlit_drawable_canvas import st_canvas

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Costurero Digital - Diseño de Modas",
    page_icon="🧵",
    layout="wide",
)

# ---------------------------------------------------------
# CSS AMBIENTACIÓN COSTURERO MORADO
# ---------------------------------------------------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f3e8ff 0%, #e9d5ff 50%, #d8b4fe 100%);
    }
    h1 {
        font-family: 'Georgia', serif;
        color: #6b21a8;
        text-align: center;
        text-shadow: 1px 1px 3px rgba(107, 33, 168, 0.2);
        border-bottom: 3px dashed #a855f7;
        padding-bottom: 10px;
    }
    h2, h3 {
        font-family: 'Georgia', serif;
        color: #6b21a8;
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #faf5ff 0%, #f3e8ff 100%);
        border-right: 2px dashed #c084fc;
    }
    .stButton > button {
        background-color: #7e22ce;
        color: white;
        border-radius: 20px;
        border: 2px solid #6b21a8;
        font-weight: bold;
        padding: 0.5em 1.5em;
    }
    .stButton > button:hover {
        background-color: #6b21a8;
        color: #faf5ff;
    }
    div[data-testid="stCanvas"] {
        border: 3px solid #a855f7;
        border-radius: 10px;
        box-shadow: 5px 5px 15px rgba(107, 33, 168, 0.25);
        background: white;
        padding: 5px;
    }
    .descripcion {
        background-color: rgba(255, 255, 255, 0.75);
        border-left: 5px solid #9333ea;
        padding: 10px 15px;
        border-radius: 5px;
        font-family: 'Georgia', serif;
        color: #4c1d95;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# TÍTULO
# ---------------------------------------------------------
st.title("🧵 Costurero Digital")
st.markdown(
    '<div class="descripcion">✂️ Bienvenido a tu taller de diseño. Elige una silueta, '
    'selecciona tu tela favorita, ajusta tu pincel y da rienda suelta a tu creatividad.</div>',
    unsafe_allow_html=True,
)
st.write("")

# ---------------------------------------------------------
# GENERADOR DE SILUETAS
# ---------------------------------------------------------

def crear_silueta(tipo: str, talla: str) -> Image.Image:
    """Genera una silueta de cuerpo humano en PNG con transparencia."""
    W, H = 500, 800
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    escala = {"Pequeña": 0.85, "Mediana": 1.0, "Grande": 1.15, "Extra Grande": 1.30}[talla]
    cx = W / 2

    def e(v):
        return v * escala

    # CABEZA
    r_cabeza = e(45)
    draw.ellipse(
        [cx - r_cabeza, e(60), cx + r_cabeza, e(60) + 2 * r_cabeza],
        outline=(140, 100, 180, 255),
        width=4,
    )

    # CUELLO
    draw.line([(cx, e(150)), (cx, e(190))], fill=(140, 100, 180, 255), width=4)

    # TORSO
    ancho_hombros = e(130) if tipo == "Mujer" else e(160)
    ancho_cintura = e(70) if tipo == "Mujer" else e(110)
    ancho_caderas = e(120)

    torso = [
        (cx - ancho_hombros, e(200)),
        (cx - ancho_cintura, e(400)),
        (cx - ancho_caderas, e(470)),
        (cx + ancho_caderas, e(470)),
        (cx + ancho_cintura, e(400)),
        (cx + ancho_hombros, e(200)),
    ]
    draw.polygon(torso, outline=(140, 100, 180, 255), width=4)

    # BRAZOS
    largo_brazo = e(280)
    draw.line(
        [(cx - ancho_hombros, e(210)), (cx - ancho_hombros - e(20), e(210) + largo_brazo)],
        fill=(140, 100, 180, 255), width=4,
    )
    draw.line(
        [(cx + ancho_hombros, e(210)), (cx + ancho_hombros + e(20), e(210) + largo_brazo)],
        fill=(140, 100, 180, 255), width=4,
    )

    # PIERNAS
    largo_pierna = e(300)
    draw.line(
        [(cx - ancho_caderas * 0.5, e(470)), (cx - ancho_caderas * 0.6, e(470) + largo_pierna)],
        fill=(140, 100, 180, 255), width=4,
    )
    draw.line(
        [(cx + ancho_caderas * 0.5, e(470)), (cx + ancho_caderas * 0.6, e(470) + largo_pierna)],
        fill=(140, 100, 180, 255), width=4,
    )

    # Detalles
    if tipo == "Mujer":
        draw.arc(
            [cx - e(50), e(370), cx + e(50), e(430)],
            start=0, end=180, fill=(140, 100, 180, 255), width=3,
        )
    else:
        draw.line(
            [(cx - ancho_hombros * 0.7, e(280)), (cx + ancho_hombros * 0.7, e(280))],
            fill=(140, 100, 180, 200), width=2,
        )

    return img


def pil_a_data_uri(img: Image.Image) -> str:
    """Convierte PIL Image a data URI (string base64) para st_canvas."""
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    encoded = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{encoded}"


# ---------------------------------------------------------
# SIDEBAR: CONTROLES
# ---------------------------------------------------------
with st.sidebar:
    st.header("🧵 Panel del Costurero")

    # SILUETA
    st.subheader("👗 Silueta")
    tipo_cuerpo = st.radio("Tipo de cuerpo:", ["Mujer", "Hombre"], horizontal=True)
    talla = st.select_slider(
        "Tallaje:",
        options=["Pequeña", "Mediana", "Grande", "Extra Grande"],
        value="Mediana",
    )
    mostrar_silueta = st.checkbox("Mostrar silueta de fondo", value=True)

    st.divider()

    # PINCEL
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
    stroke_color = st.color_picker("Color del trazo:", "#4c1d95")

    st.divider()

    # TELAS
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
        "Selecciona tu tela de fondo:",
        options=list(telas.keys()),
        format_func=lambda x: telas[x]["nombre"],
    )

    usar_color_tela = st.checkbox("Usar color de tela como trazo", value=False)
    if usar_color_tela:
        stroke_color = telas[tela_sel]["color"]

    bg_color = telas[tela_sel]["bg"]

    st.divider()

    # ACCIONES
    st.subheader("📐 Acciones")
    if st.button("🗑️ Limpiar lienzo", use_container_width=True):
        st.session_state["canvas_key"] = st.session_state.get("canvas_key", 0) + 1
        st.rerun()

    st.info(
        "💡 **Tip de costurero:** Dibuja sobre la silueta para crear tu "
        "boceto. Cambia de tela para inspirarte con nuevos colores."
    )


# ---------------------------------------------------------
# LIENZO CON SILUETA DE FONDO
# ---------------------------------------------------------
ancho_canvas, alto_canvas = 500, 700

# Fondo con color de tela
fondo = Image.new("RGBA", (ancho_canvas, alto_canvas), bg_color)

if mostrar_silueta:
    silueta = crear_silueta(tipo_cuerpo, talla)
    silueta = silueta.resize((ancho_canvas, alto_canvas))
    fondo = Image.alpha_composite(fondo.convert("RGBA"), silueta)

# IMPORTANTE: pasar un data URI (string), no un PIL Image
fondo_uri = pil_a_data_uri(fondo)

# Inicializar clave para resetear canvas
if "canvas_key" not in st.session_state:
    st.session_state["canvas_key"] = 0

col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    canvas_result = st_canvas(
        fill_color="rgba(168, 85, 247, 0.15)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        background_image=fondo_uri,  # string data URI
        height=alto_canvas,
        width=ancho_canvas,
        drawing_mode=drawing_mode,
        key=f"canvas_{st.session_state['canvas_key']}",
    )

st.write("")
st.markdown(
    f'<div class="descripcion">🧵 <b>Tela actual:</b> {telas[tela_sel]["nombre"]} | '
    f'<b>Silueta:</b> {tipo_cuerpo} - Talla {talla} | '
    f'<b>Modo:</b> {drawing_mode}</div>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# DESCARGA DEL DISEÑO
# ---------------------------------------------------------
if canvas_result.image_data is not None:
    st.write("")
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        # Generar el PNG combinado en cuanto haya datos
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

# Footer
st.markdown("---")
st.caption("✂️ Costurero Digital — Donde tu creatividad cobra vida")
