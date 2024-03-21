#llamamos a las librerias
import json
from requests_html import HTMLSession
from bs4 import BeautifulSoup

#iniciamos la session de la pagina
s = HTMLSession()

#obtenemos la data de la pagina web
def getdata(url):
    r = s.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

#extramos la data de la pagina web
def extract_table_data(soup):
    table = soup.find('table') #encuentra dentro del HTML la tabla de la pagina web
    if not table:
        return None

    table_data = [] #inicializa un array para ir guardando la data de cada fila y columna
    headers = [header.text.strip() for header in table.find_all('th')] #headers de la tabla
    rows = table.find_all('tr')[1:] #filas de la tabla

    for row in rows:
        row_data = {}
        columns = row.find_all('td')
        for index, column in enumerate(columns):
            # extraer y añadir el enlace si existe en la columna
            link = column.find('a') #encuenta los links de entity y data from
            header = headers[index]
            if link is not None:
                row_data[header] = link.text.strip()

                if link['href'].startswith('https://www.icij.org'): 
                    row_data[header + ' link'] = link['href'] #añade el link del data from
                else:
                    row_data[header + ' link'] = 'https://offshoreleaks.icij.org' + link['href'] #añade los links del entity (son nodos)
            else:
                row_data[header] = column.text.strip() 
        table_data.append(row_data)

    return table_data


def scrape_data(search_query): #funcion la cual agarra el valor de busqueda
    url = f'https://offshoreleaks.icij.org/search?q={search_query}&c=&j=&d=' #inicializa el link con el elemento de busqueda
    soup = getdata(url)
    table_data = extract_table_data(soup) #extrae toda la data

    with open(f'{search_query}_table_data_W_LINKS.json', 'w') as json_file: #exporta en un archivo JSON de la información de la tabla
        json.dump(table_data, json_file, indent=4)


search_queries = ['china', 'peru', 'italy', 'france']  #añadir más elementos de busqueda para el webscrap


for search_query in search_queries:
    scrape_data(search_query) #va cambiando los elementos de busqueda


print("Download complete.")
