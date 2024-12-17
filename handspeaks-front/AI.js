import * as THREE from 'three';
import { GLTFLoader } from 'GLTFLoader';

const watch = new TouchSDK.Watch();

// Create a connect button for the smartwatch
const connectButton = watch.createConnectButton();
document.body.appendChild(connectButton);

const sequenceLength = 130; // Number of samples needed for prediction
let sensorDataBuffer = []; // Buffer to accumulate sensor data
let isCollectingData = true; // Flag to control data collection

// Object to store sensor data
const sensorData = {
    acceleration: [0, 0, 0],
    gravity: [0, 0, 0],
    angularVelocity: [0, 0, 0],
    orientation: [0, 0, 0, 0],
};

let startTime = null;

// Create elements to display prediction result and time taken
const predictionElement = document.createElement('div');
predictionElement.id = 'prediction';
document.body.appendChild(predictionElement);

const timeTakenElement = document.createElement('div');
timeTakenElement.id = 'timeTaken';
document.body.appendChild(timeTakenElement);

// Handle sensor data updates
watch.addEventListener('accelerationchanged', (event) => {
    const { x, y, z } = event.detail;
    sensorData.acceleration = [x, y, z];
});

watch.addEventListener('angularvelocitychanged', (event) => {
    const { x, y, z } = event.detail;
    sensorData.angularVelocity = [x, y, z];
});

watch.addEventListener('gravityvectorchanged', (event) => {
    const { x, y, z } = event.detail;
    sensorData.gravity = [x, y, z];
});

watch.addEventListener('orientationchanged', (event) => {
    const { x, y, z, w } = event.detail;
    sensorData.orientation = [x, y, z, w];
});

// Function to check if all sensor data values are non-zero
function isSensorDataValid() {
    const allData = [
        ...sensorData.acceleration,
        ...sensorData.gravity,
        ...sensorData.angularVelocity,
        ...sensorData.orientation
    ];
    return allData.every(value => value !== 0);
}

// Initialize Three.js scene
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

// Position the camera along the negative Z-axis to face the model
camera.position.set(0, 30, -50);  // Z is negative to place the camera opposite to the model

// The camera will look at the origin (where your hand model is placed)
camera.lookAt(new THREE.Vector3(0, 0, 0));

// Add the camera to the scene
scene.add(camera);

const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Add Ambient Light for general illumination
const ambientLight = new THREE.AmbientLight(0x404040, 2); // Soft light with intensity 2
scene.add(ambientLight);

// Add Directional Light for strong lighting and shadows
const directionalLight = new THREE.DirectionalLight(0xffffff, 1); // White light with intensity 1
directionalLight.position.set(5, 5, 5).normalize(); // Position the light in the scene
scene.add(directionalLight);

// Load the textures for the skybox (you will need 6 images for each face of the cube)
const skyboxLoader = new THREE.CubeTextureLoader();
const texture = skyboxLoader.load([
    'textures/skybox/px.jpg', // +X face
    'textures/skybox/nx.jpg', // -X face
    'textures/skybox/py.jpg', // +Y face
    'textures/skybox/ny.jpg', // -Y face
    'textures/skybox/pz.jpg', // +Z face
    'textures/skybox/nz.jpg'  // -Z face
]);

// Set the scene background to the loaded texture
scene.background = texture;

let handModel = null;

// Load the 3D hand model
const loader = new GLTFLoader();
loader.load('../3dmodel/arm.glb', (gltf) => {
    handModel = gltf.scene;

    // Invert the model's rotation to fix the upside down issue
    scene.add(handModel);
    animate(); // Start the animation loop after loading the model
});

// Function to update the 3D hand model's rotation based on sensor orientation
function updateHandModel() {
    if (handModel && isSensorDataValid()) {
        const [qx, qy, qz, qw] = sensorData.orientation; // Get quaternion values
        
        // Convert sensor quaternion to Three.js quaternion
        const quaternion = new THREE.Quaternion(qy, -qz, qx, -qw); // (x, z = rotation in place, y = side)

        // Convert quaternion to Euler angles
        const euler = new THREE.Euler().setFromQuaternion(quaternion, 'XYZ'); // Adjust rotation order if needed

        // Apply the calculated rotation to the hand model
        handModel.rotation.x = euler.x;
        handModel.rotation.y = euler.y;
        handModel.rotation.z = euler.z;
    }
}

// Render loop
function animate() {
    requestAnimationFrame(animate);
    updateHandModel(); // Update hand model's orientation
    renderer.render(scene, camera);
}

// Function to accumulate sensor data
function accumulateSensorData() {
    if (!isCollectingData || !isSensorDataValid()) return;

    if (sensorDataBuffer.length === 0) {
        startTime = Date.now();
    }

    const structuredData = [
        ...sensorData.acceleration,
        ...sensorData.gravity,
        ...sensorData.angularVelocity,
        ...sensorData.orientation.slice(0, 3) // Only take x, y, z from orientation
    ];

    sensorDataBuffer.push(structuredData);

    if (sensorDataBuffer.length >= sequenceLength) {
        // Stop collecting data temporarily
        isCollectingData = false;

        // Log the accumulated sensor data
        console.log("Accumulated Sensor Data: ", sensorDataBuffer);

        // Record the time taken
        const endTime = Date.now();
        const timeTaken = (endTime - startTime) / 1000;
        timeTakenElement.innerHTML = `Time taken to collect 130 samples: ${timeTaken.toFixed(2)} seconds`;

        // Send data to Flask API
        const dataToSend = sensorDataBuffer.slice(0, sequenceLength);
        sensorDataBuffer = [];

        sendDataToFlask(dataToSend);

        // Delay before clearing the buffer and restarting data collection
        setTimeout(() => {
            isCollectingData = true; // Resume data collection after 1 second
        }, 1000); // 1-second delay
    }
}

// Function to send accumulated data to Flask API
async function sendDataToFlask(dataToSend) {
    const flattenedData = dataToSend.flat();

    try {
        const response = await fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                sensor_data: flattenedData
            })
        });

        const data = await response.json();
        if (data.prediction) {
            predictionElement.innerHTML = `Predicted Gesture: ${data.prediction}`;
        } else {
            predictionElement.innerHTML = `Error: ${data.error}`;
        }
    } catch (error) {
        predictionElement.innerHTML = `Error sending data to Flask: ${error.message}`;
    }
}

// Start accumulating sensor data at 50 Hz
setInterval(accumulateSensorData, 20); // Collect data every 20ms (50Hz)
