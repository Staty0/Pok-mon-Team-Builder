import requests
import time

class ApiAccess:
    BASE_URL = "https://smogonapi.herokuapp.com/"
    MAX_RETRIES = 4

    def __init__(self):
        pass

    def make_request(self, endpoint):
        for attempt in range(self.MAX_RETRIES):
            response = requests.get(endpoint)

            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error on attempt {attempt + 1}: {response.status_code}")
                if attempt < self.MAX_RETRIES - 1:
                    # Increase delay between retries (e.g., exponentially)
                    delay_seconds = 5 ** attempt
                    print(f"Retrying in {delay_seconds} seconds...")
                    time.sleep(delay_seconds)

        print(f"Maximum number of retries reached. Unable to get data from {endpoint}.")
        return None

    def get_pokemon_data(self, gen_name, pokemon_name):
        endpoint = f"{self.BASE_URL}GetSmogonData/{gen_name}/{pokemon_name}"
        return self.make_request(endpoint)

    def get_pokemon_by_gen(self, gen_name):
        endpoint = f"{self.BASE_URL}GetPokemonByGen/{gen_name}"
        return self.make_request(endpoint)
