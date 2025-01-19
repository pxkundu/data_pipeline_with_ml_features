import json
import os
import random
from datetime import datetime

# Configuration
OUTPUT_FOLDER = "data/raw"  # Path to the raw data folder
NUM_ENTRIES = 1000  # Number of entries to generate

# Ensure the output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Generate random data
def generate_data(num_entries):
    data = []
    for i in range(num_entries):
        entry = {
            "sensor_id": i + 1,
            "temperature": round(random.uniform(20.0, 30.0), 2),  # Random temperature between 20-30
            "vibration": round(random.uniform(0.01, 0.1), 4),    # Random vibration between 0.01-0.1
            "timestamp": f"2025-01-17T12:{random.randint(0, 59):02}:{random.randint(0, 59):02}Z"
        }
        data.append(entry)
    return data

# Write data to the raw folder
def save_data_to_raw_folder(folder, data):
    # Generate a dynamic file name based on the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"raw_data_{timestamp}.json"
    file_path = os.path.join(folder, file_name)

    # Save the data to the file
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
    
    print(f"Generated {len(data)} entries and saved to {file_path}")
    return file_path

if __name__ == "__main__":
    # Generate data
    data = generate_data(NUM_ENTRIES)

    # Save the data in the raw folder
    save_data_to_raw_folder(OUTPUT_FOLDER, data)
