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


def parse_html(zipcode: int=98105) -> str:
    """
    """
    prices_element = 'span[class*="styles__price"]'
    station_name_element = 'h3[class*="styles__stationNameHeader"]'
    station_address_element = 'div[class*="styles__address"]'
    fuel_prices_html = retrieve_gas_prices(zipcode)
    soup = BeautifulSoup(fuel_prices_html, 'html.parser')
    prices = [element.text for element in soup.select(prices_element)]
    names = [element.text for element in soup.select(station_name_element)]
    addresses = [element.text for element in soup.select(station_address_element)]

    # import pdb; pdb.set_trace()

    return [{'name': name, 'price': price, 'address': address}
            for price, name, address in zip(prices, names, addresses)]





    

