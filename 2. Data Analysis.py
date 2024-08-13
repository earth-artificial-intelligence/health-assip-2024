import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from esda.moran import Moran, Moran_Local
from libpysal.weights import Queen
from splot.esda import lisa_cluster

# Load the merged dataset
merged_df = pd.read_csv('/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/Interstitial Lung Disease/merged_df.csv')

# Load the shapefile into a GeoDataFrame
gdf = gpd.read_file('/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/Interstitial Lung Disease/merged_geodataframe.shp')

# Verify the loaded GeoDataFrame
print(gdf.head())
print(gdf.columns)
print(gdf.crs)  # Check the Coordinate Reference System

# Descriptive Statistics
summary_stats = gdf.describe()
print(summary_stats)

# Plot distribution of PM2.5 levels and Ozone levels
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
gdf['PM2.5'].hist(bins=20)
plt.title('Distribution of PM2.5 Levels')
plt.xlabel('PM2.5')
plt.ylabel('Frequency')

plt.subplot(1, 2, 2)
gdf['Ozone'].hist(bins=20)
plt.title('Distribution of Ozone Levels')
plt.xlabel('Ozone')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()

# Scatter plot of PM2.5 vs. Mortality
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.scatter(gdf['PM2.5'], gdf['Mortality'], alpha=0.5, edgecolors='w', s=80)
plt.title('PM2.5 vs. Mortality')
plt.xlabel('PM2.5')
plt.ylabel('Mortality')

# Scatter plot of Ozone vs. Mortality
plt.subplot(1, 2, 2)
plt.scatter(gdf['Ozone'], gdf['Mortality'], alpha=0.5, edgecolors='w', s=80)
plt.title('Ozone vs. Mortality')
plt.xlabel('Ozone')
plt.ylabel('Mortality')

plt.tight_layout()
plt.show()

# Display sample data for verification
print(gdf[['PM2.5', 'Mortality', 'Ozone']].head())

# Extract the main value from 'Mortality'
def extract_mortality(value):
    return value.split(' ')[0]

gdf['Mortality'] = gdf['Mortality'].apply(extract_mortality).astype(float)

# Set the CRS manually to EPSG:4326 if needed
gdf.crs = 'EPSG:4326'

# Verify the CRS
print("CRS:", gdf.crs)

# Create spatial weights matrix using Queen contiguity
weights = Queen.from_dataframe(gdf, use_index=True)

# Perform Moran's I analysis
moran = Moran(gdf['Mortality'], weights)
print(f"Moran's I: {moran.I}, p-value: {moran.p_sim}")

# Perform Local Moran's I analysis
moran_local = Moran_Local(gdf['Mortality'], weights)

# Print Local Moran's I results
print(f"Local Moran's I: {moran_local.Is}")
print(f"Local Moran's p-values: {moran_local.p_sim}")

# Plot Local Moran's I clusters
lisa_cluster(moran_local, gdf, p=0.05)
plt.show()

