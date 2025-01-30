import config
import requests
import json

headers = {
    'X-Access-Token': config.TOKEN
}

def golemio_get_data():

    print("Connecting...")

    try:
        # Assemble query
        query=""
        for stop in config.STOPS:
           query += "ids[]="+stop["id"]+"&"
        query += "limit="+str(config.QUERY_LIMIT)

        # Send the request
        response = requests.get('https://api.golemio.cz/v2/pid/departureboards?'+query, headers=headers, timeout=10)

        # Check if the request was successful
        if response.status_code == 200:

              # Parse the JSON response into a dictionary
              data = response.json()

              response.close()
              return True, data
        else:
              response.close()
              print(f"Failed to retrieve data: {response.status_code}")
              return False, "Failed to retrieve data:\n{response.status_code}"

    except Exception as error:
        print("An exception occurred:", error, type(error).__name__)
        return False, str(error) + "\n" + type(error).__name__
 

