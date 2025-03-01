# StockFlow Description

"StockFlow: Fetch, analyze, and plot stock trends with Alpha Vantage and langgraph. 30-day data, moving averages, and visuals in a Python pipeline."  

# StockFlow

StockFlow is a Python tool that fetches, analyzes, and visualizes stock trends using Alpha Vantage and a `langgraph` pipeline. It retrieves 30 days of daily stock data, calculates a 10-day moving average and volatility, and plots the results with Matplotlib.

## Features
- Fetches real-time stock data from Alpha Vantage.
- Computes 10-day moving average and volatility metrics.
- Generates a plot of closing prices and trends, saved as a PNG.
- Modular workflow with `langgraph` for easy extension.

## Prerequisites
- Python 3.8+
- Git
- An [Alpha Vantage API key](https://www.alphavantage.co/support/#api-key) (free tier available)

## Setup Instructions

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/your-username/stock-flow.git
   cd stock-flow
