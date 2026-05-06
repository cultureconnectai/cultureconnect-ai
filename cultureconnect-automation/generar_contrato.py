"""
CultureConnect AI — Generador de Contratos PDF
Uso: python generar_contrato.py "Nombre" "Plan" "email@cliente.com" "2026-06-01"
Planes: Starter / Growth / "Full Autopilot" / Elite
Email y fecha son opcionales — si no los pones quedan en blanco para llenar a mano.
"""

import sys
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_RIGHT

# ── COLORS ──────────────────────────────────────────────
NAVY    = HexColor('#0a0e1a')
GOLD    = HexColor('#c9a227')
TEAL    = HexColor('#00d4b1')
GRAY    = HexColor('#667788')
LIGHT   = HexColor('#f8f9fc')
BORDER  = HexColor('#e2e8f0')
RED     = HexColor('#e53e3e')

# ── PACKAGES ─────────────────────────────────────────────
PACKAGES = {
    'Starter': {
        'regular': '$399.99/mo',
        'price':   '$149.99/mo',
        'report':  'Reporte mensual de resultados',
        'desc':    '2 plataformas (IG + FB)\nCaptions bilingues, 3 posts/semana\nReporte mensual, setup en 48hrs'
    },
    'Growth': {
        'regular': '$599.99/mo',
        'price':   '$349.99/mo',
        'report':  'Reporte semanal por WhatsApp',
        'desc':    '4 plataformas (IG + FB + YouTube + Google)\nPosts diarios, ManyChat DM replies\nReporte semanal por WhatsApp'
    },
    'Full Autopilot': {
        'regular': '$1,199.99/mo',
        'price':   '$999.99/mo',
        'report':  'Reporte semanal + analisis mensual de competencia',
        'desc':    '6+ plataformas, autopilot 24/7\nManyChat avanzado + keywords, watermark\nAnalisis de competencia, soporte prioritario'
    },
    'Elite': {
        'regular': '$1,999.99/mo',
        'price':   '$1,799.99/mo',
        'report':  'Reporte semanal + sesion 1-on-1 mensual con Xavier',
        'desc':    'Todo en Full Autopilot\n+ FB & IG Ads gestionados\n+ SEO local, Google Business\n+ Estrategia 1-on-1 con Xavier'
    }
}

def build_contract(client_name: str, plan: str, client_email: str = None, start_date: str = None, output_dir: str = None):
    if plan not in PACKAGES:
        print(f"ERROR: Plan '{plan}' no válido. Opciones: {', '.join(PACKAGES.keys())}")
        sys.exit(1)

    pkg = PACKAGES[plan]
    today = datetime.now().strftime('%B %d, %Y')
    filename = f"Contrato_{client_name.replace(' ', '_')}.pdf"
    if output_dir:
        filename = os.path.join(output_dir, filename)

    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.6*inch,
        bottomMargin=0.6*inch
    )

    story = []

    # ── HEADER ───────────────────────────────────────────
    header_data = [
        [
            Paragraph(
                '<font color="#c9a227">Culture</font><font color="#ffffff">Connect AI</font>',
                ParagraphStyle('logo', fontSize=22, textColor=white, fontName='Helvetica-Bold', leading=26)
            ),
            Paragraph(
                '<font color="#aabbcc">San Antonio, TX 78224<br/>(956) 319-4741<br/>cultureconnectai.net</font>',
                ParagraphStyle('meta', fontSize=9, textColor=HexColor('#aabbcc'),
                               alignment=TA_RIGHT, leading=14)
            )
        ]
    ]
    header_table = Table(header_data, colWidths=[4*inch, 3*inch])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), NAVY),
        ('PADDING', (0,0), (-1,-1), 16),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 0.2*inch))

    # ── TITLE ────────────────────────────────────────────
    story.append(Paragraph(
        'CONTRATO DE SERVICIOS DE MARKETING DIGITAL',
        ParagraphStyle('title', fontSize=13, fontName='Helvetica-Bold',
                       alignment=TA_CENTER, spaceAfter=4, textColor=NAVY,
                       letterSpacing=1)
    ))
    story.append(Paragraph(
        'Digital Marketing Services Agreement',
        ParagraphStyle('subtitle', fontSize=9, alignment=TA_CENTER,
                       textColor=GRAY, spaceAfter=12)
    ))
    story.append(HRFlowable(width='100%', thickness=2, color=NAVY))
    story.append(Spacer(1, 0.15*inch))

    # ── PARTIES ──────────────────────────────────────────
    party_style = ParagraphStyle('party', fontSize=9, leading=14)
    email_display = client_email if client_email else '_______________________'

    parties_data = [
        [
            Paragraph('<b>PROVEEDOR / AGENCY</b>',
                      ParagraphStyle('ph', fontSize=8, textColor=GOLD, fontName='Helvetica-Bold')),
            Paragraph('<b>CLIENTE / CLIENT</b>',
                      ParagraphStyle('ph', fontSize=8, textColor=TEAL, fontName='Helvetica-Bold'))
        ],
        [
            Paragraph('<b>CultureConnect AI</b><br/>Xavier Solis<br/>cultureconnectai1@gmail.com<br/>(956) 319-4741', party_style),
            Paragraph(f'<b>{client_name}</b><br/>{email_display}', party_style)
        ]
    ]
    parties_table = Table(parties_data, colWidths=[3.5*inch, 3.5*inch])
    parties_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT),
        ('BACKGROUND', (0,0), (-1,0), HexColor('#1a2233')),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('PADDING', (0,0), (-1,-1), 10),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(parties_table)
    story.append(Spacer(1, 0.2*inch))

    # ── SECTION HELPER ───────────────────────────────────
    def section_title(text):
        return [
            Paragraph(
                f'<font color="#c9a227">▌</font> <b>{text}</b>',
                ParagraphStyle('sec', fontSize=10, fontName='Helvetica-Bold',
                               textColor=NAVY, spaceBefore=12, spaceAfter=6)
            )
        ]

    body = ParagraphStyle('body', fontSize=9, leading=14, textColor=HexColor('#2d3748'))
    bullet = ParagraphStyle('bullet', fontSize=9, leading=14, leftIndent=14,
                            textColor=HexColor('#2d3748'))

    # ── SERVICES ─────────────────────────────────────────
    story += section_title('1. SERVICIOS CONTRATADOS / SERVICES')

    pkg_data = [
        ['Paquete Contratado', 'Incluye', 'Precio Mensual'],
        [plan, pkg['desc'], pkg['price']]
    ]
    pkg_table = Table(pkg_data, colWidths=[1.4*inch, 4*inch, 1.3*inch])
    pkg_style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('PADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,1), (-1,1), HexColor('#fffbeb')),
        ('FONTNAME', (0,1), (0,1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (2,1), (2,1), HexColor('#7b5c00')),
        ('FONTNAME', (2,1), (2,1), 'Helvetica-Bold'),
        ('FONTSIZE', (2,1), (2,1), 11),
    ])
    pkg_table.setStyle(pkg_style)
    story.append(pkg_table)

    # ── PAYMENT ──────────────────────────────────────────
    story += section_title('2. PAGO / PAYMENT')
    payment_data = [
        ['Fecha de inicio / Start date:', start_date if start_date else '_______________'],
        ['Facturación / Billing cycle:', 'Mensual / Monthly'],
        ['Método de pago / Payment method:', 'Stripe (tarjeta de crédito / credit card)'],
        ['Oferta de lanzamiento válida hasta:', 'July 31, 2026'],
        ['Total mensual / Monthly total:', pkg['price']],
    ]
    pay_table = Table(payment_data, colWidths=[3*inch, 4*inch])
    pay_table.setStyle(TableStyle([
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('PADDING', (0,0), (-1,-1), 6),
        ('BACKGROUND', (0,0), (-1,-1), LIGHT),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0,-1), (-1,-1), HexColor('#7b5c00')),
        ('BACKGROUND', (0,-1), (-1,-1), HexColor('#fffbeb')),
    ]))
    story.append(pay_table)
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        'El pago se cobra automáticamente cada mes. Si el pago falla, los servicios se pausan hasta regularizar.',
        body
    ))

    # ── OBLIGATIONS ──────────────────────────────────────
    story += section_title('3. OBLIGACIONES DEL CLIENTE / CLIENT RESPONSIBILITIES')
    obligations = [
        'Proveer acceso a redes sociales dentro de los primeros 3 días hábiles.',
        'Aprobar o solicitar cambios al contenido en un plazo máximo de <b>48 horas</b>.',
        'Proveer fotos, videos, o material de contenido según lo acordado en el onboarding.',
        'Mantener información de pago actualizada en Stripe.',
    ]
    for o in obligations:
        story.append(Paragraph(f'• {o}', bullet))

    # ── AGENCY OBLIGATIONS ────────────────────────────────
    story += section_title('4. OBLIGACIONES DE CULTURECONNECT AI')
    agency_obs = [
        'Publicar el contenido acordado en las plataformas y frecuencia del paquete seleccionado.',
        f'Entregar <b>{pkg["report"]}</b> (metricas de alcance, engagement, y crecimiento).',
        'Responder mensajes y consultas dentro de <b>24 horas hábiles</b>.',
        'Mantener confidencialidad de credenciales y datos del cliente.',
    ]
    for o in agency_obs:
        story.append(Paragraph(f'• {o}', bullet))

    # ── CANCELLATION + IP ────────────────────────────────
    story += section_title('5. CANCELACIÓN · IP · RESULTADOS')
    story.append(Paragraph(
        '<b>Cancelación:</b> Cualquiera de las partes puede cancelar con <b>15 días de aviso</b> por escrito '
        '(WhatsApp o email). No hay penalidad. No se realizan reembolsos por períodos ya facturados.',
        body
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        '<b>Propiedad Intelectual:</b> El contenido creado es propiedad del cliente una vez pagado. '
        'CultureConnect AI puede usar ejemplos como portafolio (sin datos privados) a menos que el cliente indique lo contrario.',
        body
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        '<b>Resultados:</b> CultureConnect AI no garantiza resultados específicos de ventas o seguidores. '
        'Nos comprometemos a aplicar las mejores prácticas y reportar con transparencia. '
        'Jurisdicción: Leyes de Texas, disputas en San Antonio TX.',
        body
    ))

    # ── SIGNATURES ───────────────────────────────────────
    story.append(Spacer(1, 0.25*inch))
    story.append(HRFlowable(width='100%', thickness=1, color=BORDER))
    story.append(Spacer(1, 0.15*inch))

    sig_data = [
        [
            Paragraph('<b>Firma del Proveedor / Agency Signature</b>',
                      ParagraphStyle('sigl', fontSize=8, textColor=GRAY, fontName='Helvetica-Bold')),
            Paragraph('<b>Firma del Cliente / Client Signature</b>',
                      ParagraphStyle('sigr', fontSize=8, textColor=GRAY, fontName='Helvetica-Bold'))
        ],
        [
            Paragraph('<br/><br/>___________________________<br/>'
                      '<font size="8" color="#667788">Xavier Solis — CultureConnect AI</font>', body),
            Paragraph('<br/><br/>___________________________<br/>'
                      f'<font size="8" color="#667788">{client_name}</font>', body)
        ],
        [
            Paragraph(f'<font size="8" color="#667788">Fecha: {today}</font>', body),
            Paragraph('<font size="8" color="#667788">Fecha: _______________</font>', body)
        ]
    ]
    sig_table = Table(sig_data, colWidths=[3.5*inch, 3.5*inch])
    sig_table.setStyle(TableStyle([
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(sig_table)

    # ── FOOTER ───────────────────────────────────────────
    story.append(HRFlowable(width='100%', thickness=0.5, color=BORDER))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        'Al firmar, ambas partes aceptan los términos descritos. · By signing, both parties agree to the terms above.<br/>'
        '<font color="#667788">CultureConnect AI · San Antonio, TX · cultureconnectai.net · (956) 319-4741</font>',
        ParagraphStyle('footer', fontSize=8, alignment=TA_CENTER, textColor=GRAY, leading=14)
    ))

    # ── BUILD ────────────────────────────────────────────
    doc.build(story)
    print(f"OK Contrato generado: {filename}")
    return filename


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Uso: python generar_contrato.py \"Nombre\" \"Plan\" \"email@cliente.com\" \"2026-06-01\"")
        print("Planes: Starter / Growth / Full Autopilot / Elite")
        print("Email y fecha son opcionales.")
        print('\nEjemplo: python generar_contrato.py "Rosa Mendoza" "Growth" "rosa@gmail.com" "2026-06-01"')
        sys.exit(1)

    client      = sys.argv[1]
    plan        = sys.argv[2]
    email       = sys.argv[3] if len(sys.argv) > 3 else None
    start_date  = sys.argv[4] if len(sys.argv) > 4 else None

    build_contract(client, plan, email, start_date)
