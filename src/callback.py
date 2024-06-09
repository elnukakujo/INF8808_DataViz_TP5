'''
    This file contains the functions to call when
    a click is detected on the map, depending on the context
'''
import dash_html_components as html
import app 

def no_clicks(style):
    '''
        Deals with the case where the map was not clicked

        Args:
            style: The current display style for the panel
        Returns:
            title: The updated display title
            mode: The updated display title
            theme: The updated display theme
            style: The updated display style for the panel
    '''
    title = ""
    mode = ""
    theme = ""
    style = {**style, 'visibility': 'hidden'}  # Hide the panel
    return title, mode, theme, style

def map_base_clicked(title, mode, theme, style):
    '''
        Deals with the case where the map base is
        clicked (but not a marker)

        Args:
            title: The current display title
            mode: The current display title
            theme: The current display theme
            style: The current display style for the panel
        Returns:
            title: The updated display title
            mode: The updated display title
            theme: The updated display theme
            style: The updated display style for the panel
    '''
    if style.get('visibility') == 'visible':  # Panel is displayed
        # Return the current panel information without any change
        return title, mode, theme, style
    else:  # Panel is not displayed
        # Hide the panel
        style = {**style, 'visibility': 'hidden'}
        return title, mode, theme, style

def map_marker_clicked(figure, curve, point, title, mode, theme, style):
    '''
        Deals with the case where a marker is clicked

        Args:
            figure: The current figure
            curve: The index of the curve containing the clicked marker
            point: The index of the clicked marker
            title: The current display title
            mode: The current display title
            theme: The current display theme
            style: The current display style for the panel
        Returns:
            title: The updated display title
            mode: The updated display title
            theme: The updated display theme
            style: The updated display style for the panel
    '''
    marker_data = figure['data'][curve]
    lon = marker_data['lon'][point]
    lat = marker_data['lat'][point]

    # Find the corresponding feature in the original data
    for feature in app.street_data['features']:  # Access street_df from app module
        if feature['geometry']['coordinates'] == [lon, lat]:
            properties = feature['properties']
            break
    else:
        raise ValueError("Feature not found")

    # Extract relevant properties
    project_name = properties.get('NOM_PROJET', 'Unknown Project')
    duration = properties.get('MODE_IMPLANTATION', 'Unknown Duration')
    themes = properties.get('OBJECTIF_THEMATIQUE', '')
    themes_list = themes.split('\n') if themes else []

    # Creating the panel content
    title = project_name
    mode = duration
    theme = html.Ul([html.Li(theme) for theme in themes_list])
    
    # Add color:
    color = marker_data['marker']['color']
    
    # Apply the color to the displayed project name
    #title = html.Span(title, style={'color': color})
    title = html.Div(project_name, style={'color': color})
    
    style = {**style, 'visibility': 'visible'}  # Show the panel

    return title, mode, theme, style