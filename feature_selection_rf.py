# feature_selection_rf.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Load HRV data for both relax and stress phases
relax_data = pd.read_csv('combined_hrv_relax_data.csv')
stress_data = pd.read_csv('combined_hrv_stress_data.csv')

# Add class labels: 0 for relax, 1 for stress
relax_data['class'] = 0
stress_data['class'] = 1

# Combine data from both phases
combined_data = pd.concat([relax_data, stress_data])

# Remove columns with missing values
combined_data_cleaned = combined_data.dropna(axis=1)

# Separate features and labels
features = combined_data_cleaned.drop('class', axis=1)
labels = combined_data_cleaned['class']

# Train Random Forest classifier
rf = RandomForestClassifier(random_state=24)
rf.fit(features, labels)

# Get the top 6 features
feature_importances = pd.Series(rf.feature_importances_, index=features.columns)
selected_features = feature_importances.nlargest(6).index

# Save the selected features for both phases
filtered_relax_data = relax_data[selected_features]
filtered_stress_data = stress_data[selected_features]
filtered_relax_data.to_csv('filtered_relax_data_rf.csv', index=False)
filtered_stress_data.to_csv('filtered_stress_data_rf.csv', index=False)

print(f"Selected features: {list(selected_features)}")