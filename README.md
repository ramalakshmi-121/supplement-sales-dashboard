# Supplement Sales Dashboard

[![Streamlit App](https://img.shields.io/badge/Open-Dashboard-blue)](https://supplement-sales-dashboard-majcsczecb6pmbpqdvg7xt.streamlit.app/)

An interactive dashboard was built using Streamlit to visualize business performance across categories, products, regions, and platforms.

Source: https://www.kaggle.com/datasets/zahidmughal2343/supplement-sales-data

# Dataset Overview
This dataset contains weekly sales data for a variety of health and wellness supplements from January 2020 to April 2025. The data includes products in categories like Protein, Vitamins, Omega, and Amino Acids, among others, and covers multiple e-commerce platforms such as Amazon, Walmart, and iHerb. The dataset also tracks sales in several locations including the USA, UK, and Canada.

# Dataset Details
Time Range: January 2020 to April 2025

Frequency: Weekly (Every Monday)

Number of Rows: 4,384

# Columns:
Date: The week of the sale.

Product Name: The name of the supplement (e.g., Whey Protein, Vitamin C, etc.).

Category: The category of the supplement (e.g., Protein, Vitamin, Omega).

Units Sold: The number of units sold in that week.

Price: The selling price of the product.

Revenue: The total revenue generated (Units Sold * Price).

Discount: The discount applied on the product (as a percentage of original price).

Units Returned: The number of units returned in that week.

Location: The location of the sale (USA, UK, or Canada).

Platform: The e-commerce platform (Amazon, Walmart, iHerb).

# Project Overview
Developed an interactive sales analytics dashboard to analyze supplement sales performance across products, categories, regions, and platforms. The dashboard provides data-driven insights on revenue, pricing, discounts, and customer behaviour to support business decision-making.

# Tools Used 
- Python Libraries: Pandas, Matplotlib, Seaborn 
- Framework: Streamlit 

# Data Insights
## Overall Business Performance
- The business generated $22.9M total revenue with 658K units sold, showing strong demand in the supplement market.
- The average selling price of $39.11 indicates products are positioned in a mid-premium pricing segment.
- Return rate is only 1.02%, which is very low, suggesting good product quality and customer satisfaction.
- However, Net Revenue ($20.07M) is significantly lower than Gross Revenue, indicating that discounts and returns reduce revenue by about 12.4%.

## Sales Overview Insights
### Category Performance
-	Mineral supplements lead in units sold (123,668) showing strong customer demand for mineral-based health products.
-	Fat Burner products have the lowest sales (40,743) indicating weaker market demand.

### Product Performance
-	Biotin is the best-selling product (41,533 units) and also the top revenue generator.
-	Vitamin C is the lowest-selling product, indicating relatively lower customer demand compared to other supplements.

### Geographic Sales Performance
-	Canada appears to be the highest selling market (226,053 units), suggesting higher supplement demand or stronger brand presence there. 

### Platform Performance
-	iHerb is the top-performing platform (225,427 units sold), showing primary online distribution channel for supplements.

## Category-wise Insights
### Revenue Contribution
-	Vitamin category generates the highest revenue ($4.3M).
-	Amino Acid category has the highest average revenue per product ($5,346).

### Return Rate
-	Hydration category has the highest return rate (1.07%).
-	Hydration products might face quality perception issues, taste preferences, or customer expectation gaps, which could be investigated further.
-	Herbal supplements have the lowest return rate (0.95%).

## Product-wise Insights
### Revenue Contribution
-	Biotin generates the highest revenue ($1.48M).
-	Magnesium has the lowest revenue among products analyzed.

### Product Demand by Country
Customer preferences vary by region:
-	Canada – Creatine sells the most (Performance supplements)
-	UK – Biotin sells the most (Vitamin supplements)
-	USA – Ashwagandha sells the most (Herbal supplements)

### Revenue vs Units Sold (Product-wise)
-	Biotin generates the highest revenue (~$1.48M) and also has one of the highest units sold (~41.5K).
-	Magnesium has the lowest revenue, even though its units sold are similar to other products.
-	Units sold across products are very similar (around 40K–41K).

### Returns Analysis
-	Vitamin C has the highest return units (457) and highest return rate (1.12%).
-	Vitamin C may have expectation mismatch issues.
-	Ashwagandha has the lowest return rate (0.95%), shows strong customer satisfaction.

## Platform-wise Insights
### Revenue Contribution
-	iHerb generates the highest revenue ($7.85M).
-	iHerb appears to be the most effective sales channel for supplements.
-	Walmart generates the lowest revenue among platforms.

### Platform Performance by Country
-	Canada – iHerb dominates revenue
-	UK – Walmart dominates revenue
-	USA – Amazon dominates revenue
Each country has different dominant e-commerce ecosystems, so platform strategy should be localized by region.

### Discount vs Units Sold (Platform-wise)
-	Units sold generally increase when discounts are between 5% and 20%.
-	Extremely high discounts (25%) cause a sharp drop in sales across all platforms.
-	iHerb consistently performs strong at mid-range discounts.
-	Amazon sales fluctuate more compared to Walmart and iHerb.
Very high discounts do not increase demand, suggesting customer demand is not highly price-sensitive beyond a certain point.

### Returns by Platform
-	Amazon has the highest returned units (2,295) and highest return rate (1.04%).
-	Walmart has the lowest return rate (1.00%).
- Higher returns on Amazon may be due to:
    -	higher order volumes 
    -	easy return policies.

## Time-based Insights
### Units Sold vs Revenue Over Time
-	Units sold fluctuate between ~2300 and ~2500 weekly.
-	Revenue follows a similar pattern to units sold, indicating a direct relationship.
-	The stable trend indicates consistent demand for supplements across weeks.
-	Occasional spikes in revenue correspond with increases in units sold.

### Year-over-Year Trend
-	Revenue increased from 2021 → 2023, indicating business growth.
-	Revenue declined in 2024, suggesting a potential slowdown in demand or market changes.

### Month-over-Month Trend
-	April has the lowest revenue
-	May has the highest revenue
Supplement demand may increase heading into summer months, possibly due to fitness goals, weight loss programs, or seasonal health trends.

## Discount and Pricing Impact 
### Pareto Chart – Revenue by Discount
-	0–5% discount contributes the highest revenue (~$5M).
-	Around 80% of total revenue comes from discounts below ~15%.
-	Higher discount ranges contribute significantly less revenue.
-	Most revenue is generated with low or moderate discounts, meaning customers are willing to purchase without heavy price reductions.

### Revenue and Units Sold by Discount
-	Units sold increase gradually as discounts increase up to around 10%.
-	After 11–20% discount, both units sold and revenue fluctuate rather than increase consistently.
-	At 25% discount, both revenue and units sold drop sharply.
-	There is a clear “sweet spot” around 5%–10% discount, where both revenue and sales volume are strong.

### Price Range vs Units Sold 
-	Units sold are fairly stable across all price ranges (≈61K – 70K).
-	The highest sales occur in the $30–40 range:
     - $30–35 → ~70,706 units (peak)
     - $35–40 → ~70,265 units
-	Sales slightly decline at very low ($20–25) and very high ($50–60) price ranges.
-	Demand is not highly price sensitive — customers are buying almost similar quantities across price points.
-	However, there is a clear peak demand in the mid-price range ($30–40).

### Price vs Units Sold 
-	The data is densely concentrated around 140–160 units sold, regardless of price.
-	There is no strong upward or downward trend as price increases.
- The pattern is almost horizontal, indicating there is no relationship between price and units sold.
