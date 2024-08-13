import numpy as np
import pandas as pd
import geopandas as gpd
from mgwr.gwr import GWR
from mgwr.sel_bw import Sel_BW
import os
import libpysal as lp

import geopandas as gpd

import geopandas as gpd
# Load the shapefiles
gdf_updated = gpd.read_file('/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/updated_geodataframe/updated_geodataframe.shp')
gdf_merged = gpd.read_file('/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/merged_gdf/merged_gdf.shp')

import pandas as pd

# Load your GeoDataFrame or DataFrame
# gdf = gpd.read_file('your_shapefile.shp')  # Example for GeoDataFrame
gdf_merged['Mortality'] = gdf_merged['Mortality'].astype(str)

# Extract the main value (before the parentheses)
gdf_merged['Mortality'] = gdf_merged['Mortality'].str.extract(r'([0-9.]+)')

# Convert the extracted value to float
gdf_merged['Mortality'] = gdf_merged['Mortality'].astype(float)

# Add an ID column with sequential integers
gdf_merged['ID'] = range(1, len(gdf_merged) + 1)


# Display the DataFrame to check the result
print(gdf_merged[['Mortality']].head())


print("Updated GeoDataFrame columns:")
print(gdf_updated.columns)

print("Merged GeoDataFrame columns:")
print(gdf_merged.columns)

# Rename a column
gdf_updated = gdf_updated.rename(columns={'County Nam': 'County Name'})
gdf_merged = gdf_merged.rename(columns={'County Nam': 'County Name'})

# Merge on key columns to identify unique rows
key_columns = ['County Name', 'FIPS', 'year']  # Adjust according to your data

# Ensure both GeoDataFrames have the same columns for comparison
unique_in_updated = gdf_updated.merge(gdf_merged, on=key_columns, how='left', indicator=True).query('_merge == "left_only"')
print("Rows in updated_geodataframe but not in merged_gdf:")
print(unique_in_updated)


# Load the shapefile into a GeoDataFrame
gdf = gpd.read_file('/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/merged_geodataframe/merged_geodataframe.shp')
print(gdf.head())

# Rename the columns to fix any typos and remove unwanted suffixes
gdf = gdf.rename(columns={'County Nam': 'County Name', '% Change i': '% Change in Mortality Rate, 1980-2014', 'geometry_x': 'geometry'})
print(gdf.head())

coords = list(zip(gdf.geometry.centroid.x, gdf.geometry.centroid.y))
y = gdf[['Mortality']].values
X = gdf[['PM2.5', 'Ozone']].values

# Create the spatial weights matrix
w = lp.weights.Queen.from_dataframe(gdf)
w.transform = 'r'

# Initialize the bandwidth selection object
sel_bw = Sel_BW(coords, y, X)

try:
    bw = sel_bw.search()
    print("Bandwidth selection successful. Bandwidth:", bw)
    
    # Proceed with GWR model fitting
    gwr_model = GWR(coords, y, X, bw).fit()
    print(gwr_model.summary())
except Exception as e:
    print("Error in bandwidth selection:", e)
    # Handle or log the exception as needed






# Assuming gdf is your GeoDataFrame with cleaned data
gdf_merged.to_file('/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/merged_gdf/merged_gdf.shp', driver='ESRI Shapefile')


