# 📊 GTM Demo

Go-to-market operations with opportunity management and revenue forecasting.

## 🚀 Quick Start

```bash
git clone git@github.com:hasura/axiom.git
cd axiom
cp .data/.env.template .data/gtm/.env
cd demos/gtm
ddn run dataset-up
ddn supergraph build local
ddn run docker-start
```

## ✨ Actions

- **Sales Operations** - Opportunity management, forecasting, pipeline analytics
- **Marketing Automation** - Campaign management, lead nurturing, sequence creation
- **Revenue Intelligence** - Call analytics, opportunity insights, revenue forecasting
- **Account Management** - Customer 360° view with contact and account data
- **MEDDPICC Framework** - Complex sales opportunity qualification

## 📊 Data

- **Accounts** - Customer accounts, contacts, relationships, user roles
- **Opportunities** - Sales pipeline, forecasts, win/loss analysis, MEDDPICC scoring
- **Campaigns** - Marketing campaigns, lead sequences, engagement metrics
- **Calls** - Transcriptions, action items, topics discussed, participants
- **Products** - Product catalog, opportunity line items, contracts
- **Sequences** - Lead sequences, sequence steps, contact assignment

# Project README (on PromptQL project)

# GTM

## Overview

This PromptQL project provides AI-powered analytics for Go-To-Market (GTM) operations, focusing on sales performance, revenue forecasting, and pipeline management.

**What problem does it solve?**

- Transforms complex sales data into actionable insights without requiring SQL expertise
- Enables sales leaders to quickly analyze pipeline health, forecast accuracy, and team performance
- Automates revenue operations reporting and identifies growth opportunities

**Key features and capabilities:**

- Real-time pipeline analytics and coverage analysis
- Sales performance tracking and quota attainment monitoring
- Competitive win/loss analysis
- Territory and market potential assessment
- Deal velocity and sales cycle optimization

## Getting Started

To use this GTM PromptQL agent effectively:

1. Start with simple queries about current pipeline or recent performance
2. Progress to more complex analyses involving correlations and predictions
3. Use natural language - no technical knowledge required

## Sample Evaluation Prompts

Below are example prompts organized by complexity level to help you understand the agent's capabilities.

| Rank | Prompt | Complexity |
| ---- | ------ | ---------- |
| 1 | [Compare pipeline coverage ratio across different sales segments](https://promptql.console.hasura.io/project/gtm/promptql-playground/thread/ca499e09-64b9-4606-983e-de97d84feb7a/shared) | **Moderate**: Requires ratio calculations across segments |
| 2 | [What's our average sales cycle length by deal size?](https://promptql.console.hasura.io/project/gtm/promptql-playground/thread/bddd7cf5-b8a8-4d06-a443-5b0f96364631/shared) | **Moderate**: Requires duration calculations with segmentation |
| 3 | [Analyze win rates by competitor across different product lines](https://promptql.console.hasura.io/project/gtm/promptql-playground/thread/6a3bdb5e-84af-4498-8b31-e25510c5f276/shared) | **Moderate**: Multiple dimensions, competitive analysis |
| 4 | [Identify which lead sources generate the highest quality pipeline](https://promptql.console.hasura.io/project/gtm/promptql-playground/thread/c160079d-2336-43eb-9be9-17f088c7e244/shared) | **Moderate-Hard**: Requires quality scoring and source attribution |
| 5 | [Analyze the correlation between number of touchpoints and deal close rates](https://promptql.console.hasura.io/project/gtm/promptql-playground/thread/8109fe76-8aa7-422a-847e-565a7d2c10f2/shared) | **Hard**: Statistical correlation across engagement metrics |
| 6 | [What's the impact of multi-threading on enterprise deal velocity?](https://promptql.console.hasura.io/project/gtm/promptql-playground/thread/884c95de-a4f6-46a7-8e91-3fe40f4b1dae/shared) | **Hard**: Complex relationship analysis, stakeholder mapping |
| 7 | [Compare forecast accuracy across different sales managers over the past 3 quarters](https://promptql.console.hasura.io/project/gtm/promptql-playground/thread/3de51612-f908-4570-82be-86dde3d53554/shared) | **Very Hard**: Historical variance analysis, management hierarchy |
| 8 | [Analyze deal slippage patterns and identify early warning signals](https://promptql.console.hasura.io/project/gtm/promptql-playground/thread/2e0c6ce9-caa7-494b-9670-1740c901083e/shared) | **Very Hard**: Pattern recognition, predictive indicators |
| 9 | [Identify accounts with expansion potential based on product usage and engagement](https://promptql.console.hasura.io/project/gtm/promptql-playground/thread/0aa35adc-e9fb-4b85-93b2-1eef1a98cd20/shared) | **Hard**: Multi-source analysis, usage patterns |
| 10 | [Analyze the relationship between sales activity levels and quota attainment](https://promptql.console.hasura.io/project/gtm/promptql-playground/thread/983bab89-7082-4706-aecc-696618edae8f/shared) | **Very Hard**: Activity correlation with performance outcomes |
| 11 | [Compare CAC payback periods across different customer segments and acquisition channels](https://promptql.console.hasura.io/project/gtm/promptql-playground/thread/ed80968d-8b1e-4c9e-9582-ed6566f45efc/shared) | **Hard**: Complex financial metrics across dimensions |
| 12 | [Identify cross-sell opportunities based on customer product adoption patterns](https://promptql.console.hasura.io/project/gtm/promptql-playground/thread/3dd58f51-8424-4051-98ab-51f3060e03b9/shared) | **Very Hard**: Product affinity analysis, adoption sequencing |
| 13 | [Analyze the impact of sales methodology adoption on rep performance](https://promptql.console.hasura.io/project/gtm/promptql-playground/thread/995570e7-6219-4255-9517-d2d2ae11d49d/shared) | **Hard**: Process adherence correlation with outcomes |
| 14 | [What's driving the variance between committed and actual revenue this quarter?](https://promptql.console.hasura.io/project/gtm/promptql-playground/thread/d9de33ff-ac5d-49ee-98d1-2e95908d47fe/shared) | **Hard**: Variance analysis with root cause identification |
| 15 | [Which territories have the highest untapped market potential?](https://promptql.console.hasura.io/project/gtm/promptql-playground/thread/902711e6-6b1e-4d37-9ab8-addd7135ae67/shared) | **Moderate-Hard**: TAM analysis with penetration metrics |
| 16 | [Analyze seasonal patterns in deal closures across different industries](https://promptql.console.hasura.io/project/gtm/promptql-playground/thread/033abf46-eeb0-4373-ba0e-113fe76c04cc/shared) | **Moderate-Hard**: Time-series analysis with industry segmentation |
| 17 | How do proof of concept conversions vary by technical complexity? | **Hard**: POC analysis with complexity scoring |
| 18 | [Create a comprehensive revenue operations dashboard](https://promptql.console.hasura.io/project/gtm/promptql-playground/thread/d6d32e90-c359-4d95-883d-bfb8c73e9638/shared) that shows: Pipeline velocity metrics by stage, Current quarter forecast with confidence levels, Rep performance against quota with pacing, Deal health scores for at-risk opportunities, Territory coverage and white space analysis. Make it actionable with clear signals for where sales leadership should focus. | **Extremely Hard**: Integration of multiple complex metrics and predictive insights. Warning: This prompt can take up to 3 minutes to execute. |
| 19 | [Identify which accounts are showing buying signals based on engagement patterns](https://promptql.console.hasura.io/project/gtm/promptql-playground/thread/61b057e4-8e9f-4154-82ef-e7c8859a0534/shared) | **Hard**: Intent scoring from multiple signal sources |
| 20 | [Analyze the effectiveness of different sales plays by market segment](https://promptql.console.hasura.io/project/gtm/promptql-playground/thread/9a14eb40-d87c-461b-acf1-459008926c84/shared) | **Very Hard**: Play performance analysis with segmentation |
| 21 | [What's the relationship between deal size and number of stakeholders involved?](https://promptql.console.hasura.io/project/gtm/promptql-playground/thread/1cc07307-8c6c-4bdb-a82b-964c1db2541d/shared) | **Moderate-Hard**: Stakeholder analysis with deal correlation |

<!--
## Commented out prompts (not working well in PromptQL currently)

| 1 | Simple | [What are my top opportunities by ARR this quarter?](https://promptql.console.hasura.io/project/gtm/promptql-playground/thread/29cf4c4f-e1d6-4b32-8cae-5df5f1ebb6f4/shared) | **Easy**: Simple ranking with single metric, clear time boundary |
| 2 | Simple | [Which accounts have the highest probability to close this month?](https://promptql.console.hasura.io/project/gtm/promptql-playground/thread/74716202-32ce-467a-9bac-32f4d8338de7/shared) | **Easy**: Binary scoring with clear criteria, single time frame |
| 4 | Simple | [Which sales reps are exceeding their quota targets?](https://promptql.console.hasura.io/project/gtm/promptql-playground/thread/e8a9b575-e59f-4162-a2aa-13bcae589581/shared) | **Moderate**: Requires quota attainment calculations |
| 12 | Complex | [What's the optimal discount threshold that maximizes both win rate and deal value?](https://promptql.console.hasura.io/project/gtm/promptql-playground/thread/f1549b2b-92e7-44d6-9803-ddcb4886ecb6/shared) | **Very Hard**: Optimization problem with multiple constraints |
-->
