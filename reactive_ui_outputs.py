"""
Purpose: Display output for Reactive datasets.

@imports shiny.ui as ui
@imports shinywidgets.output_widget for interactive charts
"""
from shiny import ui
from shinywidgets import output_widget


def get_reactive_outputs():
    return ui.panel_main(
        ui.h2("Outputs for selected interactions"),
        ui.tags.hr(),
        ui.tags.section(
            ui.h3("Tracking weather changes with a weather API"),
            ui.tags.br(),
            ui.output_text("reactive_location_string"),
            ui.tags.br(),
            ui.output_ui("reactive_location_table"),
            ui.tags.br(),
            output_widget("reactive_location_chart"),
            ui.tags.br(),
            ui.tags.hr(),
            ui.h3("Tracking stock changes with a stock API"),
            ui.tags.br(),
            ui.output_text("reactive_stock_string"),
            ui.tags.br(),
            ui.output_ui("reactive_stock_table"),
            ui.tags.br(),
            output_widget("reactive_stock_chart"),
            ui.tags.hr(),
        ),
    )   