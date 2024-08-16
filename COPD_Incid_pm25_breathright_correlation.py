import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the CSV file into a DataFrame
file_path = '/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/COPD/COPD_Incid_pm25_merged_df.csv'
COPD_Incid_merged_pm25_df = pd.read_csv(file_path)

COPD_Incid_merged_pm25_df = COPD_Incid_merged_pm25_df.drop(columns=['COPD_min', 'COPD_max', 'county', 'County Name'])



# Display the first few rows of the DataFrame
print(COPD_Incid_merged_pm25_df.head())
print(COPD_Incid_merged_pm25_df.columns)

def do_breatheright_correlation_analysis():
    # Read in the merged CSV file with ozone and lung disease data
    COPD_Incid_merged_pm25_df = pd.read_csv(f"/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/COPD/COPD_Incid_pm25_merged_df.csv")
    print(COPD_Incid_merged_pm25_df.head())
    print(COPD_Incid_merged_pm25_df.columns)

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
COPD_Incid_merged_pm25_df['State Name'] = COPD_Incid_merged_pm25_df['State Name'].str.lower()

# Convert state names in 'state' to lowercase
COPD_Incid_merged_pm25_df['state'] = COPD_Incid_merged_pm25_df['state'].str.lower()

# Get unique values in 'State Name' and 'state'
state_name_values = set(COPD_Incid_merged_pm25_df['State Name'].dropna().unique())
state_values = set(COPD_Incid_merged_pm25_df['state'].dropna().unique())

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
print(COPD_Incid_merged_pm25_df['State Name'].isnull().sum())

print("\nNull values in 'state':")
print(COPD_Incid_merged_pm25_df['state'].isnull().sum())

# Drop the 'state' column
COPD_Incid_merged_pm25_df = COPD_Incid_merged_pm25_df.drop(columns=['state'])

# Renaming columns for clarity
COPD_Incid_merged_pm25_df = COPD_Incid_merged_pm25_df.rename(columns={
    'Max': 'pm25_max',
    'Min': 'pm25_min',
    'Mean': 'pm25_mean',
    'Median': 'pm25_median',
    'Std': 'pm25_std',
})

# Calculate correlations
correlation_matrix = COPD_Incid_merged_pm25_df[[
    'COPD_average', 'lower', 'upper',
    'pm25_max', 'pm25_min', 'pm25_mean', 'pm25_median', 'pm25_std'
]].corr()

# Save correlation matrix to CSV
correlation_matrix.to_csv(f'/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/COPD/COPD_Incid_pm25_correlation_matrix.csv')

# Plot Correlation Heatmap
plt.figure(figsize=(12, 13))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0)
plt.title('COPD Incidence vs. PM2.5 Correlation Heatmap')
plt.savefig(f'/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/COPD/COPD_Incid_correlation_heatmap_pm25.png')
# plt.show()

