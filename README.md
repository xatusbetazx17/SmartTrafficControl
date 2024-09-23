# SmartTrafficControl



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
