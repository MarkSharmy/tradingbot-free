#Beta Version
import json
import numpy as np
import pandas as pd
import plotly.graph_objects as go

#Function to display candle stick chart
def display_chart(dataframe = None, count = 100, ma = None, bgcolor = "#1e1e1e", font_color = "#e1e1e1", grid_color = "#1f292f"):
    """
    Function to display a candle stick chart to the user, based on the dataframe passed as an argument.
    The function returns a fig object that displays the last {count} candles. If EMA is not null, a 
    moving cross average will be drawn on the chart.

    :param dataframe: dataframe object with the candle sticks
    :param count: integer of the number of candles to be displayed
    :param ma: list of strings with the specified moving averages to be displayed. If null, not MAs are drawn
    :optional params: Background color, font color, grid color
    :return: Figure object
    """
    colors = ["#027FC3", "#FE3B1F", "#FFD600", "#CC009F", "#EA0029"]


    candles = dataframe[-count:]
    fig = go.Figure()

    
    fig.add_trace(go.Candlestick(
        x = candles["time"],
        open = candles["open"],
        high = candles["high"],
        low = candles["low"],
        close = candles["close"],
        line = dict(width = 1),
        opacity = 1,
        increasing_fillcolor = "#24A06B",
        decreasing_fillcolor = "#CC2E3C",
        increasing_line_color = "#2EC886",
        decreasing_line_color = "#FF3A4C"
    ))

    fig.update_layout(
        width = 1300,
        height = 400,
        margin = dict(l = 10, r = 10, t = 10, b = 10),
        font = dict(color = font_color, size = 1),
        paper_bgcolor = bgcolor,
        plot_bgcolor = bgcolor,
    )

    fig.update_xaxes(
        gridcolor = grid_color,
        showgrid = True,
        fixedrange = True,
        rangeslider = dict(visible = True)
    )

    fig.update_yaxes(
        gridcolor = grid_color,
        showgrid = True
    )

    if  ma:
        try:
            for moving_average in ma:
                fig.add_trace(go.Scatter(
                x = candles.time,
                y = candles[moving_average],
                line = dict(color = colors[ma.index(moving_average)], width = 2),
                line_shape = "spline",
                name = moving_average
            ))
        except KeyError as e:
            print(f"Invalid key: Moving average {moving_average} does not exist")
        except IndexError as g:
            print(f"Index out of bounds: Not enough colors")

            
    return fig