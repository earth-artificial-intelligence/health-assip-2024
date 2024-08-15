# Write your first Python code in Geoweaver
import pandas as pd
import geopandas as gpd

# Read CDC lung disease data
COPD_df = pd.read_csv('/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/COPD/COPD_data.csv')

# Read EPA air quality data for PM2.5 and ozone
pm25_df = pd.read_csv('/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/combined_pm25_data.csv', low_memory=False)
ozone_df = pd.read_csv('/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/combined_ozone_data.csv', low_memory=False)

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

# Ensure 'County Name' and 'year' exist
print(pm25_df[['County Name', 'year']].head())
print(ozone_df[['County Name', 'year']].head())

# Group by county and year to calculate annual averages
pm25_annual = pm25_df.groupby(['County Name', 'year'])['PM2.5'].mean().reset_index()
ozone_annual = ozone_df.groupby(['County Name', 'year'])['Ozone'].mean().reset_index()

# Get latitude and longitude for each county-year pair
lat_lon_pm25 = pm25_df.groupby(['County Name', 'year']).agg({
    'Latitude': 'first',
    'Longitude': 'first'
}).reset_index()

lat_lon_ozone = ozone_df.groupby(['County Name', 'year']).agg({
    'Latitude': 'first',
    'Longitude': 'first'
}).reset_index()

# Merge latitude and longitude with PM2.5 and Ozone averages
pm25_annual = pd.merge(pm25_annual, lat_lon_pm25, on=['County Name', 'year'])
ozone_annual = pd.merge(ozone_annual, lat_lon_ozone, on=['County Name', 'year'])
# this worked but merging had error described below

# Problems to fix: the lung disease dataframe columns are unnamed, the PM and ozone dataframe columns have 'County Name' while the lung disease doesn't

# The header of the Lung disease data is 'Interstitial lung...' not the column name so...
# Reload the lung disease dataframe with the correct header
COPD_df = pd.read_csv('/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/COPD/COPD_data.csv', header=1)


# Problem: lung disease data does not have 'County Name'
# Rename columns to be consistent
COPD_df.rename(columns={'Location': 'County Name'}, inplace=True)

# Verify the columns, all should have 'County Name' and 'year'
print("PM2.5 DataFrame columns after renaming:")
print(pm25_df.columns)
print("Ozone DataFrame columns after renaming:")
print(ozone_df.columns)
print("COPD DataFrame columns after renaming:")
print(COPD_df.columns)

# problem is 'year'
# extract the year from the columns, "'Mortality Rate, 1980*', 'Mortality Rate, 1985*'"
# Melt the DataFrame

# Use the melt function to transform the DataFrame from wide to long format. This will convert the year-specific columns into rows.
COPD_long = COPD_df.melt(
    id_vars=['County Name', 'FIPS', '% Change in Mortality Rate, 1980-2014'],
    var_name='year',
    value_name='Mortality Rate'
)

# Extract the Year
# Extract the year from the 'Year' column using string operations and convert it to an integer.
COPD_long['year'] = COPD_long['year'].str.extract(r'(\d{4})').astype(int)
# r'(\d{4})' is a regex pattern that matches and captures a four-digit year.

# test again and see what it looks like now, make sure to print the long version (changed version)
print(COPD_long)

# Ensure that the year column exists in all DataFrames used in the merge operation. 
print("Lung Disease DataFrame columns:")
print(COPD_long.columns)

print("PM2.5 Annual DataFrame columns:")
print(pm25_annual.columns)

print("Ozone Annual DataFrame columns:")
print(ozone_annual.columns)

# Convert year columns to integer type
COPD_long['year'] = COPD_long['year'].astype(int)
pm25_annual['year'] = pm25_annual['year'].astype(int)
ozone_annual['year'] = ozone_annual['year'].astype(int)

# Tried merging but the merged_df file contained no data
# Problem: Lung disease data doesn't have latitude and longitutde like PM2.5 and ozone data
# County Names are different

# Check unique values in the County Name and year columns
print(COPD_long[['County Name', 'year']].drop_duplicates().head())
print(pm25_annual[['County Name', 'year']].drop_duplicates().head())
print(ozone_annual[['County Name', 'year']].drop_duplicates().head())

# Define a function to standardize county names
def clean_county_name(name):
    return name.strip().lower()

# Apply the function to each DataFrame
COPD_long['County Name'] = COPD_long['County Name'].apply(clean_county_name)
pm25_annual['County Name'] = pm25_annual['County Name'].apply(clean_county_name)
ozone_annual['County Name'] = ozone_annual['County Name'].apply(clean_county_name)


# Remove 'county' from the County Name in the lung disease dataset
COPD_long['County Name'] = COPD_long['County Name'].str.replace(' county', '', case=False)

# Assuming the state and county columns are named 'State' and 'County Name'
# Adjust column names if they are different in your datasets

# Remove any extra spaces and clean up
pm25_annual['County Name'] = pm25_annual['County Name'].str.strip()
ozone_annual['County Name'] = ozone_annual['County Name'].str.strip()

# Verify the new format
print(pm25_annual[['County Name', 'year']].drop_duplicates().sort_values(['County Name', 'year']))
print(ozone_annual[['County Name', 'year']].drop_duplicates().sort_values(['County Name', 'year']))


print(pm25_annual.head)
print(ozone_annual.head)

# Convert county names to lowercase to standardize
pm25_annual['County Name'] = pm25_annual['County Name'].str.lower()
ozone_annual['County Name'] = ozone_annual['County Name'].str.lower()
COPD_long['County Name'] = COPD_long['County Name'].str.lower()

# Find common counties
common_counties = set(pm25_annual['County Name']).intersection(set(ozone_annual['County Name']))

# Filter DataFrames by common counties
pm25_common = pm25_annual[pm25_annual['County Name'].isin(common_counties)]
ozone_common = ozone_annual[ozone_annual['County Name'].isin(common_counties)]
COPD_common = COPD_long[COPD_long['County Name'].isin(common_counties)]

# Print results
print("PM2.5 DataFrame with common counties:\n", pm25_common)
print("Ozone DataFrame with common counties:\n", ozone_common)
print("Lung Disease DataFrame with common counties:\n", ozone_common)
print(f"Number of common counties: {len(common_counties)}")

# Fixed county problem
# Now I need to find common years

# Find common years across the datasets
common_years = set(pm25_common['year']).intersection(set(ozone_common['year'])).intersection(set(COPD_common['year']))

# Filter DataFrames by common years
pm25_common = pm25_common[pm25_common['year'].isin(common_years)]
ozone_common = ozone_common[ozone_common['year'].isin(common_years)]
COPD_common = COPD_common[COPD_common['year'].isin(common_years)]

# Verify the common counties and years
print(f"Number of common counties: {len(common_counties)}")
print(f"Number of common years: {len(common_years)}")

# Check unique years in each DataFrame
print("Unique years in PM2.5 data:", pm25_common['year'].unique())
print("Unique years in Ozone data:", ozone_common['year'].unique())
print("Unique years in Lung Disease data:", COPD_common['year'].unique())

print("Number of rows in PM2.5 data before filtering:", len(pm25_annual))
print("Number of rows in Ozone data before filtering:", len(ozone_annual))
print("Number of rows in Lung Disease data before filtering:", len(COPD_long))

# Find common counties again and print them
common_counties = set(pm25_annual['County Name']).intersection(set(ozone_annual['County Name']))
print(f"Number of common counties: {len(common_counties)}")
print(f"Common counties: {common_counties}")

# Filter DataFrames by common counties and print their lengths
pm25_common = pm25_annual[pm25_annual['County Name'].isin(common_counties)]
ozone_common = ozone_annual[ozone_annual['County Name'].isin(common_counties)]
COPD_common = COPD_long[COPD_long['County Name'].isin(common_counties)]

print("Number of rows in PM2.5 data after filtering:", len(pm25_common))
print("Number of rows in Ozone data after filtering:", len(ozone_common))
print("Number of rows in Lung Disease data after filtering:", len(COPD_common))

print("Unique years in PM2.5 data before filtering:", pm25_annual['year'].unique())
print("Unique years in Ozone data before filtering:", ozone_annual['year'].unique())
print("Unique years in Lung Disease data before filtering:", COPD_long['year'].unique())

# Now county name and year columns should be fixed
# Merge lung disease data with PM2.5 and ozone data
new_merged_df = pd.merge(COPD_long, pm25_annual, on=['County Name', 'year'])
new_merged_df = pd.merge(new_merged_df, ozone_annual, on=['County Name', 'year'])

print(new_merged_df.head)

new_merged_df.to_csv('/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/new_merged_df.csv', index=False)


# Find rows where Latitude_x and Latitude_y differ
discrepancies = new_merged_df[new_merged_df['Latitude_x'] != new_merged_df['Latitude_y']]

# Display the rows with discrepancies
print(discrepancies[['County Name', 'year', 'Latitude_x', 'Latitude_y']])

# Drop the incorrect columns and rename the correct ones
new_merged_df = new_merged_df.drop(columns=['Latitude_y', 'Longitude_y'])
new_merged_df = new_merged_df.rename(columns={'Latitude_x': 'Latitude', 'Longitude_x': 'Longitude'})

# Recreate the Geometry Column - Once you have cleaned up the latitude and longitude columns:
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Create the geometry column using the cleaned latitude and longitude columns
new_merged_df['geometry'] = new_merged_df.apply(lambda row: Point(row['Longitude'], row['Latitude']), axis=1)

# Convert to GeoDataFrame
gdf1 = gpd.GeoDataFrame(new_merged_df, geometry='geometry')

# Optionally, set the coordinate reference system (CRS) if you know it
# Example: gdf.set_crs(epsg=4326, inplace=True) # WGS84 CRS

# Save the GeoDataFrame to a shapefile or other format if needed
gdf1.to_file('/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/new_merged_geodataframe.shp')

# Save the updated DataFrame to CSV
new_merged_df.to_csv('/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/new_merged_df.csv', index=False)



