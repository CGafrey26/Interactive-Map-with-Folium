# Import required libraries
import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

spacex_df = pd.read_csv("spacex_launch_data.csv")
# Initialize the Dash app
app = Dash(__name__)

# Get unique launch sites
launch_sites = spacex_df['Launch Site'].unique().tolist()
dropdown_options = [{'label': 'All Sites', 'value': 'ALL'}] + \
                  [{'label': site, 'value': site} for site in launch_sites]

# Define min and max payload for the slider
min_payload = 0
max_payload = 10000

# App layout
app.layout = html.Div([
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center'}),
    
    # TASK 1: Dropdown for launch site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=dropdown_options,
        value='ALL',
        placeholder='Select a Launch Site here',
        searchable=True
    ),
    
    # Graph for pie chart
    dcc.Graph(id='success-pie-chart'),
    
    # TASK 3: Range slider for payload
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={i: str(i) for i in range(0, 11000, 1000)},
        value=[min_payload, max_payload]
    ),
    
    # Graph for scatter plot
    dcc.Graph(id='success-payload-scatter-chart')
])

# TASK 2: Callback for pie chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # Aggregate success counts for all sites
        fig = px.pie(
            spacex_df,
            values='class',
            names='class',
            title='Total Success Launches for All Sites'
        )
    else:
        # Filter for selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        # Count success (1) and failure (0)
        fig = px.pie(
            filtered_df,
            values=filtered_df['class'].value_counts().values,
            names=filtered_df['class'].value_counts().index,
            title=f'Success vs Failure for {entered_site}'
        )
    return fig

# TASK 4: Callback for scatter plot
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def get_scatter_plot(entered_site, payload_range):
    # Filter by payload range
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
        (spacex_df['Payload Mass (kg)'] <= payload_range[1])
    ]
    
    if entered_site == 'ALL':
        # Scatter plot for all sites
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Payload vs. Mission Outcome for All Sites'
        )
    else:
        # Scatter plot for selected site
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Payload vs. Mission Outcome for {entered_site}'
        )
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)