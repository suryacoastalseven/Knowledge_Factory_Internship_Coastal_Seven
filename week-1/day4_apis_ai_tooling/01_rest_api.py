# 01_rest_api.py
import requests

def fetch_random_joke():
    """Fetches a random programming joke from a public REST API using GET method."""
    url = "https://official-joke-api.appspot.com/jokes/programming/random"
    
    try:
        print("Calling API... ⏳")
        # Timeout పెట్టడం అనేది ఒక 'Topper' లక్షణం. సర్వర్ రెస్పాండ్ అవ్వకపోతే ఆగిపోదు.
        response = requests.get(url, timeout=5)
        
        # ఇది HTTP Status Code 200 (Success) కాకపోతే ఎర్రర్ త్రో చేస్తుంది
        response.raise_for_status() 
        
        # API ఇచ్చిన JSON డేటాని పైథాన్ డిక్షనరీ లాగా మారుస్తుంది
        data = response.json()
        
        if data:
            joke = data[0]
            print("\n✅ API Success! Here is the data:")
            print(f"Setup: {joke['setup']}")
            print(f"Punchline: {joke['punchline']}")
            return joke
            
    except requests.exceptions.Timeout:
        print("❌ Error: API request timed out.")
    except requests.exceptions.HTTPError as err:
        print(f"❌ HTTP Error occurred: {err}")
    except requests.exceptions.RequestException as err:
        print(f"❌ Connection Error: {err}")

# రన్ చేసి చూడు
fetch_random_joke()