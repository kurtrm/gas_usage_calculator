"""
"""
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException


GAS_PRICES_ADDRESS = 'https://www.gasbuddy.com/home?search={}&fuel=1'


def retrieve_gas_prices(zipcode: int) -> str:
    """
    """
    full_query = GAS_PRICES_ADDRESS.format(zipcode)
    response = requests.get(full_query)
    if response.status_code == 200:
        return response.content
    else:
        raise RequestException(f'Error: Received connection status {response.status_code}')


def parse_html(html) -> str:
    """
    """
    prices_element = 'span[class*="styles__price"]'
    station_name_element = 'h3[class*="styles__stationNameHeader"]'
    station_address_element = 'div[class*="styles__address"]'
    soup = BeautifulSoup(html, 'html.parser')
    prices = [element.text for element in soup.select(prices_element)]
    names = [element.text for element in soup.select(station_name_element)]
    addresses = [element.text for element in soup.select(station_address_element)]

    return names, addresses, prices


def get_gas_information(zipcode: int=98105) -> str:
    """
    """
    fuel_prices_html = retrieve_gas_prices(zipcode)
    names, addresses, prices = parse_html(fuel_prices_html)
    return [{'name': name, 'price': price, 'address': address}
            for price, name, address in zip(prices, names, addresses)]
