import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the CSV file into a DataFrame
file_path = '/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/COPD/COPD_Incid_ozone_merged_df.csv'
COPD_Incid_merged_ozone_df = pd.read_csv(file_path)

COPD_Incid_merged_ozone_df = COPD_Incid_merged_ozone_df.drop(columns=['COPD_min', 'COPD_max', 'county', 'County Name'])



# Display the first few rows of the DataFrame
print(COPD_Incid_merged_ozone_df.head())
print(COPD_Incid_merged_ozone_df.columns)

def do_breatheright_correlation_analysis():
    # Read in the merged CSV file with ozone and lung disease data
    COPD_Incid_merged_ozone_df = pd.read_csv(f"/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/COPD/COPD_Incid_ozone_merged_df.csv")
    print(COPD_Incid_merged_ozone_df.head())
    print(COPD_Incid_merged_ozone_df.columns)

# Drop the unnecessary columns
# COPD_merged_pm25_df = COPD_merged_pm25_df.drop(columns=["county_x", 'State Name', 'county_y', 'State Name_y'])

# Figuring out which columns to drop
# Values in 'county_x' but not in 'county_y'
#county_x_not_in_county_y = set(ILD_merged_pm25_df['county_x'].dropna()).difference(set(ILD_merged_pm25_df['county_y'].dropna()))
#print("Values in 'county_x' but not in 'county_y':")
#print(county_x_not_in_county_y)

# Values in 'county_y' but not in 'county_x'
#county_y_not_in_county_x = set(ILD_merged_pm25_df['county_y'].dropna()).difference(set(ILD_merged_pm25_df['county_x'].dropna()))
#print("\nValues in 'county_y' but not in 'county_x':")
#print(county_y_not_in_county_x)

# Check for null values
#print("\nNull values in 'county_x':")
#print(ILD_merged_pm25_df['county_x'].isnull().sum())

#print("\nNull values in 'county_y':")
#print(ILD_merged_pm25_df['county_y'].isnull().sum())

# Drop the 'county_x' column
#ILD_merged_pm25_df = ILD_merged_pm25_df.drop(columns=['county_x'])

# Convert state names in 'State Name' to lowercase
COPD_Incid_merged_ozone_df['State Name'] = COPD_Incid_merged_ozone_df['State Name'].str.lower()

# Convert state names in 'state' to lowercase
COPD_Incid_merged_ozone_df['state'] = COPD_Incid_merged_ozone_df['state'].str.lower()

# Get unique values in 'State Name' and 'state'
state_name_values = set(COPD_Incid_merged_ozone_df['State Name'].dropna().unique())
state_values = set(COPD_Incid_merged_ozone_df['state'].dropna().unique())

# Find differences
diff_state_name_not_in_state = state_name_values - state_values
diff_state_not_in_state_name = state_values - state_name_values

# Print the differences
print("Values in 'State Name' but not in 'state':")
print(diff_state_name_not_in_state)

print("\nValues in 'state' but not in 'State Name':")
print(diff_state_not_in_state_name)

# Check for null values
print("\nNull values in 'State Name':")
print(COPD_Incid_merged_ozone_df['State Name'].isnull().sum())

print("\nNull values in 'state':")
print(COPD_Incid_merged_ozone_df['state'].isnull().sum())

# Drop the 'state' column
COPD_Incid_merged_ozone_df = COPD_Incid_merged_ozone_df.drop(columns=['state'])

# Renaming columns for clarity
COPD_Incid_merged_ozone_df = COPD_Incid_merged_ozone_df.rename(columns={
    'Max': 'ozone_max',
    'Min': 'ozone_min',
    'Mean': 'ozone_mean',
    'Median': 'ozone_median',
    'Std': 'ozone_std',
})

# Calculate correlations
correlation_matrix = COPD_Incid_merged_ozone_df[[
    'COPD_average', 'lower', 'upper',
    'ozone_max', 'ozone_min', 'ozone_mean', 'ozone_median', 'ozone_std'
]].corr()

# Save correlation matrix to CSV
correlation_matrix.to_csv(f'/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/COPD/COPD_Incid_ozone_correlation_matrix.csv')

# Plot Correlation Heatmap
plt.figure(figsize=(12, 13))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0)
plt.title('COPD Incidence vs. Ozone Correlation Heatmap')
plt.savefig(f'/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/COPD/COPD_Incid_correlation_heatmap_ozone.png')
# plt.show()

