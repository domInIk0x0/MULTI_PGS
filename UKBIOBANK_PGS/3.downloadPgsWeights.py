import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import subprocess
from tqdm import tqdm
import shutil

df = pd.read_csv('data/filtered_tab.csv')
links = df['prs_weights_link']

dir_path = 'UKBIOBANK_WEIGHTS/'

folders = os.listdir(dir_path)
for f in folders:
  p = os.path.join(dir_path, f)
  shutil.rmtree(p)
print('Folder structure has been cleaned.')
print('\n')

for li in tqdm(links):
    time.sleep(0.01)
    response = requests.get(li)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        trait = df[df['prs_weights_link'] == li].Trait_name
        prs_weights_li = soup.find('a', class_='btn btn-block btn-primary')['href']
        full_link = f'https://biobankengine.stanford.edu{prs_weights_li}'

        target_dir = os.path.join(dir_path, trait.values[0].upper())
        print(f'Sciezka: {target_dir}')
        os.makedirs(target_dir, exist_ok=True)

        subprocess.run(['wget', '-P', target_dir, full_link])
