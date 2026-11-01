"""Build printable adaptations of existing worksheets without collecting answers."""
import json
import os
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

ROOT = Path(__file__).resolve().parents[1]
WIDTH, HEIGHT = A4
MARGIN = 45
INK = HexColor("#2D1636")
MUTED = HexColor("#63556A")
ACCENT = HexColor("#9E315D")
LINE = HexColor("#D8CCD9")

def fonts():
    options = [
        (os.environ.get("PDF_FONT_REGULAR"), os.environ.get("PDF_FONT_BOLD")),
        ("/System/Library/Fonts/Supplemental/Arial.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    ]
    for regular, bold in options:
        if regular and bold and Path(regular).is_file() and Path(bold).is_file():
            pdfmetrics.registerFont(TTFont("Kit", regular))
            pdfmetrics.registerFont(TTFont("KitBold", bold))
            return
    raise RuntimeError("Set PDF_FONT_REGULAR and PDF_FONT_BOLD to readable TTF fonts.")

def paragraph(pdf, text, x, top, size=10, color=INK, bold=False, leading=None, width=None):
    style = ParagraphStyle("kit", fontName="KitBold" if bold else "Kit",
                           fontSize=size, leading=leading or size * 1.35, textColor=color)
    block = Paragraph(escape(text), style)
    available_width = width or WIDTH - 2 * MARGIN
    _, height = block.wrap(available_width, HEIGHT)
    block.drawOn(pdf, x, top - height)
    return top - height

def footer(pdf, data, number):
    pdf.setStrokeColor(LINE)
    pdf.line(MARGIN, 45, WIDTH-MARGIN, 45)
    paragraph(pdf, data["footer"], MARGIN, 34, size=8, color=MUTED)
    pdf.setFont("Kit", 8)
    pdf.setFillColor(MUTED)
    pdf.drawRightString(WIDTH-MARGIN, 25, str(number))

def build(data):
    target = ROOT / "distribution" / ("couples-conversation-kit-" + data["lang"] + ".pdf")
    pdf = canvas.Canvas(str(target), pagesize=A4, pageCompression=1, invariant=1)
    pdf.setTitle(data["title"])
    pdf.setAuthor("Yes · No · Maybe")
    for index, sheet in enumerate(data["sheets"], 1):
        top = paragraph(pdf, data["subtitle"].upper(), MARGIN, HEIGHT-40, 8, ACCENT, True)
        top = paragraph(pdf, sheet["title"], MARGIN, top-12, 23, INK, True)
        top = paragraph(pdf, sheet["purpose"], MARGIN, top-10, 10, MUTED)
        if index == 1:
            top = paragraph(pdf, data["intro"], MARGIN, top-9, 9, MUTED)
        top -= 17
        for number, (question, choices) in enumerate(sheet["questions"], 1):
            top = paragraph(pdf, str(number)+". "+question, MARGIN, top, 10, INK, True)
            if choices:
                top = paragraph(pdf, choices, MARGIN+13, top-4, 8.5, MUTED)
            pdf.setStrokeColor(LINE)
            pdf.line(MARGIN+13, top-19, WIDTH-MARGIN, top-19)
            top -= 43 if not choices else 37
        top = paragraph(pdf, sheet["note"], MARGIN, top-3, 9, ACCENT)
        assert top > 65, "Worksheet text overlaps footer: "+sheet["title"]
        footer(pdf, data, index)
        pdf.showPage()
    top = paragraph(pdf, data["licenseTitle"], MARGIN, HEIGHT-45, 23, INK, True)
    top = paragraph(pdf, data["licenseIntro"], MARGIN, top-17, 10)
    top = paragraph(pdf, data["translation"], MARGIN, top-12, 10, MUTED)
    top = paragraph(pdf, data["cta"], MARGIN, top-18, 11, ACCENT, True)
    pdf.linkURL("https://www.yes-no-maybe.app/"+data["lang"], (MARGIN,top-3,WIDTH-MARGIN,top+17))
    top = paragraph(pdf, data["sourceLabel"], MARGIN, top-23, 11, INK, True)
    for sheet in data["sheets"]:
        top = paragraph(pdf, sheet["source"], MARGIN, top-6, 8.5, MUTED)
    top = paragraph(pdf, "github.com/djedie/couple-communication-worksheets", MARGIN, top-10, 8.5, MUTED)
    pdf.linkURL("https://github.com/djedie/couple-communication-worksheets", (MARGIN,top-3,WIDTH-MARGIN,top+13))
    for block in (ROOT/"LICENSE").read_text().strip().split("\n\n"):
        top = paragraph(pdf, " ".join(block.splitlines()), MARGIN, top-12, 8.5, MUTED)
    assert top > 65, "License text overlaps footer"
    footer(pdf, data, 4)
    pdf.showPage()
    pdf.save()
    print(target.name)

if __name__ == "__main__":
    fonts()
    for language in ("en", "fr"):
        build(json.loads((ROOT/"distribution"/("kit."+language+".json")).read_text()))
