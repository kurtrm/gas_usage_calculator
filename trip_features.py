"""
Module containing functions to calculate routes via the Google Maps
API, and return the total number of miles on the route.
"""
import os

import googlemaps


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
