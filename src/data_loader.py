import pandas as pd
import numpy as np

def load_china_map_data(filepath="FAOSTAT_data_en_12-9-2025.csv"):
    """
    Loads Dataset 1 for the Map: Trade relations between Exporters and China.
    - Reporter: All the exporting countries (e.g., Brazil, US)
    - Partner: China, as the importer
    - Element: 'Export quantity' (The dataset also includes monetory value, but we can filter it out)
    """
    print(f"Loading map data from {filepath}...")

    try:
        df = pd.read_csv(filepath)
        df_vol = df[df['Element'] == 'Export quantity'].copy()

        df_vol = df_vol.rename(columns={'Reporter Countries': 'Reporter Country',
                                        'Partner Countries': 'Partner Country'})
        df_vol['Value'] = pd.to_numeric(df_vol['Value'], errors='coerce').fillna(0)
        final_df = df_vol[['Year', 'Reporter Country', 'Partner Country', 'Value']]

        print(f"✅ Map Data Loaded: {len(final_df)} records.")
        print(f"Unique Exporters: {final_df['Reporter Country'].nunique()}")

        return final_df

    except FileNotFoundError:
        print(f"Error: File '{filepath} not found." )
        return pd.DataFrame() # Return an empty data frame
    except Exception as e:
        print(f"❌ Error processing data: {e}")
        return pd.DataFrame()
def load_global_sankey_data(filepath="FAOSTAT_data_en_12-9-2025-2.csv"):
    """
    Loads Dataset 2 for Sankey: Top Exporters to the World.
    """
    print(f"Sankey Data Loading {filepath}...")
    try:
        df = pd.read_csv(filepath)
        if 'Element' in df.columns:
            df = df[df['Element'] == 'Export quantity'].copy()

        df = df.rename(columns={
            'Reporter Countries': 'Reporter Country', 
            'Partner Countries': 'Partner Country'
        })
        
        df['Value'] = pd.to_numeric(df['Value'], errors='coerce').fillna(0)
        
        print(f"✅ Sankey Data Loaded: {len(df)} records (Global Flows).")
        return df[['Year', 'Reporter Country', 'Partner Country', 'Value']]

    except Exception as e:
        print(f"Error loading Sankey data: {e}")
        return pd.DataFrame()