# normalize_and_filter.py
import pandas as pd
from scipy.signal import find_peaks
import glob
import os

# Function to normalize data within the range [0, 1]
def normalize_data(df, column):
    df[column] = (df[column] - df[column].min()) / (df[column].max() - df[column].min())
    return df

# Function to filter outliers using the interquartile range (IQR) method
def filter_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

# Process resistance data for a specific phase (relax or stress)
def process_resistance_data(phase):
    results = []
    file_paths = glob.glob(f'./{phase}/*.csv')

    for file_path in file_paths:
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        df = pd.read_csv(file_path)
        
        # Filter outliers and normalize resistance data
        df_filtered = filter_outliers(df, 'Resistance')
        df_normalized = normalize_data(df_filtered, 'Resistance')
        
        # Find peaks in the resistance data
        peaks, properties = find_peaks(
            df_normalized['Resistance'], height=0.1, distance=450, width=8, prominence=0.1
        )
        num_peaks = len(peaks)

        results.append({'File': file_name, 'Number_of_Peaks': num_peaks})

    # Save peak analysis results to CSV
    results_df = pd.DataFrame(results)
    results_df.to_csv(f'peaks_{phase}.csv', index=False)
    print(f"Peaks analysis saved for {phase} phase.")

# Run the analysis for both relax and stress phases
process_resistance_data('relax')
process_resistance_data('stress')

# Combine peak data with filtered HRV data
def combine_data_with_peaks():
    # Load HRV data for both phases
    filtered_relax_data = pd.read_csv('filtered_relax_data.csv')
    filtered_stress_data = pd.read_csv('filtered_stress_data.csv')

    # Load peak data for both phases
    resistance_std_relax = pd.read_csv('peaks_relax.csv')
    resistance_std_stress = pd.read_csv('peaks_stress.csv')

    # Add the Number_of_Peaks column to the HRV data
    filtered_relax_data['Number_of_Peaks'] = resistance_std_relax['Number_of_Peaks']
    filtered_stress_data['Number_of_Peaks'] = resistance_std_stress['Number_of_Peaks']

    # Save the updated datasets
    filtered_relax_data.to_csv('combined_filtered_relax_data.csv', index=False)
    filtered_stress_data.to_csv('combined_filtered_stress_data.csv', index=False)

    print('Updated data with peak counts saved successfully.')

# Run the combination step
combine_data_with_peaks()