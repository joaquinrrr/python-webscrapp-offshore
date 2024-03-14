import json
from requests_html import HTMLSession
from bs4 import BeautifulSoup

s = HTMLSession()
url = 'https://offshoreleaks.icij.org/search?q=china&c=&j=&d='

def getdata(url):
    r = s.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def getnextpage(soup):
    page = soup.find('div', {'class': 'my-5', 'id': 'more_results'})
    if page:
        url = 'https://offshoreleaks.icij.org' + page.find('a')['href']
        return url
    else:
        return None

def extract_table_data(soup):
    table = soup.find('table')
    if not table:
        return None

    table_data = []
    headers = [header.text.strip() for header in table.find_all('th')]
    rows = table.find_all('tr')[1:]  # Excluyendo la fila de encabezados

    for row in rows:
        row_data = {}
        columns = row.find_all('td')
        for index, column in enumerate(columns):
            row_data[headers[index]] = column.text.strip()
        table_data.append(row_data)

    return table_data

# Contador para el número de páginas descargadas
page_count = 0

# Llamar a la función extract_table_data dentro del bucle
while True:
    soup = getdata(url)
    table_data = extract_table_data(soup)
    if not table_data:
        break
    
    page_count += 1  # Incrementar el contador de página
    print(f"Página {page_count} descargada.")

    with open('table_data.json', 'a') as json_file:
        json.dump(table_data, json_file, indent=4)  # Exportar los datos de la tabla como JSON
        json_file.write('\n')

    url = getnextpage(soup)

print("Descarga completa.")