"""
Module containing functions to retrieve gas prices from popular gas
price reporting website.
"""
from typing import List

from bs4 import BeautifulSoup
from requests.exceptions import RequestException

import requests


GAS_PRICES_ADDRESS = 'https://www.gasbuddy.com/home?search={}&fuel=1'


def retrieve_gas_prices(zipcode: int) -> str:
    """
    Function using the requests library to retrieve
    html from website.

    Parameters
    ----------
    zipcode: The zipcode from which to retrieve gas prices.
             This is passed into the global address string.

    Returns
    -------
    string: The html content to be parsed by bs4.

    Exceptions
    ----------
    RequestException: Raises an exception if a status code
    other than 200 is received.
    """
    full_query = GAS_PRICES_ADDRESS.format(zipcode)
    response = requests.get(full_query)
    if response.status_code == 200:
        return response.content
    else:
        raise RequestException(f'Error: Received connection status '
                               '{response.status_code}')


def parse_html(html) -> List:
    """
    Using the raw html passed in, returns the gas price, name, address
    of each station listed in the html.

    The prices, names, and address elements are hard coded since
    these had to be predetermined while exploring the raw html. If one
    visits the global GAS_PRICES_ADDRESS, these patterns are recurrent
    among most pages.

    Parameters
    ----------
    html: The raw html that will be parsed for bs4 to retrieve relevant
    data.

    Returns
    -------
    names, addresses, prices: Lists of names, addresses, and prices for
    all gas stations listed in the html.
    """
    prices_element = 'span[class*="styles__price"]'
    station_name_element = 'h3[class*="styles__stationNameHeader"]'
    station_address_element = 'div[class*="styles__address"]'
    soup = BeautifulSoup(html, 'html.parser')
    prices = [element.text for element in soup.select(prices_element)]
    names = [element.text for element in soup.select(station_name_element)]
    addresses = [element.text
                 for element in soup.select(station_address_element)]

    return names, addresses, prices


def get_gas_information(zipcode: int=98105) -> List[dict]:
    """
    """
    fuel_prices_html = retrieve_gas_prices(zipcode)
    names, addresses, prices = parse_html(fuel_prices_html)
    return [{'name': name, 'price': price, 'address': address}
            for price, name, address in zip(prices, names, addresses)]
