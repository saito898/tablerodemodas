import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageDraw
import numpy as np
import io

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Costurero Digital - Diseño de Modas",
    page_icon="🧵",
    layout="wide",
)

# ---------------------------------------------------------
# CSS AMBIENTACIÓN COSTURERO
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Fondo tipo madera / costurero */
    .stApp {
        background: linear-gradient(135deg, #f5e6d3 0%, #e8d5b7 50%, #d4b896 100%);
    }
    /* Título estilo letrero de costura */
    h1 {
        font-family: 'Georgia', serif;
        color: #6b4423;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.15);
        border-bottom: 3px dashed #8b6f47;
        padding-bottom: 10px;
    }
    h2, h3 {
        font-family: 'Georgia', serif;
        color: #6b4423;
    }
    /* Sidebar con textura */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #faf3e8 0%, #efe2cc 100%);
        border-right: 2px dashed #b89968;
    }
    /* Botones estilo botón de costura */
    .stButton > button {
        background-color: #8b6f47;
        color: white;
        border-radius: 20px;
        border: 2px solid #6b4423;
        font-weight: bold;
        padding: 0.5em 1.5em;
    }
    .stButton > button:hover {
        background-color: #6b4423;
        color: #faf3e8;
    }
    /* Contenedor del canvas con sombra de tela */
    div[data-testid="stCanvas"] {
        border: 3px solid #8b6f47;
        border-radius: 10px;
        box-shadow: 5px 5px 15px rgba(107, 68, 35, 0.3);
        background: white;
        padding: 5px;
    }
    /* Texto descriptivo */
    .descripcion {
        background-color: rgba(255, 255, 255, 0.7);
        border-left: 5px solid #8b6f47;
        padding: 10px 15px;
        border-radius: 5px;
        font-family: 'Georgia', serif;
        color: #4a2f1a;
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

    # Factor de escala según talla
    escala = {"Pequeña": 0.85, "Mediana": 1.0, "Grande": 1.15, "Extra Grande": 1.30}[talla]
    cx = W / 2

    def e(v):  # escalar
        return v * escala

    # --- CABEZA ---
    r_cabeza = e(45)
    draw.ellipse(
        [cx - r_cabeza, e(60), cx + r_cabeza, e(60) + 2 * r_cabeza],
        outline=(180, 160, 140, 255),
        width=4,
    )

    # --- CUELLO ---
    draw.line([(cx, e(150)), (cx, e(190))], fill=(180, 160, 140, 255), width=4)

    # --- HOMBROS / TRONCO ---
    ancho_hombros = e(130) if tipo == "Mujer" else e(160)
    ancho_cintura = e(70) if tipo == "Mujer" else e(110)
    ancho_caderas = e(120) if tipo == "Mujer" else e(120)

    # Torso
    torso = [
        (cx - ancho_hombros, e(200)),
        (cx - ancho_cintura, e(400)),
        (cx - ancho_caderas, e(470)),
        (cx + ancho_caderas, e(470)),
        (cx + ancho_cintura, e(400)),
        (cx + ancho_hombros, e(200)),
    ]
    draw.polygon(torso, outline=(180, 160, 140, 255), width=4)

    # --- BRAZOS ---
    largo_brazo = e(280)
    # Brazo izquierdo
    draw.line(
        [(cx - ancho_hombros, e(210)), (cx - ancho_hombros - e(20), e(210) + largo_brazo)],
        fill=(180, 160, 140, 255), width=4,
    )
    # Brazo derecho
    draw.line(
        [(cx + ancho_hombros, e(210)), (cx + ancho_hombros + e(20), e(210) + largo_brazo)],
        fill=(180, 160, 140, 255), width=4,
    )

    # --- PIERNAS ---
    largo_pierna = e(300)
    # Pierna izquierda
    draw.line(
        [(cx - ancho_caderas * 0.5, e(470)), (cx - ancho_caderas * 0.6, e(470) + largo_pierna)],
        fill=(180, 160, 140, 255), width=4,
    )
    # Pierna derecha
    draw.line(
        [(cx + ancho_caderas * 0.5, e(470)), (cx + ancho_caderas * 0.6, e(470) + largo_pierna)],
        fill=(180, 160, 140, 255), width=4,
    )

    # Detalles según tipo
    if tipo == "Mujer":
        # Curvas de cintura
        draw.arc(
            [cx - e(50), e(370), cx + e(50), e(430)],
            start=0, end=180, fill=(180, 160, 140, 255), width=3,
        )
    else:
        # Línea pectoral
        draw.line(
            [(cx - ancho_hombros * 0.7, e(280)), (cx + ancho_hombros * 0.7, e(280))],
            fill=(180, 160, 140, 200), width=2,
        )

    return img


def imagen_a_base64(imagen: Image.Image) -> str:
    buffered = io.BytesIO()
    imagen.save(buffered, format="PNG")
    return "data:image/png;base64," + __import__("base64").b64encode(buffered.getvalue()).decode()


# ---------------------------------------------------------
# SIDEBAR: CONTROLES
# ---------------------------------------------------------
with st.sidebar:
    st.header("🧵 Panel del Costurero")

    # --- SILUETA ---
    st.subheader("👗 Silueta")
    tipo_cuerpo = st.radio("Tipo de cuerpo:", ["Mujer", "Hombre"], horizontal=True)
    talla = st.select_slider(
        "Tallaje:",
        options=["Pequeña", "Mediana", "Grande", "Extra Grande"],
        value="Mediana",
    )
    mostrar_silueta = st.checkbox("Mostrar silueta de fondo", value=True)

    st.divider()

    # --- PINCEL ---
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
    stroke_color = st.color_picker("Color del trazo:", "#2c1810")

    st.divider()

    # --- TELAS ---
    st.subheader("🧶 Telas")
    telas = {
        "Papel de boceto": {"bg": "#FFFFFF", "color": "#2c1810", "nombre": "📄 Papel"},
        "Lino natural": {"bg": "#F5EBD8", "color": "#5c3d1e", "nombre": "🌾 Lino"},
        "Denim": {"bg": "#4A6FA5", "color": "#FFFFFF", "nombre": "👖 Denim"},
        "Seda rosa": {"bg": "#F8D7DA", "color": "#8B2A3F", "nombre": "🌸 Seda"},
        "Terciopelo": {"bg": "#4B0082", "color": "#F0E68C", "nombre": "💜 Terciopelo"},
        "Lentejuela": {"bg": "#1A1A2E", "color": "#FFD700", "nombre": "✨ Lentejuela"},
        "Verde oliva": {"bg": "#808000", "color": "#F5F5DC", "nombre": "🫒 Oliva"},
        "Encaje": {"bg": "#FFF5EE", "color": "#8B4513", "nombre": "🕸️ Encaje"},
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

    # --- ACCIONES ---
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
# Generar imagen de fondo combinada (tela + silueta)
ancho_canvas, alto_canvas = 500, 700

# Crear fondo con color de tela
fondo = Image.new("RGBA", (ancho_canvas, alto_canvas), bg_color)

if mostrar_silueta:
    silueta = crear_silueta(tipo_cuerpo, talla)
    # Redimensionar y centrar silueta
    silueta = silueta.resize((ancho_canvas, alto_canvas))
    fondo = Image.alpha_composite(fondo.convert("RGBA"), silueta)

fondo_b64 = imagen_a_base64(fondo)
bg_image = Image.open(io.BytesIO(__import__("base64").b64decode(fondo_b64.split(",")[1])))

# Inicializar clave del canvas para resetear
if "canvas_key" not in st.session_state:
    st.session_state["canvas_key"] = 0

col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.15)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        background_image=bg_image,
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
        if st.button("💾 Descargar mi diseño", use_container_width=True):
            # Combinar fondo + dibujo del usuario
            arr = np.array(canvas_result.image_data).astype("uint8")
            dibujo = Image.fromarray(arr, "RGBA")
            resultado = Image.alpha_composite(fondo.copy(), dibujo)

            buf = io.BytesIO()
            resultado.save(buf, format="PNG")
            st.download_button(
                label="⬇️ Haz clic para guardar",
                data=buf.getvalue(),
                file_name=f"diseno_{tipo_cuerpo}_{talla}.png",
                mime="image/png",
                use_container_width=True,
            )

# Footer
st.markdown("---")
st.caption("✂️ Costurero Digital — Donde tu creatividad cobra vida")
