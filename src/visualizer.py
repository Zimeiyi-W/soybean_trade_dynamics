import plotly.express as px
import plotly.graph_objects as go

class TradeVisualizer:
    
    @staticmethod
    def generate_map(df_map):
        """
        Generates the Animated Choropleth Map (China-centric).
        """
        if df_map.empty: return go.Figure()
        
        fig = px.choropleth(
            df_map,
            locations="Reporter Country",
            locationmode='country names',
            color="Value",
            animation_frame="Year",
            hover_name="Reporter Country",
            color_continuous_scale=px.colors.sequential.Greens,
            range_color=[0, df_map['Value'].max()],
            title="<b>The China Pull: Global Soybean Exports to China (1986-2023)</b><br>Color intensity = Volume in Tonnes"
        )
        
        fig.update_layout(
            geo=dict(showframe=False, showcoastlines=True, projection_type='natural earth'),
            margin={"r":0,"t":50,"l":0,"b":0},
            height=600
        )
        return fig

    @staticmethod
    def generate_slider_sankey(yearly_data):
        """
        Generates the Time-Slider Sankey (Global Export Flows).
        """
        if not yearly_data: return go.Figure()
        
        years = sorted(yearly_data.keys())
        initial_year = years[0]
        
        # Step 1, master node list (all years) for consistent coloring
        all_nodes = set()
        for y in years:
            all_nodes.update(yearly_data[y]['Reporter Country'].unique())
            all_nodes.update(yearly_data[y]['Partner Country'].unique())
        
        node_list = sorted(list(all_nodes))
        # Ensure 'Rest of World' is at the bottom
        if 'Rest of World' in node_list:
            node_list.remove('Rest of World')
            node_list.append('Rest of World')
            
        node_map = {name: i for i, name in enumerate(node_list)}
        
        # Colors: green for reporter, blue/grey for partner
        colors = []
        sources_set = set()
        for y in years: sources_set.update(yearly_data[y]['Reporter Country'].unique())
        
        for n in node_list:
            if n in sources_set: colors.append("#2E8B57") # SeaGreen (Exporters)
            elif n == "Rest of World": colors.append("#D3D3D3") # LightGrey
            else: colors.append("#4682B4") # SteelBlue (Importers)

        # Step 2, build frames (slider steps)
        steps = []
        # Initial trace data
        init_df = yearly_data[initial_year]
        
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15, thickness=20,
                line=dict(color="black", width=0.5),
                label=node_list,
                color=colors
            ),
            link=dict(
                source=init_df['Reporter Country'].map(node_map),
                target=init_df['Partner Country'].map(node_map),
                value=init_df['Value'],
                color='rgba(154, 205, 50, 0.4)' # Semi-transparent Green links
            )
        )])

        # Create steps for every year
        for year in years:
            df = yearly_data[year]
            link_data = dict(
                source=df['Reporter Country'].map(node_map),
                target=df['Partner Country'].map(node_map),
                value=df['Value'],
                color='rgba(154, 205, 50, 0.4)'
            )
            
            step = dict(
                method="restyle",
                args=[{"link": [link_data]}],
                label=str(year)
            )
            steps.append(step)

        fig.update_layout(
            title_text=f"<b>Global Soybean Trade Architecture ({years[0]}-{years[-1]})</b><br>Major Exporters to Top Markets",
            font_size=12,
            height=700,
            sliders=[{
                "active": 0,
                "currentvalue": {"prefix": "Year: "},
                "pad": {"t": 50},
                "steps": steps
            }]
        )
        return fig