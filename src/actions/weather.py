
"""
weather actions for alfred using mashery
"""
import urllib2
import re
import json
import yaml
import string

def fill_in_space(unprocessed_text):
    location = re.sub(' ', '+', unprocessed_text)
    return location

def get_json_data(location):
    url = "http://api.worldweatheronline.com/free/v1/weather.ashx?q=" + location + "&format=json&num_of_days=1&key=c6y27sgvkadpycg54dgh8z2e"
    response = urllib2.urlopen(url)
    response_data = response.read()

    # return json data for other modules to parse
    json_data = json.loads(response_data)

    return json_data

def get_f_degrees(weather_json):
    print(weather_json)
    temp_f = yaml.load(weather_json['data']['current_condition'][0]['temp_F'])
    return temp_f

def get_weather_desc(weather_json):
    desc = yaml.load(weather_json['data']['current_condition'][0]['weatherDesc'][0]['value'])
    return desc

def handler(text, alfred):
    if(re.search("in|for", text)):
        # "what's the weather in/for/at LA?"
        tokens = text.split()
        for i in range(0,len(tokens)):
            #TODO try \b(in|for|at)\b
            if (re.search("in|for", tokens[i])):
                unprocessed_location = string.join(tokens[i+1:len(tokens)])
                break
    else:
        # "what's the weather?"
        #TODO get current location
        unprocessed_location = "Los Angeles"

    location = fill_in_space(unprocessed_location)
    weather_json = get_json_data(location)
    temp_f = get_f_degrees(weather_json)
    weather_desc = get_weather_desc(weather_json)

    message = "The weather for " + unprocessed_location + " is " + str(temp_f) + " degrees fahrenheit and " + weather_desc
    alfred.says(message)
