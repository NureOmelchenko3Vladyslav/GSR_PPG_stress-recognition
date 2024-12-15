import pandas as pd
import matplotlib.pyplot as plt
import os
import glob

# Create output directories if they don't exist
os.makedirs('filtered_by_time', exist_ok=True)
os.makedirs('graphs', exist_ok=True)
os.makedirs('graphs/resistance', exist_ok=True)
os.makedirs('graphs/conductance', exist_ok=True)
os.makedirs('graphs/ppg', exist_ok=True)

# Find all CSV files in the ./clean directory
file_paths = glob.glob('./clean/*.csv')

for file_path in file_paths:
    # Get the base file name (without extension) to use in output names
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    new_file_path = f'./filtered_by_time/filtered_{file_name}.csv'
    
    # Load data and preprocess
    df = pd.read_csv(file_path)
    df['Time_Since_Start'] = (df['Shimmer_D630_TimestampSync_Unix_CAL'] - df['Shimmer_D630_TimestampSync_Unix_CAL'].iloc[0]) / (1000 / 128.0)
    max_count_900s = 900 * 128
    df_ready = df[df['Time_Since_Start'] < max_count_900s]
    
    # Rename columns for clarity
    df_ready.rename(columns={
        'Shimmer_D630_TimestampSync_Unix_CAL': 'Unix_Time',
        'Shimmer_D630_GSR_Skin_Resistance_CAL': 'Resistance',
        'Shimmer_D630_GSR_Skin_Conductance_CAL': 'Conductance',
        'Shimmer_D630_PPG_A13_CAL': 'PPG',
        'Shimmer_D630_PPG_IBI_CAL': 'IBI',
        'Shimmer_D630_PPGtoHR_CAL': 'HR'}, inplace=True)
    
    # Save the processed data
    df_ready.to_csv(new_file_path, index=False)
    print(f'Processed file {file_name}')

    # Convert index to time in minutes
    time_data = df_ready.index / 7680  # converting indices to minutes

    # Plot Resistance graph
    plt.figure(figsize=(10, 6))
    plt.plot(time_data, df_ready['Resistance'], label='Resistance', color='b')
    plt.title(f'Resistance Signal for {file_name}')
    plt.xlabel('Time (min)')
    plt.ylabel('Resistance (kOhms)')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'graphs/resistance/resistance_{file_name}.png')
    plt.close()

    # Plot Conductance graph if column is present
    if 'Conductance' in df_ready.columns:
        plt.figure(figsize=(10, 6))
        plt.plot(time_data, df_ready['Conductance'], label='Conductance', color='r')
        plt.title(f'Conductance Signal for {file_name}')
        plt.xlabel('Time (min)')
        plt.ylabel('Conductance (uS)')
        plt.legend()
        plt.grid(True)
        plt.savefig(f'graphs/conductance/conductance_{file_name}.png')
        plt.close()
    else:
        print(f"Conductance column not found in file {file_name}")

    # Plot PPG graph
    plt.figure(figsize=(10, 6))
    plt.plot(time_data, df_ready['PPG'], label='PPG', color='g')
    plt.title(f'PPG Signal for {file_name}')
    plt.xlabel('Time (min)')
    plt.ylabel('PPG Amplitude')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'graphs/ppg/ppg_{file_name}.png')
    plt.close()