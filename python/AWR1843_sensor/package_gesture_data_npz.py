import numpy as np
import os

# Define the folders and corresponding labels
folders = ["left", "right", "up", "down", "r_left", "r_right"]
labels_dict = {"left": 0, "right": 1, "up": 2, "down": 3, "r_left": 4, "r_right": 5}

# Initialize lists to hold features and labels
all_features = []
all_labels = []

# Process each folder
for folder in folders:
    label = labels_dict[folder]
    folder_path = os.path.join("gesture_data", folder)

    # List all .npy files in the folder
    npy_files = [f for f in os.listdir(folder_path) if f.endswith(".npy")]

    # Load each .npy file and append the data and label
    for npy_file in npy_files:
        file_path = os.path.join(folder_path, npy_file)
        data = np.load(file_path)

        # Reshape from 2x30 to 1x60
        reshaped_data = data.flatten()

        all_features.append(reshaped_data)
        all_labels.append(label)

# Convert lists to numpy arrays
all_features = np.vstack(all_features)  # Stack to create a 2D array
all_labels = np.array(all_labels)

# Save to an npz file
np.savez("combined_data.npz", features=all_features, labels=all_labels)

print("Data has been successfully saved to 'combined_data.npz'.")
