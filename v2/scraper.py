import requests
from bs4 import BeautifulSoup

url = 'https://www.bbc.com'
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    html_content = response.text
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(html_content)
else:
    print("Failed to retrieve the website")
