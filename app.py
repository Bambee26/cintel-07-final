""" Implementing skills learned from Modules 1-6
"""

import asyncio
from shiny import App, ui
import shinyswatch

from continuous_location import update_csv_location
from continuous_stock import update_csv_stock
from reactive_server import get_reactive_server_functions
from reactive_ui_inputs import get_reactive_inputs
from reactive_ui_outputs import get_reactive_outputs
from iris_ui_inputs import get_iris_inputs
from iris_ui_outputs import get_iris_outputs
from util_logger import setup_logger

logger, logname = setup_logger(__file__)

async def update_csv_files():
    while True:
        logger.info("Calling continuous updates ...")
        task1 = asyncio.create_task(update_csv_location())
        task2 = asyncio.create_task(update_csv_stock())
        await asyncio.gather(task1, task2)
        await asyncio.sleep(60)

app_ui = ui.page_navbar(
    shinyswatch.theme.darkly(),
    ui.nav(
        "Home",
        ui.layout_sidebar(
            ui.panel_sidebar(
                ui.h4("Northwest Missouri State University"),
                ui.h5("44630 Continuous Intelligence & Interactive Analytics"),
                ui.tags.hr(),
                ui.h6("Course description: an introduction to the concepts and implementation of systems for continuous intelligence and interactive analytics. It includes ingesting and processing raw data and presenting evolving analytics in engaging, easy-to-understand, actionable formats."),
                ui.tags.hr(),
            ),
            ui.panel_main(
                ui.h3("Bambee Garfield"),
                ui.tags.hr(),
                ui.h4("Final Project"),
                ui.tags.ul(
                    ui.tags.li(ui.h5("To view skills learned in imperative programming, please click on the Imperative tab above.")),
                    ui.tags.li(ui.h5("To view skills learned in reactive programming, please click on the Reactive tab above.")),
                ),
            ),
        ),
    ),
    ui.nav(
        "Imperative",
        ui.layout_sidebar(
            get_iris_inputs(),
            get_iris_outputs(),
        ),
    ),
    ui.nav(
        "Reactive",
        ui.layout_sidebar(
            get_reactive_inputs(),
            get_reactive_outputs(),
        ),
    ),
    ui.nav(ui.a("About", href="https://github.com/Bambee26")),
    ui.nav(ui.a("GitHub", href="https://github.com/Bambee26/cintel-07-final")),
    ui.nav(ui.a("App", href="https://bambee26.shinyapps.io/cintel-07-final/")),
    ui.nav(ui.a("Plotly Express", href="https://plotly.com/python/line-and-scatter/")),
    ui.nav(ui.a("WeatherAPI", href="https://openweathermap.org/api")),
    ui.nav(ui.a("OneCallAPI", href="https://openweathermap.org/api/one-call-3")),
    ui.nav(ui.a("File_Reader", href="https://shiny.rstudio.com/py/api/reactive.file_reader.html")),
    title=ui.h1("Bambee's Dashboard"),
)

def server(input, output, session):
    """Define functions to create UI outputs."""
    logger.info("Starting server ...")
    asyncio.create_task(update_csv_files())
    logger.info("Starting continuous updates ...")
    get_reactive_server_functions(input, output, session)

app = App(app_ui, server, debug=True)
