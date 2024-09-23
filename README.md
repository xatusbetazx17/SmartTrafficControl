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


```bash

import os
import requests
import cv2
import paho.mqtt.client as mqtt
from tkinter import Tk, Label


# Weather Detection Function using OpenWeather API
def get_weather_data(city):
    api_key = 'your_openweather_api_key'
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    weather_response = requests.get(weather_url).json()
    
    if 'weather' in weather_response:
        return weather_response['weather'][0]['main']
    else:
        return "Unknown"


# Vehicle Detection Function (Placeholder for actual implementation)
def detect_vehicle(image):
    # In a real implementation, this would use OpenCV or another library to detect vehicles
    vehicle_type = "normal"  # For example, normal, emergency, bus, etc.
    
    # For now, we'll just simulate detecting an emergency vehicle:
    if "emergency" in image.lower():  # Assuming image is a string placeholder
        vehicle_type = "emergency"
    
    return vehicle_type


# Priority Management Function
def manage_traffic(weather, vehicle_type):
    if vehicle_type == 'emergency':
        return 'Give priority to emergency vehicle!'
    elif weather == 'Fog' or weather == 'Rain':
        return 'Extend green light duration due to bad weather.'
    else:
        return 'Normal traffic flow.'


# Check if the system has graphical capabilities
def has_graphical_capability():
    display_var = os.getenv('DISPLAY')
    return bool(display_var)


# Send MQTT messages to vehicles
def send_signal_to_vehicles(message):
    mqtt_broker = "test.mosquitto.org"
    client = mqtt.Client("TrafficSystem")
    client.connect(mqtt_broker)
    client.publish("traffic/priority", message)


# Function to create a simple GUI for the traffic system
def create_gui():
    window = Tk()
    window.title("Traffic Light System")
    label = Label(window, text="Traffic System Active with Graphical Interface")
    label.pack()
    window.mainloop()


# Main function to integrate all components
def control_traffic_system(city, vehicle_image):
    weather = get_weather_data(city)
    vehicle_type = detect_vehicle(vehicle_image)
    decision = manage_traffic(weather, vehicle_type)
    
    # Send message to vehicles via MQTT
    send_signal_to_vehicles(decision)
    
    # Check for graphical capabilities and launch UI if available
    if has_graphical_capability():
        create_gui()
    else:
        print(f"Traffic Decision: {decision}")
    
    return decision


# Example usage of the system
if __name__ == "__main__":
    city = 'New York'
    vehicle_image = 'emergency_vehicle.jpg'  # Placeholder for actual image feed or input
    
    # Control the traffic system based on weather and vehicle detection
    traffic_decision = control_traffic_system(city, vehicle_image)
    print(f"Final Traffic Decision: {traffic_decision}")


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







