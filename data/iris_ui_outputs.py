"""
Purpose: Display outputs for iris dataset.

Choose the correct ui method for the type of output you want to display.
Provide the exact name of the server function that will provide the output.
"""
from shiny import ui


def get_iris_outputs():
    return ui.panel_main(
        ui.h2("Main Panel with Output (Not Yet Reactive)"),
        ui.tags.hr(),
        ui.tags.section(
            ui.h3("Iris Chart (Seaborn Scatter Plot)"),
            ui.output_plot("iris_plot"),
            ui.tags.hr(),
            ui.h3("Iris Table"),
            ui.output_text("iris_record_count_string"),
            ui.output_table("iris_table"),
            ui.tags.hr(),
        ),
    )
