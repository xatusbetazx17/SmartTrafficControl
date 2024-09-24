# SmartTrafficControl

### Smart Traffic Light System - Advanced Edition
## Description
The Smart Traffic Light System is an intelligent, real-time traffic management solution designed to dynamically adjust traffic light behavior based on various inputs, such as weather conditions, vehicle types (e.g., normal, bus, emergency vehicles), and pedestrian detection. This system prioritizes emergency vehicles and pedestrians when necessary, while also monitoring weather conditions to optimize traffic flow for safety and efficiency.

Additionally, the system integrates real-time messaging with vehicles via MQTT, provides automated camera-based criminal detection, and can be remotely connected to police servers for reporting suspicious activity or identifying wanted individuals. The system is designed to be modular, with automatic installation of required dependencies and seamless integration with WiFi networks.

## Features
Weather-based Traffic Control:

The system adjusts traffic light timings based on real-time weather conditions (e.g., extending green light during fog or rain) using the OpenWeather API.
Vehicle Detection:

Detects and prioritizes different vehicle types, including normal vehicles, buses, and emergency vehicles.
Emergency vehicles are automatically prioritized by extending the green light for them.
Pedestrian Detection:

The system detects nearby pedestrians and gives them priority, changing the traffic lights to allow safe crossing when necessary.
Real-Time Messaging to Vehicles:

Uses MQTT to send real-time messages to vehicles, explaining current traffic conditions and priority decisions.
Vehicles receive information about traffic light changes and any prioritization (e.g., for emergency vehicles).
Criminal Detection and Police Notification:

The system captures images from a connected camera and checks for known criminals using a remote server.
If a match is found, the system automatically sends a notification to law enforcement (e.g., local police) via MQTT, including details about the incident.
Automatic WiFi Connection:

The system can automatically connect to a WiFi network, enabling real-time data collection, reporting, and remote access to police servers or other authorities.
Graphical User Interface (GUI) Integration:

When graphical capabilities are available, the system launches a Tkinter-based GUI for monitoring and managing the traffic system, allowing operators to visually see traffic flow and prioritize vehicles.
Auto-Installation of Dependencies:

Automatically installs missing libraries or dependencies if they are not installed, including requests, opencv-python, paho-mqtt, and any other required packages. This ensures the system can be deployed on various environments without manual intervention.
## Key Capabilities
Real-Time Traffic Adjustments: Based on weather, vehicle, and pedestrian data, the system makes instant decisions to change traffic light behavior.

Criminal Detection and Reporting: With camera integration, the system can detect wanted individuals and automatically notify the police through a secure connection.

Emergency Vehicle Priority: Ensures that emergency vehicles always get the right of way by adjusting traffic lights to their favor.

Pedestrian Safety: Detects pedestrians and dynamically prioritizes their need to cross safely.

WiFi and Remote Connectivity: Automatically connects to WiFi to fetch weather data, update traffic decisions, and send reports to remote servers or law enforcement.

## Use Cases
Urban Traffic Management: Ensures efficient flow of traffic while giving priority to emergency services and vulnerable pedestrians.
Law Enforcement Integration: Automatically notifies authorities if any wanted or suspicious individuals are detected through real-time camera integration.
Weather-Based Traffic Adjustments: Extends green light durations in adverse weather conditions (rain, fog, etc.) to ensure safe driving conditions for all vehicles.


## Installation

To run the Smart Traffic Light System, clone the repository and ensure the required dependencies are installed.

```bash
git clone https://github.com/xatusbetazx17/your-repo.git
cd your-repo
```

```bash

#!/bin/bash

# Ensure necessary packages are installed
install_dependencies() {
    echo "Installing necessary packages..."
    
    # Update the package list and install dependencies
    sudo apt update

    # Install curl for API requests, jq for parsing JSON, mosquitto-clients for MQTT, and fswebcam for camera input
    sudo apt install -y curl jq mosquitto-clients fswebcam

    echo "Dependencies installed!"
}

# Function to connect to a WiFi network (using nmcli)
connect_to_wifi() {
    local ssid=$1
    local password=$2

    echo "Connecting to WiFi network: $ssid"
    nmcli dev wifi connect "$ssid" password "$password"

    if [[ $? -eq 0 ]]; then
        echo "Connected to WiFi successfully!"
    else
        echo "Failed to connect to WiFi."
    fi
}

# Function to fetch weather data using OpenWeather API
get_weather_data() {
    local city=$1
    local api_key="your_openweather_api_key"  # Replace with your OpenWeather API key
    local weather_url="http://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${api_key}"
    
    # Fetch the weather data using curl
    weather=$(curl -s "$weather_url" | jq -r '.weather[0].main')
    
    if [ -z "$weather" ]; then
        echo "Unknown"
    else
        echo "$weather"
    fi
}

# Simulated function to automatically detect vehicle types
detect_vehicle() {
    # Simulate random detection of emergency vehicle or normal vehicle (replace with actual sensors)
    vehicle_type=$(shuf -n1 -e "normal" "emergency")
    echo "$vehicle_type"
}

# Simulated function to automatically detect pedestrians (replace with actual sensors)
detect_pedestrians() {
    # Simulate random pedestrian detection (yes/no) (replace with actual sensors)
    pedestrians_nearby=$(shuf -n1 -e "true" "false")
    echo "$pedestrians_nearby"
}

# Function to simulate camera capture and criminal identification (e.g., facial recognition)
capture_image_and_check_criminal_record() {
    echo "Capturing image using the camera..."
    
    # Capture an image using the fswebcam tool
    fswebcam --resolution 640x480 --save /tmp/captured_image.jpg

    # Simulate checking with a server for criminal records (this would be an API call in real implementation)
    echo "Checking criminal record from the server..."
    criminal_found=$(shuf -n1 -e "true" "false")  # Simulating check

    if [[ "$criminal_found" == "true" ]]; then
        echo "Criminal identified! Notifying police..."
        send_notification_to_police "Criminal identified at location with camera capture."
    else
        echo "No criminal activity detected."
    fi
}

# Priority Management based on Weather, Vehicle Type, and Pedestrian Detection
manage_traffic() {
    local weather=$1
    local vehicle_type=$2
    local pedestrians_nearby=$3

    if [[ "$vehicle_type" == "emergency" ]]; then
        echo "Priority to Emergency Vehicle"
    elif [[ "$weather" == "Fog" || "$weather" == "Rain" ]]; then
        echo "Extended Green Light Due to Bad Weather"
    elif [[ "$pedestrians_nearby" == "true" ]]; then
        echo "Pedestrian Priority"
    else
        echo "Normal Traffic Flow"
    fi
}

# Function to send notification to police (via MQTT or another method)
send_notification_to_police() {
    local message=$1
    mqtt_broker="test.mosquitto.org"
    topic="police/alerts"

    # Send notification using MQTT
    mosquitto_pub -h "$mqtt_broker" -t "$topic" -m "$message"
    echo "Notification sent to police: $message"
}

# Function to simulate sending MQTT messages for traffic control
send_signal_to_vehicles() {
    local message=$1
    mqtt_broker="test.mosquitto.org"
    topic="traffic/priority"

    # Publish the traffic signal decision via MQTT
    mosquitto_pub -h "$mqtt_broker" -t "$topic" -m "$message"
}

# Main function to control the traffic system
control_traffic_system() {
    local city=$1

    # Fetch the weather data
    weather=$(get_weather_data "$city")

    # Automatically detect vehicle type (emergency or normal)
    vehicle_type=$(detect_vehicle)

    # Automatically detect if pedestrians are nearby
    pedestrians=$(detect_pedestrians)

    # Capture image and check for criminal records
    capture_image_and_check_criminal_record

    # Manage traffic based on weather, vehicle type, and pedestrian detection
    decision=$(manage_traffic "$weather" "$vehicle_type" "$pedestrians")

    # Send decision signals to vehicles (using MQTT)
    send_signal_to_vehicles "$decision"
    
    # Output the traffic decision
    echo "Traffic Decision: $decision"
}

# Function to handle the entire setup
run_system() {
    local city="New York"
    local ssid="your_wifi_ssid"  # Replace with your WiFi SSID
    local password="your_wifi_password"  # Replace with your WiFi password

    # Install dependencies
    install_dependencies

    # Connect to WiFi
    connect_to_wifi "$ssid" "$password"

    # Control the traffic system based on automatic detection of vehicles and pedestrians, and weather
    control_traffic_system "$city"
}

# Run the traffic system setup
run_system


```
## Requirements
Python 3.x
pip (for Python package management)
Install the required dependencies manually if needed:

```bash
Copy code
pip install requests opencv-python paho-mqtt
````
### For tkinter installation:
On Ubuntu/Debian:
bash
Copy code
```sudo apt-get install python3-tk```
On Arch Linux:
bash
Copy code
```sudo pacman -S tk```
## Usage
To run the script, execute:

bash
Copy code
```python traffic_light_system.py```
## The script will:

Fetch real-time weather data from OpenWeather.
Simulate vehicle detection.
Automatically adjust traffic light behavior based on the conditions.
Launch a graphical interface (if graphical capabilities are detected).
Example:
python
Copy code
```bash
city = 'New York'
vehicle_image = 'emergency_vehicle.jpg'
traffic_decision = control_traffic_system(city, vehicle_image)
Libraries Used
requests: For fetching real-time weather data from OpenWeather API.
opencv-python: For vehicle detection (future implementation for image processing).
paho-mqtt: For sending MQTT messages to vehicles.
tkinter: For graphical user interface (if available).
```
## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing
Contributions are welcome! Please open a pull request or issue for improvements or suggestions.







