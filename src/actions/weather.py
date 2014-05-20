
"""
weather actions for alfred using mashery

sample queries:

what is the weather in New York
what is the weather for tomorrow (implied current location)
what is the weather for this Friday
what is the weather in New York this Friday
"""
import urllib2
import re
import json

# yaml module used to convert unicode to ascii
import yaml
import string
import unirest

import pprint

def get_ip_address():
    url = 'http://bot.whatismyipaddress.com'
    response = urllib2.urlopen(url)
    ip_address = response.read()
    return ip_address

def get_location(ip_address):
    response = unirest.get("https://community-telize-json-ip-and-geoip.p.mashape.com/geoip/" \
    + str(ip_address),

        headers={
            "X-Mashape-Authorization": "W5slDXnAej8yvytZaE3mkrPnZIoQsgcU"
        }
    )

    return yaml.load(response.body['city'])

def fill_in_space(unprocessed_text):
    location = re.sub(' ', '+', unprocessed_text)
    return location

def get_json_data(unprocessed_location):
    location = fill_in_space(unprocessed_location)
    url = "http://api.worldweatheronline.com/free/v1/weather.ashx?q=" \
          + location \
          + "&format=json&num_of_days=5&key=c6y27sgvkadpycg54dgh8z2e"
    response = urllib2.urlopen(url)
    response_data = response.read()

    # return json data for other modules to parse
    json_data = json.loads(response_data)

    # debug
    pp = pprint.PrettyPrinter()
    pp.pprint(json_data)

    return json_data

def get_date(day, pos):
    """1
        get date from day and POS tag
        ie, this Tuesday, next Friday

        input should be "Tuesday", "JJ"
        where "JJ" refers to "next"
        and where "DT" refers to "this"
    """



def get_current_temp(weather_json):
    """
        returns temperature in Fahrenheit for current day
    """
    temp = yaml.load(weather_json['data']['current_condition'][0]['temp_F'])
    return temp

def get_other_temp(weather_json, date):
    """
        return the high and low temperature in Fahrenheit for other days
    """

def get_wind_speed(weather_json):
    speed = yaml.load(weather_json['data']['current_condition']['windspeedMiles'])
    return speed

def get_wind_dir(weather_json):
    temp = yaml.load(weather_json['data']['current_condition']['winddir16Point'])
    if (temp == 'N'):
        direction = "north"
    elif (temp == 'E'):
        direction = "east"
    elif (temp == 'W'):
        direction = "west"
    elif (temp == 'S'):
        direction = "south"

    return direction


def get_weather_desc(weather_json):
    desc = yaml.load(weather_json['data']['current_condition'][0]['weatherDesc'][0]['value'])
    return desc

def handle(message):
    if(re.search("in|for", message)):
        # "what's the weather in/for/at LA?"
        tokens = message.split()
        for i in range(0,len(tokens)):
            #TODO try \b(in|for|at)\b
            if (re.search("in|for", tokens[i])):
                unprocessed_location = string.join(tokens[i+1:len(tokens)])
                break

    else:
        # "what's the weather?"
        unprocessed_location = get_location(get_ip_address())

    weather_json = get_json_data(unprocessed_location)
    temp_f = get_current_temp(weather_json)
    # exception KeyError for bad return data
    weather_desc = get_weather_desc(weather_json)

    response = "The weather for " + unprocessed_location + " is " + str(temp_f) + " degrees fahrenheit and " + weather_desc
    return response
