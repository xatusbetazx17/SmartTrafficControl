 import traci  # SUMO's Python API
import paho.mqtt.client as mqtt
import requests

# Constants
MQTT_BROKER = "test.mosquitto.org"
TOPIC = "traffic/priority"
OPENWEATHER_API_KEY = "your_openweather_api_key"
CITY = "New York"

# Initialize MQTT Client
client = mqtt.Client("TrafficSystem")
client.connect(MQTT_BROKER)

# Function to get weather data
def get_weather_data():
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={OPENWEATHER_API_KEY}"
    response = requests.get(weather_url).json()
    return response['weather'][0]['main']

# Priority Management based on Weather and Vehicle Type
def manage_traffic(vehicle_type, weather):
    if vehicle_type == 'emergency':
        decision = 'Priority to Emergency Vehicle'
    elif weather in ['Fog', 'Rain']:
        decision = 'Extend Green Light Due to Bad Weather'
    else:
        decision = 'Normal Traffic Flow'
    return decision

# Main control loop for SUMO simulation
def control_traffic_system():
    traci.start(["sumo", "-c", "sumo_config.sumocfg"])

    while traci.simulation.getMinExpectedNumber() > 0:
        # Get current weather
        weather = get_weather_data()

        # Check if emergency vehicle is present
        for veh_id in traci.vehicle.getIDList():
            vehicle_type = traci.vehicle.getTypeID(veh_id)
            pedestrians_nearby = traci.person.getIDCount() > 0

            # Make traffic management decision
            decision = manage_traffic(vehicle_type, weather)

            # Send decision via MQTT
            client.publish(TOPIC, decision)

            # Adjust traffic lights (using SUMO's traffic light logic)
            if decision == 'Priority to Emergency Vehicle':
                traci.trafficlight.setPhase("1", 0)  # Green light for emergency
            elif pedestrians_nearby:
                traci.trafficlight.setPhase("1", 2)  # Give priority to pedestrians
            else:
                traci.trafficlight.setPhase("1", 1)  # Normal flow

        traci.simulationStep()

    traci.close()

# Run the traffic control system
if __name__ == "__main__":
    control_traffic_system()

