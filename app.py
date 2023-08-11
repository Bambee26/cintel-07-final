import asyncio

# Then, outside imports (these must be installed into your active Python environment).
from shiny import App, ui   # pip install shiny
import shinyswatch          # pip install shinyswatch

# Finally, import what we need from other local code files.
from continuous_location import update_csv_location
from continuous_stock import update_csv_stock
from reactive_server import get_reactive_server_functions
from reactive_ui_inputs import get_reactive_inputs
from reactive_ui_outputs import get_reactive_outputs
from iris_ui_inputs import get_iris_inputs
from iris_ui_outputs import get_iris_outputs
from util_logger import setup_logger

# Set up a logger for this file (see the logs folder to help with debugging).
logger, logname = setup_logger(__file__)


# Define a function that will run continuously to update our data.
# We update to a local file, but we could also update to a database.
# Or a cloud service. Or a data lake. Or a data warehouse.
async def update_csv_files():
    while True:
        logger.info("Calling continuous updates ...")
        task1 = asyncio.create_task(update_csv_location())
        task2 = asyncio.create_task(update_csv_stock())
        await asyncio.gather(task1)
        await asyncio.gather(task2)
        await asyncio.sleep(60)  # wait for 60 seconds

app_ui = ui.page_navbar(
    shinyswatch.theme.darkly(),
     ui.nav(
        "Data",
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

    # Kick off continuous updates when the app starts
    asyncio.create_task(update_csv_files())
    logger.info("Starting continuous updates ...")

    get_reactive_server_functions(input, output, session)



app = App(app_ui, server, debug=True)