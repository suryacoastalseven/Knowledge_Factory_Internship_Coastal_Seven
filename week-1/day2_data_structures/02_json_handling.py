# 02_json_handling.py
import json
import os

def process_json_file():
    input_file = 'sample.json'
    output_file = 'updated_sample.json'

    # Day-1 లో నేర్చుకున్న Error Handling ఇక్కడ వాడుతున్నాం
    try:
        # 1. Reading JSON file
        with open(input_file, 'r') as file:
            data = json.load(file)
            print("--- Original JSON Data ---")
            print(data)
        
        # 2. Modifying the data (Adding a new key-value pair)
        data['status'] = 'completed'
        data['team_members'].append("Priya") # Adding new member to the list
        
        # 3. Writing back to a new JSON file
        with open(output_file, 'w') as file:
            # indent=4 వాడితే JSON ఫైల్ నీట్ గా ఫార్మాట్ అవుతుంది
            json.dump(data, file, indent=4)
            print(f"\nSuccessfully modified and saved to {output_file}")

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except json.JSONDecodeError:
        print("Error: The file does not contain valid JSON.")

process_json_file()