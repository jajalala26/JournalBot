let currentState = 'Idle';
let collisionDetected = false; // Flag to track collision
let messageSpoken = false; // Flag to track if the message has been spoken
let gyroMaxTriggered = false; // Flag to track if gyromax has been triggered
let landingDetected = false; 

async function idle() {
    if (!messageSpoken) {
        await speak("Give me a whirl");
        messageSpoken = true; // Set the flag to true after speaking
    }

    // Set LED effects while in idle state
    setMainLed({ r: 0, g: 255, b: 0 }); // Set LED to green
    await delay(0.5); // Delay for half a second
    setMainLed({ r: 0, g: 0, b: 0 }); // Turn off LED
    await delay(0.5); // Delay for half a second
}

async function movingForward() {
    collisionDetected = false; // Reset the collision flag
    await roll(0, 100, 2); // Roll forward at speed 100 for 2 seconds
}

async function handleCollision() {
    stopRoll();
    setMainLed({ r: 255, g: 0, b: 0 });
    await speak("Collision detected!", false);
    await roll((getHeading() + 180) % 360, 100, 2); // Reverse direction
    setMainLed({ r: 255, g: 22, b: 255 });
    collisionDetected = true; // Set the collision flag
}

async function turning() {
    await roll((getHeading() + 90) % 360, 100, 1); // Fixed turn to the right
}

async function finalState() {
    stopRoll(); // Stop any movement
    setMainLed({ r: 255, g: 0, b: 0 }); // Change LED to indicate final state
    await speak("Stopping now."); // Announce stopping
}

async function onGyroMax() {
    setMainLed({ r: 255, g: 0, b: 0 }); // Change LED to red
    await speak("gyromax", true); // Speak "gyromax"
    gyroMaxTriggered = true; // Set the flag to indicate gyromax has been triggered
}

registerEvent(EventType.onGyroMax, onGyroMax);

async function onLanding() {
    setMainLed({ r: 0, g: 255, b: 0 });
    await speak("landing", false);
    await delay(0.5);
    landingDetected = true; // Set landing detected flag
}

registerEvent(EventType.onLanding, onLanding);

async function lookupNextState() {
    switch (currentState) {
        case 'Idle':
            return gyroMaxTriggered ? 'Moving Forward' : 'Idle'; // Transition to Moving Forward if gyromax is triggered
        case 'Moving Forward':
            return collisionDetected ? 'Collision Detected' : 'Moving Forward';
        case 'Collision Detected':
            return landingDetected ? 'Final State' : 'Turning'; // Go to Final State if landing detected
        case 'Turning':
            return 'Moving Forward'; // Go back to Moving Forward after turning
        case 'Final State':
            return 'Final State'; // No transitions needed here
        default:
            return 'Idle'; // Fallback to Idle
    }
}

// Function mapping
const stateFunctions = {
    'Idle': idle,
    'Moving Forward': movingForward,
    'Collision Detected': handleCollision,
    'Turning': turning,
    'Final State': finalState,
};

async function run() {
    while (currentState !== 'Final State') {
        await stateFunctions[currentState](); // Call the state function using the mapping
        currentState = await lookupNextState(); // Update current state based on conditions
    }
    await finalState(); // Final state behavior after exiting loop
}

// Register collision event
registerEvent(EventType.onCollision, handleCollision);

// Start the program
async function startProgram() {
    currentState = 'Idle'; // Initialize to Idle state
    await run(); // Start the state machine loop
}

// Call startProgram to initiate the behavior
startProgram();
