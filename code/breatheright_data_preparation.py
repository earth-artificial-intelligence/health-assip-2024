import os
import pandas as pd
import re

home_directory = os.path.expanduser("~")
print(home_directory)

data_folder = f"{home_directory}/Documents/GitHub/health-assip-2024/data"
merged_ozone_file_name = "ozone_lung_disease_yearly_merged.csv"


def split_mortality_column_into_three(lung_disease_df):
    # Define a function to split the mortality rate
    def split_mortality_rate(mortality_rate):
        # Regular expression to extract the values - regex
        match = re.match(r'(\d+\.\d+) \((\d+\.\d+), (\d+\.\d+)\)', mortality_rate)
        if match:
            avg, min_val, max_val = match.groups()
            return pd.Series([float(avg), float(min_val), float(max_val)], index=['mortality_average', 'mortality_min', 'mortality_max'])
        else:
            return pd.Series([None, None, None], index=['mortality_average', 'mortality_min', 'mortality_max'])

    # Apply the function to split the 'mortality_rate' column
    lung_disease_df[['mortality_average', 'mortality_min', 'mortality_max']] = lung_disease_df['Mortality Rate'].apply(split_mortality_rate)

    # Drop the original 'mortality_rate' column if you no longer need it
    lung_disease_df = lung_disease_df.drop(columns=['Mortality Rate'])

    return lung_disease_df

def parse_and_load_data():
    files = [f for f in os.listdir(data_folder) if os.path.isfile(os.path.join(data_folder, f))]
    print(files)

    ozone_data_path = f"{data_folder}/Ozonecombined.csv"
    lung_disease_data_path = f"{data_folder}/lung_disease_data.csv"
    pm25_data_path = f"{data_folder}/PM2.5combined.csv"

    # Read all the csv into pandas dataframe in memory
    ozone_df = pd.read_csv(ozone_data_path, parse_dates=['Date Local'])
    lung_disease_df = pd.read_csv(lung_disease_data_path)
    pm25_df = pd.read_csv(pm25_data_path)

    print("ozone head: ", ozone_df.columns)
    print("pm25 header: ", pm25_df.columns)
    pd.set_option('display.max_columns', None)
    print("ozone header: ", ozone_df.head())
    print("lung disease head: ", lung_disease_df.columns)

    # convert the daily ozone into yearly data
    ozone_df['year'] = ozone_df['Date Local'].dt.year
    
    # Group by additional columns and 'year'
    grouped = ozone_df.groupby(['State Name', 'County Name', 'year'])['Arithmetic Mean']

    # Compute statistics
    stats_df = grouped.agg(['max', 'min', 'mean', 'median', 'std']).reset_index()

    # Rename columns for clarity
    stats_df.columns = ['State Name', 'County Name', 'year', 'Max', 'Min', 'Mean', 'Median', 'Std']

    

    # Convert columns to string in both DataFrames
    stats_df['county'] = stats_df['County Name'].str.lower()
    stats_df['state'] = stats_df['State Name'].str.lower()
    stats_df['year'] = stats_df['year'].astype(int)

    lung_disease_df['county'] = lung_disease_df['County Name'].str.strip()
    lung_disease_df['county'] = lung_disease_df['county'].str.lower()
    lung_disease_df['state'] = lung_disease_df['State Name'].str.lower()
    lung_disease_df['year'] = lung_disease_df['year'].astype(int)

    # Print the results
    print("ozone aggregated yearly data: ", stats_df)

    lung_disease_df = split_mortality_column_into_three(lung_disease_df)
    print("split lung disease header:", lung_disease_df.head())

    # Merge the statistics oznone DataFrame with the lung disease DataFrame
    merged_df = pd.merge(lung_disease_df, stats_df,  
                        on=['county', 'state', 'year'],
                        how='inner')

    print("Merged dataframe is: ", merged_df.head())

    # Save to a CSV file
    merged_df.to_csv(f'{data_folder}/{merged_ozone_file_name}', index=False)



if __name__ == "__main__":
    parse_and_load_data()

