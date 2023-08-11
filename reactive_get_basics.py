"""
Purpose: 

Provide basic non-reactive functions to support 
the Reactive continuous intelligence and interactive analytics dashboard.

These functions can be used and tested independently of our Shiny app.

Keeping them separate makes our dashboard code cleaner and easier to read.
"""
import pathlib
import os
import pandas as pd
from util_logger import setup_logger

logger, logname = setup_logger(__name__)


def get_reactive_df():
    p = pathlib.Path(__file__).parent.joinpath("data").joinpath("reactive.csv")
    logger.info(f"Reading data from {p}")
    df = pd.read_csv(p)
    return df