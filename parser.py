from typing import Any

import requests
from bs4 import BeautifulSoup
from lxml import etree


def parse_xpath(url: str, xpath: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()
        html = BeautifulSoup(response.text, 'lxml')
        dom = etree.HTML(str(html))
        return dom.xpath(xpath)[0].text
    except Exception as e:
        raise e
