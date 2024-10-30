import numpy as np
from tensorflow.keras.models import load_model
from touch_sdk import Watch
import time
import logging

# Load the pre-trained model
model = load_model('model.h5')  # Update with your model's path
unique_labels=["hello","thank you"]
# Constants
sequence_length = 130  # Length of sequences for prediction
sampling_rate = 50  # Assume sensor provides data at 50 Hz
buffer_size = sampling_rate * 3  # Number of samples for 3 seconds

class RealTimeWatch(Watch):
    def __init__(self):
        super().__init__()
        self.data_buffer = []  # Buffer to hold incoming sensor data
        self.id = 0  # Placeholder for segment ID
        self.start_time = None  # To track the start time of data collection

    def on_sensors(self, sensors):
        # Gather sensor data
        sensor_data = [
            sensors.acceleration[0],
            sensors.acceleration[1],
            sensors.acceleration[2],
            sensors.gravity[0],
            sensors.gravity[1],
            sensors.gravity[2],
            sensors.angular_velocity[0],
            sensors.angular_velocity[1],
            sensors.angular_velocity[2],
            sensors.orientation[0],
            sensors.orientation[1],
            sensors.orientation[2],
        ]

        self.data_buffer.append(sensor_data)

        # Check if we have collected enough data for a full 3 seconds
        if len(self.data_buffer) >= buffer_size:
            # Convert buffer to a numpy array
            segment = np.array(self.data_buffer[-buffer_size:])  # Get the latest 'buffer_size' samples
            
            # Reshape for prediction (if needed)
            segment = segment.reshape((1, segment.shape[0], segment.shape[1]))  # (1, 130, 12) for LSTM input

            # Make a prediction
            prediction = model.predict(segment)
            predicted_class = np.argmax(prediction, axis=1)

            # Output the predicted class
            print(f"Predicted Character: {unique_labels[predicted_class[0]]}")  # Assuming 'unique_labels' is accessible

            # Clear the buffer after prediction
            self.data_buffer = []  # Optionally clear the buffer

# Example usage
watch = RealTimeWatch()
try:
    watch.start()  # Start the watch to collect sensor data
except KeyboardInterrupt:
    watch.close()  # Close the CSV file on interrupt
    logging.info("Data collection stopped.")
