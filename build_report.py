from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image,
                                 PageBreak, Table, TableStyle, HRFlowable)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

NAVY = colors.HexColor("#1F2A44")
TEAL = colors.HexColor("#2A9D8F")
ORANGE = colors.HexColor("#E76F51")
GREY = colors.HexColor("#555555")

styles = getSampleStyleSheet()
title_style = ParagraphStyle("TitleBig", parent=styles["Title"], fontSize=26, textColor=NAVY, spaceAfter=6)
subtitle_style = ParagraphStyle("Subtitle", parent=styles["Normal"], fontSize=13, textColor=GREY, spaceAfter=20)
h1 = ParagraphStyle("H1", parent=styles["Heading1"], fontSize=17, textColor=NAVY, spaceBefore=14, spaceAfter=8)
h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=13, textColor=TEAL, spaceBefore=10, spaceAfter=6)
body = ParagraphStyle("Body", parent=styles["Normal"], fontSize=10.5, leading=15, spaceAfter=8)
bullet = ParagraphStyle("Bullet", parent=body, leftIndent=14, bulletIndent=2)
caption = ParagraphStyle("Caption", parent=styles["Normal"], fontSize=9, textColor=GREY, alignment=TA_CENTER, spaceBefore=4, spaceAfter=14)
kpi_label = ParagraphStyle("KPILabel", parent=styles["Normal"], fontSize=9.5, textColor=GREY, alignment=TA_CENTER)
kpi_value = ParagraphStyle("KPIValue", parent=styles["Normal"], fontSize=18, textColor=NAVY, alignment=TA_CENTER, fontName="Helvetica-Bold")

doc = SimpleDocTemplate("Superstore_Visual_Storytelling_Report.pdf", pagesize=letter,
                         topMargin=0.7*inch, bottomMargin=0.7*inch,
                         leftMargin=0.7*inch, rightMargin=0.7*inch)

story = []

# ---------- COVER ----------
story.append(Spacer(1, 1.2*inch))
story.append(Paragraph("Superstore Sales", title_style))
story.append(Paragraph("A Visual Storytelling Report on Sales, Profit & Discount Strategy", subtitle_style))
story.append(HRFlowable(width="100%", thickness=1, color=TEAL, spaceAfter=20))
story.append(Paragraph("Prepared as part of the Data Analyst Internship — Task 2: Data Visualization and Storytelling", body))
story.append(Paragraph("Dataset: Sample Superstore (9,994 orders across the US)", body))
story.append(Spacer(1, 0.5*inch))

kpi_data = [
    [Paragraph("TOTAL SALES", kpi_label), Paragraph("TOTAL PROFIT", kpi_label), Paragraph("PROFIT MARGIN", kpi_label)],
    [Paragraph("$2.30M", kpi_value), Paragraph("$286K", kpi_value), Paragraph("12.5%", kpi_value)],
]
kpi_table = Table(kpi_data, colWidths=[1.9*inch]*3)
kpi_table.setStyle(TableStyle([
    ("BOX", (0,0), (-1,-1), 0.75, TEAL),
    ("INNERGRID", (0,0), (-1,-1), 0.5, colors.HexColor("#DDDDDD")),
    ("TOPPADDING", (0,0), (-1,-1), 10),
    ("BOTTOMPADDING", (0,0), (-1,-1), 10),
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#F1F5F4")),
]))
story.append(kpi_table)
story.append(PageBreak())

# ---------- THE STORY / EXEC SUMMARY ----------
story.append(Paragraph("The Story in Three Lines", h1))
story.append(Paragraph(
    "1. Technology and Office Supplies are the real profit engines of the business — Furniture "
    "brings in almost as much revenue as Technology but returns barely a tenth of the profit.", bullet, bulletText="•"))
story.append(Paragraph(
    "2. A handful of sub-categories are quietly bleeding money. Tables alone wiped out over $17,000 "
    "in profit, and Bookcases aren't far behind — both sit inside the \"profitable\" Furniture category, "
    "which is exactly why the loss is easy to miss.", bullet, bulletText="•"))
story.append(Paragraph(
    "3. Heavy discounting is the common thread behind most loss-making orders. Once a discount crosses "
    "roughly 30%, orders are far more likely to be sold at a loss than at a profit.", bullet, bulletText="•"))

story.append(Paragraph("Objective", h2))
story.append(Paragraph(
    "This report looks past raw sales numbers to understand where the Superstore business actually "
    "makes money, where it quietly loses money, and what pricing/discount behaviour is driving that gap — "
    "using the Sample Superstore dataset (9,994 orders, 4 regions, 3 segments, 17 sub-categories).", body))

story.append(Paragraph("1. Category-Level Performance", h1))
story.append(Image("charts/01_sales_profit_category.png", width=6.3*inch, height=3.78*inch))
story.append(Paragraph("Sales vs. profit, side by side, by category.", caption))
story.append(Paragraph(
    "Technology and Office Supplies generate similar revenue, but Technology converts it into "
    "nearly $145K of profit versus Office Supplies' $122K. Furniture is the outlier: it earns "
    "$742K in sales — almost on par with Technology — yet returns only about $18K in profit, a "
    "margin under 2.5%. Something inside Furniture is dragging the category down.", body))

story.append(Paragraph("2. Where the Money Actually Leaks", h1))
story.append(Image("charts/02_profit_subcategory.png", width=6.3*inch, height=5.04*inch))
story.append(Paragraph("Total profit by sub-category. Red bars are net loss-makers.", caption))
story.append(Paragraph(
    "Tables and Bookcases are the two sub-categories losing money overall, and both belong to "
    "Furniture — this is the answer to the pattern seen on the previous page. Supplies is also "
    "marginally unprofitable. On the other end, Copiers, Phones, Accessories, Paper and Binders "
    "are the strongest performers and are effectively subsidising the weak sub-categories.", body))
story.append(PageBreak())

story.append(Paragraph("3. Regional Split", h1))
story.append(Image("charts/03_sales_region_donut.png", width=4.4*inch, height=4.4*inch, hAlign="CENTER"))
story.append(Paragraph("Share of total sales by region.", caption))
story.append(Paragraph(
    "The West and East regions together account for well over half of all sales, while the South "
    "region contributes the least. This is useful context for the loss-making sub-categories: it's "
    "worth checking in a follow-up analysis whether Tables and Bookcases are losing money everywhere, "
    "or mainly concentrated in specific regions.", body))

story.append(Paragraph("4. Why the Losses Happen: Discounting", h1))
story.append(Image("charts/04_discount_vs_profit.png", width=6.3*inch, height=4.03*inch))
story.append(Paragraph("Each point is one order; red points are loss-making orders.", caption))
story.append(Paragraph(
    "There's a clear negative relationship between discount level and profit. Orders with little "
    "or no discount are almost always profitable (the cluster of teal points near 0% discount sits "
    "comfortably above the zero line). But past roughly a 30% discount, loss-making orders (red) "
    "start to dominate. In this dataset, the 1,393 orders discounted 30% or more lost a combined "
    "$135K — nearly half of the company's total profit, wiped out by discounting decisions on "
    "about 14% of orders.", body))

story.append(Paragraph("5. Top Sellers", h1))
story.append(Image("charts/05_top10_subcategory_sales.png", width=6.3*inch, height=4.2*inch))
story.append(Paragraph("Top 10 sub-categories by total sales.", caption))
story.append(Paragraph(
    "Phones and Chairs lead in raw sales volume. Chairs is worth watching alongside Tables and "
    "Bookcases — it sells well, but since it's in the same weak-margin Furniture category, it "
    "deserves its own profit check rather than being judged on sales alone.", body))

story.append(Paragraph("6. Customer Segments", h1))
story.append(Image("charts/06_segment_sales_profit.png", width=6.1*inch, height=3.92*inch))
story.append(Paragraph("Sales (bars) and profit (line) by customer segment.", caption))
story.append(Paragraph(
    "Consumer is the largest segment by both sales and profit, followed by Corporate, then Home "
    "Office. Profit scales roughly in line with sales across segments, so — unlike category or "
    "discount level — segment doesn't appear to be a major driver of the loss pattern seen earlier.", body))
story.append(PageBreak())

# ---------- SUMMARY / STORYBOARD ----------
story.append(Paragraph("Summary Storyboard", h1))
story.append(Paragraph(
    "Putting the six charts together into a single narrative arc:", body))

summary_points = [
    ("Where we stand", "$2.3M in sales, $286K in profit — a 12.5% overall margin across 9,994 orders."),
    ("The strength", "Technology and Office Supplies drive almost all of the profit. Copiers, Phones, "
                      "Accessories, Paper and Binders are the standout performers."),
    ("The leak", "Furniture looks healthy on revenue but is barely profitable overall, dragged down "
                 "specifically by Tables and Bookcases, which lose money outright."),
    ("The likely cause", "Heavy discounting (30%+) is strongly associated with unprofitable orders — "
                          "this pattern shows up across the dataset, not just in Furniture."),
    ("The recommendation", "Cap or tighten discount thresholds on Tables and Bookcases specifically, "
                            "revisit their base pricing, and audit any order discounted above ~30% "
                            "before it's approved."),
]
tbl_data = [[Paragraph(f"<b>{k}</b>", body), Paragraph(v, body)] for k, v in summary_points]
tbl = Table(tbl_data, colWidths=[1.6*inch, 4.7*inch])
tbl.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("LINEBELOW", (0,0), (-1,-1), 0.4, colors.HexColor("#DDDDDD")),
    ("TOPPADDING", (0,0), (-1,-1), 8),
    ("BOTTOMPADDING", (0,0), (-1,-1), 8),
]))
story.append(tbl)

story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("Next Steps", h2))
story.append(Paragraph(
    "If I were taking this further: break the discount-vs-profit view down by sub-category to find "
    "the exact discount tipping point for Tables and Bookcases, and check whether the same "
    "loss-making pattern is concentrated in specific regions or ship modes.", body))

doc.build(story)
print("PDF built.")
