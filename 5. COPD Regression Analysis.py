import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Point
import libpysal as lp
from spreg import ML_Lag, ML_Error
from libpysal.weights import Queen
import os


# Load the shapefile into a GeoDataFrame
gdf1 = gpd.read_file('/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/new_merged_geodataframe.shp')

# Load the merged dataset
new_merged_df = pd.read_csv('/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/new_merged_df.csv')

# Load the county shapefile
shapefile_path = '/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/County data/county_shapefile.shp'
county_gdf = gpd.read_file(shapefile_path)

# Load the fixed_geodataframe1
fixed_geodataframe1 = gpd.read_file('/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/COPD/fixed_geodataframe1.shp')

print(new_merged_df)
print(fixed_geodataframe1)

# Check the geometry type of merged_geodataframe
print("Geometry type of gdf:")
print(gdf1.geometry.geom_type.unique())

# Check the geometry type of fixed_geodataframe1
print("Geometry type of fixed_geodataframe1:")
print(fixed_geodataframe1.geometry.geom_type.unique())

# Check common columns
common_columns = set(gdf1.columns) & set(fixed_geodataframe1.columns)
print("Common Columns:")
print(common_columns)

# Merge the GeoDataFrames on common columns to see differences
comparison_df = gdf1.merge(fixed_geodataframe1, on=list(common_columns), how='outer', indicator=True)
print(comparison_df.head())

# Check if there are any differences
differences = comparison_df[comparison_df['_merge'] != 'both']
print("Differences between the two GeoDataFrames:")
print(differences)

# Perform the merge operation and assign the result to gdf
gdf1 = gdf1.merge(fixed_geodataframe1, on=list(common_columns), how='outer', indicator=True)


# Optionally, you can drop the '_merge' column if it's no longer needed
gdf1 = gdf1.drop(columns=['_merge'])

# Now gdf contains the merged data


# Convert 'FIPS' in gdf to string
gdf1['FIPS'] = gdf1['FIPS'].astype(str)

# Convert 'COUNTYFP' in county_gdf to string
county_gdf['COUNTYFP'] = county_gdf['COUNTYFP'].astype(str)

print(gdf1['FIPS'].dtype)
print(county_gdf['COUNTYFP'].dtype)

# Perform the merge
new_merged_gdf = gdf1.merge(county_gdf, left_on='FIPS', right_on='COUNTYFP', how='left')

print(new_merged_gdf.head())
print(new_merged_gdf.columns)

# Merge was successful, now cleaning columns
# Rename the columns to fix any typos and remove unwanted suffixes
new_merged_gdf = new_merged_gdf.rename(columns={'County Nam': 'County Name', '% Change i': '% Change in Mortality Rate, 1980-2014', 'geometry_x': 'geometry'})

# Drop unnecessary columns (if any)
columns_to_drop = ['STATEFP', 'COUNTYFP', 'COUNTYNS', 'AFFGEOID', 'GEOID', 'NAME_y', 'LSAD', 'NAME', 'geometry_y', 'ALAND', 'AWATER']
new_merged_gdf = new_merged_gdf.drop(columns=columns_to_drop, errors='ignore')

# Convert 'Mortality' to numeric
gdf1['Mortality'] = gdf1['Mortality'].str.extract(r'(\d+\.\d+)').astype(float)

# Handle NaNs
gdf1['Mortality'] = gdf1['Mortality'].fillna(gdf1['Mortality'].mean())

# Check the result
print(gdf1.head())

# Ensure that the columns of interest are present and correctly named
print(new_merged_gdf.head())
print(new_merged_gdf.columns)

# Check the data types of your DataFrame columns
print(gdf1[['Mortality', 'PM2.5', 'Ozone']].dtypes)

# Convert to numeric, if necessary
gdf1['Mortality'] = pd.to_numeric(gdf1['Mortality'], errors='coerce')
gdf1['PM2.5'] = pd.to_numeric(gdf1['PM2.5'], errors='coerce')
gdf1['Ozone'] = pd.to_numeric(gdf1['Ozone'], errors='coerce')

# Calculate the mean of each column
means = gdf1[['Mortality', 'PM2.5', 'Ozone']].mean()

# Replace NaN values with the column mean
gdf1[['Mortality', 'PM2.5', 'Ozone']] = gdf1[['Mortality', 'PM2.5', 'Ozone']].fillna(means)

# Optionally, ensure no infinite values are present
gdf1 = gdf1[~gdf1[['Mortality', 'PM2.5', 'Ozone']].isin([np.inf, -np.inf]).any(axis=1)]

# Convert 'Mortality' to numeric, coerce errors to NaN
gdf1['Mortality'] = pd.to_numeric(gdf1['Mortality'], errors='coerce')

# Recalculate means and replace NaNs with the column mean
means = gdf1[['Mortality', 'PM2.5', 'Ozone']].mean()
print(means)
gdf1[['Mortality', 'PM2.5', 'Ozone']] = gdf1[['Mortality', 'PM2.5', 'Ozone']].fillna(means)

# Check the data types of your DataFrame columns
print(gdf1[['Mortality', 'PM2.5', 'Ozone']].dtypes)

# Check data types
print(gdf1.dtypes)

# Ensure no infinite values are present
gdf1 = gdf1[~gdf1[['Mortality', 'PM2.5', 'Ozone']].isin([np.inf, -np.inf]).any(axis=1)]

# Confirm the cleaned data
print(gdf1.head())

# Check for NaN values in your DataFrame columns
print(gdf1[['Mortality', 'PM2.5', 'Ozone']].isna().sum())

# Confirm that there are no infinite values
print((np.isinf(gdf1[['Mortality', 'PM2.5', 'Ozone']])).sum())

# Buffer points to create polygons
buffer_distance = 1  # Adjust this distance based on your analysis
gdf1['geometry'] = gdf1['geometry'].buffer(buffer_distance)

# Verify that the geometry type is now polygons
print("Geometry type after buffering:")
print(gdf1.geometry.geom_type.unique())

# Recreate GeoDataFrame with new polygon geometries
gdf1 = gpd.GeoDataFrame(gdf1, geometry='geometry')

# Check for NaN values in your DataFrame columns
print("NaN values in columns before processing:")
print(gdf1[['Mortality', 'PM2.5', 'Ozone']].isna().sum())

# Check data types and ensure no infinite values are present
print("Checking for infinite values before processing:")
print(gdf1[~gdf1[['Mortality', 'PM2.5', 'Ozone']].isin([np.inf, -np.inf]).any(axis=1)])

# Convert 'Mortality' to numeric
gdf1['Mortality'] = pd.to_numeric(gdf1['Mortality'], errors='coerce')

# Check for NaN values and fill with column mean
means = gdf1[['Mortality', 'PM2.5', 'Ozone']].mean()
gdf1[['Mortality', 'PM2.5', 'Ozone']] = gdf1[['Mortality', 'PM2.5', 'Ozone']].fillna(means)

# Check the final data types and presence of NaN/infinite values
print("Data types of columns after processing:")
print(gdf1.dtypes)
print("Number of NaN values after processing:")
print(gdf1[['Mortality', 'PM2.5', 'Ozone']].isna().sum())
print("Number of infinite values after processing:")
print((np.isinf(gdf1[['Mortality', 'PM2.5', 'Ozone']])).sum())

# Define your dependent and independent variables
y = gdf1[['Mortality']].values.flatten()  # Flatten to 1D array
X = gdf1[['PM2.5', 'Ozone']].values

# Ensure that the input data is valid
print("Shape of y:", y.shape)
print("Shape of X:", X.shape)
print("First 5 rows of y:", y[:5])
print("First 5 rows of X:", X[:5])

# Recalculate weights matrix for polygons
try:
    w = lp.weights.Queen.from_dataframe(gdf1, use_index=False)
    w.transform = 'r'  # Row-standardize the weights
    print("Row-standardized Weights matrix:")
    print(w.full())  # For binary weights

    # Check the type of weights matrix
    print("Weights matrix:")
    print("Type of weights matrix:", type(w))
    print("Weights matrix W:")
    print(w)

    # Print the number of weights and some example values
    print("Number of weights:", len(w.weights))  # Total number of weights

    # Sample output for binary weights
    print("Sample weights (first 5 entries):")
    for key in list(w.weights.keys())[:5]:
        print(f"{key}: {w.weights[key]}")
except Exception as e:
    print("Error in creating weights matrix:", e)

# Perform the regression with explicitly set weights matrix
try:
    # Fit the ML_Lag model
    model_lag = ML_Lag(y, X, w=w)
    print("ML_Lag Model Summary:")
    print(model_lag.summary)
except Exception as e:
    print("Error in ML_Lag model:", e)

try:
    # Fit the ML_Error model
    model_error = ML_Error(y, X, w=w)
    print("ML_Error Model Summary:")
    print(model_error.summary)
except Exception as e:
    print("Error in ML_Error model:", e)

# Check the columns after renaming
print(new_merged_gdf.columns)

# Ensure the CRS is set
if new_merged_gdf.crs is None:
    new_merged_gdf.crs = 'EPSG:4326'  # or the appropriate EPSG code for your CRS

# Assuming your GeoDataFrame is named COPD_new_merged_gdf
new_merged_gdf.to_file('/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/COPD/new_merged_gdf.gpkg', layer='new_merged_gdf', driver='GPKG')

import libpysal as ps
from mgwr.sel_bw import Sel_BW
#import mgwr 
#from mgwr.sel import Sel_BW

#import mgwr 

#try:
#    from mgwr.sel import Sel_BW
 #   print("Sel_BW imported successfully!")
#except ImportError as e:
 #   print(f"ImportError: {e}")


coords = list(zip(gdf1.geometry.centroid.x, gdf1.geometry.centroid.y))
y = gdf1[['Mortality']].values
X = gdf1[['PM2.5', 'Ozone']].values

# Bandwidth selection
#sel_bw = Sel_BW(coords, y, X,w=w)
#bw = sel_bw.search()




