""" 
Purpose: Building on existing modules for final
Author: Bambee Garfield
"""

# Standard Library
from pathlib import Path
import pandas as pd
import plotly.express as px
from shiny import render, reactive
from shinywidgets import render_widget
import plotly.io as pio
pio.templates.default = 'plotly_dark'

# Local Imports
from mtcars_get_basics import get_mtcars_df
from util_logger import setup_logger

# Set up a global logger for this file
logger, logname = setup_logger(__name__)

# Declare our file path variables globally so they can be used in all the functions (like logger)
csv_locations = Path(__file__).parent.joinpath("data").joinpath("mtcars_location.csv")
csv_stocks = Path(__file__).parent.joinpath("data").joinpath("mtcars_stock.csv")


def get_mtcars_server_functions(input, output, session):
    """Define functions to create UI outputs."""

    # First, declare shared reactive values (used between functions) up front
    # Initialize the values on startup

    reactive_location = reactive.Value("San Diego CA")
    reactive_stock = reactive.Value("Norstrom Inc")

    reactive_df = reactive.Value()
     
    original_df = get_mtcars_df()
    total_count = len(original_df)

##Location Reactions
    @reactive.Effect
    @reactive.event(input.MTCARS_LOCATION_SELECT)
    def _():
        """Set two reactive values (the location and temps df) when user changes location"""
        reactive_location.set(input.MTCARS_LOCATION_SELECT())
        # init_mtcars_temps_csv()
        df = get_mtcars_temp_df()
        logger.info(f"init reactive_temp_df len: {len(df)}")

    @reactive.file_reader(str(csv_locations))
    def get_mtcars_temp_df():
        """Return mtcars temperatures pandas Dataframe."""
        logger.info(f"READING df from {csv_locations}")
        df = pd.read_csv(csv_locations)
        logger.info(f"READING df len {len(df)}")
        return df

    @output
    @render.text
    def mtcars_location_string():
        """Return a string based on selected location."""
        logger.info("mtcars_temperature_location_string starting")
        selected = reactive_location.get()
        line1 = f"Recent Temperature in F for {selected}."
        line2 = "Updated once per minute for 15 minutes."
        line3 = "Keeps the most recent 10 minutes of data."
        message = f"{line1}\n{line2}\n{line3}"
        logger.info(f"{message}")
        return message

    @output
    @render.table
    def mtcars_location_table():
        df = get_mtcars_temp_df()
        selected_locations = input.MTCARS_LOCATION_SELECT()
        # Filter the data based on the selected location
        df_selected_locations = df[df["Location"].isin(selected_locations)]
        logger.info(f"Rendering TEMP table with {len(df_selected_locations)} rows")
        return df_selected_locations

    @output
    @render_widget
    def mtcars_location_chart():
        df = get_mtcars_temp_df()
        selected_locations = input.MTCARS_LOCATION_SELECT()
        # Filter the data based on the selected location
        df_selected_locations = df[df["Location"].isin(selected_locations)]
        logger.info(f"Rendering TEMP chart with {len(df_selected_locations)} points")
        plotly_express_plot = px.line(
            df_selected_locations, x="Time", y="Temp_F", color="Location", markers=True,
        )
        plotly_express_plot.update_layout(title="Continuous Temperature (F)")
        return plotly_express_plot
    
##Stock Reactions
    @reactive.Effect
    @reactive.event(input.MTCARS_STOCK_SELECT)
    def _():
        """Set reactive_stock and update data when user changes selection"""
        reactive_stock.set(input.MTCARS_STOCK_SELECT())
        # init_mtcars_stock_csv()  # Initialize stocks data if needed
        df = get_mtcars_stock_df()
        logger.info(f"Updated reactive_stock selection: {reactive_stock.get()}. DataFrame length: {len(df)}")

    @reactive.file_reader(str(csv_stocks))
    def get_mtcars_stock_df():
        """Return mtcars stocks pandas DataFrame."""
        logger.info(f"READING df from {csv_stocks}")
        df = pd.read_csv(csv_stocks)
        logger.info(f"READING df len {len(df)}")
        return df

    @output
    @render.text
    def mtcars_stock_string():
        """Return a string based on selected stock."""
        logger.info("mtcars_stock_string starting")
        selected = reactive_stock.get()
        line1 = f"Recent Price in USD for {selected}."
        line2 = "Updated once per minute for 15 minutes."
        line3 = "Keeps the most recent 10 minutes of data."
        message = f"{line1}\n{line2}\n{line3}"
        logger.info(message)
        return message

    @output
    @render.table
    def mtcars_stock_table():
        df = get_mtcars_stock_df()
        selected_stocks = input.MTCARS_STOCK_SELECT()  # Get selected stocks from the input
        # Filter the data based on the selected tickers
        df_selected_stocks = df[df["Company"].isin(selected_stocks)]
        logger.info(f"Rendering price table with {len(df_selected_stocks)} rows")
        return df_selected_stocks

    @output
    @render_widget
    def mtcars_stock_chart():
        df = get_mtcars_stock_df()
        selected_stocks = input.MTCARS_STOCK_SELECT()  # Get selected stocks from the input
        # Filter the data based on the selected stocks
        df_selected_stocks = df[df["Company"].isin(selected_stocks)]
        logger.info(f"Rendering Price chart with {len(df_selected_stocks)} points")
        plotly_express_plot = px.line(
            df_selected_stocks, x="Time", y="Price", color="Company", markers=True
        )
        plotly_express_plot.update_layout(title="Continuous Price (USD)")
        return plotly_express_plot


    return [
        mtcars_location_string,
        mtcars_location_table,
        mtcars_location_chart,
        mtcars_stock_string,
        mtcars_stock_table,
        mtcars_stock_chart,
    ]