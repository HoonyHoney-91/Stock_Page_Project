import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go

def get_stock_price_chart(ticker_symbol):
    company_name = yf.Ticker(ticker_symbol).info
    short_name = company_name['shortName']
    data = yf.download(tickers=ticker_symbol, period='1y', interval='1h')
    fig = go.Figure()
    # Line graph
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name='market data', line=dict(color='blue')))
    # Candlestick
    fig.add_trace(go.Candlestick(x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='market data'
            )
        )
    # titles
    fig.update_layout(
            title=f'{short_name} live share price evolution',
            yaxis_title='Stock Price ($ per Share)',
            height=700
        )
    fig.update_xaxes(
            rangeslider_visible=True,
            type='date',
            tickformat="%Y-%m-%d %H:%M"
        )
    fig.update_xaxes(
        rangeslider_visible=True,
        type='date',
        rangebreaks=[
        # Remove weekends
            dict(bounds=["sat", "mon"]),
        ],
        # Set the initial range to show all available data
        range=[data.index[0].replace(hour=9, minute=30), data.index[-1].replace(hour=15, minute=59)],
        tickformat="%Y-%m-%d %H:%M"
    )
    fig.update_xaxes(
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1d", step="day", stepmode="todate"),
                dict(count=5, label="5d", step="day", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ]),
            bgcolor="rgba(150, 200, 250, 0.4)",
            x=0.05,
            font=dict(color="#000000")
        ),
        rangeslider=dict(visible=True)
    )
    return fig.to_html(full_html=False)
