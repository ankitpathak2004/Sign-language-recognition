import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load the test dataset
test_data = pd.read_csv('test_data1.csv')  # Replace with your actual test file path
unique_labels=["hello","thank you"]
# Sort data by 'ID' and 'Elapsed Time' for consistency
test_data = test_data.sort_values(by=['ID', 'Elapsed Time (s)'])

# Group by 'ID' to treat each ID as a separate segment
grouped_test_data = test_data.groupby('ID')

# Set the sequence length to match the model's expected input
sequence_length = 130  # Adjust based on training

# Initialize lists to store predictions and corresponding IDs
predicted_labels = []
test_ids = []
model = tf.keras.models.load_model('model.h5')
# Process each segment (ID group)
for id_, group in grouped_test_data:
    # Extract feature values, excluding 'ID' and 'Character'
    X_segment = group.iloc[:, 2:-1].values

    # Pad or truncate each sequence to the required length
    X_segment_padded = pad_sequences([X_segment], maxlen=sequence_length, padding='post', truncating='post', dtype='float32')

    # Predict for this padded segment
    prediction = model.predict(X_segment_padded)
    predicted_class = np.argmax(prediction, axis=1)

    # Map the predicted index to the original label
    predicted_labels.append(unique_labels[predicted_class[0]])
    test_ids.append(id_)

# Combine results into a DataFrame
results = pd.DataFrame({'ID': test_ids, 'Predicted Character': predicted_labels})

# Display predictions
print(results.head())
