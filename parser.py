import sys
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
        return str(e)


if __name__ == '__main__':
    requests.post('http://127.0.0.1:8000/add_parse_data/',
                  data={"data": parse_xpath(sys.argv[1], sys.argv[2]), 'url_id': sys.argv[3]})
