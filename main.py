import requests
import aiogram
from bs4 import BeautifulSoup as b

URL = "https://t.me/d4815162342d"
r = requests.get(URL)
print(r.status_code)
print(r.text)