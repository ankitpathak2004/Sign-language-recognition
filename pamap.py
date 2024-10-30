import pandas as pd

# Load the dataset (update the file path accordingly)
# Use sep='\s+' for space-separated values
data = pd.read_csv('subject101.dat', sep='\s+', header=None, engine='python', skip_blank_lines=True)

# Display the initial structure of the dataset
print("Initial data:")
print(data.head())

# Step 1: Check for the number of columns
print("\nNumber of columns:", data.shape[1])

# Step 2: Checking for missing values
print("\nChecking for missing values:")
print(data.isnull().sum())

# Rename columns based on the expected structure
column_names = [
    "Timestamp",  # 1: Timestamp (s)
    "ActivityID",  # 2: Activity ID
    "Heart_Rate",  # 3: Heart Rate (bpm)
    # IMU Hand (4-20)
    "Hand_Accelerometer_X",  # 4
    "Hand_Accelerometer_Y",  # 5
    "Hand_Accelerometer_Z",  # 6
    "Hand_Gyroscope_X",  # 7
    "Hand_Gyroscope_Y",  # 8
    "Hand_Gyroscope_Z",  # 9
    "Hand_Magnetometer_X",  # 10
    "Hand_Magnetometer_Y",  # 11
    "Hand_Magnetometer_Z",  # 12
    "Hand_Quaternion_X",  # 13
    "Hand_Quaternion_Y",  # 14
    "Hand_Quaternion_Z",  # 15
    "Hand_Quaternion_W",  # 16
    "Hand_Temperature",  # 17
    "Hand_Reserved_1",  # 18
    "Hand_Reserved_2",  # 19
    "Hand_Reserved_3",  # 20
    # IMU Chest (21-37)
    "Chest_Accelerometer_X",  # 21
    "Chest_Accelerometer_Y",  # 22
    "Chest_Accelerometer_Z",  # 23
    "Chest_Gyroscope_X",  # 24
    "Chest_Gyroscope_Y",  # 25
    "Chest_Gyroscope_Z",  # 26
    "Chest_Magnetometer_X",  # 27
    "Chest_Magnetometer_Y",  # 28
    "Chest_Magnetometer_Z",  # 29
    "Chest_Quaternion_X",  # 30
    "Chest_Quaternion_Y",  # 31
    "Chest_Quaternion_Z",  # 32
    "Chest_Quaternion_W",  # 33
    "Chest_Temperature",  # 34
    "Chest_Reserved_1",  # 35
    "Chest_Reserved_2",  # 36
    "Chest_Reserved_3",  # 37
    # IMU Ankle (38-54)
    "Ankle_Accelerometer_X",  # 38
    "Ankle_Accelerometer_Y",  # 39
    "Ankle_Accelerometer_Z",  # 40
    "Ankle_Gyroscope_X",  # 41
    "Ankle_Gyroscope_Y",  # 42
    "Ankle_Gyroscope_Z",  # 43
    "Ankle_Magnetometer_X",  # 44
    "Ankle_Magnetometer_Y",  # 45
    "Ankle_Magnetometer_Z",  # 46
    "Ankle_Quaternion_X",  # 47
    "Ankle_Quaternion_Y",  # 48
    "Ankle_Quaternion_Z",  # 49
    "Ankle_Quaternion_W",  # 50
    "Ankle_Temperature",  # 51
    "Ankle_Reserved_1",  # 52
    "Ankle_Reserved_2",  # 53
    "Ankle_Reserved_3"   # 54
]

# Check if the number of columns matches
if data.shape[1] == len(column_names):
    data.columns = column_names  # Assign the column names
else:
    print(f"Warning: Expected {len(column_names)} columns, but got {data.shape[1]}.")

# Step 3: Convert data types if necessary
# For example, converting Timestamp to a datetime type
data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit='s')

# Display the cleaned data
print("\nCleaned data:")
print(data.head())
data.to_csv("1.csv")
