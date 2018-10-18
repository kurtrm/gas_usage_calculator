"""
Module containing functions to calculate routes via the Google Maps
API, and return the total number of miles on the route.
"""
import os

import googlemaps
import requests

from bs4 import BeautifulSoup


def get_maps_data(start_point: str, end_point: str, api_key: str=None) -> str:
    """
    """
    if api_key is None:
        try:
            api_key = os.environ['GMAPS_API_KEY']
        except KeyError:
            raise ValueError('No API key is available in the environment, '
                             'please pass in a valid api key.')
    gmaps = googlemaps.Client(key=api_key)
    directions_json = gmaps.directions(start_point, end_point, mode='driving')
    total_dist = directions_json[0]['legs'][0]['distance']['text']

    return total_dist


def parse_dist_text(text: str) -> float:
    """
    """
    try:
        return float(text[:-3])
    except ValueError:
        for i in range(0, -11, -1):
            try:
                return float(text[:i])
            except ValueError:
                continue
        else:
            raise ValueError('Unable to parse distance from string')


def get_gas_mileage(year: str, make: str, model: str) -> str:
    """
    """
    fueleconomy_car_menu = 'https://www.fueleconomy.gov/'
    'ws/rest/vehicle/menu/options?year={}&make={}&model={}'.format(year, make, model)

    fueleconomy_car_info = 'https://www.fueleconomy.gov/ws/rest/vehicle/{}'

    menu_response = requests.get(fueleconomy_car_menu)
    menu_soup = BeautifulSoup(menu_response.content, 'html.parser')
    car_id = menu_soup.find('value').text
    car_response = requests.get(fueleconomy_car_info.format(car_id))
    car_soup = BeautifulSoup(car_response.content, 'html.parser')
    car_mileage_highway = car_soup.find('highway08').text
    car_mileage_city = car_soup.find('city08').text
    car_mileage_combined = car_soup.find('comb08').text

    return car_mileage_highway, car_mileage_city, car_mileage_combined
