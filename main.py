from src.data_loader import load_china_map_data, load_global_sankey_data
from src.data_processor import process_for_map, process_for_sankey
from src.visualizer import TradeVisualizer

def main():
    print("=== SOYBEAN TRADE ANALYTICS PROJECT ===")
    
    # --- PHASE 1: THE MAP (China Focus) ---
    print("\n[1/4] Processing Map Data (Dataset 1)...")
    df_china = load_china_map_data("FAOSTAT_data_en_12-9-2025.csv")
    
    if not df_china.empty:
        df_map_agg = process_for_map(df_china)
        
        viz = TradeVisualizer()
        fig_map = viz.generate_map(df_map_agg)
        
        map_filename = "1_China_Soybean_Map.html"
        fig_map.write_html(map_filename)
        print(f"   >> Generated Map: {map_filename}")
    else:
        print("   !! Skipping Map (No data)")

    # --- PHASE 2: THE SANKEY (Global Focus) ---
    print("\n[2/4] Processing Sankey Data (Dataset 2)...")
    df_global = load_global_sankey_data("FAOSTAT_data_en_12-9-2025-2.csv")
    
    if not df_global.empty:
        # Create yearly dictionary for slider
        yearly_sankey_data = process_for_sankey(df_global, top_n_importers=15)
        
        viz = TradeVisualizer()
        fig_sankey = viz.generate_slider_sankey(yearly_sankey_data)
        
        sankey_filename = "2_Global_Sankey_Flow.html"
        fig_sankey.write_html(sankey_filename)
        print(f"   >> Generated Sankey: {sankey_filename}")
    else:
        print("   !! Skipping Sankey (No data)")

    print("\n=== PROJECT COMPLETE ===")
    print("Open the HTML files in your browser to view the visuals.")

if __name__ == "__main__":
    main()