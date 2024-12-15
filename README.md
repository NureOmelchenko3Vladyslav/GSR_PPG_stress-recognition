# GSR_PPG_stress-recognition
This project analyzes physiological signals like skin resistance, conductance, and PPG data to differentiate between relaxation and stress states.

# Features
Data preprocessing and cleaning.
Phase separation (relax/stress).
HRV calculation using PPG signals.
Feature selection with Random Forest.
Machine learning-based classification.
# Installation
Clone the repository:
git clone <repository_url>
Install dependencies:
pip install -r requirements.txt
# Usage
Preprocess data:
python preprocessing.py

Divide data into phases:
python divide.py

Calculate HRV:
python calculate_hrv.py

Normalize data:
python normalize_and_filter.py

Perform classification:
python classification.py
