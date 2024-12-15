import neurokit2 as nk
import pandas as pd
import glob

def calculate_hrv(phase):
    # List to store HRV data for each file
    hrv_data_list = []
    
    # Find all CSV files in the specified phase directory (either 'relax' or 'stress')
    file_paths = glob.glob(f'./{phase}/*.csv')

    for file_path in file_paths:
        # Load data
        data = pd.read_csv(file_path)
        
        # Process PPG signal
        ppg = data['PPG']
        ppg_elgendi = nk.ppg_clean(ppg, sampling_rate=128, method='elgendi')
        
        # Detect peaks
        peaks, _ = nk.ppg_peaks(ppg_elgendi, sampling_rate=128, method="elgendi", correct_artifacts=True)
        
        # Calculate HRV metrics
        hrv_time = nk.hrv_time(peaks, sampling_rate=128)
        hrv_frequency = nk.hrv_frequency(peaks, sampling_rate=128, psd_method="welch")
        hrv_nonlinear = nk.hrv_nonlinear(peaks, sampling_rate=128)
        
        # Combine HRV metrics into a single DataFrame
        hrv_combined = pd.concat([hrv_time, hrv_frequency, hrv_nonlinear], axis=1)
        hrv_data_list.append(hrv_combined)
    
    # Concatenate all HRV data and save to CSV
    pd.concat(hrv_data_list, ignore_index=True).to_csv(f'combined_hrv_{phase}_data.csv', index=False)
    print(f'HRV data saved for {phase} phase')

# Calculate HRV for both relax and stress phases
calculate_hrv('relax')
calculate_hrv('stress')