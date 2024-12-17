import pandas as pd
import numpy as np
import keras
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.utils import to_categorical

# Load your dataset
data = pd.read_csv('AI_model/sensor.csv')  # Replace with your actual file path

# Step 1: Add average acceleration columns
# Calculate the average of x, y, z acceleration for each row
data['Acceleration_avg'] = data[['Acceleration_x', 'Acceleration_y', 'Acceleration_z']].mean(axis=1)

# Step 2: Segment data into sequences
sequence_length = 130  # Adjust based on your data
segments = []

# Group data by ID (segment) and create sequences
for id_, group in data.groupby('ID'):
    label = group['Character'].iloc[0]  # Extract the gesture label
    samples = group.iloc[:, 2:].values  # Select all columns except 'ID' and 'Character'
    for start in range(0, len(samples) - sequence_length + 1):
        segment = samples[start:start + sequence_length]
        segments.append((segment, label))

# Convert to DataFrame for easier manipulation
segment_df = pd.DataFrame(segments, columns=['Segment', 'Label'])

# Step 3: Prepare features and labels
X = np.array(segment_df['Segment'].tolist())  # Features
y = np.array(segment_df['Label'].tolist())  # Labels

# Step 4: Encode labels
y_encoded, unique_labels = pd.factorize(y)
y_categorical = to_categorical(y_encoded)  # Convert to one-hot encoding

# Step 5: Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y_categorical, test_size=0.2, random_state=42)

# Step 6: Build the LSTM model
model = Sequential()
model.add(LSTM(64, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(Dropout(0.2))
model.add(LSTM(64))
model.add(Dropout(0.2))
model.add(Dense(len(unique_labels), activation='softmax'))  # Adjust the number of outputs

# Step 7: Compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Step 8: Train the model
model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))

# Step 9: Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print(f'Test Loss: {loss:.4f}, Test Accuracy: {accuracy:.4f}')

# Step 10: Save the model
keras.saving.save_model(model, 'AI_model/model.h5')
