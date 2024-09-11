from dash import Dash, html, dcc, callback, Output, Input, callback_context
import dash_mantine_components as dmc
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import dash_leaflet as dl
app = Dash()
def load_dataframe():
    df= pd.read_excel('./data/data.xlsx')
    columns= {
        "DISTRICT": 'district',
        'WARD': 'ward',
        'VILLAGE': 'village',
        'LATITUDE': 'latitude',
        'LONGITUDE': 'longitude',
        'YEAR': 'year',
        'HH_SERVED': 'hh_served',
        'FUNCTIONAL_STAT': 'functional_stat',
        'PUMP_TYPE': 'pump_type',
        'OUTLET': 'outlet',
        'SOAK_AWAY_PIT': 'soak_away_pit',
        'PROTECTE': 'protecte',
        'DATE OF LAST VISIT': 'date_of_last_visit',
        'VPM_VISITS/YEAR': 'vpm_visits_yearly',
        'BH_COMMITTE': 'bh_committe',
        'SEASONALITY': 'seasonality',
        'AQUIFER_YIELD': 'aquifer_yield',
        'BH_DEPT': 'bh_depth',
        'PALATABILIT': 'palatabilit',
        'TOTAL _DISSOLVED -SOLIDS': 'total_dissolved_solids'
    }
    df.rename(columns=columns, inplace= True)
    return df

df= load_dataframe()
def year_distribution():
    grouped_data= df.groupby('year').size().reset_index(name="Boreholes")
    return {
        "data": [
            go.Scatter(
                x=grouped_data["year"],
                y=grouped_data["Boreholes"],
                name="Pump Type Borehole distribution",
                marker=dict(
                    color='orange',
                ),
            )
        ],
        "layout": go.Layout(
            barmode="stack",
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff",
            title={
                "text": "<b> Borehole Distribution Over the years</b>",
                "y": 0.93,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
            },
            titlefont={"color": "black", "size": 20},
            hovermode="x",
            xaxis=dict(
                title="<b>Year</b>",
                color="black",
                showline=True,
                showgrid=True,
                showticklabels=True,
                linecolor="black",
                linewidth=2,
                ticks="outside",
                tickfont=dict(family="Arial", size=12, color="black"),
            ),
            yaxis=dict(
                title="<b> Boreholes </b>",
                color="black",
                showline=True,
                showgrid=True,
                showticklabels=True,
                linecolor="black",
                linewidth=2,
                ticks="outside",
                tickfont=dict(family="Arial", size=12, color="black"),
            ),
            legend={
                "orientation": "h",
                "bgcolor": "#ffffff",
                "xanchor": "center",
                "x": 0.5,
                "y": -0.6,
            },
            font=dict(family="sans-serif", size=12, color="black"),
        ),
    }
def pumptype_distribution():
    grouped_data= df.groupby('pump_type').size().reset_index(name="Boreholes")
    return {
        "data": [
            go.Bar(
                x=grouped_data["pump_type"],
                y=grouped_data["Boreholes"],
                name="Pump Type Borehole distribution",
                marker=dict(
                    color='orange',
                ),
                hoverinfo='text',
                hovertext='<b>Pump Type: </b>'+ grouped_data['pump_type'] + '<br>' + '<b>Boreholes: </b>' + grouped_data['Boreholes'].astype(str)
            )
        ],
        "layout": go.Layout(
            barmode="stack",
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff",
            title={
                "text": "<b>Pump Type Borehole Distribution</b>",
                "y": 0.93,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
            },
            titlefont={"color": "black", "size": 20},
            hovermode="x",
            xaxis=dict(
                title="<b>Pump Type</b>",
                color="black",
                showline=True,
                showgrid=True,
                showticklabels=True,
                linecolor="black",
                linewidth=2,
                ticks="outside",
                tickfont=dict(family="Arial", size=12, color="black"),
            ),
            yaxis=dict(
                title="<b> Boreholes </b>",
                color="black",
                showline=True,
                showgrid=True,
                showticklabels=True,
                linecolor="black",
                linewidth=2,
                ticks="outside",
                tickfont=dict(family="Arial", size=12, color="black"),
            ),
            legend={
                "orientation": "h",
                "bgcolor": "#ffffff",
                "xanchor": "center",
                "x": 0.5,
                "y": -0.6,
            },
            font=dict(family="sans-serif", size=12, color="black"),
        ),
    }
def district_distribution():
    data_grouped= df.groupby('district').size().reset_index(name= "Boreholes")
    return {
        "data": [
            go.Pie(
                labels=data_grouped['district'],
                values=data_grouped["Boreholes"],
                hoverinfo="label+value+percent",
                textinfo="percent",
                texttemplate="<b>%{percent}</b>",
                textfont=dict(size=12),
                hole=0.7,
                rotation=45,
                marker=dict(
                    colors=data_grouped['district']
                ),
            )
        ],
        "layout": go.Layout(
            hovermode="closest",
            title={
                "text": f"<b>District Borehole Distribution</b>",
                "y": 0.93,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
            },
            titlefont={"color": "black", "size": 12},
            legend={"orientation": "v", "xanchor": "right", "x": 1, "y": 1},
            font=dict(family="sans-serif", size=12, color="black"),
        ),
    }
def borhole_depth_vs_aquifer_yield(pumptypes):
    hover_text = (
        '<b>District:</b> %{customdata[0]}<br>'
        '<b>Pump Type:</b> %{customdata[1]}<br>'
        '<b>Borehole Depth:</b> %{x}<br>'
        '<b>Aquifer Yield:</b> %{y}<br>'
        '<b>Functional Status:</b> %{customdata[2]}'
    )
    fig = px.scatter(df[df['pump_type'].isin(pumptypes)], x="bh_depth", y="aquifer_yield", color="pump_type", symbol="pump_type", custom_data=['district', 'pump_type', 'functional_stat'],
        labels={
            "bh_depth": "Borehole Depth (m)", 
            "aquifer_yield": "Aquifer Yield (L/s)", 
            "pump_type": "Pump Type" 
        })
    fig.update_traces(hovertemplate=hover_text)
    fig.update_layout(
        title="<b>Borehole Depth vs Aquifer Yield</b>",
        xaxis_title="<b>Borehole Depth (m)</b>",
        yaxis_title="<b>Aquifer Yield (L/s)</b>",
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font=dict(family="Arial", size=12, color="black"), 
    )
    return fig



min_year= df.year.min()
max_year= df.year.max()
year_range= df.year.unique().tolist()
pump_types= df.pump_type.unique().tolist()
app.layout = html.Div([
    html.H1(children='Borehole Spatial Data Dashboard', style={'textAlign':'center'}),
    dmc.Grid(
        children=[
            dmc.Col(html.Div([
                dcc.Graph(id= 'pumptype_distribution', figure= pumptype_distribution())
            ]), span=4),
            dmc.Col(html.Div([
                dmc.RangeSlider(
                    id="range-slider-callback",
                    min= min_year,
                    max= max_year,
                    marks=year_range,
                    value= [min_year, max_year],
                    mb=5,
                ),
                dcc.Graph(id='year_distribution', figure= year_distribution())
            ]), span=4),
            dmc.Col(html.Div([
                dmc.Button(
                    "🡠",
                    id="back-button",
                    variant="subtle",
                    style={"display": "none"},
                ),
                dcc.Graph(id='district_distribution', figure= district_distribution())
            ]), span=4),
        ],
        gutter="xl",
    ),
    dmc.Grid(
        children=[
            dmc.Col(html.Div([
                dmc.MultiSelect(
                        label="Select Pump Type",
                        id="select-pump-type",
                        value=pump_types,
                        data=pump_types,
                        style={ "marginBottom": 10},
                    ),
                dcc.Graph(id= 'borhole_depth_vs_aquifer_yield'),
        ]), span=12),
        dmc.Col(html.Div([
            dcc.Graph(id= 'heat-map'),
            dmc.Text('Pump Types Include: ', weight=500, size= 'sm'),
            dcc.Checklist(
                id='pump-types',
                options=pump_types,
                value=pump_types[:3],
                style={'display': 'flex'}
            ),
        ]), span=12, style={'marginBottom': "20px"}),
    ],
        gutter="xl",
    ),
    dmc.Title(f"Borehole Locations", order=3, align='center', style={"marginTop": '20px'}),
    dl.Map([
        dl.TileLayer(),
        *[dl.Marker(position=[row['latitude'], row['longitude']], 
                    children=[
                        dl.Popup(content=f"<b>District</b>: {row['district']} <br><b>Aquifer Yield</b>: {row['aquifer_yield']}<br><b>Pump Type</b>: {row['pump_type']}<br><b>Borehole Depth</b>: {row['bh_depth']}<br><b>Functional Status</b>: {row['functional_stat']}")
        ]) for _, row in df.iterrows()],
    ], center=[df['latitude'].mean(), df['longitude'].mean()], zoom=6, style={'height': '50vh'})
], style={"width": "90%", 'margin': '10px auto'})


#callbacks 
#heat map
@app.callback(
    Output("heat-map", "figure"), 
    Input("pump-types", "value"))
def filter_heatmap(cols):
    heatmap_data = df[df['pump_type'].isin(cols)].groupby(['district', 'pump_type']).size().reset_index(name='count')
    heatmap_matrix = heatmap_data.pivot(index='district', columns='pump_type', values='count').fillna(0)
    hovertext = [[f'<b>District: </b>{district}<br><b>Pump Type: </b>{pump_type}<br><b>Boreholes: </b>{heatmap_matrix.at[district, pump_type]}'
              for pump_type in heatmap_matrix.columns] 
             for district in heatmap_matrix.index]
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_matrix.values,
        x=heatmap_matrix.columns,
        y=heatmap_matrix.index,
        colorscale='Viridis' ,
        hoverinfo='text',
        hovertext=hovertext
    ))
    fig.update_layout(
        title='<b>Heatmap of Pump Type vs District</b>',
        xaxis_title='<b>Pump Type</b>',
        yaxis_title='<b>District</b>',
        plot_bgcolor='white'
    )
    return fig
@callback(
    Output("borhole_depth_vs_aquifer_yield", "figure"),
    Input("select-pump-type", "value"),
)
def update_pumptype(value):
    return borhole_depth_vs_aquifer_yield(value)
    
@callback(
    Output("year_distribution", "figure"), Input("range-slider-callback", "value")
)
def update_value(value):
    new_df= df[df['year'].between(value[0], value[1])]
    grouped_data= new_df.groupby('year').size().reset_index(name="Boreholes")
    return {
        "data": [
            go.Scatter(
                x=grouped_data["year"],
                y=grouped_data["Boreholes"],
                name="Pump Type Borehole distribution",
                marker=dict(
                    color='orange',
                ),
                hoverinfo='text',
                hovertext='<b>Year: </b>' + grouped_data['year'].astype(str) + '<br>' + '<b>Boreholes: </b>' + grouped_data['Boreholes'].astype(str)
            )
        ],
        "layout": go.Layout(
            barmode="stack",
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff",
            title={
                "text": "<b> Borehole Distribution Over the years</b>",
                "y": 0.93,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
            },
            titlefont={"color": "black", "size": 20},
            hovermode="x",
            xaxis=dict(
                title="<b>Year</b>",
                color="black",
                showline=True,
                showgrid=True,
                showticklabels=True,
                linecolor="black",
                linewidth=2,
                ticks="outside",
                tickfont=dict(family="Arial", size=12, color="black"),
            ),
            yaxis=dict(
                title="<b> Boreholes </b>",
                color="black",
                showline=True,
                showgrid=True,
                showticklabels=True,
                linecolor="black",
                linewidth=2,
                ticks="outside",
                tickfont=dict(family="Arial", size=12, color="black"),
            ),
            legend={
                "orientation": "h",
                "bgcolor": "#ffffff",
                "xanchor": "center",
                "x": 0.5,
                "y": -0.6,
            },
            font=dict(family="sans-serif", size=12, color="black"),
        ),
    }

#drill through staff 
@callback(
    Output("district_distribution", "figure"),
    Output("back-button", "style"),
    [
        Input("district_distribution", "clickData"),
        Input("back-button", "n_clicks"),
    ],
)
def district_distribution_drilldown(click_data, n_clicks,):
    ctx = callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if trigger_id == "district_distribution":
        if click_data is not None:
            district = click_data["points"][0]["label"].split("(")[0]
            if district in df["district"].unique().tolist():
                grouped_data = (
                    df[df["district"] == district]
                    .groupby(by="pump_type").size()
                    .reset_index(name="Boreholes")
                )
                return {
                    "data": [
                        go.Bar(
                            x=grouped_data["pump_type"],
                            y=grouped_data["Boreholes"],
                            name="Pump Type Borehole distribution",
                            marker=dict(
                                color='orange',
                            ),
                        )
                    ],
                    "layout": go.Layout(
                        barmode="stack",
                        plot_bgcolor="#ffffff",
                        paper_bgcolor="#ffffff",
                        title={
                            "text": "<b>Pump Type Borehole Distribution</b>",
                            "y": 0.93,
                            "x": 0.5,
                            "xanchor": "center",
                            "yanchor": "top",
                        },
                        titlefont={"color": "black", "size": 20},
                        hovermode="x",
                        xaxis=dict(
                            title="<b>Pump Type</b>",
                            color="black",
                            showline=True,
                            showgrid=True,
                            showticklabels=True,
                            linecolor="black",
                            linewidth=2,
                            ticks="outside",
                            tickfont=dict(family="Arial", size=12, color="black"),
                        ),
                        yaxis=dict(
                            title="<b> Boreholes </b>",
                            color="black",
                            showline=True,
                            showgrid=True,
                            showticklabels=True,
                            linecolor="black",
                            linewidth=2,
                            ticks="outside",
                            tickfont=dict(family="Arial", size=12, color="black"),
                        ),
                        legend={
                            "orientation": "h",
                            "bgcolor": "#ffffff",
                            "xanchor": "center",
                            "x": 0.5,
                            "y": -0.6,
                        },
                        font=dict(family="sans-serif", size=12, color="black"),
                    ),
                }, {"display": "block"}
    else:
       return district_distribution(), {"display": "none"}

if __name__ == '__main__':
    app.run(debug=True)
