import requests
from bs4 import BeautifulSoup
from lxml import etree
import json


def parse_xpath(url: str, xpath: str, url_id: int):
    print("Start parsing")
    try:
        response = requests.get(url)
        response.raise_for_status()
        html = BeautifulSoup(response.text, 'lxml')
        dom = etree.HTML(str(html))
        data = dom.xpath(xpath)[0].text
        response = requests.post('http://127.0.0.1:8000/add_parse_data/',
                                 data=json.dumps({"data": data, "url_id": url_id}))
        print(response.text)
    except Exception as e:
        requests.post('http://127.0.0.1:8000/add_parse_data/',
                      data=json.dumps({"data": str(e), "url_id": url_id}))

