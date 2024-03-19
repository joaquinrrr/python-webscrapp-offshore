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
            # extraer y añadir el enlace si existe en la columna
            link = column.find('a')
            header = headers[index]
            if link is not None:
                row_data[header] = link.text.strip()
                
                if link['href'].startswith('https://www.icij.org'):
                    row_data[header + ' link'] = link['href']
                else:
                    row_data[header + ' link'] = 'https://offshoreleaks.icij.org' + link['href']
            else:
                row_data[header] = column.text.strip()
        table_data.append(row_data)

    return table_data


def scrape_data(search_query):
    url = f'https://offshoreleaks.icij.org/search?q={search_query}&c=&j=&d='
    soup = getdata(url)
    table_data = extract_table_data(soup)

    with open(f'{search_query}_table_data_W_LINKS.json', 'w') as json_file:
        json.dump(table_data, json_file, indent=4)


search_queries = ['china', 'peru', 'italy', 'france']  # Add more search queries here


for search_query in search_queries:
    scrape_data(search_query)


print("Download complete.")
