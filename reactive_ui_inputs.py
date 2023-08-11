"""
Purpose: Provide user interaction options for Reactive dataset.

"""
from shiny import ui

# Define the UI inputs and include our new selection options

def get_reactive_inputs():
    return ui.panel_sidebar(
        ui.h2("Reactive Interaction"),
        ui.h4("Please select your options from below"),
        ui.tags.hr(),
        
        ui.input_select(
            id="REACTIVE_LOCATION_SELECT",
            label="Choose your location(s) (hold CTRL to select multiple)",
            choices=["Seattle WA",
                "Portland OR", 
                "San Francisco CA", 
                "San Diego CA", 
                "Phoenix AZ"
                ],
            selected="San Diego CA",
            multiple=True,
        ),
        ui.input_select(
            id="REACTIVE_STOCK_SELECT",
            label="Choose your stock(s) (hold CTRL to select multiple)",
            choices=["Nordstrom Inc",
                "Lululemon Athletica Inc",
                "Starbucks Corporation",
                "NIKE Inc",
                "Amazon.com Inc",
                ],
            selected = "Nordstrom Inc",
            multiple=True
        ),
        ui.tags.hr(),
        ui.tags.hr(),
        ui.p("🕒 Please be patient. Outputs may take a few seconds to load."),
        ui.tags.hr(),
    )