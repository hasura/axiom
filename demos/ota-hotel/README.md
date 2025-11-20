## Overview

This demo suited for the OTA (Online Travel Aggregator) platform , for now we have limited to hotel booking but in future it will expand to flights as well. It contains database, semantic layer and instructions containing few metrics which can help user perform data analysis on hotels, bookings, users, traffic, marketing, and external factors (cities, festivals, weather)

## Getting started

Please make sure you've created `.env` and `.env.cloud` files in current directory of demo project (`/<demo>/.env` and `/<demo>/.env.cloud`) before running below commands.

```
# start the database instance and load data
ddn run dataset-up

# start the DDN engine and promptql playground using the docker-start command
ddn run docker-start

```

There are two SQL scripts:

- `01-setup.sql` - creates the database schema
- `02-generate_seeds.sql` - loads the data into the database

There are couple of python scripts which you can use to generate seeds as well in case if you want to generate more data.

## Analysis areas

Here are some **high-impact analyses** you can perform on this dataset:

### **Revenue & Business Performance**

**Booking conversion funnel analysis** \- Track user journey from traffic source → search → booking to identify drop-off points. Which stages lose the most potential customers? This directly informs where product improvements will have maximum impact.

**Marketing ROI by channel** \- Calculate cost per acquisition and lifetime value by traffic source (paid search, social, organic, email). Which channels bring profitable customers vs. one-time bookers? This guides budget reallocation and product features for high-value channels.

**Cancellation pattern analysis** \- Identify what drives cancellations: booking window, hotel type, price point, user segments. High cancellation rates might indicate product friction like unclear policies or poor hotel descriptions.

### **User Behavior & Segmentation**

**User cohort analysis** \- Group users by first booking date and track retention, repeat booking rates, and revenue over time. Are users who book during promotions less loyal? This shapes retention strategies and product personalization.

**Search-to-booking patterns** \- Analyze search filters used, number of searches before booking, price sensitivity by segment. This reveals whether your search/filter UI matches user needs or creates friction.

**Device & platform analysis** \- Compare mobile vs. desktop booking behavior, conversion rates, and average order value. If mobile converts poorly, the product team needs to prioritize mobile UX improvements.

### **External Factor Impact**

**Festival/event impact on demand** \- Correlate booking spikes with local festivals, conferences, or events. This helps with dynamic pricing algorithms and targeted marketing campaigns.

**Weather influence on booking behavior** \- Does weather at origin or destination affect booking timing or cancellations? This could inform product features like weather-based recommendations or flexible booking options.

**Seasonality and lead time analysis** \- How far in advance do users book for different seasons or destinations? This informs inventory management and promotional timing.

### **Product-Specific Insights**

**Price elasticity analysis** \- Test how booking rates respond to price changes across different segments and hotel categories. This calibrates your pricing engine and discount strategies.

**Feature usage vs. conversion** \- If you have product features (filters, reviews, photos, virtual tours), measure which ones correlate with higher conversion and customer satisfaction. This prioritizes feature development.

**Customer lifetime value prediction** \- Build a model predicting which users will become repeat customers based on first booking characteristics. This helps personalize the experience for high-potential users.
