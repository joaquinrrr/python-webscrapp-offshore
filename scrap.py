#video from yt https://www.youtube.com/watch?v=YjpGdFwIAxg
#page: https://offshoreleaks.icij.org/search?q=Peru&c=&j=&d=

from requests_html import HTMLSession

s = HTMLSession()

url = 'https://offshoreleaks.icij.org/search?q=Peru&c=&j=&d='

r = s.get(url)

table = r.html.find('table')[0]

for row in table.find('tr'):
  for c in row.find('td'):
    print(c.text)

tabledata = [[c.text for c in row.find('td')[:-1]] for row in table.find('tr')][1:]
tableheaders = [[c.text for c in row.find('th')[:-1]] for row in table.find('tr')][0]

res = [dict(zip(tableheaders,t)) for t in tabledata]

with open('table.json','w') as f:
  json.dump(res,f)

