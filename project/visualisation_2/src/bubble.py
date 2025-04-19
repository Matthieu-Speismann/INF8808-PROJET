'''
    This file contains the code for the bubble plot.
'''

import plotly.express as px  # Importing Plotly Express for creating visualizations
import math  # Importing math module (not used in the current code)

import project.visualisation_2.src.hover_template as hover_template  # Importing custom hover template module


def get_plot(df, graph_id: int = 1):
    '''
        Generates the bubble plot.

        The x and y axes are log scaled, and there is
        an animation between the data for years 2000 and 2015.

        The discrete color scale (sequence) to use is Set1 (see : https://plotly.com/python/discrete-color/)

        The markers' maximum size is 30 and their minimum
        size is 6.

        Args:
            df: The dataframe to display
        Returns:
            The generated figure
    '''
    # Calculate the minimum and maximum population values in the dataframe
    min, max = df['Population'].min(), df['Population'].max()
    
    # Scale marker sizes between 3 and 200 based on population values
    df['marker_size'] = 3 + ((df['Population'] - min) / (max - min)) * (200 - 3)

    # Create a scatter plot with animation frames for different years
    fig = px.scatter(
        df,
        x="PIB_per_Capita",  # X-axis: GDP per capita
        y="nb_medals",  # Y-axis: Number of medals
        animation_frame="Year_Group",  # Animation based on year groups
        size="marker_size",  # Marker size based on scaled population
        size_max=50,  # Maximum marker size
        color="continent" if graph_id == 1 else "Climate",  # Color by continent or climate
        color_discrete_sequence=px.colors.qualitative.Set1,  # Use Set1 color scale
        log_x=True,  # Logarithmic scale for x-axis
        log_y=True,  # Logarithmic scale for y-axis
        range_x=[100, 130000],  # X-axis range
        range_y=[0.5, 800],  # Y-axis range
        custom_data=["Region", "Population", "continent", "Climate"]  # Additional data for hover templates
    )

    return fig


def update_animation_hover_template(fig):
    '''
        Sets the hover template of the figure,
        as well as the hover template of each
        trace of each animation frame of the figure

        Args:
            fig: The figure to update
        Returns:
            The updated figure
    '''

    # Update the hover template for the main figure traces
    fig.update_traces(hovertemplate=hover_template.get_bubble_hover_template())

    # Update the hover template for each trace in each animation frame
    for frame in fig.frames:
        for trace in frame.data:
            trace.hovertemplate = hover_template.get_bubble_hover_template()
    return fig


def update_animation_menu(fig, graph_id: int = 1):
    '''
        Updates the animation menu to show the current year, and to remove
        the unnecessary 'Stop' button.

        Args:
            fig: The figure containing the menu to update
        Returns
            The updated figure
    '''
    # Remove the default animation menu
    fig.layout.pop("updatemenus", None)

    # Add a custom animation menu with a single "Animate" button
    fig.update_layout(
        updatemenus=[
            {
                "buttons": [
                    {
                        "args": [None, {"frame": {"duration": 500, "redraw": True}, "fromcurrent": False, 'visible': True}],
                        "label": "Animate",  # Label for the button
                        "method": "animate"  # Method to trigger animation
                    },
                ],
                "direction": "left",  # Direction of the menu
                "pad": {"r": 10, "t": 87},  # Padding for positioning
                "showactive": False,  # Disable active state for buttons
                "type": "buttons",  # Type of menu
                "x": 0.09,  # X position of the menu
                "xanchor": "right",  # Anchor position for x
                "y": 0.03,  # Y position of the menu
                "yanchor": "top"  # Anchor position for y
            }
        ],
        sliders=[{
            "currentvalue": {
                "prefix": "Data for year: ",  # Prefix for the current year slider
            }
        }]
    )
    return fig


def update_axes_labels(fig):
    '''
        Updates the axes labels with their corresponding titles.

        Args:
            fig: The figure to be updated
        Returns:
            The updated figure
    '''
    # Set the title for the x-axis
    fig.update_xaxes(title="PIB par Capita ($ USD)")
    
    # Set the title for the y-axis
    fig.update_yaxes(title="Médailles par jeux olympiques")
    return fig


def update_template(fig):
    '''
        Updates the layout of the figure, setting
        its template to 'simple_white'

        Args:
            fig: The figure to update
        Returns:
            The updated figure
    '''
    # Set the layout template to 'simple_white'
    fig.update_layout(template='simple_white')
    return fig


def update_legend(fig):
    '''
        Updated the legend title

        Args:
            fig: The figure to be updated
        Returns:
            The updated figure
    '''
    # Update the legend title text
    fig.update_layout(legend_title_text="Legende")
    return fig