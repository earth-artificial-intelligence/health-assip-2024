import os
import pandas as pd
import re

# Paths to your data
Non_Smoke_merged_df = "/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/COPD/Non Smoke/Non_Smoke_merged_df.csv"
great_pm25_combined_df = pd.read_csv('/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/Ozone and PM2.5 Data/great_combined_daily_pm25.csv', low_memory=False)
great_ozone_combined_df = pd.read_csv('/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/Ozone and PM2.5 Data/great_combined_daily_ozone.csv', low_memory=False)

# Read all the csv into pandas dataframe in memory
#great_ozone_combined_df = pd.read_csv(ozone_data_path, parse_dates=['Date Local'])
Non_Smoke_merged_df = pd.read_csv(Non_Smoke_merged_df)
#great_pm25_combined_df = pd.read_csv(great_pm25_combined_df)

print(Non_Smoke_merged_df.columns)
print(Non_Smoke_merged_df['COPD_prevalence_percentage_total'].head())


# Convert 'Date Local' to datetime format
great_ozone_combined_df['Date Local'] = pd.to_datetime(great_ozone_combined_df['Date Local'], errors='coerce')

print(Non_Smoke_merged_df.columns)

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
import pandas as pd

def split_COPD_prevalence_percentage_total_column_into_three(COPD_prevalence_percentage_total):
    if pd.isna(COPD_prevalence_percentage_total):
        return pd.Series([None, None, None], index=['Average', 'Min', 'Max'])
    
    COPD_prevalence_percentage_total = str(COPD_prevalence_percentage_total)
    
    # Check for range format
    match = re.match(r'(\d+\.\d+) \((\d+\.\d+), (\d+\.\d+)\)', COPD_prevalence_percentage_total)
    if match:
        avg, min_val, max_val = match.groups()
        return pd.Series([float(avg), float(min_val), float(max_val)], index=['Average', 'Min', 'Max'])
    
    # Handle single value format
    try:
        avg = float(COPD_prevalence_percentage_total)
        return pd.Series([avg, avg, avg], index=['Average', 'Min', 'Max'])
    except ValueError:
        return pd.Series([None, None, None], index=['Average', 'Min', 'Max'])
# Apply the function to the DataFrame
Non_Smoke_merged_df[['Average', 'Min', 'Max']] = Non_Smoke_merged_df['COPD_prevalence_percentage_total'].apply(split_COPD_prevalence_percentage_total_column_into_three)



# Ensure 'COPD Incidence' is a string and handle NaN values
Non_Smoke_merged_df['COPD_prevalence_percentage_total'] = Non_Smoke_merged_df['COPD_prevalence_percentage_total'].astype(str)

# Apply the function to the DataFrame
Non_Smoke_merged_df[['Average', 'Min', 'Max']] = Non_Smoke_merged_df['COPD_prevalence_percentage_total'].apply(split_COPD_prevalence_percentage_total_column_into_three)

# Drop the original 'Mortality' column if no longer needed
#COPD_incidence_df = COPD_incidence_df.drop(columns=['COPD In'])

print("COPD_prevalence_percentage_total DataFrame columns:", Non_Smoke_merged_df.columns)

# Convert the daily ozone into yearly data
great_ozone_combined_df['year'] = great_ozone_combined_df['Date Local'].dt.year

# Group by additional columns and 'year'
grouped = great_ozone_combined_df.groupby(['State Name', 'year'])['Arithmetic Mean']

# Compute statistics
stats_df = grouped.agg(['max', 'min', 'mean', 'median', 'std']).reset_index()

# Rename columns for clarity
#stats_df.columns = ['State Name', 'County Name', 'year', 'Max', 'Min', 'Mean', 'Median', 'Std']

# Convert columns to string in both DataFrames
#stats_df['county'] = stats_df['County Name'].str.lower()
stats_df['state'] = stats_df['State Name'].str.lower()
stats_df['year'] = stats_df['year'].astype(int)

#COPD_incidence_df['county'] = COPD_incidence_df['County Name'].str.strip().str.lower()
Non_Smoke_merged_df['year'] = Non_Smoke_merged_df['year'].astype(int)

# Check unique values in each DataFrame for the merge columns
print("Unique State Names in Non_Smoke_merged_df:")
print(Non_Smoke_merged_df['State Name'].unique())

print("Unique State Names in stats_df:")
print(stats_df['State Name'].unique())

print("Unique Years in Non_Smoke_merged_df:")
print(Non_Smoke_merged_df['year'].unique())

print("Unique Years in stats_df:")
print(stats_df['year'].unique())


# Print the results
print("Ozone aggregated yearly data:", stats_df)
print("COPD Incidence data header:", Non_Smoke_merged_df.head())

# Merge the statistics ozone DataFrame with the COPD_long DataFrame
totalCOPD_ozone_merged_df = pd.merge(Non_Smoke_merged_df, stats_df, on=['State Name', 'year'], how='inner')

print("Merged DataFrame:", totalCOPD_ozone_merged_df.head())

# Save to a CSV file
totalCOPD_ozone_merged_df.to_csv(f'/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/COPD/Non Smoke/totalCOPD_ozone_merged_df.csv', index=False)


print(totalCOPD_ozone_merged_df)
print(totalCOPD_ozone_merged_df.columns)




