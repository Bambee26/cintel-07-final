""" 
Purpose: Provide reactive output for iris dataset.

Matching the IDs in the UI Sidebar and function/output names in the UI Main Panel
to this server code is critical. They are case sensitive and must match exactly.

"""
import pathlib
from shiny import render
import pandas as pd
import seaborn as sns
import plotly.io as pio
pio.templates.default = 'plotly_dark'

from util_logger import setup_logger

logger, logname = setup_logger(__name__)


def get_iris_server_functions(input, output, session):
    """Define functions to create UI outputs."""

    path_to_data = pathlib.Path(__file__).parent.joinpath("data").joinpath("iris.csv")
    original_df = pd.read_csv(path_to_data)

    # Use the len() function to get the number of rows in the DataFrame.
    total_count = len(original_df)

    @output
    @render.table
    def iris_table():
        return original_df

    @output
    @render.text
    def iris_record_count_string():
        message = f"Showing {total_count} records"
        logger.debug(f"filter message: {message}")
        return message

    @output
    @render.plot
    def iris_plot():
        """
        Use Seaborn to make a quick scatterplot.
        Provide a pandas DataFrame and the names of the columns to plot.
        Learn more at https://stackabuse.com/seaborn-scatter-plot-tutorial-and-examples/
        """
        plt = sns.scatterplot(
            data=original_df,
            x="sep_len",
            y="sep_wid",
        )
        return plt

    # return a list of function names for use in reactive outputs
    return [
        iris_table,
        iris_record_count_string,
        iris_plot,
    ]
