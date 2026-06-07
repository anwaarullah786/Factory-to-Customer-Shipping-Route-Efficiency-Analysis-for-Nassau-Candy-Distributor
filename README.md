# Factory-to-Customer Shipping Route Efficiency Analysis for Nassau Candy Distributor

## Project Overview
This project analyzes factory-to-customer shipping route efficiency for Nassau Candy Distributor using order and shipment data. The goal is to identify efficient routes, delayed routes, state and regional bottlenecks, and ship mode performance patterns through a live Streamlit dashboard and supporting reports.

## Problem Statement
Nassau Candy Distributor needs route-level visibility into shipping performance across factories, customer states, regions, and shipping modes. Without this visibility, logistics decisions remain reactive instead of data-driven.

## Dataset
The analysis uses `nassau_candy_processed.csv`, which contains order, shipment, customer geography, product, sales, cost, and gross profit fields.

Important note: `Shipping Lead Time` is calculated as:

```text
Ship Date - Order Date
```

Because the dataset does not include final delivery date or carrier scan events, the dashboard measures recorded order-to-shipment lead time, not confirmed end-customer delivery time.

## Dashboard Modules
The Streamlit dashboard includes:

1. **Route Efficiency Overview**
   - Average lead time by route
   - Fastest and slowest routes
   - Shipment volume by region

2. **Route Performance Leaderboard**
   - Top 10 most efficient routes
   - Bottom 10 least efficient routes
   - Route volume, delay rate, variability, and efficiency score

3. **Geographic Shipping Map**
   - US state-level heatmap
   - Average lead time, delay rate, and bottleneck score views
   - Regional and state-level bottleneck tables

4. **Ship Mode Comparison**
   - Average lead time by shipping method
   - Delay rate by shipping method
   - Lead time distribution by ship mode

5. **Route Drill-Down**
   - State-level performance insights
   - Searchable order-level data
   - Order-level shipment timelines from Order Date to Ship Date
   - Filtered CSV download

## User Filters
The dashboard supports:

- Date range filter
- Factory selector
- Region selector
- State selector
- Ship mode selector
- Lead-time threshold slider
- Route selector
- Order/customer/product search

## Files Included

```text
app.py
nassau_candy_processed.csv
requirements.txt
Corrected Research Paper - Nassau Candy Route Efficiency.pdf
Corrected Executive Summary - Nassau Candy Route Efficiency.pdf
```

## How to Run Locally
Install the required packages:

```bash
pip install -r requirements.txt
```

Run the Streamlit app:

```bash
streamlit run app.py
```

## Deployment Notes
For Streamlit Cloud, upload at least these files to the GitHub repository root:

```text
app.py
nassau_candy_processed.csv
requirements.txt
README.md
```

Then connect the repository to Streamlit Cloud and select `app.py` as the main file.

## Deliverables

- Streamlit dashboard for live analytics
- Research paper with EDA, insights, and recommendations
- Executive summary for government stakeholders
- Cleaned processed dataset
- GitHub-ready code and dependency files
