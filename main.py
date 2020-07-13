import re
from data import Data
from audio import *

API_KEY = "thaK1-NzfA3J"
PROJECT_TOKEN = "tgebU5BuL2XZ"
RUN_TOKEN = "tBMpHU37icxz"

END_COMMAND = "stop"
UPDATE_COMMAND = "update"

def main():
    print("Assistant Started")

    data = Data(API_KEY, PROJECT_TOKEN)

    country_list = data.get_list_of_country()

    TOTAL_PATTERNS = {
        re.compile("[\w\s]+ total [\w\s]+ cases"): data.get_total_cases(),
        re.compile("[\w\s]+ total cases"): data.get_total_cases(),
        re.compile("[\w\s]+ total [\w\s]+ deaths"): data.get_total_deaths(),
        re.compile("[\w\s]+ total deaths"): data.get_total_deaths(),
        re.compile("[\w\s]+ total [\w\s]+ recoveries"): data.get_total_deaths(),
        re.compile("[\w\s]+ total recoveries"): data.get_total_deaths(),
        re.compile("[\w\s]+ total [\w\s]+ recovered"): data.get_total_deaths(),
        re.compile("[\w\s]+ total recovered"): data.get_total_deaths()
    }

    COUNTRY_PATTERNS = {
        re.compile("[\w\s]+ cases [\w\s]+"): lambda country: data.get_country_cases(country),
        re.compile("[\w\s]+ deaths [\w\s]+"): lambda country: data.get_country_deaths(country),
        re.compile("[\w\s]+ recoveries [\w\s]+"): lambda country: data.get_country_recovered(country),
        re.compile("[\w\s]+ recovered [\w\s]+"): lambda country: data.get_country_recovered(country),
    }

    while True:
        text = get_audio()
        result = None

        for pattern, func in COUNTRY_PATTERNS.items():
            if pattern.match(text):
                words = set(text.split(" "))
                for country in country_list:
                    if country in words:
                        result = func(country)
                        break

        for pattern, func in TOTAL_PATTERNS.items():
            if pattern.match(text):
                result = func
                break

        if text == UPDATE_COMMAND:
            result = "Data is being Updated"
            data.update_data()

        if text.find(END_COMMAND) != -1:
            result = "Thank you"
            break

        if result:
            speak(result)


main()
