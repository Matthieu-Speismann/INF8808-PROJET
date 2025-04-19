'''
    Provides the template for the tooltips.
'''


def get_bubble_hover_template():
    '''
        Sets the template for the hover tooltips.
        
        Contains four labels, followed by their corresponding
        value and units where appropriate, separated by a
        colon : country, population, GDP and CO2 emissions.

        The labels' font is bold and the values are normal weight

        returns:
            The content of the tooltip
    '''
    # Define the hover template as a formatted string
    hover_template = (
        # Start the tooltip with a span tag to set the font family
        "<span style='font-family:Inter;'>"
        # Display the country name in bold, using customdata[0] for the value
        "<b>Country: </b> %{customdata[0]}<br>"
        # Display the continent name in bold, using customdata[2] for the value
        "<b>Continent: </b> %{customdata[2]}<br>"
        # Display the climate in bold, using customdata[3] for the value
        "<b>Climate: </b> %{customdata[3]}<br>"
        # Display the average population in bold, formatted with commas, using customdata[1]
        "<b>Average Population: </b> %{customdata[1]:,}<br>"
        # Display the GDP per capita in bold, formatted with commas and a dollar sign, using x
        "<b>GDP per Capita: </b> %{x:,} $ (USD)<br>"
        # Display the medals per Olympic Games in bold, formatted with commas, using y
        "<b>Medals per Olympic Games: </b> %{y:,}</span>"
        # Add an empty <extra> tag to remove the default hover box
        "<extra></extra>"
    )
    # Return the formatted hover template
    return hover_template