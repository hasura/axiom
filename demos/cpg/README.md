# 🛒 CPG Demo

Consumer packaged goods retail operations with product management and promotional planning.

## 🚀 Quick Start

```bash
cd demos/cpg
cp ../../.data/.env.template ../../.data/cpg/.env
ddn run dataset-up
ddn run docker-start
```

# Sample Prompts
## CPG Demo Prompts, with explanations

Most of these prompts will run to completion in under one minute, but some can take a bit longer.  For those, make sure to expand the execution page to watch PromptQL build the answer in real-time!

| Rank | Complexity | Prompt | Difficulty Assessment |
|------|------------|--------|------------------------|
| 1 | Simple | Which retailers have the highest out-of-stock incidents, and what products are most affected? | **Very Easy**: Simple data retrieval with clear metrics, straightforward visualization |
| 2 | Simple | Compare the performance of organic vs. non-organic products in our portfolio | **Easy**: Binary comparison with clear grouping criteria, intuitive metrics |
| 3 | Simple | Which retailers should we prioritize for our new product launches based on historical performance? | **Moderate**: Requires multi-dimensional analysis of retailer performance |
| 4 | Simple | Which retailers have the highest growth potential based on our current market penetration? | **Moderate**: Requires market analysis and growth modeling |
| 5 | Simple | Which products have the highest variance between forecasted and actual demand? | **Moderate**: Requires forecast accuracy analysis and variance calculations |
| 6 | Complex | Analyze our top-performing products by sales volume and revenue over the past year | **Moderate**: Multiple ranking criteria and metrics, requires business context |
| 7 | Complex | Identify which promotional strategies have generated the highest ROI in the last 6 months | **Moderate-Hard**: Complex ROI calculations, multiple dimensions to analyze |
| 8 | Complex | Analyze inventory turnover rates across our warehouses and suggest optimization opportunities | **Hard**: Complex inventory metrics, financial impact calculations |
| 9 | Complex | Compare our pricing strategy against competitor products in the same category | **Hard**: Competitive analysis requiring external data, strategic interpretation |
| 10 | Complex | What's the correlation between product facings and sales performance across different retailers? | **Very Hard**: Statistical correlation analysis across multiple dimensions |
| 11 | Complex | Analyze the impact of supply chain disruptions on our product availability and sales | **Very Hard**: Requires causal analysis and supply chain expertise |
| 12 | Complex | Identify products with declining sales trends that might need promotional attention or reformulation | **Hard**: Trend analysis with causal interpretation |
| 13 | Complex | Analyze the relationship between promotional discounts and long-term sales performance | **Very Hard**: Time-series analysis with promotional lift and long-term effects |
| 14 | Complex | What's the optimal inventory level for our high-velocity products to minimize stockouts while controlling holding costs? | **Very Hard**: Optimization problem requiring inventory modeling |
| 15 | Complex | Compare the performance of our premium vs. value brand tiers across different retailer segments | **Hard**: Multi-dimensional analysis across brand tiers and retailer segments |
| 16 | Complex | Identify cross-selling opportunities based on product purchase patterns | **Very Hard**: Requires market basket analysis and association rules |
| 17 | Complex | Analyze the impact of e-commerce vs. brick-and-mortar sales channels on our product mix | **Hard**: Channel analysis with product mix implications |
| 18 | Complex | Create a comprehensive retail operations dashboard | **Extremely Hard**: Integration of multiple metrics, KPIs, and visualizations into a cohesive dashboard |
| 19 | Complex | Which products perform better in urban vs. rural markets? | **Moderate**: Requires regional segmentation and sales correlation |
| 20 | Complex | What seasonal trends can we observe in sales across product categories? | **Moderate-Hard**: Needs time-series and seasonal decomposition analysis |
| 21 | Complex | How do bundle promotions impact sales of individual SKUs? | **Hard**: Bundle uplift modeling and SKU-level impact tracking |
| 22 | Complex | Create a comprehensive retail operations dashboard that shows:<br><br>- Monthly sales trends by product category<br>- Current inventory levels with alerts for products approaching reorder points<br>- Market share visualization across key categories<br>- Supply chain indicators for days of supply<br><br>Make it visually appealing with clear KPIs and actionable insights that would help me make quick strategic decisions. | **Hard**: Composition and visualization of multiple complex queries<br><br>* Warning: This Prompt can take up to 3 min to execute.   |

## ✨ Actions

- **Retail Actions** - Update product pricing, create promotions, allocate inventory
- **Product Management** - Catalog and category management
- **Promotional Planning** - Campaign creation and discount management
- **Market Analytics** - Sales tracking and competitive intelligence
- **Supply Chain Visibility** - Event tracking and management

## 📊 Data

- **Products** - Catalog with categories and attributes
- **Inventory** - Stock levels, availability, warehouse locations
- **Sales** - Transactions, pricing history, promotional effectiveness
- **Market** - Competitor products, market shares, demand forecasts
- **Retail** - Retailers, channels, brands, assortment planning
- **Supply Chain** - Events, shipping information
- **Promotions** - Campaign effectiveness, discount strategies
