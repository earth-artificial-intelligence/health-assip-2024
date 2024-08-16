import os
import pandas as pd
import re

# Paths to your data
ozone_data_path = "/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/Ozone and PM2.5 Data/combined_ozone_data.csv"
COPD_incidence_data_path = "/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/COPD/IHME_2000-2021_COPD_Incidence_DATA.csv"
pm25_data_path = "/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/Ozone and PM2.5 Data/combined_pm25_data.csv"

# Read all the csv into pandas dataframe in memory
ozone_df = pd.read_csv(ozone_data_path, parse_dates=['Date Local'])
COPD_incidence_df = pd.read_csv(COPD_incidence_data_path)
pm25_df = pd.read_csv(pm25_data_path)

print(COPD_incidence_df.columns)

# Convert 'Date Local' to datetime format
pm25_df['Date Local'] = pd.to_datetime(pm25_df['Date Local'], errors='coerce')

# Rename columns to be consistent
#COPD_incidence_df.rename(columns={'Location': 'County Name'}, inplace=True)

# Use the melt function to transform the DataFrame from wide to long format. This will convert the year-specific columns into rows.
#COPD_incidence_long = COPD_incidence_df.melt(
    #id_vars=['County Name', 'FIPS', '% Change in Mortality Rate, 1980-2014'],
    #var_name='year',
    #value_name='Mortality'
#)

# Extract the year from the 'year' column using string operations and convert it to an integer.
#ILD_long['year'] = ILD_long['year'].str.extract(r'(\d{4})').astype(int)

# Function to split the Mortality Rate column
def split_COPD_Incidence_column_into_three(COPD_Incidence):
    match = re.match(r'(\d+\.\d+) \((\d+\.\d+), (\d+\.\d+)\)', COPD_Incidence)
    if match:
        avg, min_val, max_val = match.groups()
        return pd.Series([float(avg), float(min_val), float(max_val)], index=['COPD_average', 'COPD_min', 'COPD_max'])
    else:
        return pd.Series([None, None, None], index=['COPD_average', 'COPD_min', 'COPD_max'])

# Ensure 'COPD Incidence' is a string and handle NaN values
COPD_incidence_df['COPD Incidence'] = COPD_incidence_df['COPD Incidence'].astype(str)


# Apply the function to split the 'Mortality' column
COPD_incidence_df[['COPD_average', 'COPD_min', 'COPD_max']] = COPD_incidence_df['COPD Incidence'].apply(split_COPD_Incidence_column_into_three)

# Drop the original 'Mortality' column if no longer needed
#COPD_incidence_df = COPD_incidence_df.drop(columns=['COPD In'])

print("COPD_Incidence DataFrame columns:", COPD_incidence_df.columns)

# Convert the daily ozone into yearly data
pm25_df['year'] = pm25_df['Date Local'].dt.year

# Group by additional columns and 'year'
grouped = pm25_df.groupby(['State Name', 'County Name', 'year'])['Arithmetic Mean']

# Compute statistics
stats_df = grouped.agg(['max', 'min', 'mean', 'median', 'std']).reset_index()

# Rename columns for clarity
stats_df.columns = ['State Name', 'County Name', 'year', 'Max', 'Min', 'Mean', 'Median', 'Std']

# Convert columns to string in both DataFrames
stats_df['county'] = stats_df['County Name'].str.lower()
stats_df['state'] = stats_df['State Name'].str.lower()
stats_df['year'] = stats_df['year'].astype(int)

#COPD_incidence_df['county'] = COPD_incidence_df['County Name'].str.strip().str.lower()
COPD_incidence_df['year'] = COPD_incidence_df['year'].astype(int)

# Print the results
print("Ozone aggregated yearly data:", stats_df)
print("COPD Incidence data header:", COPD_incidence_df.head())

# Merge the statistics ozone DataFrame with the COPD_long DataFrame
COPD_Incid_merged_pm25_df = pd.merge(COPD_incidence_df, stats_df, on=['State Name', 'year'], how='inner')

print("Merged DataFrame:", COPD_Incid_merged_pm25_df.head())

# Save to a CSV file
COPD_Incid_merged_pm25_df.to_csv(f'/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/COPD/COPD_Incid_pm25_merged_df.csv', index=False)







