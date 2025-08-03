import json
import random
from datetime import datetime, timedelta

# --- Configuration: Lists of possible values ---
LOCATIONS = [
    "living_room", "kitchen", "main_bedroom", "guest_bedroom", 
    "bathroom", "home_office", "garage", "outside_patio", "hallway"
]
USERS = ["owner", "guest", "teenager", "child"]

# --- Scenario Generation Functions ---
# Each function creates a dictionary for a specific, logical scenario.

def create_security_alert_scenario(timestamp):
    """Scenario: Motion is detected when no one is supposed to be home."""
    location = random.choice(LOCATIONS)
    return {
        "input": {
            "timestamp": timestamp,
            "sensors": [
                {"type": "motion", "location": location, "status": "detected"},
                {"type": "system_mode", "status": "away"},
                {"type": "light", "location": location, "level_lux": random.randint(1, 15)}
            ]
        },
        "output": {
            "action": "trigger_security_alarm; turn_on_all_lights(); send_push_notification()",
            "notification": f"SECURITY ALERT: Motion detected in the {location.replace('_', ' ')} while the system is in Away Mode.",
            "log": "Potential intrusion detected. High priority."
        }
    }

def create_welcome_home_scenario(timestamp):
    """Scenario: The owner is approaching home, so the house prepares for their arrival."""
    user = "owner"
    temp_preference = random.randint(20, 22)
    return {
        "input": {
            "timestamp": timestamp,
            "sensors": [
                {"type": "gps", "user": user, "status": "approaching_home", "distance_meters": random.randint(100, 500)},
                {"type": "temperature", "location": "living_room", "value_celsius": 18}
            ]
        },
        "output": {
            "action": f"adjust_hvac('heat', {temp_preference}); turn_on_light('hallway')",
            "notification": f"Welcome home, {user}! Preparing the house for your arrival.",
            "log": "Geofence triggered for user arrival. Adjusting climate."
        }
    }

def create_lights_on_convenience_scenario(timestamp):
    """Scenario: Someone enters a dark room, so the lights turn on."""
    location = random.choice(["living_room", "kitchen", "home_office", "hallway"])
    return {
        "input": {
            "timestamp": timestamp,
            "sensors": [
                {"type": "motion", "location": location, "status": "detected"},
                {"type": "light", "location": location, "level_lux": random.randint(1, 20)},
                {"type": "system_mode", "status": "home"}
            ]
        },
        "output": {
            "action": f"set_light_brightness('{location}', {random.randint(70, 90)})",
            "notification": f"Turning on the {location.replace('_', ' ')} lights.",
            "log": "Automated lighting for convenience."
        }
    }

def create_energy_saving_window_open_scenario(timestamp):
    """Scenario: A window is opened while the HVAC is running."""
    location = random.choice(["living_room", "main_bedroom", "kitchen"])
    hvac_mode = random.choice(["heat", "cool"])
    return {
        "input": {
            "timestamp": timestamp,
            "sensors": [
                {"type": "window", "location": location, "status": "opened"},
                {"type": "hvac", "status": hvac_mode}
            ]
        },
        "output": {
            "action": f"adjust_hvac('pause', '{location}_zone')",
            "notification": f"{location.replace('_', ' ').capitalize()} window is open. Pausing HVAC to save energy.",
            "log": "Energy saving: HVAC paused due to open window."
        }
    }

def create_water_leak_scenario(timestamp):
    """Scenario: A water leak is detected."""
    location = random.choice(["bathroom", "laundry_room", "kitchen"])
    return {
        "input": {
            "timestamp": timestamp,
            "sensors": [
                {"type": "water_leak", "location": location, "status": "detected"}
            ]
        },
        "output": {
            "action": "shutoff_main_water_valve(); send_push_notification()",
            "notification": f"CRITICAL LEAK: Water detected in the {location.replace('_', ' ')}! Main water valve has been shut off.",
            "log": "Water leak detected and mitigated. Urgent."
        }
    }
    
def create_bedtime_scenario(timestamp):
    """Scenario: The user gets into bed, triggering the 'good night' routine."""
    return {
        "input": {
            "timestamp": timestamp,
            "sensors": [
                {"type": "bed_occupancy", "location": "main_bedroom", "status": "occupied"},
                {"type": "light", "location": "main_bedroom", "status": "on"}
            ]
        },
        "output": {
            "action": "set_light_brightness('main_bedroom', 5); close_blinds(); set_system_mode('night')",
            "notification": "Good night! Setting the room to sleep mode.",
            "log": "Bedtime routine initiated by occupancy sensor."
        }
    }

def create_air_quality_scenario(timestamp):
    """Scenario: Air quality drops, triggering the air purifier."""
    location = random.choice(["home_office", "living_room", "main_bedroom"])
    return {
        "input": {
            "timestamp": timestamp,
            "sensors": [
                {"type": "air_quality", "location": location, "voc_level": "high", "value_ppm": random.randint(3, 8)}
            ]
        },
        "output": {
            "action": f"turn_on_device('air_purifier', '{location}')",
            "notification": f"Air quality in the {location.replace('_', ' ')} is poor. Starting the air purifier.",
            "log": "Environmental control: Air purifier activated."
        }
    }

def create_fire_alert_scenario(timestamp):
    """Scenario: Smoke is detected."""
    location = random.choice(["kitchen", "hallway", "garage"])
    return {
        "input": {
            "timestamp": timestamp,
            "sensors": [
                {"type": "smoke", "location": location, "status": "detected"},
                {"type": "carbon_monoxide", "location": location, "level_ppm": random.randint(15, 50)}
            ]
        },
        "output": {
            "action": "trigger_fire_alarm; call_emergency_services(); shutoff_hvac()",
            "notification": f"EMERGENCY: Smoke detected in the {location.replace('_', ' ')}! Authorities have been notified.",
            "log": "CRITICAL: Fire event detected. Emergency protocols activated."
        }
    }

def create_no_action_scenario(timestamp):
    """Scenario: Normal, everyday events that require no special action."""
    location = random.choice(LOCATIONS)
    return {
        "input": {
            "timestamp": timestamp,
            "sensors": [
                {"type": "door", "location": "front_door", "status": "closed"},
                {"type": "system_mode", "status": "home"},
                {"type": "temperature", "location": location, "value_celsius": 21.5}
            ]
        },
        "output": {
            "action": "none",
            "notification": "System nominal. All sensors reporting normal status.",
            "log": "Standard system check. No action required."
        }
    }


# --- Main Generator Function ---

def generate_smart_home_data(amount):
    """
    Generates a specified amount of synthetic smart home sensor data.

    Args:
        amount (int): The number of data entries to generate.

    Returns:
        dict: A dictionary containing the list of training data, ready for JSON conversion.
    """
    # List of all possible scenario-generating functions
    scenario_functions = [
        create_security_alert_scenario,
        create_welcome_home_scenario,
        create_lights_on_convenience_scenario,
        create_energy_saving_window_open_scenario,
        create_water_leak_scenario,
        create_bedtime_scenario,
        create_air_quality_scenario,
        create_fire_alert_scenario,
        create_no_action_scenario 
    ]
    
    training_data = []
    current_time = datetime.now()

    for _ in range(amount):
        # Choose a random scenario function to execute
        chosen_scenario_function = random.choice(scenario_functions)
        
        # Generate the data for that scenario
        # We pass the current time to be used in the data point
        iso_timestamp = current_time.isoformat() + "Z"
        data_entry = chosen_scenario_function(iso_timestamp)
        
        training_data.append(data_entry)
        
        # Increment time by a random amount for the next event
        current_time += timedelta(minutes=random.randint(1, 180), seconds=random.randint(0, 59))

    return {"training_data": training_data}


# --- Main execution block ---
if __name__ == "__main__":
    # <<-- SET YOUR DESIRED DATA AMOUNT HERE -->>
    DATA_AMOUNT_X = 100

    print(f"Generating {DATA_AMOUNT_X} random sensor data entries...")
    
    # Generate the data
    generated_data = generate_smart_home_data(DATA_AMOUNT_X)
    
    # Convert the Python dictionary to a JSON formatted string for output
    json_output = json.dumps(generated_data, indent=2)
    
    # Print the JSON to the console
    print(json_output)
    
    # Optionally, save to a file
    file_name = f"smart_home_training_data_{DATA_AMOUNT_X}.json"
    with open(file_name, "w") as f:
        f.write(json_output)
    
    print(f"\nData successfully generated and saved to '{file_name}'")