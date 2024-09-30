import os
import subprocess
import sys
import requests
import traci  # SUMO TraCI module for Python
import cv2
import time
from playsound import playsound

# Paths to sound files (adjust these paths to where your sound files are stored)
green_light_sound = "green_sound.mp3"
red_light_sound = "red_sound.mp3"
yellow_light_sound = "yellow_sound.mp3"

# Function to install missing Python packages
def install_python_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Function to ensure Python dependencies are installed
def check_and_install_dependencies():
    print("Checking and installing Python dependencies...")

    # List of required Python packages
    python_packages = ["requests", "traci", "opencv-python", "playsound"]

    for package in python_packages:
        try:
            __import__(package)
            print(f"{package} is already installed.")
        except ImportError:
            print(f"{package} is missing. Installing...")
            install_python_package(package)

# Function to detect the Linux distribution and install system dependencies
def install_system_dependencies():
    print("Installing necessary system packages...")

    if os.name == 'nt':  # Windows
        print("Windows detected. Skipping system-level package installation.")
        return

    # Detect the Linux distribution
    if os.path.exists('/etc/os-release'):
        with open('/etc/os-release') as f:
            distro = f.read().split('=')[1].strip()

    # Install necessary system packages based on the Linux distribution
    try:
        if "ubuntu" in distro or "debian" in distro:
            subprocess.run(["sudo", "apt", "update"], check=True)
            subprocess.run(["sudo", "apt", "install", "-y", "curl", "jq", "fswebcam"], check=True)
        elif "arch" in distro or "manjaro" in distro or "steamos" in distro:
            subprocess.run(["sudo", "pacman", "-S", "--noconfirm", "curl", "jq", "fswebcam"], check=True)
        elif "fedora" in distro:
            subprocess.run(["sudo", "dnf", "install", "-y", "curl", "jq", "fswebcam"], check=True)
        else:
            print(f"Unsupported Linux distribution: {distro}")
            return
        print("System dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing system dependencies: {e}")

# Function to check if SUMO is installed
def check_sumo_installation():
    try:
        subprocess.run(["sumo", "-h"], check=True)
        print("SUMO is already installed.")
    except subprocess.CalledProcessError:
        print("SUMO is not installed or not in the PATH. Please install SUMO manually.")
        sys.exit(1)

# Main function to set up the environment and run the traffic control system
def setup_environment():
    print("Setting up environment...")
    
    # Check and install Python dependencies
    check_and_install_dependencies()

    # Check and install system dependencies
    install_system_dependencies()

    # Check if SUMO is installed
    check_sumo_installation()

    print("Environment setup complete.")

# 1. Generate the network file using netconvert
def generate_network():
    print("Generating network...")
    nodes_xml = '''<nodes>
    <node id="1" x="0" y="0"/>
    <node id="2" x="100" y="0"/>
</nodes>'''

    edges_xml = '''<edges>
    <edge id="e1" from="1" to="2" priority="1"/>
    <edge id="e2" from="2" to="1" priority="1"/>
</edges>'''

    # Write node and edge files
    with open("my_nodes.nod.xml", "w") as f:
        f.write(nodes_xml)
    with open("my_edges.edg.xml", "w") as f:
        f.write(edges_xml)

    # Generate network using netconvert
    result = subprocess.run([
        "netconvert",
        "--node-files", "my_nodes.nod.xml",
        "--edge-files", "my_edges.edg.xml",
        "-o", "my_network.net.xml"
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error generating network: {result.stderr}")
        raise Exception(f"Network generation failed: {result.stderr}")
    else:
        print("Network generated!")

# 2. Generate the vehicle routes based on selected scenario
def generate_routes(scenario):
    print(f"Generating vehicle routes for scenario: {scenario}")
    random_trips_path = os.path.join(os.environ.get("SUMO_HOME"), "tools", "randomTrips.py")
    if not os.path.exists(random_trips_path):
        raise FileNotFoundError(f"randomTrips.py not found at {random_trips_path}. Check your SUMO installation.")

    if scenario == "best":
        number_of_vehicles = 200
    elif scenario == "medium":
        number_of_vehicles = 500
    else:  # Worst case scenario
        number_of_vehicles = 1000

    result = subprocess.run([
        "python", random_trips_path,
        "-n", "my_network.net.xml", 
        "-o", "routes.rou.xml", 
        "--trip-attributes", 'type="car"', 
        "--end", "3600",
        "--number", str(number_of_vehicles)
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error generating routes: {result.stderr}")
        raise Exception(f"Route generation failed: {result.stderr}")
    else:
        print(f"Routes generated for {scenario} scenario!")

# 3. Run SUMO and control traffic lights based on weather, scenario, and camera detection
def run_sumo(scenario):
    print("Starting SUMO simulation...")
    sumo_binary = "sumo-gui"  # or use "sumo" if you don’t need GUI
    sumo_cmd = [sumo_binary, "-c", "sumo_config.sumocfg", "--log", "sumo.log"]

    try:
        traci.start(sumo_cmd)
        print("SUMO started successfully.")
    except Exception as e:
        print(f"Error starting SUMO: {e}")
        sys.exit(1)

    try:
        # Simulate indefinitely until user stops
        step = 0
        while True:
            traci.simulationStep()
            step += 1
            time.sleep(0.1)  # Add a small sleep for better performance monitoring
            if step % 100 == 0:
                print(f"Simulation running... step: {step}")
    
    except KeyboardInterrupt:
        print("Simulation interrupted by user.")

    finally:
        # Ensure the simulation is closed correctly after user interrupts or an error occurs
        traci.close()
        print(f"Simulation completed at step: {step}")

# 4. Create the SUMO configuration file
def create_sumo_config():
    print("Creating SUMO configuration file...")
    sumo_config = '''<configuration>
    <input>
        <net-file value="my_network.net.xml"/>
        <route-files value="routes.rou.xml"/>
    </input>
    <time>
        <begin value="0"/>
        <end value="3600"/>
    </time>
</configuration>'''
    
    with open("sumo_config.sumocfg", "w") as f:
        f.write(sumo_config)
    print("SUMO configuration file created!")

# Main function to run the whole process
def main():
    print("Starting the Smart Traffic Control system...")

    try:
        # Step 1: Set up environment and check/install dependencies
        setup_environment()

        # Step 2: Generate network and vehicle routes
        scenario = input("Select scenario (best, medium, worst): ").strip().lower()
        if scenario not in ["best", "medium", "worst"]:
            raise ValueError("Invalid scenario selected!")
        generate_network()  # Generate the network
        generate_routes(scenario)  # Generate the vehicle routes

        # Step 3: Create the SUMO configuration and run the simulation
        create_sumo_config()
        run_sumo(scenario)  # Run the SUMO simulation

    except Exception as e:
        print(f"Error: {e}")
    
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
