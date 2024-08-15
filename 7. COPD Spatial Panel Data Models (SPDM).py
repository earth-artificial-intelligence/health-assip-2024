import pandas as pd
import geopandas as gpd
from linearmodels.panel import PanelOLS


# Load the GeoPackage
new_merged_gdf = gpd.read_file('/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/COPD/new_merged_gdf.gpkg', layer='new_merged_gdf')

# Convert 'Mortality' column to numeric, removing any non-numeric characters if necessary
new_merged_gdf['Mortality'] = pd.to_numeric(new_merged_gdf['Mortality'].str.extract('(\d+.\d+)')[0], errors='coerce')

# Print the first few rows of the GeoDataFrame
print(new_merged_gdf.head())


print(new_merged_gdf.columns)

panel_data = new_merged_gdf.set_index(['County Name', 'year'])

print(panel_data[['PM2.5', 'Ozone', 'Mortality']].isnull().sum())

# Assuming panel_data is a DataFrame with 'county', 'year', and other variables
panel_data = new_merged_gdf.set_index(['County Name', 'year'])
exog_vars = panel_data[['PM2.5', 'Ozone']]
endog_var = panel_data['Mortality']

print(len(exog_vars), len(endog_var))

print(panel_data[['PM2.5', 'Ozone', 'Mortality']].dtypes)

print(panel_data.head())


sdm_model = PanelOLS(endog_var, exog_vars)
results = sdm_model.fit()
print(results.summary)
