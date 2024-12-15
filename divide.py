import pandas as pd
import os
import glob

# Create output directories if they don't exist
os.makedirs('relax', exist_ok=True)
os.makedirs('stress', exist_ok=True)

# Find all CSV files in the ./filtered_by_time directory
file_paths = glob.glob('./filtered_by_time/*.csv')

for file_path in file_paths:
    # Get the base file name (without extension) to use in output names
    file_name = os.path.splitext(os.path.basename(file_path))[0]

    # Load data
    df = pd.read_csv(file_path)

    # Process Relax phase (skip first 5 minutes)
    skip_5_min = 300 * 128
    df_relax = df[df['Time_Since_Start'] >= skip_5_min].copy()
    df_relax['Time_Since_Start'] -= df_relax['Time_Since_Start'].min()
    relax_path = f'./relax/relax_{file_name}.csv'
    df_relax.to_csv(relax_path, index=False)
    print(f'Relax phase saved for file {file_name}')

    # Process Stress phase (skip first 8 minutes)
    skip_8_min = 480 * 128
    df_stress = df[df['Time_Since_Start'] >= skip_8_min].copy()
    df_stress['Time_Since_Start'] -= df_stress['Time_Since_Start'].min()
    stress_path = f'./stress/stress_{file_name}.csv'
    df_stress.to_csv(stress_path, index=False)
    print(f'Stress phase saved for file {file_name}')