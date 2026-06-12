"""Genera el PDF profesional del resumen ejecutivo de DuniPets."""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether,
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import PageBreak
from reportlab.lib.styles import getSampleStyleSheet
import os

_base_styles = getSampleStyleSheet()

OUT_PATH = r"C:\Users\tuto6\Projects\DuniPets\reports\DuniPets_Investigacion_Mercado_2026.pdf"

# ── Paleta ────────────────────────────────────────────────────────────────────
VERDE       = colors.HexColor("#2E7D32")
VERDE_CLARO = colors.HexColor("#A5D6A7")
VERDE_BG    = colors.HexColor("#F1F8E9")
NARANJA     = colors.HexColor("#E65C00")
GRIS_OSC    = colors.HexColor("#212121")
GRIS_MED    = colors.HexColor("#555555")
GRIS_CLARO  = colors.HexColor("#F5F5F5")
BLANCO      = colors.white

# ── Estilos ───────────────────────────────────────────────────────────────────
def s(name, **kw):
    base_name = kw.pop("parent", "Normal")
    parent = _base_styles[base_name] if isinstance(base_name, str) else base_name
    return ParagraphStyle(name, parent=parent, **kw)

ST = {
    "h1": s("h1", fontSize=22, textColor=BLANCO, leading=28,
             spaceAfter=4, fontName="Helvetica-Bold", alignment=TA_CENTER),
    "h2": s("h2", fontSize=14, textColor=VERDE, leading=18,
             spaceBefore=14, spaceAfter=4, fontName="Helvetica-Bold"),
    "h3": s("h3", fontSize=10.5, textColor=GRIS_OSC, leading=14,
             spaceBefore=8, spaceAfter=2, fontName="Helvetica-Bold"),
    "body": s("body", fontSize=9.5, textColor=GRIS_MED, leading=14,
              spaceAfter=4, fontName="Helvetica", alignment=TA_JUSTIFY),
    "small": s("small", fontSize=7.5, textColor=GRIS_MED, leading=10,
               fontName="Helvetica"),
    "label": s("label", fontSize=8, textColor=VERDE, leading=10,
                fontName="Helvetica-Bold"),
    "highlight": s("highlight", fontSize=10, textColor=VERDE, leading=13,
                   fontName="Helvetica-Bold"),
    "cell": s("cell", fontSize=8.5, textColor=GRIS_MED, leading=11,
              fontName="Helvetica"),
    "cell_h": s("cell_h", fontSize=8.5, textColor=BLANCO, leading=11,
                fontName="Helvetica-Bold", alignment=TA_CENTER),
    "cell_c": s("cell_c", fontSize=8.5, textColor=GRIS_MED, leading=11,
                fontName="Helvetica", alignment=TA_CENTER),
    "cell_green": s("cell_green", fontSize=8.5, textColor=VERDE, leading=11,
                    fontName="Helvetica-Bold", alignment=TA_CENTER),
    "cell_gray": s("cell_gray", fontSize=8.5, textColor=colors.HexColor("#BDBDBD"),
                   leading=11, fontName="Helvetica", alignment=TA_CENTER),
    "naranja": s("naranja", fontSize=9, textColor=NARANJA, leading=12,
                 fontName="Helvetica-Bold"),
    "quote": s("quote", fontSize=11, textColor=VERDE, leading=16,
               fontName="Helvetica-BoldOblique", alignment=TA_CENTER,
               borderPadding=(8, 12, 8, 12)),
}

def hr():
    return HRFlowable(width="100%", thickness=1, color=VERDE_CLARO, spaceAfter=6)

def section_title(text):
    return [
        Spacer(1, 0.3*cm),
        Paragraph(text, ST["h2"]),
        HRFlowable(width="100%", thickness=2, color=VERDE, spaceAfter=6),
    ]

def table_style_base(col_widths):
    return TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0), VERDE),
        ("TEXTCOLOR",    (0, 0), (-1, 0), BLANCO),
        ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, 0), 8.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [BLANCO, GRIS_CLARO]),
        ("GRID",         (0, 0), (-1, -1), 0.5, VERDE_CLARO),
        ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",   (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 5),
        ("LEFTPADDING",  (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ])

# ── Portada (primera página) via canvas override ──────────────────────────────
class CoverPage:
    def __init__(self, doc_width, doc_height):
        self.w = doc_width
        self.h = doc_height

    def wrap(self, aw, ah):
        return self.w, self.h

    def draw(self):
        pass  # no-op; portada se dibuja via onFirstPage

def on_first_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(VERDE)
    canvas.rect(0, 0, w, h, fill=1, stroke=0)

    # Bloque blanco central
    bx, by, bw, bh = 2*cm, 4.5*cm, w - 4*cm, 14*cm
    canvas.setFillColor(BLANCO)
    canvas.roundRect(bx, by, bw, bh, 8, fill=1, stroke=0)

    # Nombre
    canvas.setFillColor(VERDE)
    canvas.setFont("Helvetica-Bold", 46)
    canvas.drawCentredString(w/2, by + bh - 2.8*cm, "DuniPets")

    # Línea decorativa
    canvas.setStrokeColor(VERDE_CLARO)
    canvas.setLineWidth(2)
    canvas.line(w/2 - 4*cm, by + bh - 3.5*cm, w/2 + 4*cm, by + bh - 3.5*cm)

    # Subtítulo
    canvas.setFillColor(GRIS_OSC)
    canvas.setFont("Helvetica", 16)
    canvas.drawCentredString(w/2, by + bh - 4.5*cm, "Investigación de Mercado")
    canvas.setFont("Helvetica", 11)
    canvas.setFillColor(GRIS_MED)
    canvas.drawCentredString(w/2, by + bh - 5.4*cm,
        "Marketplace Premium de Cuidado de Mascotas · Bogotá, Colombia")

    # Datos clave
    canvas.setFont("Helvetica-Bold", 10)
    canvas.setFillColor(VERDE)
    datos = [
        ("Junio 2026",     w/2 - 8*cm),
        ("5 Competidores", w/2 - 2*cm),
        ("3 Perfiles",     w/2 + 4*cm),
    ]
    for texto, x in datos:
        canvas.setFillColor(VERDE_BG)
        canvas.roundRect(x - 1.8*cm, by + 2.2*cm, 4.5*cm, 1*cm, 5, fill=1, stroke=0)
        canvas.setFillColor(VERDE)
        canvas.drawCentredString(x + 0.5*cm, by + 2.6*cm, texto)

    # Tagline
    canvas.setFont("Helvetica-BoldOblique", 11)
    canvas.setFillColor(BLANCO)
    canvas.drawCentredString(w/2, by - 1.5*cm,
        "Cero jaulas · Entorno familiar · Paz mental para el dueño")

    # Footer portada
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(VERDE_CLARO)
    canvas.drawCentredString(w/2, 1*cm,
        "Documento confidencial · Solo para uso interno · DuniPets 2026")
    canvas.restoreState()

def on_later_pages(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(VERDE)
    canvas.rect(0, h - 1.2*cm, w, 1.2*cm, fill=1, stroke=0)
    canvas.setFillColor(BLANCO)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(1.5*cm, h - 0.85*cm, "DuniPets")
    canvas.setFont("Helvetica", 9)
    canvas.drawCentredString(w/2, h - 0.85*cm,
        "Investigación de Mercado · Bogotá 2026")
    canvas.drawRightString(w - 1.5*cm, h - 0.85*cm, f"Página {doc.page}")

    canvas.setStrokeColor(VERDE_CLARO)
    canvas.setLineWidth(0.5)
    canvas.line(1.5*cm, 1.5*cm, w - 1.5*cm, 1.5*cm)
    canvas.setFillColor(GRIS_MED)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawCentredString(w/2, 0.9*cm,
        "Documento confidencial · DuniPets · Junio 2026")
    canvas.restoreState()

# ── Contenido ─────────────────────────────────────────────────────────────────
story = [PageBreak()]  # primera "página" es la portada dibujada en onFirstPage

# ─── 1. El negocio ────────────────────────────────────────────────────────────
story += section_title("1. El Negocio en una Línea")
story.append(Paragraph(
    "DuniPets conecta a dueños de mascotas en Bogotá con cuidadores verificados que ofrecen "
    "hospedaje, guardería, paseos, visitas para gatos y house sitting — todos los servicios en "
    "entornos domésticos, <b>sin jaulas</b>, con precios publicados y reserva sin fricción.",
    ST["body"]))

# ─── 2. Mapa competitivo ──────────────────────────────────────────────────────
story += section_title("2. Mapa Competitivo (Junio 2026)")

story.append(Paragraph("Competidores activos", ST["h3"]))
activos_data = [
    [Paragraph(h, ST["cell_h"]) for h in ["Competidor", "Tipo", "Sin jaulas", "Gatos", "Precio ref."]],
    ["Dog Garden",     "Guardería física · 3 sedes", "✓ Explícito",    "✗",                 "Desde $35.000/día"],
    ["Mywak",          "App / Marketplace",           "No especificado","No especificado",    "No publicado"],
    ["Diverpool",      "Centro integral premium",     "No especificado","Hotel en sede",      "$40K–$80K/noche"],
    ["Cruz Roja Bog.", "Guardería / Hotel físico",    "Instalaciones",  "✗",                 "Desde $6.900/hora"],
    ["Tierra de Perros","Hotel campestre",             "No especificado","✗",                 "No publicado"],
]
for i in range(1, len(activos_data)):
    activos_data[i] = [Paragraph(str(c), ST["cell"]) for c in activos_data[i]]

t_activos = Table(activos_data, colWidths=[3.5*cm, 4.2*cm, 2.8*cm, 3.0*cm, 3.5*cm])
ts = table_style_base(None)
ts.add("TEXTCOLOR", (2, 1), (2, 1), VERDE)
ts.add("FONTNAME",  (2, 1), (2, 1), "Helvetica-Bold")
story.append(t_activos)
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("Competidores inactivos (referencia histórica)", ST["h3"]))
inactivos_data = [
    [Paragraph(h, ST["cell_h"]) for h in ["Competidor", "Tipo", "Estado verificado"]],
    ["Waggy",          "App / Marketplace", "waggy.co redirige a atom.com. Dominio abandonado. ❌ Inactivo"],
    ["DogHero Colombia","App / Marketplace", "Sin presencia web activa en Colombia 2025–2026. ❌ Probable salida"],
]
for i in range(1, len(inactivos_data)):
    inactivos_data[i] = [Paragraph(str(c), ST["cell"]) for c in inactivos_data[i]]

t_inactivos = Table(inactivos_data, colWidths=[3.5*cm, 4.2*cm, 9.3*cm])
ts2 = table_style_base(None)
ts2.add("TEXTCOLOR", (2, 1), (2, 2), NARANJA)
story.append(t_inactivos)

story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    "<b>Hallazgo clave:</b> Los dos marketplaces de referencia en Colombia (Waggy y DogHero) ya no operan activamente. "
    "El segmento de plataformas digitales de cuidado de mascotas en Bogotá tiene un vacío que Mywak ocupa "
    "parcialmente, pero sin comunicar calidad diferenciada.",
    ParagraphStyle("insight", parent=ST["body"], backColor=VERDE_BG,
                   borderPadding=(8, 10, 8, 10), borderColor=VERDE_CLARO,
                   borderWidth=1, borderRadius=4, textColor=GRIS_OSC)))

# ─── 3. Benchmark de precios ──────────────────────────────────────────────────
story += section_title("3. Benchmark de Precios")

precios_data = [
    [Paragraph(h, ST["cell_h"]) for h in ["Servicio", "Dog Garden", "Diverpool", "Cruz Roja", "Mywak", "DuniPets"]],
    ["Hospedaje/noche",  "Por consultar",    "$40K–$80K",   "Por plan",      "No publicado", "$47.500"],
    ["Guardería/día",    "Desde $35.000",    "Por consultar","~$55.200 (8h)","No publicado", "$35.000"],
    ["Paseo 1 hora",     "Incluido*",        "Por consultar","No aplica",    "No publicado", "$13.500"],
    ["Visita gatos",     "No ofrece",        "No ofrece",    "No ofrece",    "Sin confirmar","$12.000–$18.000"],
    ["House sitting/n.", "No ofrece",        "No ofrece",    "No ofrece",    "Sin confirmar","Por definir**"],
]

col_w_p = [3.8*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 3.2*cm]
for i in range(1, len(precios_data)):
    row = precios_data[i]
    styled = []
    for j, cell in enumerate(row):
        if j == 0:
            styled.append(Paragraph(str(cell), ST["cell"]))
        elif j == 5:
            styled.append(Paragraph(str(cell), ST["cell_green"]))
        elif str(cell) in ("No ofrece","No aplica","Sin confirmar","No publicado","Por consultar","Por definir**","Incluido*"):
            styled.append(Paragraph(str(cell), ST["cell_gray"]))
        else:
            styled.append(Paragraph(str(cell), ST["cell_c"]))
    precios_data[i] = styled

t_precios = Table(precios_data, colWidths=col_w_p)
ts_p = table_style_base(None)
ts_p.add("BACKGROUND", (5, 0), (5, -1), colors.HexColor("#E8F5E9"))
story.append(t_precios)
story.append(Spacer(1, 0.2*cm))
story.append(Paragraph(
    "* En Dog Garden los paseos están incluidos en la guardería, no se venden por separado.  "
    "** House sitting DuniPets: rango recomendado $65.000–$85.000/noche.",
    ST["small"]))
story.append(Paragraph(
    "<b>Conclusión:</b> DuniPets es el único competidor activo con tabla de precios publicada para todos sus servicios — "
    "ventaja directa de conversión en un mercado donde la norma es \"contáctenos por WhatsApp\".",
    ParagraphStyle("concl", parent=ST["body"], backColor=VERDE_BG,
                   borderPadding=(8, 10, 8, 10), borderColor=VERDE_CLARO,
                   borderWidth=1, spaceBefore=8)))

# ─── 4. Los 3 gaps ────────────────────────────────────────────────────────────
story += section_title("4. Los 3 Gaps de Mercado")

gaps = [
    (
        "Gap 1 — El mercado felino está completamente desatendido",
        "0 de 5 competidores activos auditados ofrece visitas a domicilio para gatos. "
        "El gato necesita quedarse en su entorno habitual; el mercado actual lo obliga a salir o "
        "a quedarse solo. Ningún competidor físico ni digital cubre este servicio actualmente.",
        "DuniPets entra como el único jugador activo con visitas a domicilio para gatos en Bogotá. "
        "Precio de entrada bajo ($12.000/visita) para reducir la barrera de primera prueba. "
        "Alto potencial de fidelización: el dueño de gato que encuentra una solución confiable no la cambia.",
    ),
    (
        "Gap 2 — \"Sin jaulas\" existe en instalaciones, no en hogares",
        "Dog Garden validó demanda con 3 sedes activas y posicionamiento explícito \"100% libre de jaulas\". "
        "Sin embargo, el dueño sigue obligado a trasladar su mascota a una sede física en el norte de Bogotá. "
        "La ciudad fuera del eje Chicó–Cedritos queda sin cobertura.",
        "\"Hogar de verdad\" es el escalón superior: el cuidador recibe en su casa o se queda en la del cliente. "
        "Sin sedes fijas, los cuidadores de DuniPets están distribuidos por toda la ciudad. "
        "No compite de frente con Dog Garden — ofrece la siguiente categoría.",
    ),
    (
        "Gap 3 — Los precios son opacos en toda la industria",
        "4 de 5 competidores activos no publican precios completos en sus canales. "
        "La norma es \"contáctenos por WhatsApp\". Esto genera abandono en el funnel de conversión "
        "y desconfianza en un servicio de alta implicación emocional.",
        "DuniPets publica tabla completa de precios desde el primer contacto — web, Instagram, WhatsApp. "
        "En mercados donde nadie publica precios, el primero que lo hace se vuelve el referente. "
        "La transparencia es parte de la propuesta de valor, no solo del marketing.",
    ),
]

for num, titulo, evidencia, oportunidad in [(i+1,*g) for i,g in enumerate(gaps)]:
    story.append(KeepTogether([
        Paragraph(titulo, ST["h3"]),
        Paragraph(f"<b>Evidencia:</b> {evidencia}", ST["body"]),
        Paragraph(f"<b>Cómo lo capitaliza DuniPets:</b> {oportunidad}",
                  ParagraphStyle("op", parent=ST["body"],
                                 backColor=VERDE_BG, borderPadding=(6, 8, 6, 8),
                                 borderColor=VERDE_CLARO, borderWidth=1)),
        Spacer(1, 0.3*cm),
    ]))

# ─── 5. Perfiles de cliente ───────────────────────────────────────────────────
story += section_title("5. Los 3 Perfiles de Cliente")

perfiles = [
    {
        "titulo": "Perfil 1 — \"La Viajera con Gatos\" (Valentina)",
        "campos": [
            ("Zona",             "Chapinero / Teusaquillo"),
            ("Mascota",          "1–2 gatos"),
            ("Servicio",         "Visitas a domicilio + House sitting"),
            ("Barrera",          "No sabe que el servicio existe; cuando lo encuentra, necesita prueba de confianza"),
            ("Canal",            "Instagram (cuentas de gatos) · Grupos de Facebook de dueños de gatos"),
            ("Mensaje clave",    "\"Tus gatos se quedan en su hogar. Nosotros vamos donde ellos.\""),
            ("Valor anual est.", "$700.000–$1.050.000"),
        ],
        "gap": "Gap 1",
    },
    {
        "titulo": "Perfil 2 — \"El Ejecutivo Viajero\" (Andrés / Camila)",
        "campos": [
            ("Zona",             "Usaquén / Chicó / Santa Bárbara"),
            ("Mascota",          "Perro mediano o grande"),
            ("Servicio",         "Hospedaje nocturno"),
            ("Barrera",          "Mala experiencia previa en kennel — necesita señales fuertes de confianza"),
            ("Canal",            "Recomendación directa · Google (\"hospedaje perros Bogotá sin jaulas\")"),
            ("Mensaje clave",    "\"Tu perro en un hogar de verdad, no en un kennel. Fotos cada noche.\""),
            ("Valor anual est.", "$1.520.000"),
        ],
        "gap": "Gap 2",
    },
    {
        "titulo": "Perfil 3 — \"La Profesional con Agenda Llena\" (Daniela / Juan Felipe)",
        "campos": [
            ("Zona",             "Suba / Cedritos / Chapinero"),
            ("Mascota",          "Perro pequeño o mediano"),
            ("Servicio",         "Guardería diurna + Paseos recurrentes"),
            ("Barrera",          "Fricción del proceso de cotización — abandona si hay pasos extras"),
            ("Canal",            "Instagram · TikTok · Grupos de WhatsApp del edificio"),
            ("Mensaje clave",    "\"$13.500 el paseo. $35.000 la guardería. Recogemos en tu puerta. Reserva en 2 minutos.\""),
            ("Valor anual est.", "$1.296.000–$3.360.000 (mayor recurrencia)"),
        ],
        "gap": "Gap 3",
    },
]

for p in perfiles:
    rows = [[Paragraph(f"<b>{k}</b>", ST["cell"]), Paragraph(v, ST["cell"])] for k, v in p["campos"]]
    t = Table([[Paragraph(p["titulo"], ST["h3"]), Paragraph(f"→ {p['gap']}", ST["highlight"])]] +
              rows, colWidths=[4.5*cm, 12.5*cm])
    ts_p2 = TableStyle([
        ("SPAN",         (0, 0), (1, 0)),
        ("BACKGROUND",   (0, 0), (-1, 0), VERDE_BG),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [BLANCO, GRIS_CLARO]),
        ("GRID",         (0, 0), (-1, -1), 0.5, VERDE_CLARO),
        ("VALIGN",       (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",   (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 5),
        ("LEFTPADDING",  (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("FONTNAME",     (0, 1), (0, -1), "Helvetica-Bold"),
        ("TEXTCOLOR",    (0, 1), (0, -1), GRIS_MED),
    ])
    story.append(KeepTogether([t, Spacer(1, 0.4*cm)]))

# ─── 6. Posicionamiento y próximos pasos ──────────────────────────────────────
story += section_title("6. Posicionamiento y Próximos Pasos")

story.append(Paragraph("Posicionamiento recomendado", ST["h3"]))
story.append(Paragraph(
    "DuniPets es el servicio de cuidado de mascotas más confiable de Bogotá para dueños que no aceptan jaulas. "
    "Cuidamos perros y gatos en entornos domésticos — en el hogar de nuestros cuidadores o en el tuyo — "
    "con precios claros y cero sorpresas.",
    ParagraphStyle("pos", parent=ST["body"], backColor=VERDE_BG, fontSize=11,
                   borderPadding=(10, 12, 10, 12), borderColor=VERDE,
                   borderWidth=2, textColor=GRIS_OSC, leading=17, alignment=TA_CENTER)))

story.append(Spacer(1, 0.4*cm))
story.append(Paragraph("Los tres pilares", ST["h3"]))

pilares_data = [
    [Paragraph(h, ST["cell_h"]) for h in ["Pilar", "Promesa"]],
    ["Cero jaulas",          "Siempre en un hogar real — nunca en instalaciones comerciales"],
    ["Perros y gatos",       "Servicios para ambas especies, incluyendo visitas a domicilio para gatos"],
    ["Precio transparente",  "Tabla publicada desde el primer contacto. Sin WhatsApp previo. Sin sorpresas."],
]
for i in range(1, len(pilares_data)):
    pilares_data[i] = [Paragraph(str(c), ST["cell"]) for c in pilares_data[i]]

t_pilares = Table(pilares_data, colWidths=[5*cm, 12*cm])
story.append(t_pilares)

story.append(Spacer(1, 0.5*cm))
story.append(Paragraph("Próximos pasos prioritarios", ST["h3"]))

pasos_data = [
    [Paragraph(h, ST["cell_h"]) for h in ["Prioridad", "Plazo", "Acción", "Objetivo"]],
    ["1", "Sem. 1–2", "Entrevistar 15 dueños de gatos",     "Validar Gap 1 con datos primarios"],
    ["2", "Sem. 1",   "Mystery shopping Dog Garden",         "Mapear precios reales y experiencia de cliente"],
    ["3", "Sem. 1",   "Descargar Mywak y simular reserva",  "Obtener precios reales y evaluar UX"],
    ["4", "Sem. 1",   "Definir precio de house sitting",     "Completar tabla de precios de DuniPets"],
    ["5", "Sem. 3–4", "Encuesta disposición a pagar",        "Validar sensibilidad al precio por perfil"],
]
for i in range(1, len(pasos_data)):
    pasos_data[i] = [Paragraph(str(c), ST["cell_c"] if j < 2 else ST["cell"]) for j, c in enumerate(pasos_data[i])]

t_pasos = Table(pasos_data, colWidths=[1.8*cm, 2*cm, 7*cm, 6.2*cm])
story.append(t_pasos)

story.append(Spacer(1, 0.6*cm))
story.append(HRFlowable(width="100%", thickness=1, color=VERDE_CLARO))
story.append(Spacer(1, 0.2*cm))
story.append(Paragraph(
    "Todos los datos de esta investigación son de fuente primaria (auditoría web directa) o estimaciones "
    "basadas en información pública. Los precios marcados como pendientes deben verificarse antes de "
    "tomar decisiones comerciales. Ver archivos de respaldo en /data/competencia/, /data/precios/ y "
    "/data/perfiles_cliente/.",
    ST["small"]))

# ── Construir el PDF ──────────────────────────────────────────────────────────
os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
doc = SimpleDocTemplate(
    OUT_PATH,
    pagesize=A4,
    leftMargin=1.8*cm, rightMargin=1.8*cm,
    topMargin=1.8*cm, bottomMargin=2*cm,
    title="DuniPets — Investigación de Mercado 2026",
    author="DuniPets",
)
doc.build(story,
          onFirstPage=on_first_page,
          onLaterPages=on_later_pages)
print(f"PDF guardado: {OUT_PATH}")
