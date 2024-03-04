import pandas as pd

url = 'https://offshoreleaks.icij.org/search?q=peru&c=&j=&d='

df = pd.read_html(url)
df = df[0]

df.to_json('pandastable.json', orient='records')