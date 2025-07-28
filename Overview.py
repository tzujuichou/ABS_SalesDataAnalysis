import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
import pandas as pd
from utils import (query, load)

st.title('Overview')
t1, t2, t3, t4 = st.tabs(['Abstract', 'Context', 'Data', 'Source'])


with t1:
        st.header("Project Abstract")

with t2:
        st.header("Business Context")
        st.subheader("Backgound")
        st.write("""
        Lets start with some context about Montgomery County and its alcohol control.
        Montgomery County is located roughly northeast of Washington DC. Its a control jurisdiction, meaning the local government 
        manages the sale and/or distribution of alcohol, rather than relying entirely on private businesses.
        """)

        # --- Folium Map ---
        geojson_url = "assets/Montgomery County Boundary.geojson"

        try:
            gdf = gpd.read_file(geojson_url)
            m = folium.Map(location=[39.15, -77.20], zoom_start=9)
            folium.GeoJson(
                gdf,
                style_function=lambda feature: {
                    'fillColor': '#0044ff',
                    'color': 'white',
                    'weight': 2,
                    'fillOpacity': 0.2
                }
            ).add_to(m)

            st_folium(m, width=725, height=500)

        except Exception as e:
            st.error(f"Could not load map data. The data source may be temporarily unavailable. Error: {e}")
        st.write("""
        The agency that is responsible for controlling all the alcohol beverages, is the Department of Liquor Control (DLC), which later rebranded into
        Montgomery County Alcohol Beverage Services (ABS).
        """)

        st.subheader("Distribution")
        st.write("ABS operates by having one giant central warehouse act as the main distributor to its 25 retail stores and other 1000-ish privately owned local licensed business")
        st.write("Source: https://www.nabca.org/sites/default/files/assets/files/MontgomeryCo_MD.pdf")





with t3:
        st.header("About the dataset")
        st.write("""
        This dataset is acquired from data.gov. The original dataset contains 9 columns, with 308K rows:
        """)

        column_data = {
        "Column Name": [
            "YEAR",
            "MONTH",
            "SUPPLIER",
            "ITEM CODE",
            "ITEM DESCRIPTION",
            "ITEM TYPE",
            "RETAIL SALES",
            "RETAIL TRANSFERS",
            "WAREHOUSE SALES"
        ],
        "Description": [
            "Calendar Year",
            "Month",
            "Supplier Name",
            "Item code",
            "Item Description",
            "Item Type",
            "Cases of product sold from DLC(ABS) dispensaries",
            "Cases of product transferred to DLC(ABS) dispensaries",
            "Cases of product sold to MC licensees"
        ]}
        df_columns = pd.DataFrame(column_data)
        st.dataframe(df_columns, hide_index=True)

        st.subheader("Methodology: From Raw Data to Dashboard")
        st.write("""
        To make this data easier to work with for analysis and to power this dashboard efficiently,
        I transformed the original flat Excel-like sheet into a more structured database format.
        """)
        with st.expander("Here's how I set it up"):
            st.markdown("""
            * **Normalization & Database Design:** The raw data was normalized and organized into a **star schema** design.
                This means separating out related information into distinct tables.
                You can see a visual representation of this process:
            """)

            # Assuming 'image_3de2bf.png' is in your app's main directory
            st.image("assets/ERD.png", caption="Database Schema Design: From Flat File to Star Schema")

            st.markdown("""
            * **Data Storage:** The transformed data is stored in **Supabase**, a cloud-based platform that makes it easy to manage and access.

            * **Schema Details & Design Choices:**
                * **`fact_transaction` (The "Fact" Table):** holding the actual sales and transfer numbers (`retail_sales`, `retail_transfers`, `warehouse_sales`) and linking to other tables. Each row here represents a specific transaction of an item from a supplier on a certain date.
                * **`dim_date` (The "Date" Dimension):** I pulled out the `YEAR` and `MONTH` data into a dedicated date table. I also generated `month_name` (e.g., "January", "February") and `quarter` (e.g., Q1, Q2) here, which can be helpful for potential time series analysis.
                * **`dim_item` (The "Item" Dimension):** All the item-specific details like `item_code`, `item_description`, and `item_type` were moved into this table. This avoids repeating item info for every single transaction.
                * **`dim_supplier` (The "Supplier" Dimension):** Similarly, `supplier` names were moved to their own table to keep things clean and efficient.

            """)

        st.subheader("Scope of the Analysis")

        df = load('data/time_scope.parquet')
        st.write("""
        It's important to understand the specific time periods covered by this dashboard, and thus the limitations.
        While the raw dataset spans from mid-2017 to late 2020, it **does not contain every month for every year:**
        """)

        st.dataframe(df, hide_index=True)
        st.write("""
        As we can see:
        - 2017 contains data from June to December
        - 2018 contains data from January and February only
        - 2019 contains data from January to November
        - 2020 contains data from January, March, July, and September
        """)

        st.write("""
        Therefore, the scope of this analysis is determined to be focusing on year 2019 because it is the only year with the most complete data record across time (Jan. to Nov.)
        for better validity and integrity.
        """)


with t4:
        st.header("Source and Licensing")
        st.write("""
            This dashboard utilizes a publicly available dataset provided by Montgomery County, Maryland.
        """)

        st.subheader("Original Data Source")
        st.markdown("""
        **Dataset Title:** Warehouse and Retail Sales  
        **Publisher:** Montgomery County, MD - Department of Alcohol Beverage Services (ABS)  
        **Last Updated on Source:** July 5, 2025 (as indicated on the data portal)  
        **URL:** [https://data.montgomerycountymd.gov/Community-Recreation/Warehouse-and-Retail-Sales/v76h-r7br/about_data](https://data.montgomerycountymd.gov/Community-Recreation/Warehouse-and-Retail-Sales/v76h-r7br/about_data)
        """)

        st.subheader("Data Licensing")
        st.markdown("""
        **Dataset Catalog (Data.gov):**  
        [https://catalog.data.gov/dataset/warehouse-and-retail-sales](https://catalog.data.gov/dataset/warehouse-and-retail-sales)

        **Official Dataset Landing Page (Montgomery County Open Data Portal):**  
        [https://data.montgomerycountymd.gov/Community-Recreation/Warehouse-and-Retail-Sales/v76h-r7br/about_data](https://data.montgomerycountymd.gov/Community-Recreation/Warehouse-and-Retail-Sales/v76h-r7br/about_data)

        **License:**  
        This dataset is provided under a **Public Domain** license by Montgomery County, MD, permitting free use, sharing, and adaptation.
        """)

        st.subheader("Citation")
        st.code("""
        Montgomery County, MD - Department of Alcohol Beverage Services. (2025).
        Warehouse and Retail Sales [Data set].
        Data.MontgomeryCountyMD.gov.
        Retrieved from https://data.montgomerycountymd.gov/Community-Recreation/Warehouse-and-Retail-Sales/v76h-r7br/about_data
        """, language='text')


        st.subheader("Project Repository")
        st.write("You can find the code and additional project details for this Streamlit application on GitHub:")
        st.markdown("[Link to your GitHub Repository](YOUR_GITHUB_REPO_URL_HERE)")

