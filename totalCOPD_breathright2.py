import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the CSV file into a DataFrame
#file_path = '/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/COPD/Non Smoke/totalCOPD_ozone_merged_df.csv'
#totalCOPD_ozone_merged_df = pd.read_csv(file_path)


# Verify the data types after conversion
#print(totalCOPD_ozone_merged_df.dtypes)


# Display the first few rows of the DataFrame
#print(totalCOPD_ozone_merged_df.head())
#print(totalCOPD_ozone_merged_df.columns)

# Assuming 'Min_x' and 'Min_y' are already in the DataFrame
#totalCOPD_ozone_merged_df['difference_Min_x_Min_y'] = totalCOPD_ozone_merged_df['Min_x'] - totalCOPD_ozone_merged_df['Min_y']

# Display the first few rows to check the new column
#print(totalCOPD_ozone_merged_df[['Min_x', 'Min_y', 'difference_Min_x_Min_y']].head())

# Calculate basic statistics for the difference
#diff_mean = totalCOPD_ozone_merged_df['difference_Min_x_Min_y'].mean()
#diff_median = totalCOPD_ozone_merged_df['difference_Min_x_Min_y'].median()
#diff_std = totalCOPD_ozone_merged_df['difference_Min_x_Min_y'].std()

# Fill NaN values in Min_x or Min_y with a specific value, e.g., 0
#totalCOPD_ozone_merged_df_filled = totalCOPD_ozone_merged_df.fillna({'Min_x': 0, 'Min_y': 0})

# Recalculate the difference
#totalCOPD_ozone_merged_df_filled['difference_Min_x_Min_y'] = totalCOPD_ozone_merged_df_filled['Min_x'] - totalCOPD_ozone_merged_df_filled['Min_y']

# Display the updated DataFrame
#print(totalCOPD_ozone_merged_df_filled[['Min_x', 'Min_y', 'difference_Min_x_Min_y']].head())

# Calculate basic statistics
#diff_mean = totalCOPD_ozone_merged_df_filled['difference_Min_x_Min_y'].mean()
#diff_median = totalCOPD_ozone_merged_df_filled['difference_Min_x_Min_y'].median()
#diff_std = totalCOPD_ozone_merged_df_filled['difference_Min_x_Min_y'].std()

#print(f"Mean of the difference: {diff_mean}")
#print(f"Median of the difference: {diff_median}")
#print(f"Standard deviation of the difference: {diff_std}")

# Drop the Min_x column
#totalCOPD_ozone_merged_df = totalCOPD_ozone_merged_df.drop(columns=['Min_x', 'Max_x'])

# Rename columns
#totalCOPD_ozone_merged_df = totalCOPD_ozone_merged_df.rename(columns={'Min_y': 'Min', 'Max_y': 'Max'})


#def do_breatheright_correlation_analysis():
    # Read in the merged CSV file with ozone and lung disease data
    #totalCOPD_ozone_merged_df = pd.read_csv(f"/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/COPD/Non Smoke/totalCOPD_ozone_merged_df.csv")
    #print(totalCOPD_ozone_merged_df.head())
    #print(totalCOPD_ozone_merged_df.columns)

# Drop the unnecessary columns
# ILD_merged_pm25_df = ILD_merged_pm25_df.drop(columns=["county_x", 'State Name', 'county_y', 'State Name_y'])

# Figuring out which columns to drop
# Values in 'county_x' but not in 'county_y'
#county_x_not_in_county_y = set(nosmokeCOPD_merged_pm25_df['county_x'].dropna()).difference(set(ILD_merged_pm25_df['county_y'].dropna()))
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
#totalCOPD_ozone_merged_df['State Name'] = totalCOPD_ozone_merged_df['State Name'].str.lower()

# Convert state names in 'state' to lowercase
#totalCOPD_ozone_merged_df['state'] = totalCOPD_ozone_merged_df['state'].str.lower()

# Get unique values in 'State Name' and 'state'
#state_name_values = set(totalCOPD_ozone_merged_df['State Name'].dropna().unique())
#state_values = set(totalCOPD_ozone_merged_df['state'].dropna().unique())

# Find differences
#diff_state_name_not_in_state = state_name_values - state_values
#diff_state_not_in_state_name = state_values - state_name_values

# Print the differences
#print("Values in 'State Name' but not in 'state':")
#print(diff_state_name_not_in_state)

#print("\nValues in 'state' but not in 'State Name':")
#print(diff_state_not_in_state_name)

# Check for null values
#print("\nNull values in 'State Name':")
#print(totalCOPD_ozone_merged_df['State Name'].isnull().sum())

#print("\nNull values in 'state':")
#print(totalCOPD_ozone_merged_df['state'].isnull().sum())

# Drop the 'state' column
#totalCOPD_ozone_merged_df = totalCOPD_ozone_merged_df.drop(columns=['state'])

# Renaming columns for clarity
#totalCOPD_ozone_merged_df = totalCOPD_ozone_merged_df.rename(columns={
    #'Max': 'ozone_max',
    #'Min': 'ozone_min',
    #'Mean': 'ozone_mean',
    #'Median': 'ozone_median',
    #'Std': 'ozone_std',
#})

# Calculate correlations
#correlation_matrix = totalCOPD_ozone_merged_df[[
    #'Average', 'Min', 'Max',
    #'ozone_max', 'ozone_min', 'ozone_mean', 'ozone_median', 'ozone_std'
#]].corr()

# Convert columns to numeric where applicable
#numeric_columns = ['average', 'min', 'max', 'ozone_max', 'ozone_min', 'ozone_mean', 'ozone_median', 'ozone_std']
#totalCOPD_ozone_merged_df[numeric_columns] = totalCOPD_ozone_merged_df[numeric_columns].apply(pd.to_numeric, errors='coerce')

# Verify the data types after conversion
#print(totalCOPD_ozone_merged_df.dtypes)

# Save correlation matrix to CSV
#correlation_matrix.to_csv(f'/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/COPD/Non Smoke/COPDtotalozone_correlation_matrix.csv')

# Plot Correlation Heatmap
#plt.figure(figsize=(12, 13))
#sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0)
#plt.title('COPD Total Incidence vs. Ozone Correlation Heatmap')
#plt.savefig(f'/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/COPD/Non Smoke/totalCOPD1_correlation_heatmap_ozone.png')
# plt.show()


# Check for missing values in relevant columns
#print(totalCOPD_ozone_merged_df[['average', 'min', 'max', 'ozone_max', 'ozone_min', 'ozone_mean', 'ozone_median', 'ozone_std']].isnull().sum())


#print(totalCOPD_ozone_merged_df.dtypes)


#print(totalCOPD_ozone_merged_df[['average', 'min', 'max', 'ozone_max', 'ozone_min', 'ozone_mean', 'ozone_median', 'ozone_std']].sample(10))




import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the CSV file into a DataFrame
file_path = '/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/COPD/Non Smoke/totalCOPD_ozone_merged_df.csv'
totalCOPD_ozone_merged_df = pd.read_csv(file_path)

# Verify the data types after conversion
print(totalCOPD_ozone_merged_df.dtypes)

# Display the first few rows of the DataFrame
print(totalCOPD_ozone_merged_df.head())
print(totalCOPD_ozone_merged_df.columns)

# Assuming 'Min_x' and 'Min_y' are already in the DataFrame
#totalCOPD_ozone_merged_df['difference_Min_x_Min_y'] = totalCOPD_ozone_merged_df['Min_x'] - totalCOPD_ozone_merged_df['Min_y']

# Display the first few rows to check the new column
#print(totalCOPD_ozone_merged_df[['Min_x', 'Min_y', 'difference_Min_x_Min_y']].head())

# Calculate basic statistics for the difference
#diff_mean = totalCOPD_ozone_merged_df['difference_Min_x_Min_y'].mean()
#diff_median = totalCOPD_ozone_merged_df['difference_Min_x_Min_y'].median()
#diff_std = totalCOPD_ozone_merged_df['difference_Min_x_Min_y'].std()

# Fill NaN values in Min_x or Min_y with a specific value, e.g., 0
#totalCOPD_ozone_merged_df_filled = totalCOPD_ozone_merged_df.fillna({'Min_x': 0, 'Min_y': 0})

# Recalculate the difference
#totalCOPD_ozone_merged_df_filled['difference_Min_x_Min_y'] = totalCOPD_ozone_merged_df_filled['Min_x'] - totalCOPD_ozone_merged_df_filled['Min_y']

# Display the updated DataFrame
#print(totalCOPD_ozone_merged_df_filled[['Min_x', 'Min_y', 'difference_Min_x_Min_y']].head())

# Calculate basic statistics
#diff_mean = totalCOPD_ozone_merged_df_filled['difference_Min_x_Min_y'].mean()
#diff_median = totalCOPD_ozone_merged_df_filled['difference_Min_x_Min_y'].median()
#diff_std = totalCOPD_ozone_merged_df_filled['difference_Min_x_Min_y'].std()

#print(f"Mean of the difference: {diff_mean}")
#print(f"Median of the difference: {diff_median}")
#print(f"Standard deviation of the difference: {diff_std}")

# Drop the Min_x and Max_x columns
#totalCOPD_ozone_merged_df = totalCOPD_ozone_merged_df.drop(columns=['Min_x', 'Max_x'])

# Rename columns
#totalCOPD_ozone_merged_df = totalCOPD_ozone_merged_df.rename(columns={'Min_y': 'Min', 'Max_y': 'Max'})

# Ensure the renaming has taken place
print(totalCOPD_ozone_merged_df.columns)

# Drop the 'state' column
totalCOPD_ozone_merged_df = totalCOPD_ozone_merged_df.drop(columns=['state'])

# Renaming columns for clarity
#totalCOPD_ozone_merged_df = totalCOPD_ozone_merged_df.rename(columns={
    #'Max': 'ozone_max',
    #'Min': 'ozone_min',
    #'Mean': 'ozone_mean',
    #'Median': 'ozone_median',
    #'Std': 'ozone_std',
#})

# Convert columns to numeric where applicable
numeric_columns = ['Average', 'ozone_max', 'ozone_min', 'ozone_mean', 'ozone_median', 'ozone_std']
totalCOPD_ozone_merged_df[numeric_columns] = totalCOPD_ozone_merged_df[numeric_columns].apply(pd.to_numeric, errors='coerce')

# Verify the data types after conversion
print(totalCOPD_ozone_merged_df.dtypes)

# Calculate correlations
correlation_matrix = totalCOPD_ozone_merged_df[[
    'Average', 'ozone_max', 'ozone_min', 'ozone_mean', 'ozone_median', 'ozone_std'
]].corr()

# Save correlation matrix to CSV
correlation_matrix.to_csv(f'/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/COPD/Non Smoke/COPDtotalozone_correlation_matrix.csv')

# Plot Correlation Heatmap
plt.figure(figsize=(12, 13))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0)
plt.title('COPD Total Incidence vs. Ozone Correlation Heatmap')
plt.savefig(f'/Users/icce_icecweam7/gw-workspace/S6wTraiideDo/COPD/Non Smoke/totalCOPD1_correlation_heatmap_ozone.png')
# plt.show()

# Check for missing values in relevant columns
print(totalCOPD_ozone_merged_df[['Average', 'ozone_max', 'ozone_min', 'ozone_mean', 'ozone_median', 'ozone_std']].isnull().sum())

print(totalCOPD_ozone_merged_df.dtypes)

print(totalCOPD_ozone_merged_df[['Average', 'ozone_max', 'ozone_min', 'ozone_mean', 'ozone_median', 'ozone_std']].sample(10))




