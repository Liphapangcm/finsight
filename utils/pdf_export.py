"""
Generates a professional PDF credit report for download.
Uses ReportLab — no browser or HTML rendering required.
"""

import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether,
)

from core.schemas import ScoreResult

# ── Brand colors ──────────────────────────────────────────────────────────────
NAV = colors.HexColor("#0B1F3A")
TEAL = colors.HexColor("#00BFA6")
SUCCESS = colors.HexColor("#43A047")
WARNING = colors.HexColor("#FB8C00")
DANGER = colors.HexColor("#E53935")
LIGHT_BG = colors.HexColor("#F7F9FC")
BORDER = colors.HexColor("#E5E7EB")
MUTED = colors.HexColor("#6B7280")
WHITE = colors.white

SCORE_BAND_COLORS = {
    "Poor": colors.HexColor("#E53935"),
    "Fair": colors.HexColor("#FB8C00"),
    "Good": colors.HexColor("#43A047"),
    "Excellent": colors.HexColor("#00897B"),
}


def _get_styles():
    return {
        "title": ParagraphStyle(
            "title",
            fontSize=22,
            fontName="Helvetica-Bold",
            textColor=NAV,
            alignment=TA_CENTER,
            spaceAfter=4,
        ),
        "subtitle": ParagraphStyle(
            "subtitle",
            fontSize=10,
            fontName="Helvetica",
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceAfter=16,
        ),
        "section_header": ParagraphStyle(
            "section_header",
            fontSize=12,
            fontName="Helvetica-Bold",
            textColor=NAV,
            spaceBefore=14,
            spaceAfter=6,
        ),
        "body": ParagraphStyle(
            "body",
            fontSize=9,
            fontName="Helvetica",
            textColor=colors.HexColor("#1A1A2E"),
            leading=14,
            spaceAfter=4,
        ),
        "body_muted": ParagraphStyle(
            "body_muted",
            fontSize=8,
            fontName="Helvetica",
            textColor=MUTED,
            leading=12,
            spaceAfter=3,
        ),
        "rec_title": ParagraphStyle(
            "rec_title",
            fontSize=10,
            fontName="Helvetica-Bold",
            textColor=NAV,
            spaceAfter=3,
        ),
        "rec_body": ParagraphStyle(
            "rec_body",
            fontSize=8.5,
            fontName="Helvetica",
            textColor=colors.HexColor("#374151"),
            leading=13,
            spaceAfter=2,
        ),
        "impact": ParagraphStyle(
            "impact",
            fontSize=8,
            fontName="Helvetica-Bold",
            textColor=SUCCESS,
            spaceAfter=0,
        ),
        "score_num": ParagraphStyle(
            "score_num",
            fontSize=48,
            fontName="Helvetica-Bold",
            alignment=TA_CENTER,
            spaceAfter=0,
        ),
        "score_band": ParagraphStyle(
            "score_band",
            fontSize=14,
            fontName="Helvetica-Bold",
            alignment=TA_CENTER,
            spaceAfter=4,
        ),
        "footer": ParagraphStyle(
            "footer",
            fontSize=7.5,
            fontName="Helvetica",
            textColor=MUTED,
            alignment=TA_CENTER,
        ),
    }


def _score_color(band: str):
    return SCORE_BAND_COLORS.get(band, TEAL)


def _build_header(styles, result: ScoreResult) -> list:
    """Navy header block with logo and report title."""
    now = datetime.now().strftime("%d %B %Y, %H:%M")

    header_data = [
        [
            Paragraph(
                '<font color="#00BFA6"><b>Fin</b></font>'
                '<font color="white"><b>Sight</b></font>',
                ParagraphStyle("logo", fontSize=20, fontName="Helvetica-Bold"),
            ),
            Paragraph(
                f"Credit Score Report<br/>"
                f'<font size="8" color="#94A3B8">'
                f"Generated: {now} · ID: {result.assessment_id[:12]}"
                f"</font>",
                ParagraphStyle(
                    "hdr_right",
                    fontSize=11,
                    fontName="Helvetica-Bold",
                    textColor=WHITE,
                    alignment=TA_RIGHT,
                ),
            ),
        ]
    ]

    tbl = Table(header_data, colWidths=[80 * mm, 110 * mm])
    tbl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), NAV),
                ("TOPPADDING", (0, 0), (-1, -1), 14),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
                ("LEFTPADDING", (0, 0), (0, -1), 16),
                ("RIGHTPADDING", (-1, 0), (-1, -1), 16),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    return [tbl, Spacer(1, 14)]


def _build_score_block(styles, result: ScoreResult) -> list:
    """Large score number with band and risk level."""
    sc = result.credit_score
    band = result.score_band
    risk = result.risk_level
    color = _score_color(band)

    score_para = Paragraph(
        f'<font color="{color.hexval()}">{sc}</font>', styles["score_num"]
    )
    band_para = Paragraph(
        f'<font color="{color.hexval()}">{band.upper()}</font>', styles["score_band"]
    )
    range_para = Paragraph(
        f"Score Range: 300 – 850 &nbsp;|&nbsp; Risk Level: <b>{risk}</b>",
        ParagraphStyle(
            "range",
            fontSize=9,
            fontName="Helvetica",
            textColor=MUTED,
            alignment=TA_CENTER,
        ),
    )

    # Score band progress bar (drawn as colored table)
    bar_data = [[""] * 4]
    bar = Table(bar_data, colWidths=[37.5 * mm] * 4, rowHeights=[6])
    bar.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#FFCDD2")),
                ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#FFE0B2")),
                ("BACKGROUND", (2, 0), (2, 0), colors.HexColor("#C8E6C9")),
                ("BACKGROUND", (3, 0), (3, 0), colors.HexColor("#B2DFDB")),
                ("ROUNDEDCORNERS", [3]),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )

    block_data = [[score_para], [band_para], [range_para], [Spacer(1, 6)], [bar]]
    block = Table(block_data, colWidths=[150 * mm])
    block.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
                ("ROUNDEDCORNERS", [8]),
                ("TOPPADDING", (0, 0), (-1, -1), 14),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )

    wrapper = Table([[block]], colWidths=[190 * mm])
    wrapper.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER")]))
    return [wrapper, Spacer(1, 16)]


def _build_kpi_table(styles, result: ScoreResult) -> list:
    kpis = result.kpis

    def kpi_cell(label, value, status, status_color):
        return [
            Paragraph(
                f"<b>{value}</b>",
                ParagraphStyle(
                    "kv",
                    fontSize=14,
                    fontName="Helvetica-Bold",
                    textColor=NAV,
                    alignment=TA_CENTER,
                ),
            ),
            Paragraph(
                label,
                ParagraphStyle(
                    "kl",
                    fontSize=7.5,
                    fontName="Helvetica",
                    textColor=MUTED,
                    alignment=TA_CENTER,
                ),
            ),
            Paragraph(
                f'<font color="{status_color}">{status}</font>',
                ParagraphStyle(
                    "ks", fontSize=8, fontName="Helvetica-Bold", alignment=TA_CENTER
                ),
            ),
        ]

    dti = kpis.debt_to_income
    sr = kpis.savings_rate
    flow = kpis.net_cash_flow
    exp = kpis.expense_ratio

    dti_c = "#43A047" if dti < 35 else "#FB8C00" if dti < 50 else "#E53935"
    sr_c = "#43A047" if sr >= 10 else "#FB8C00" if sr >= 3 else "#E53935"
    fl_c = "#43A047" if flow >= 0 else "#E53935"
    ex_c = "#43A047" if exp < 70 else "#FB8C00" if exp < 90 else "#E53935"

    cells = [
        kpi_cell(
            "Debt-to-Income",
            f"{dti:.1f}%",
            "Healthy" if dti < 35 else "Moderate" if dti < 50 else "High",
            dti_c,
        ),
        kpi_cell(
            "Savings Rate",
            f"{sr:.1f}%",
            "Strong" if sr >= 10 else "Low" if sr >= 3 else "None",
            sr_c,
        ),
        kpi_cell(
            "Monthly Cash Flow",
            f"M{'+' if flow >= 0 else ''}{flow:,.0f}",
            "Surplus" if flow >= 0 else "Deficit",
            fl_c,
        ),
        kpi_cell(
            "Expense Ratio",
            f"{exp:.1f}%",
            "Healthy" if exp < 70 else "Watch" if exp < 90 else "High",
            ex_c,
        ),
    ]

    # 4 cells in a row, each cell is a sub-table
    row = []
    for cell in cells:
        sub = Table([[c] for c in cell], colWidths=[43 * mm])
        sub.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
                    ("ROUNDEDCORNERS", [6]),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )
        row.append(sub)

    tbl = Table([row], colWidths=[46 * mm] * 4, hAlign="CENTER")
    tbl.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 2),
                ("RIGHTPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    return [
        Paragraph("Financial Health Summary", styles["section_header"]),
        HRFlowable(width="100%", thickness=1, color=TEAL, spaceAfter=8),
        tbl,
        Spacer(1, 14),
    ]


def _build_shap_table(styles, result: ScoreResult) -> list:
    """Top 8 SHAP factors as a styled table."""
    explanation = result.shap_explanation
    pairs = sorted(
        zip(explanation.feature_names, explanation.shap_values),
        key=lambda x: abs(x[1]),
        reverse=True,
    )[:8]

    rows = [
        [
            Paragraph(
                "<b>Factor</b>",
                ParagraphStyle(
                    "th", fontSize=8.5, fontName="Helvetica-Bold", textColor=WHITE
                ),
            ),
            Paragraph(
                "<b>Impact</b>",
                ParagraphStyle(
                    "th",
                    fontSize=8.5,
                    fontName="Helvetica-Bold",
                    textColor=WHITE,
                    alignment=TA_CENTER,
                ),
            ),
            Paragraph(
                "<b>Effect</b>",
                ParagraphStyle(
                    "th",
                    fontSize=8.5,
                    fontName="Helvetica-Bold",
                    textColor=WHITE,
                    alignment=TA_CENTER,
                ),
            ),
        ]
    ]

    for name, val in pairs:
        effect = "▲ Positive" if val >= 0 else "▼ Negative"
        eff_c = "#43A047" if val >= 0 else "#E53935"
        rows.append(
            [
                Paragraph(name, styles["body"]),
                Paragraph(
                    f"{val:+.1f}",
                    ParagraphStyle(
                        "val",
                        fontSize=9,
                        fontName="Helvetica-Bold",
                        textColor=NAV,
                        alignment=TA_CENTER,
                    ),
                ),
                Paragraph(
                    f'<font color="{eff_c}">{effect}</font>',
                    ParagraphStyle(
                        "eff", fontSize=8.5, fontName="Helvetica", alignment=TA_CENTER
                    ),
                ),
            ]
        )

    tbl = Table(rows, colWidths=[100 * mm, 40 * mm, 50 * mm])
    tbl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAV),
                ("BACKGROUND", (0, 1), (-1, -1), WHITE),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
                ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )

    return [
        Paragraph("Score Factor Analysis", styles["section_header"]),
        HRFlowable(width="100%", thickness=1, color=TEAL, spaceAfter=8),
        tbl,
        Spacer(1, 14),
    ]


def _build_recommendations(styles, result: ScoreResult) -> list:
    elems = [
        Paragraph("Your Action Plan", styles["section_header"]),
        HRFlowable(width="100%", thickness=1, color=TEAL, spaceAfter=8),
    ]

    cat_colors = {
        "debt": "#EDE7F6",
        "savings": "#E0F7FA",
        "income": "#E8F5E9",
        "behaviour": "#FFF3E0",
        "expenses": "#FCE4EC",
    }

    for rec in result.recommendations:
        bg = colors.HexColor(cat_colors.get(rec.category, "#F7F9FC"))

        inner = Table(
            [
                [
                    Paragraph(
                        f"<b>{rec.priority}. {rec.title}</b>  "
                        f'<font size="7" color="#6B7280">'
                        f"[{rec.category.upper()}]</font>",
                        styles["rec_title"],
                    )
                ],
                [Paragraph(rec.description, styles["rec_body"])],
                [Paragraph(f"🎯 {rec.impact_estimate}", styles["impact"])],
            ],
            colWidths=[182 * mm],
        )

        inner.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), bg),
                    ("ROUNDEDCORNERS", [6]),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ]
            )
        )

        elems.append(KeepTogether([inner, Spacer(1, 6)]))

    return elems


def _build_footer(styles, result: ScoreResult) -> list:
    now = datetime.now().strftime("%d %B %Y")
    return [
        Spacer(1, 10),
        HRFlowable(width="100%", thickness=0.5, color=BORDER),
        Spacer(1, 6),
        Paragraph(
            f"This report was generated by FinSight on {now}. "
            f"It is based on self-reported financial data and is intended "
            f"for personal financial awareness only. It does not constitute "
            f"a formal credit assessment by a registered credit bureau. "
            f"Model version: {result.model_version}.",
            styles["footer"],
        ),
    ]


def generate_pdf_report(result: ScoreResult) -> bytes:
    """
    Generates a complete PDF credit report.
    Returns raw bytes ready for Streamlit download_button.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=12 * mm,
        bottomMargin=12 * mm,
        title=f"FinSight Credit Report — {result.assessment_id[:8]}",
        author="FinSight",
    )

    styles = _get_styles()
    story = []

    story += _build_header(styles, result)
    story += _build_score_block(styles, result)
    story += _build_kpi_table(styles, result)
    story += _build_shap_table(styles, result)
    story += _build_recommendations(styles, result)
    story += _build_footer(styles, result)

    doc.build(story)
    return buffer.getvalue()
