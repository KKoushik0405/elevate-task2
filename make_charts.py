import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

df = pd.read_csv("superstore.csv")

# ---- consistent color palette ----
NAVY = "#1F2A44"
TEAL = "#2A9D8F"
ORANGE = "#E76F51"
GOLD = "#E9C46A"
GREY = "#8D99AE"
RED = "#D62839"
PALETTE = [TEAL, ORANGE, GOLD, NAVY, GREY]

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.edgecolor": "#444444",
    "axes.labelcolor": "#222222",
    "text.color": "#222222",
    "xtick.color": "#333333",
    "ytick.color": "#333333",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})

def save(fig, name):
    fig.savefig(f"charts/{name}.png", dpi=200, bbox_inches="tight")
    plt.close(fig)

# 1. Sales & Profit by Category
cat = df.groupby("Category")[["Sales", "Profit"]].sum().sort_values("Sales", ascending=False)
fig, ax = plt.subplots(figsize=(7.5, 4.5))
x = np.arange(len(cat))
w = 0.35
ax.bar(x - w/2, cat["Sales"], w, label="Sales", color=TEAL)
ax.bar(x + w/2, cat["Profit"], w, label="Profit", color=ORANGE)
ax.set_xticks(x)
ax.set_xticklabels(cat.index)
ax.set_ylabel("Amount (USD)")
ax.set_title("Sales vs Profit by Category", fontsize=14, fontweight="bold", loc="left")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, p: f"${v/1000:.0f}K"))
ax.legend(frameon=False)
save(fig, "01_sales_profit_category")

# 2. Profit by Sub-Category (highlighting losses)
sub = df.groupby("Sub_Category")["Profit"].sum().sort_values()
colors = [RED if v < 0 else TEAL for v in sub.values]
fig, ax = plt.subplots(figsize=(7.5, 6))
ax.barh(sub.index, sub.values, color=colors)
ax.axvline(0, color="#444444", linewidth=0.8)
ax.set_xlabel("Total Profit (USD)")
ax.set_title("Profit by Sub-Category — where we lose money", fontsize=14, fontweight="bold", loc="left")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, p: f"${v/1000:.0f}K"))
save(fig, "02_profit_subcategory")

# 3. Sales by Region (donut)
reg = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(6, 6))
wedges, texts, autotexts = ax.pie(
    reg.values, labels=reg.index, autopct="%1.0f%%", startangle=90,
    colors=PALETTE, wedgeprops=dict(width=0.42, edgecolor="white")
)
for t in autotexts:
    t.set_color("white")
    t.set_fontweight("bold")
ax.set_title("Share of Sales by Region", fontsize=14, fontweight="bold")
save(fig, "03_sales_region_donut")

# 4. Discount vs Profit scatter
fig, ax = plt.subplots(figsize=(7.5, 4.8))
sample = df.sample(min(1200, len(df)), random_state=42)
colors2 = np.where(sample["Profit"] < 0, RED, TEAL)
ax.scatter(sample["Discount"], sample["Profit"], c=colors2, alpha=0.55, s=18, edgecolors="none")
ax.axhline(0, color="#444444", linewidth=0.8)
ax.set_xlabel("Discount")
ax.set_ylabel("Profit (USD)")
ax.set_title("Discount vs Profit — deep discounts turn orders unprofitable", fontsize=13, fontweight="bold", loc="left")
save(fig, "04_discount_vs_profit")

# 5. Top 10 sub-categories by sales
top10 = df.groupby("Sub_Category")["Sales"].sum().sort_values(ascending=False).head(10)
fig, ax = plt.subplots(figsize=(7.5, 5))
ax.barh(top10.index[::-1], top10.values[::-1], color=NAVY)
ax.set_xlabel("Total Sales (USD)")
ax.set_title("Top 10 Sub-Categories by Sales", fontsize=14, fontweight="bold", loc="left")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, p: f"${v/1000:.0f}K"))
save(fig, "05_top10_subcategory_sales")

# 6. Segment contribution
seg = df.groupby("Segment")[["Sales", "Profit"]].sum()
fig, ax = plt.subplots(figsize=(7, 4.5))
x = np.arange(len(seg))
ax.bar(x, seg["Sales"], color=GOLD, label="Sales", width=0.5)
ax2 = ax.twinx()
ax2.plot(x, seg["Profit"], color=RED, marker="o", linewidth=2, label="Profit")
ax.set_xticks(x)
ax.set_xticklabels(seg.index)
ax.set_ylabel("Sales (USD)")
ax2.set_ylabel("Profit (USD)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, p: f"${v/1000:.0f}K"))
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, p: f"${v/1000:.0f}K"))
ax.set_title("Sales & Profit by Customer Segment", fontsize=14, fontweight="bold", loc="left")
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, frameon=False, loc="upper left")
save(fig, "06_segment_sales_profit")

print("Charts created:")
import os
for f in sorted(os.listdir("charts")):
    print(" -", f)

# Print key numbers for the narrative/README
print("\n--- KEY NUMBERS ---")
print("Total Sales:", round(df['Sales'].sum(), 2))
print("Total Profit:", round(df['Profit'].sum(), 2))
print("Overall margin %:", round(100*df['Profit'].sum()/df['Sales'].sum(), 2))
print("\nBy category:\n", cat)
print("\nWorst 5 sub-categories by profit:\n", sub.head(5))
print("\nBest 5 sub-categories by profit:\n", sub.tail(5))
print("\nRegion sales:\n", reg)
print("\nCorrelation discount vs profit:", round(df['Discount'].corr(df['Profit']), 3))
high_disc = df[df['Discount'] >= 0.3]
print("\nOrders with discount >= 0.3:", len(high_disc), "| their total profit:", round(high_disc['Profit'].sum(),2))
print("Segment table:\n", seg)
