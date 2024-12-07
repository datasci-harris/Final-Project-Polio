
print("Starting the app...")
from shiny import App, render, ui, reactive
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv("/Users/afreenwala/Documents/GitHub/Final-Project-Polio/Data Wrangling/Merged Data/merged_df.csv")

# Define the User Interface
app_ui = ui.page_fluid(
    # Dropdown to select country
    ui.input_select(id='country_name', label='Choose a Country:', choices=data['country_name'].unique().tolist()),
    
    # Radio buttons to select the metric
    ui.input_radio_buttons(
        id='metric', label='Choose a Metric:', 
        choices=['Immunisation Percentage', 'Estimated Polio Cases', 'Defecation Rate']
    ),
    
    # Output plot and table
    ui.output_plot('metric_plot'),
    ui.output_table("filtered_table")
)

# Define the server logic
def server(input, output, session):
    
    @reactive.calc
    def filtered_data():
        # Filter the data based on selected country
        return data[data['country_name'] == input.country_name()]

    # Render the filtered data table
    @render.table()
    def filtered_table():
        return filtered_data()

    # Render the plot based on selected metric
    @render.plot
    def metric_plot():
        df = filtered_data()
        
        # Map the selected metric to the corresponding column in the data
        metric_column = {
            'Immunisation Percentage': 'immunisation_percentage',
            'Estimated Polio Cases': 'estimated_polio_cases',
            'Defecation Rate': 'defecation_rate'
        }[input.metric()]

        # Create the plot
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(df['year'], df[metric_column], marker='o')
        ax.set_title(f"{input.metric()} in {input.country_name()}")
        ax.set_xlabel("Year")
        ax.set_ylabel(input.metric())
        plt.xticks(rotation=45)
        plt.grid(True)

        return fig

# Create the app
app = App(app_ui, server)

