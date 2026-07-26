# Task 2 – Data Visualization and Storytelling

Internship: Data Analyst Internship (Elevate Labs)

## What this task was about

The brief was to take a sales dataset and turn it into visuals that actually tell a story, not just a bunch of random charts. I used the classic Sample Superstore dataset (9,994 orders, US-based retailer selling Furniture, Office Supplies and Technology).

## What I did

I didn't have paid access to Tableau, so I did this in Python (pandas + matplotlib) instead — it gave me full control over styling and let me build a proper PDF report, which is one of the deliverable options anyway. If you want to reproduce it in Power BI/Tableau, the same six charts + insights below work fine there too.

Steps:
1. Loaded and checked the data — no missing values, 4 regions, 3 segments, 17 sub-categories.
2. Picked one chart type per question I wanted answered (grouped bar for category comparison, diverging horizontal bar for profit by sub-category, donut for regional share, scatter for discount vs. profit, etc.) instead of defaulting to the same chart everywhere.
3. Wrote a short insight under every chart — the point was to explain *why* it matters, not just describe what's on the axis.
4. Put it all together into a single PDF report with a cover page, KPI summary, six chart sections, and a one-page storyboard summary at the end.

## Files in this repo

- `Superstore_Visual_Storytelling_Report.pdf` – the final visual report (main deliverable)
- `Superstore.csv` – the dataset used
- `make_charts.py` – script that generates all 6 charts from the CSV
- `build_report.py` – script that assembles the charts + narrative into the PDF
- `screenshots/` – the individual chart images, in case you just want to skim them

## The story, in short

- **Technology and Office Supplies are the actual profit drivers.** Furniture brings in almost as much revenue as Technology, but its profit is a fraction of it.
- **Tables and Bookcases are losing money outright.** They're hiding inside the "profitable" Furniture category, which is exactly why it's easy to miss on a top-line view.
- **Heavy discounting is the likely reason.** Once an order's discount goes past ~30%, it's far more likely to be sold at a loss than at a profit. Orders discounted 30%+ collectively lost about $135K — that's almost half the company's total profit, wiped out by a relatively small slice of orders.
- **Recommendation:** tighten discount limits on Tables and Bookcases specifically, revisit their base pricing, and flag any order above a ~30% discount for a manual check before approval.

## What I'd do next if I had more time

Break the discount-vs-profit chart down per sub-category to find the exact tipping point for Tables/Bookcases, and check if the losses are concentrated in specific regions or shipping modes rather than spread evenly.

## Interview questions – my answers

**1. What is the importance of data visualization?**
Numbers in a spreadsheet don't tell you anything on their own — you have to stare at them for a while to spot a pattern. A good chart does that work instantly. It also makes it way easier to explain findings to people who aren't going to read a table of 10,000 rows.

**2. When do you use a pie chart vs a bar chart?**
Pie charts only really work when you're showing how a handful of categories split up 100% of something, like regional share of sales. The moment you have more than 4–5 categories, or you want people to compare exact values, a bar chart wins — it's much easier to judge length than angle.

**3. How do you make visualizations more engaging?**
Give every chart a title that states the takeaway, not just the metric ("Furniture margin is barely 2.5%" instead of "Profit by Category"). Use color with a purpose (I used red only for loss-making sub-categories, everything else stayed neutral). And cut anything that doesn't add information — gridlines, legends, extra decimals, all of it if it's not helping.

**4. What is data storytelling?**
It's connecting the individual charts into one narrative instead of leaving the reader to figure out the "so what" themselves. In this report that meant going: here's the overall performance → here's where it breaks down by category → here's the sub-category actually causing the problem → here's why (discounting) → here's what to do about it.

**5. How do you avoid misleading visualizations?**
Start bar chart axes at zero, don't cherry-pick a date range that flatters the trend, label your units clearly, and don't use 3D or overly decorative chart types that distort how big things look. I also try to show the actual data points (like the scatter plot here) rather than only summarized averages, since averages can hide outliers.

**6. What are best practices in dashboard design?**
Most important number top-left, since that's where the eye lands first. Group related charts together. Keep colors consistent across the whole dashboard so people don't have to relearn what a color means on every page. Leave whitespace — a cramped dashboard is harder to read than a sparse one.

**7. What tools have you used for visualization?**
For this task I used Python (matplotlib) since I didn't want to pay for Tableau, plus reportlab to put it into a proper PDF report. I've also used Excel/Power BI for quicker exploratory charts. They all follow the same principles — the tool matters less than actually thinking through what story the chart needs to tell.
