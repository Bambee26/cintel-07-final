"""
Purpose: Provide user interaction options for MT Cars dataset.

IDs must be unique. They are capitalized in this app for clarity (not typical).
The IDs are case-sensitive and must match the server code exactly.
Preface IDs with the dataset name to avoid naming conflicts.

"""
from shiny import ui

# Define the UI inputs and include our new selection options

def get_mtcars_inputs():
    return ui.panel_sidebar(
        ui.h2("Reactive Interaction"),
        ui.h4("Please select your options from below"),
        ui.tags.hr(),
        
        ui.input_select(
            id="MTCARS_LOCATION_SELECT",
            label="Choose a location or locations",
            choices=["Seattle WA", "Portland OR", "San Francisco CA", "San Diego CA", "Phoenix AZ"],
            selected="San Diego CA",
            multiple=True,
        ),
        ui.input_select(
            id="MTCARS_STOCK_SELECT",
            label="Choose a company",
            choices=["Nordstrom Inc",
            "Lululemon Athletica Inc",
            "Starbucks Corporation",
            "NIKE Inc",
            "Amazon.com Inc",
            ],
            selected = "Nordstrom Inc",
        ),
        ui.tags.hr(),
        ui.tags.hr(),
        ui.p("🕒 Please be patient. Outputs may take a few seconds to load."),
        ui.tags.hr(),
    )