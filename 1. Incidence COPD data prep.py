import pandas as pd
import geopandas as gpd

# Read CDC COPD incidence data
COPD_incidence_df = pd.read_csv('/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/COPD/IHME_2000-2021_COPD_Incidence_DATA.csv')

# Read EPA air quality data for PM2.5 and ozone
pm25_df = pd.read_csv('/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/Ozone and PM2.5 Data/combined_pm25_data.csv', low_memory=False)
ozone_df = pd.read_csv('/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/Ozone and PM2.5 Data/combined_ozone_data.csv', low_memory=False)

# Read county shapefile for spatial analysis
counties_gdf = gpd.read_file('/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/County data/county_shapefile.shp')

# Convert date column to datetime
pm25_df['Date Local'] = pd.to_datetime(pm25_df['Date Local'], format='%Y-%m-%d')
ozone_df['Date Local'] = pd.to_datetime(ozone_df['Date Local'], format='%Y-%m-%d')

# Extract year from date
pm25_df['year'] = pm25_df['Date Local'].dt.year
ozone_df['year'] = ozone_df['Date Local'].dt.year

# Get year from PM2.5

# Convert 'Date Local' to datetime and extract year
pm25_df['Date Local'] = pd.to_datetime(pm25_df['Date Local'], format='%Y-%m-%d')
pm25_df['year'] = pm25_df['Date Local'].dt.year

# Rename 'Sample Measurement' to 'PM2.5'
pm25_df.rename(columns={'Arithmetic Mean': 'PM2.5'}, inplace=True)

# Verify the DataFrame
print(pm25_df.head())
print(pm25_df.columns)

# Convert 'Date Local' to datetime and extract year
ozone_df['Date Local'] = pd.to_datetime(ozone_df['Date Local'], format='%m/%d/%y')
ozone_df['year'] = ozone_df['Date Local'].dt.year

# Rename 'Sample Measurement' to 'Ozone'
ozone_df.rename(columns={'Arithmetic Mean': 'Ozone'}, inplace=True)

# Verify the DataFrame
print(ozone_df.head())
print(ozone_df.columns)

# Ensure 'State Name' and 'year' exist
print(pm25_df[['State Name', 'year']].head())
print(ozone_df[['State Name', 'year']].head())

# Group by state and year to calculate annual averages
pm25_annual = pm25_df.groupby(['State Name', 'year'])['PM2.5'].mean().reset_index()
ozone_annual = ozone_df.groupby(['State Name', 'year'])['Ozone'].mean().reset_index()

# Get latitude and longitude for each state-year pair
lat_lon_pm25 = pm25_df.groupby(['State Name', 'year']).agg({
    'Latitude': 'first',
    'Longitude': 'first'
}).reset_index()

lat_lon_ozone = ozone_df.groupby(['State Name', 'year']).agg({
    'Latitude': 'first',
    'Longitude': 'first'
}).reset_index()

# Merge latitude and longitude with PM2.5 and Ozone averages
pm25_annual = pd.merge(pm25_annual, lat_lon_pm25, on=['State Name', 'year'])
ozone_annual = pd.merge(ozone_annual, lat_lon_ozone, on=['State Name', 'year'])

# Verify the columns, all should have 'State Name' and 'year'
print("PM2.5 DataFrame columns:")
print(pm25_df.columns)
print("Ozone DataFrame columns:")
print(ozone_df.columns)
print("COPD incidence DataFrame columns:")
print(COPD_incidence_df.columns)

# Merge lung disease data with PM2.5 and ozone data
COPD_incidence_merged_df = pd.merge(COPD_incidence_df, pm25_annual, on=['State Name', 'year'])
COPD_incidence_merged_df = pd.merge(COPD_incidence_merged_df, ozone_annual, on=['State Name', 'year'])

# Find rows where Latitude_x and Latitude_y differ
discrepancies = COPD_incidence_merged_df[COPD_incidence_merged_df['Latitude_x'] != COPD_incidence_merged_df['Latitude_y']]

# Display the rows with discrepancies
print(discrepancies[['State Name', 'year', 'Latitude_x', 'Latitude_y']])

# Drop the incorrect columns and rename the correct ones
COPD_incidence_merged_df = COPD_incidence_merged_df.drop(columns=['Latitude_x', 'Longitude_x'])
COPD_incidence_merged_df = COPD_incidence_merged_df.rename(columns={'Latitude_y': 'Latitude', 'Longitude_y': 'Longitude'})

from shapely.geometry import Point

# Create the geometry column using the latitude and longitude columns
COPD_incidence_merged_df['geometry'] = COPD_incidence_merged_df.apply(lambda row: Point(row['Longitude'], row['Latitude']), axis=1)


# Convert merged DataFrame to GeoDataFrame for spatial analysis
COPD_incidence_gdf = gpd.GeoDataFrame(COPD_incidence_merged_df, geometry='geometry')

COPD_incidence_gdf.crs = 'EPSG:4326'  # Example CRS, adjust as needed

# Save the GeoDataFrame to a shapefile or other format if needed
COPD_incidence_gdf.to_file('/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/COPD/COPD_incidence_gdf.shp')

# Save the updated DataFrame to CSV
COPD_incidence_merged_df.to_csv('/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/COPD/COPD_incidence_merged_df.csv', index=False)




# Check for matches in State Name and year across dataframes
print(COPD_incidence_df[['State Name', 'year']].drop_duplicates())
print(pm25_annual[['State Name', 'year']].drop_duplicates())
print(ozone_annual[['State Name', 'year']].drop_duplicates())

# Check for common values between dataframes
common_states_years = pd.merge(COPD_incidence_df[['State Name', 'year']], pm25_annual[['State Name', 'year']], on=['State Name', 'year'])
print(common_states_years.head())

# Verify data types before merging
print(COPD_incidence_df.dtypes)
print(pm25_annual.dtypes)
print(ozone_annual.dtypes)

# Ensure no columns have trailing spaces or unexpected characters
COPD_incidence_df.columns = COPD_incidence_df.columns.str.strip()
pm25_annual.columns = pm25_annual.columns.str.strip()
ozone_annual.columns = ozone_annual.columns.str.strip()






# Making Random Forest Prediction Model
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Load the merged DataFrame
COPD_incidence_merged_df = pd.read_csv('/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/COPD/COPD_incidence_merged_df.csv')

print(COPD_incidence_merged_df.dtypes)

# Check for any non-numeric values or unexpected text
non_numeric_values = COPD_incidence_merged_df[~COPD_incidence_merged_df['COPD Incidence'].apply(pd.to_numeric, errors='coerce').notnull()]
print(non_numeric_values)

print(COPD_incidence_merged_df['State Name'].unique())
print(COPD_incidence_merged_df['metric_name'].unique())

COPD_incidence_merged_df['COPD Incidence'] = pd.to_numeric(COPD_incidence_merged_df['COPD Incidence'], errors='coerce')
COPD_incidence_merged_df['PM2.5'] = pd.to_numeric(COPD_incidence_merged_df['PM2.5'], errors='coerce')
COPD_incidence_merged_df['Ozone'] = pd.to_numeric(COPD_incidence_merged_df['Ozone'], errors='coerce')

# Verify if any columns were unintentionally concatenated
print(COPD_incidence_merged_df.head(10))


# Identify numeric columns
numeric_cols = COPD_incidence_merged_df.select_dtypes(include='number').columns
non_numeric_cols = COPD_incidence_merged_df.select_dtypes(exclude='number').columns


# Identify non-numeric columns
non_numeric_cols = COPD_incidence_merged_df.select_dtypes(exclude=[np.number]).columns.tolist()

# Fill NaN values in numeric columns with the mean
COPD_incidence_merged_df[numeric_cols].fillna(COPD_incidence_merged_df[numeric_cols].mean(), inplace=True)


# Check for missing values
print(COPD_incidence_merged_df.isnull().sum())

# Fill missing values if necessary
# For simplicity, you can use the mean or median of the columns with missing values
COPD_incidence_merged_df.fillna(COPD_incidence_merged_df.mean(), inplace=True)

# Extract features and target variable
# Assume 'COPD Incidence' is the target variable and the rest are features
features = COPD_incidence_merged_df[['PM2.5', 'Ozone', 'Latitude', 'Longitude']]
target = COPD_incidence_merged_df['COPD Incidence']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Initialize and fit the Random Forest model
rf_model = RandomForestRegressor(n_estimators=300, max_depth=10, min_samples_split=10, random_state=42)
rf_model.fit(X_train, y_train)

# Make predictions
y_pred = rf_model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R^2 Score: {r2}")

# Get feature importances
importances = rf_model.feature_importances_
features_importance = pd.DataFrame({
    'Feature': X_train.columns,
    'Importance': importances
}).sort_values(by='Importance', ascending=False)

print(features_importance)







