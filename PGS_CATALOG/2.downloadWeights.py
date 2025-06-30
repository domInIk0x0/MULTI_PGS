import pandas as pd
import time
import os
import subprocess
from tqdm import tqdm
import shutil


df = pd.read_csv('scraped_table_PGSCATALOG.csv')
df['Num SNPs'] = df['Num SNPs'].str.replace(',', '', regex=False).astype(int)
filtered_df = df[df['Num SNPs'] > 2000]
df_no_duplicates = filtered_df.drop_duplicates(subset='Trait', keep='first')

links = df_no_duplicates['Download Link'].values
traits = df_no_duplicates ['Trait'].values

dir_path = 'PGS_CATALOG_WEIGHTS/'
folders = os.listdir(dir_path)

for f in folders:
  p = os.path.join(dir_path, f)
  shutil.rmtree(p)
print('Folder structure has been cleaned.')
print('\n')

for li, traits in tqdm(zip(links, traits), total=len(links)):
    target_dir = os.path.join(dir_path, traits.replace(' ', '_').upper())
    print(f'Path: {target_dir}')
    os.makedirs(target_dir, exist_ok=True)

    time.sleep(1)
    subprocess.run(['wget', '-P', target_dir, li])
