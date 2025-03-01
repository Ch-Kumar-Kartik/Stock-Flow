import matplotlib.pyplot as plt
from langgraph.graph import StateGraph, END
import pandas as pd
from typing import Dict, Any, TypedDict
from alpha_vantage.timeseries import TimeSeries
import time


class StockStateDict(TypedDict):
    ticker: str
    period: str  
    interval: str  
    data: Dict[str, Any]
    plot_path: str


def fetch_stock_data(state: StockStateDict) -> StockStateDict:
    ticker = state["ticker"]
    api_key = "AV_Key"  
    
    ts = TimeSeries(key=api_key, output_format='pandas')
    for attempt in range(5):  
        try:
            data, _ = ts.get_daily(symbol=ticker, outputsize='compact')  
            data = data.tail(30)  
            data = data.rename(columns={
                '1. open': 'Open',
                '2. high': 'High',
                '3. low': 'Low',
                '4. close': 'Close',
                '5. volume': 'Volume'
            })  
            state["data"] = data.to_dict()
            break
        except Exception as e:  
            wait_time = 60
            print(f"Error fetching data: {e}. Waiting {wait_time} seconds... (Attempt {attempt + 1}/5)")
            time.sleep(wait_time)
    else:
        raise Exception("Failed to fetch data after 5 attempts.")
    return state


def analyze_stock_data(state: StockStateDict) -> StockStateDict:
    data = pd.DataFrame(state["data"])
    data["MA_10"] = data["Close"].rolling(window=10).mean()
    data["Volatility"] = data["Close"].pct_change().rolling(window=10).std()
    state["data"] = data.to_dict()
    return state


def plot_stock_data(state: StockStateDict) -> StockStateDict:
    data = pd.DataFrame(state["data"])
    ticker = state["ticker"]
    
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data["Close"], label="Close Price", color="blue")
    plt.plot(data.index, data["MA_10"], label="10-Day Moving Avg", color="red")
    plt.title(f"Stock Trends for {ticker}")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid()
    plt.xticks(rotation=45)
    plot_path = f"{ticker}_stock_plot.png"
    plt.savefig(plot_path)
    plt.close()
    
    state["plot_path"] = plot_path
    return state


def build_graph():
    workflow = StateGraph(StockStateDict)
    
    workflow.add_node("fetch_data", fetch_stock_data)
    workflow.add_node("analyze_data", analyze_stock_data)
    workflow.add_node("plot_data", plot_stock_data)
    
    workflow.add_edge("fetch_data", "analyze_data")
    workflow.add_edge("analyze_data", "plot_data")
    workflow.add_edge("plot_data", END)
    
    workflow.set_entry_point("fetch_data")
    
    return workflow.compile()


def run_demo():
    state = {
        "ticker": "AAPL",
        "period": "1mo",  
        "interval": "1d",  
        "data": None,
        "plot_path": ""
    }
    
    graph = build_graph()
    final_state = graph.invoke(state)
    
    print(f"Analysis completed for {final_state['ticker']}")
    print(f"Sample closing prices: {list(final_state['data']['Close'].values())[:5]}...")
    print(f"Plot saved at: {final_state['plot_path']}")

if __name__ == "__main__":
    run_demo()