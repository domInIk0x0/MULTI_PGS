import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

url = 'https://biobankengine.stanford.edu/prs'
base_url = 'https://biobankengine.stanford.edu'
response = requests.get(url)

columns = ['Trait_group', 'Trait_name', 'Family', 'Geno', 'Covars', 'Full',
           'delta', 'variants', 'p', 'significant', 'prs_weights_link']

data = pd.DataFrame(columns=columns)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    table_body = soup.find('tbody')
    rows = table_body.find_all('tr')

    for row in tqdm(rows):
        cells = row.find_all('td')
        row_data = []

        row_data.append(cells[0].get_text(strip=True))

        trait_cell = cells[1]
        trait_name = trait_cell.get_text(strip=True)

        link_tag = trait_cell.find('a')
        link = ''
        if link_tag and link_tag.get('href'):
            href = link_tag.get('href')
            link = base_url + href if href.startswith('/') else href

        row_data.append(trait_name)

        for i in range(2, 10):
            row_data.append(cells[i].get_text(strip=True))

        row_data.append(link)
        data.loc[len(data)] = row_data
      
    data.to_csv('data/pgs_table_info.csv', index=False)

else:
    print(f'{response.status_code}')
