import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from esda.moran import Moran, Moran_Local
from libpysal.weights import Queen
from splot.esda import lisa_cluster

# Load the merged dataset
COPD_incidence_merged_df = pd.read_csv('/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/COPD/COPD_incidence_merged_df.csv')

# Load the shapefile into a GeoDataFrame
COPD_incidence_gdf = gpd.read_file('/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/COPD/COPD_incidence_gdf.shp')

# Rename the column 'val' to 'COPD Incidence'
COPD_incidence_gdf = COPD_incidence_gdf.rename(columns={'val': 'COPD Incidence'})


# Verify the loaded GeoDataFrame
print(COPD_incidence_gdf.head())
print(COPD_incidence_gdf.columns)
print(COPD_incidence_gdf.crs)  # Check the Coordinate Reference System

# Descriptive Statistics
summary_stats = COPD_incidence_gdf.describe()
print(summary_stats)

# Plot distribution of PM2.5 levels and Ozone levels
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
COPD_incidence_gdf['PM2.5'].hist(bins=20)
plt.title('Distribution of PM2.5 Levels')
plt.xlabel('PM2.5')
plt.ylabel('Frequency')

plt.subplot(1, 2, 2)
COPD_incidence_gdf['Ozone'].hist(bins=20)
plt.title('Distribution of Ozone Levels')
plt.xlabel('Ozone')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()


# Scatter plot of PM2.5 vs. Mortality
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.scatter(COPD_incidence_gdf['PM2.5'], COPD_incidence_gdf['COPD Incidence'], alpha=0.5, edgecolors='w', s=80)
plt.title('PM2.5 vs. COPD Incidence')
plt.xlabel('PM2.5')
plt.ylabel('COPD Incidence')


# Scatter plot of Ozone vs. Mortality
plt.subplot(1, 2, 2)
plt.scatter(COPD_incidence_gdf['Ozone'], COPD_incidence_gdf['COPD Incidence'], alpha=0.5, edgecolors='w', s=80)
plt.title('Ozone vs. COPD Incidence')
plt.xlabel('Ozone')
plt.ylabel('COPD Incidence')

plt.tight_layout()
plt.show()


# Add an ID column to the GeoDataFrame to use it on GeoDa
COPD_incidence_gdf['ID'] = range(1, len(COPD_incidence_gdf) + 1)

print(COPD_incidence_gdf.columns)

# Define the path to the shapefile
shapefile_path = '/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/COPD/COPD_incidence_gdf.shp'

# Save the updated GeoDataFrame to the shapefile
COPD_incidence_gdf.to_file(shapefile_path)

# Verify the file is saved
print(f"Updated shapefile saved to {shapefile_path}")









