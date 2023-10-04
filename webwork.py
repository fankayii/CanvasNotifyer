from urllib.request import urlopen
import requests
from urllib.request import Request
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
headers = {
           'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'#每个爬虫必备的伪装
          }
session = requests.Session()

# Add cookies to the session

cookies_dict = {
    'WeBWorKCourseAuthen.2023W1_MATH_200_ALL_2023W1': 'ZP87L0A2BM05%09lDJ0OQ65IpAXFHSFOd0iYXHlN7cu28JL%091694488450',

    # Add other cookies here
}



session.cookies.update(cookies_dict)

# Use the session to get the page content
response = session.get('https://webwork.elearning.ubc.ca/webwork2/2023W1_MATH_200_ALL_2023W1/?effectiveUser=ZP87L0A2BM05')

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup)