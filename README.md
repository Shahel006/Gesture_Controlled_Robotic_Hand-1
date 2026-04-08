# Gesture Controlled Robotic Hand

A gesture-controlled robotic hand system that uses MediaPipe for hand tracking, MuJoCo for physics-based simulation, and Arduino for real-time control of robotic movements.

---
🎥 robotic hand demo

![mujoco_1080x608](https://github.com/user-attachments/assets/32693cd3-f3da-4d8d-984d-56c164360f61)

![handmovements_1080x608](https://github.com/user-attachments/assets/b643875a-8f97-447e-89ec-f45bcd9de111)





## 🧠 Overview
This project enables natural human-computer interaction by capturing hand gestures using a webcam and translating them into robotic finger movements.

It integrates:
	•	MediaPipe for hand tracking
	•	MuJoCo for physics-based simulation
	•	Arduino for real-world hardware control

The system evolves from basic gesture detection to a fully simulated robotic hand, with ongoing integration into a physical robotic hand prototype.

---

🎯 Problem Statement

Traditional robotic systems rely on manual controllers or pre-programmed instructions.
This project aims to develop an intuitive, real-time gesture-based control system that allows users to control robotic hands naturally using human gestures.

---
## ⚙️ Technologies Used
- Python  
- OpenCV  
- MediaPipe (Hand Tracking)  
- NumPy  
- Matplotlib (Early Simulation)  
- MuJoCo (Physics-based Robotic Simulation)  
- Computer Vision  
- Robotics Simulation  

---

🔬 Key Features
	•	🎯 Real-time hand gesture tracking
	•	🤖 Joint-level robotic finger control
	•	📐 Accurate angle calculation using kinematics
	•	🎮 Smooth motion using interpolation
	•	🧊 Noise reduction (dead zones + filtering)
	•	⚡ Real-time FPS and performance monitoring
	•	🧩 Modular design (Simulation + Hardware)

  ---

## 🚧 Development Progress

### 🔹 Version 1 – Software Simulation
- Implemented hand tracking using MediaPipe  
- Detected finger states (open/close)  
- Simulated servo movement using variables  
- Displayed real-time values on screen  

---

### 🔹 Version 2 – Gesture Arm Simulation
- Added smooth servo motion using interpolation  
- Mapped gestures to robotic arm movement  
- Visualized robotic arm using Matplotlib  
- Improved realism and responsiveness  

---

### 🔷 Version 3 – Advanced Gesture Control (Kinematics)
- Used vector math to calculate real finger joint angles  
- Implemented input filtering for stability  
- Added deadzone and snap threshold to reduce jitter  
- Improved accuracy and responsiveness  
- Displayed FPS and real-time servo angles  

---

### 🔷 Version 4 – Advanced Hand Tracking (MediaPipe Tasks)
- Switched to MediaPipe Tasks API for improved accuracy  
- Extracted continuous finger measurements (distance and angles)  
- Replaced binary detection with precise gesture tracking  
- Enabled smoother and more stable gesture interpretation  
- Built the foundation for physics-based simulation (MuJoCo)  

---

### 🔷 Version 5 – MuJoCo Physics-Based Simulation
- Integrated MediaPipe Tasks for real-time hand tracking  
- Controlled a MuJoCo robotic hand model using gesture input  
- Implemented joint-level control for each finger  
- Added smoothing for stable and realistic motion  
- Achieved real-time physics-based robotic hand simulation  

---
🤖 Physical Robotic Hand

The robotic hand is implemented using Arduino and servo motors.

<img width="471" height="522" alt="Screenshot 2026-04-08 at 7 44 34 AM" src="https://github.com/user-attachments/assets/6330d6e1-1118-4a4a-a4ec-e96972c22eac" />

🔌 Components
	•	Arduino Nano
	•	Servo Motors
	•	External Power Supply
	•	Jumper Wires
	•	Robotic Hand Structure

⚙️ Working
	•	Arduino controls servos to move fingers
	•	Fingers successfully perform open and close motion
	•	Mechanical system (strings/joints) converts rotation into finger movement
  
---

🤖 MuJoCo Integration
This project uses **MuJoCo (Multi-Joint dynamics with Contact)** for advanced robotic simulation.

- Simulates a realistic robotic hand using physics-based modeling  
- Uses joint control (`data.ctrl`) to move fingers  
- Maps real-time human hand gestures to robotic joints  
- Enables smooth and natural robotic motion  

This moves the project from simple visualization to real-world robotics simulation.

---

 🎯 Simulation Preview
<img width="3840" height="2160" alt="shadow_hand" src="https://github.com/user-attachments/assets/d8606925-f19a-44af-8293-93ce216bfd9d" />

This project includes a real-time simulation where:
- Hand gestures are captured using a webcam  
- Finger movements are mapped to robotic joints  
- The robotic hand moves dynamically based on gestures  
---
📘 Detailed Setup Guide (Step-by-Step)

Follow these steps to run the project from scratch.
🔹 Step 1: Clone the Repository
 -  git clone https://github.com/your-username/gesture-robotic-hand.git
 -  cd gesture-robotic-hand
   
🔹 Step 2: Create Virtual Environment   
 - python -m venv sim_env
   Activate it:
	•	Mac/Linux: source sim_env/bin/activate
	•	Windows: sim_env\Scripts\activate

🔹 Step 3: Install Dependencies
 - pip install opencv-python mediapipe numpy matplotlib mujoco
   
🔹 Step 4: Install MuJoCo (Important)
 - pip install mujoco
 • Test installation: python -c "import mujoco"

🔹 Step 5: Run the Project
 • Run basic hand tracking:
 - python v1_hand_tracking_simulation.py
 • Run gesture simulation:
 - python v2_gesture_arm_simulation.py
 • Run MuJoCo simulation:
 - python v5_mujoco_hand_simulation.py
   
---
🤖 Hardware Setup (Detailed)

🔌 Components Required
	•	Arduino Nano
	•	Servo Motors (SG90 / MG996R)
	•	External Power Supply(5V–6V recommended)
	•	Jumper Wires
	•	Breadboard (optional but recommended)
	•	Buck Converter (DC-DC Step Down Module)
⸻

⚙️ Servo Wiring (Important)

Each servo has 3 wires:

	•	🟤 Brown / Black → GND
	•	🔴 Red → VCC (5V)
	•	🟠 Orange / Yellow → Signal (Control Pin)
	
⸻  

⚙️ What is a Buck Converter?

A buck converter steps down higher voltage (e.g., 9V/12V) to a stable 5V required by servos.

👉 This prevents:

	•	Arduino resets
	•	Servo jitter
	•	Overheating
	
 ⸻   
 
 🔌 Complete Wiring (WITH Buck Converter)

🔹 Step 1: Power Input to Buck Converter
	•	Connect battery/adaptor:
	•	+ (Positive) → IN+ (Buck Converter)
	•	– (Negative) → IN– (Buck Converter)

⸻

🔹 Step 2: Set Output Voltage ⚠️
	•	Adjust potentiometer on buck converter
	•	Use multimeter
	•	Set output to 5V

⸻

🔹 Step 3: Power Servos
	•	Buck Converter OUT+ → All servo Red wires
	•	Buck Converter OUT– → All servo Brown wires

⸻

🔹 Step 4: Connect Arduino
	•	Arduino GND → Buck Converter OUT– (COMMON GROUND)

👉 This step is mandatory

⸻

🔹 Step 5: Signal Connections
	•	Thumb → D3
	•	Index → D5
	•	Middle → D6
	•	Ring → D9
	•	Pinky → D10
  
⸻
⚙️ Step-by-Step Execution
	1.	Connect power source → buck converter input
	2.	Adjust output voltage to 5V
	3.	Connect servos to buck converter output
	4.	Connect Arduino GND to buck converter GND
	5.	Connect servo signals to Arduino pins
	6.	Upload Arduino code
	7.	Test finger movement

⸻

⚠️ Common Mistakes

❌ Not setting buck converter to 5V
👉 Can damage servos

❌ No common ground
👉 Servos won’t respond

❌ Loose connections
👉 Jitter / random movement

❌ Weak power supply
👉 Servos stop or reset
⸻

⚠️ Common Issues & Solutions

❌ Issue: ModuleNotFoundError

Cause: Required Python packages are not installed

Solution:
pip install opencv-python mediapipe numpy matplotlib mujoco
---

❌ Issue: Camera Not Opening

Cause: Webcam not accessible or already in use

Solution:
	•	Check camera permissions
	•	Close other apps using the camera
	•	Try changing camera index:
   cv2.VideoCapture(0)
---
❌ Issue: Hand Not Detected Properly

Cause: Poor lighting or unclear hand position

Solution:
	•	Use good lighting
	•	Keep hand fully visible
	•	Avoid cluttered background

⸻

❌ Issue: MuJoCo Not Running

Cause: Missing dependencies or OpenGL issue
Solution:
pip install mujoco glfw
Mac users:
brew install glfw

⸻

❌ Issue: Low FPS / Lag

Cause: High processing load

Solution:
	•	Reduce camera resolution
	•	Close background apps
	•	Optimize loops in code

⸻

❌ Issue: Servo Not Moving

Cause: Wiring or power issue

Solution:
	•	Check signal pin connections
	•	Use external power supply (NOT Arduino 5V)
	•	Verify Arduino code is uploaded

⸻

❌ Issue: Servo Jitter / Noise

Cause: Unstable power or tight mechanical setup

Solution:
	•	Use stable 5V power (buck converter recommended)
	•	Loosen strings/mechanical tension
	•	Add smoothing in code

⸻

❌ Issue: Wrong Finger Movement

Cause: Incorrect servo mapping

Solution:
	•	Check pin mapping
	•	Adjust angle values in code
	•	Reverse servo direction if needed

⸻

❌ Issue: Arduino Not Detected

Cause: Wrong port or driver issue

Solution:
	•	Select correct COM port in Arduino IDE
	•	Install CH340 driver (if needed)
	•	Reconnect USB cable

⸻

❌ Issue: Serial Communication Not Working

Cause: Port mismatch or baud rate mismatch

Solution:
	•	Match baud rate in both Python and Arduino
	•	Example:serial.Serial('COM3', 9600)
	
❌ Issue: Servos Resetting / Arduino Restarting

Cause: Insufficient power supply

Solution:
	•	Use external power (≥2A recommended)
	•	Do NOT power servos from Arduino

⸻

❌ Issue: Buck Converter Not Working

Cause: Incorrect voltage setting

Solution:
	•	Use multimeter
	•	Adjust output to 5V before connecting servos

⸻

🔮 Next Steps

The following enhancements are planned to further improve the system:
	•	🔌 Real-Time Hardware Integration
Connect gesture input directly with Arduino to achieve live control of individual servo motors
	•	🖐️ Independent Finger Control
Enable precise control of each finger based on real-time gesture angles
	•	🎯 Improved Gesture Accuracy
Enhance tracking stability using advanced filtering and smoothing techniques
	•	🤖 Complete Physical Robotic Hand
Develop a fully functional robotic hand with optimized mechanical design
	•	📡 Wireless Communication (Future Scope)
Implement Bluetooth/WiFi control for untethered operation

⸻

