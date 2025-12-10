
def process_for_map(df):
    """
    Prepares data for the China-centric map.
    Groups by Year and Exporter to determine color intensity.
    """
    if df.empty: 
        return df
    # Sum exports per country per year
    df_agg = df.groupby(['Year', 'Reporter Country'])['Value'].sum().reset_index()
    return df_agg

def process_for_sankey(df, top_n_importers=8):
    """
    Prepares dictionary of yearly dataframes for the Slider Sankey.
    Groups small importers into 'Rest of World' to keep the chart clean.
    """
    if df.empty: 
        return {}
    
    yearly_data = {}
    unique_years = sorted(df['Year'].unique())

    # Ensure columns are strings to avoid categorical errors
    df['Partner Country'] = df['Partner Country'].astype(str)

    # Further filter the exporters bcs some only export limited amount
    df = df[df['Reporter Country'].isin(['United States of America', 'Brazil', 'Argentina', 'Uruguay', 'Ukraine', 'Canada'])]
    

    for year in unique_years:
        df_year = df[df['Year'] == year].copy()
        top_targets_year = df_year.groupby('Partner Country')['Value'].sum() \
                                  .nlargest(top_n_importers).index
        df_year['Partner Country'] = df_year['Partner Country'].mask(~df_year['Partner Country'].isin(top_targets_year), 'Rest of World')
        
        df_agg = df_year.groupby(['Reporter Country', 'Partner Country'])['Value'].sum().reset_index()
        df_agg = df_agg[df_agg['Value'] > 0]
        
        yearly_data[year] = df_agg
    
        
    return yearly_data