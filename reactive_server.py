""" 
Purpose: Building on existing modules for final
Author: Bambee Garfield
"""

from pathlib import Path
import pandas as pd
import plotly.express as px
from shiny import render, reactive
from shinywidgets import render_widget
import plotly.io as pio
pio.templates.default = 'plotly_dark'

from reactive_get_basics import get_reactive_df
from util_logger import setup_logger

logger, logname = setup_logger(__name__)

csv_locations = Path(__file__).parent.joinpath("data").joinpath("reactive_location.csv")
csv_stocks = Path(__file__).parent.joinpath("data").joinpath("reactive_stock.csv")


def get_reactive_server_functions(input, output, session):
    """Define functions to create UI outputs."""


    reactive_location = reactive.Value("San Diego CA")
    reactive_stock = reactive.Value("Norstrom Inc")

    reactive_df = reactive.Value()
     
    original_df = get_reactive_df()
    total_count = len(original_df)

##Location Reactions
    @reactive.Effect
    @reactive.event(input.REACTIVE_LOCATION_SELECT)
    def _():
        reactive_location.set(input.REACTIVE_LOCATION_SELECT())
        df = get_reactive_temp_df()
        logger.info(f"init reactive_temp_df len: {len(df)}")

    @reactive.file_reader(str(csv_locations))
    def get_reactive_temp_df():
        logger.info(f"READING df from {csv_locations}")
        df = pd.read_csv(csv_locations)
        logger.info(f"READING df len {len(df)}")
        return df

    @output
    @render.text
    def reactive_location_string():
        """Return a string based on selected location."""
        logger.info("reactive_temperature_location_string starting")
        selected = reactive_location.get()
        line1 = f"Recent Temperature in F for {selected}."
        line2 = "Updated once per minute for 15 minutes."
        line3 = "Keeps the most recent 10 minutes of data."
        message = f"{line1}\n{line2}\n{line3}"
        logger.info(f"{message}")
        return message

    @output
    @render.table
    def reactive_location_table():
        df = get_reactive_temp_df()
        selected_locations = input.REACTIVE_LOCATION_SELECT()
        df_selected_locations = df[df["Location"].isin(selected_locations)]
        logger.info(f"Rendering TEMP table with {len(df_selected_locations)} rows")
        return df_selected_locations

    @output
    @render_widget
    def reactive_location_chart():
        df = get_reactive_temp_df()
        selected_locations = input.REACTIVE_LOCATION_SELECT()
        df_selected_locations = df[df["Location"].isin(selected_locations)]
        logger.info(f"Rendering TEMP chart with {len(df_selected_locations)} points")
        plotly_express_plot = px.line(
            df_selected_locations, x="Time", y="Temp_F", color="Location", markers=True,
        )
        plotly_express_plot.update_layout(title="Continuous Temperature (F)")
        return plotly_express_plot
    
##Stock Reactions
    @reactive.Effect
    @reactive.event(input.REACTIVE_STOCK_SELECT)
    def _():
        """Set reactive_stock and update data when user changes selection"""
        reactive_stock.set(input.REACTIVE_STOCK_SELECT())
        df = get_reactive_stock_df()
        logger.info(f"Updated reactive_stock selection: {reactive_stock.get()}. DataFrame length: {len(df)}")

    @reactive.file_reader(str(csv_stocks))
    def get_reactive_stock_df():
        logger.info(f"READING df from {csv_stocks}")
        df = pd.read_csv(csv_stocks)
        logger.info(f"READING df len {len(df)}")
        return df

    @output
    @render.text
    def reactive_stock_string():
        logger.info("reactive_stock_string starting")
        selected = reactive_stock.get()
        line1 = f"Recent Price in USD for {selected}."
        line2 = "Updated once per minute for 15 minutes."
        line3 = "Keeps the most recent 10 minutes of data."
        message = f"{line1}\n{line2}\n{line3}"
        logger.info(message)
        return message

    @output
    @render.table
    def reactive_stock_table():
        df = get_reactive_stock_df()
        selected_stocks = input.REACTIVE_STOCK_SELECT()
        df_selected_stocks = df[df["Company"].isin(selected_stocks)]
        logger.info(f"Rendering price table with {len(df_selected_stocks)} rows")
        return df_selected_stocks

    @output
    @render_widget
    def reactive_stock_chart():
        df = get_reactive_stock_df()
        selected_stocks = input.REACTIVE_STOCK_SELECT()
        df_selected_stocks = df[df["Company"].isin(selected_stocks)]
        logger.info(f"Rendering Price chart with {len(df_selected_stocks)} points")
        plotly_express_plot = px.line(
            df_selected_stocks, x="Time", y="Price", color="Company", markers=True
        )
        plotly_express_plot.update_layout(title="Continuous Price (USD)")
        return plotly_express_plot


    return [
        reactive_location_string,
        reactive_location_table,
        reactive_location_chart,
        reactive_stock_string,
        reactive_stock_table,
        reactive_stock_chart,
    ]