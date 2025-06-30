import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
from tqdm import tqdm


BASE_URL = 'https://www.pgscatalog.org'
data = []

for page_number in tqdm(range(1, 104), desc="Przetwarzanie stron"):
    page_url = f'{BASE_URL}/browse/scores/?page={page_number}'
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table', {'id': 'scores_table'})
    rows = table.tbody.find_all('tr')

    if page_number % 10 == 0:
        print('Break...')
        time.sleep(45)

    for row in tqdm(rows, desc=f'Strona {page_number} - wiersze'):
        columns = row.find_all('td')
        if len(columns) >= 6:
            score_tag = columns[0].find('a')
            score_id = score_tag.text.strip()
            score_url = BASE_URL + score_tag['href']

            trait = columns[2].text.strip()
            num_snps = columns[4].text.strip()

            detail_response = requests.get(score_url)
            detail_soup = BeautifulSoup(detail_response.content, 'html.parser')

            weights_base_url = detail_soup.find(
                class_='btn btn-pgs pgs_no_icon_link pgs_helptip mr-2 mb-2'
            )['href']

            harmonized_url = os.path.join(weights_base_url, 'Harmonized/')
            harmonized_response = requests.get(harmonized_url)
            harmonized_soup = BeautifulSoup(harmonized_response.content, 'html.parser')

            final_weights_url = None
            for link in harmonized_soup.find_all('a'):
                href = link.get('href')
                if href and href.endswith('.txt.gz') and not href.endswith('.md5'):
                    final_weights_url = os.path.join(harmonized_url, href)

            data.append([score_id, trait, num_snps, final_weights_url])
            time.sleep(0.7)

    df_temp = pd.DataFrame(data, columns=[
        'Score ID', 'Trait', 'Num SNPs', 'Download Link'
    ])
    df_temp.to_csv('scraped_table_PGSCATALOG.csv', index=False)
