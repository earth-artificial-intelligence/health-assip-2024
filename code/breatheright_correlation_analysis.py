
from breatheright_data_preparation import data_folder, merged_ozone_file_name
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def do_breatheright_correlation_analysis():
    # read in the merged one csv file with ozone and lung disease data
    merged_ozone_df = pd.read_csv(f"{data_folder}/{merged_ozone_file_name}")

    print(merged_ozone_df.head())
    print(merged_ozone_df.columns)

    # drop the unnecessary columns
    merged_ozone_df = merged_ozone_df.drop(columns=[
        "County Name_x", 'State Name_x', 
        'County Name_y', 'State Name_y'])

    merged_ozone_df = merged_ozone_df.rename(columns={
        'Max': 'ozone_max',
        'Min': 'ozone_min',
        'Mean': 'ozone_mean',
        'Median': 'ozone_median',
        'Std': 'ozone_std'
    })
    
    # Calculate correlations
    correlation_matrix = merged_ozone_df[[
        'mortality_average', 'mortality_min', 'mortality_max',
        'ozone_max', 'ozone_min', 'ozone_mean', 'ozone_median', 
        'ozone_std']].corr()

    # Save correlation matrix to CSV
    correlation_matrix.to_csv(f'{data_folder}/correlation_matrix_ozone_lung_disease_5years.csv')

    # Plot Correlation Heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0)
    plt.title('Correlation Heatmap')
    plt.savefig(f'{data_folder}/correlation_heatmap_ozone_lung_disease.png')
    #plt.show()


if __name__ == "__main__":
    do_breatheright_correlation_analysis()
