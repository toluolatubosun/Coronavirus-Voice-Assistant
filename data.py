import requests
import threading
import time


class Data:
    def __init__(self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {
            "api_key": self.api_key
        }
        self.data = self.get_data()

    def get_data(self):
        response = requests.get(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data', params={"api_key": self.api_key})
        data = response.json()
        return data

    def get_total_cases(self):
        data = self.data['total']
        for content in data:
            if content['name'] == "Coronavirus Cases:":
                return content['value']

    def get_total_deaths(self):
        data = self.data['total']
        for content in data:
            if content['name'] == 'Deaths:':
                return f"{content['value']} people have died from corona virus"

    def get_total_recovered(self):
        data = self.data['total']
        for content in data:
            if content['name'] == 'Recovered:':
                return f"{content['value']} people have recovered from corona virus"
        return "0"

    def get_country_cases(self, country):
        data = self.data['country']
        for content in data:
            if content['name'].lower() == country.lower():
                return f"There are {content['total_cases']} corona virus cases in {country}"
        return f"There are no corona virus cases in {country}"

    def get_country_deaths(self, country):
        data = self.data['country']
        for content in data:
            if content['name'].lower() == country.lower():
                return f"There are {content['total_deaths']} corona virus deaths in {country}"
        return f"There are no corona virus deaths in {country}"

    def get_country_recovered(self, country):
        data = self.data['country']
        for content in data:
            if content['name'].lower() == country.lower():
                return f"{content['total_recovered']} people have recovered from corona virus in {country}"
        return f"There are no corona virus recoveries in {country}"

    def get_list_of_country(self):
        countries = []
        data = self.data['country']
        for content in data:
            countries.append(content['name'].lower())

        return countries

    def update_data(self):
        response = requests.post(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/run', params=self.params)

        def poll():
            time.sleep(0.1)
            old_data = self.data
            while True:
                new_data = self.data
                if new_data != old_data:
                    self.data = new_data
                    print("Data Updated")
                    break
                time.sleep(5)

        t = threading.Thread(target=poll)
        t.start()
