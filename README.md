# SmartTrafficControl

## Description

This project is a **Smart Traffic Light System** that dynamically manages traffic based on real-time conditions such as **weather** and **vehicle types** (including emergency vehicles). The system prioritizes certain vehicles (e.g., emergency vehicles) and adjusts traffic light timings according to weather conditions, providing a modern, intelligent solution for traffic management.

The system can:
- **Detect weather conditions** using the OpenWeather API.
- **Detect vehicle types**, including normal, bus, and emergency vehicles (using OpenCV).
- **Prioritize emergency vehicles**, extending green light time for them.
- **Send real-time MQTT messages** to vehicles, explaining the current traffic situation.
- **Launch a graphical user interface (GUI)** (if available) for monitoring the system.
- **Install required libraries automatically** if they are missing.

## Features
- **Weather-based Traffic Control**: Adjust traffic light timing based on real-time weather (e.g., extending green light during fog or rain).
- **Vehicle Detection**: Simulates detection of different vehicle types with the option to prioritize emergency vehicles.
- **Real-Time Messaging**: Uses MQTT to send priority messages to connected vehicles.
- **GUI Integration**: Provides a graphical user interface when the system detects available graphical capabilities (using `Tkinter`).
- **Auto-Installation of Libraries**: Automatically installs missing Python libraries (`requests`, `opencv-python`, `paho-mqtt`) if they are not installed.

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







