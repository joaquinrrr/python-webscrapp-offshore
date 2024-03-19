import json
from requests_html import HTMLSession
from bs4 import BeautifulSoup

s = HTMLSession()

def getdata(url):
    r = s.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def extract_table_data(soup):
    table = soup.find('table')
    if not table:
        return None

    table_data = []
    headers = [header.text.strip() for header in table.find_all('th')]
    rows = table.find_all('tr')[1:]

    for row in rows:
        row_data = {}
        columns = row.find_all('td')
        for index, column in enumerate(columns):
            row_data[headers[index]] = column.text.strip()
        table_data.append(row_data)

    return table_data

def scrape_data(search_query):
    url = f'https://offshoreleaks.icij.org/search?q={search_query}&c=&j=&d='
    soup = getdata(url)
    table_data = extract_table_data(soup)

    with open(f'{search_query}_table_data.json', 'w') as json_file:
        json.dump(table_data, json_file, indent=4)

search_queries = ['china', 'peru', 'italy', 'france']  # Añade más criterios de búsqueda aquí

for search_query in search_queries:
    scrape_data(search_query)

print("Descarga completa.")
