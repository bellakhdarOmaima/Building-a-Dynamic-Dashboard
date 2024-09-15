import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

def clean_column_name(col_name):
    # Remove [n] from the column name
    return col_name.split('[')[0].strip()

def scraper_with_selenium(url, folder_path='output'):
    # Check if the folder exists, create it if not
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Utiliser ChromeDriverManager pour éviter de gérer manuellement le chemin d'accès à ChromeDriver
    driver = webdriver.Chrome()

    driver.get(url)
    time.sleep(5)
    page_source = driver.page_source
    driver.quit()

    soup = BeautifulSoup(page_source, 'html.parser')
    table = soup.find('table', class_='wikitable sortable jquery-tablesorter')

    if table:
        rows = table.find_all('tr')
        data = []
        for row in rows:
            cols = row.find_all(['td', 'th'])
            cols = [col.text.strip() for col in cols]
            data.append(cols)

        # Clean up the column names
        cleaned_columns = [clean_column_name(col) for col in data[0]]

        df = pd.DataFrame(data[1:], columns=cleaned_columns)

        # Replace empty cells with NaN
        df.replace('', np.nan, inplace=True)
    
        # Replace NaN with NULL
        df.fillna('NULL', inplace=True)

        file_path = os.path.join(folder_path, 'colonies.xlsx')

        # Check if the file already exists, replace it if it does
        if os.path.exists(file_path):
            os.remove(file_path)

        df.to_excel(file_path, index=False)

        print(f"Scraping terminé et données enregistrées dans '{file_path}'")
    else:
        print("Aucune table trouvée avec la classe 'wikitable sortable jquery-tablesorter'")

# Appeler la fonction scraper_with_selenium avec l'URL du site à scraper
scraper_with_selenium('https://ar.m.wikipedia.org/wiki/%D8%A7%D9%84%D8%A5%D8%AD%D8%B5%D8%A7%D8%A6%D9%8A%D8%A7%D8%AA_%D8%A7%D9%84%D8%B3%D9%83%D8%A7%D9%86%D9%8A%D8%A9_%D9%84%D9%84%D9%85%D8%B3%D8%AA%D9%88%D8%B7%D9%86%D8%A7%D8%AA_%D8%A7%D9%84%D8%A5%D8%B3%D8%B1%D8%A7%D8%A6%D9%8A%D9%84%D9%8A%D8%A9_%D9%81%D9%8A_%D8%A7%D9%84%D8%B6%D9%81%D8%A9_%D8%A7%D9%84%D8%BA%D8%B1%D8%A8%D9%8A%D8%A9#:~text=%D9%81%D9%8A%20%D8%A7%D9%84%D9%85%D8%AC%D9%85%D9%88%D8%B9%D8%8C%20%D9%8A%D8%B9%D9%8A%D8%B4%20%D8%A3%D9%83%D8%AB%D8%B1%20%D9%85%D9%86,%D8%B9%D8%AF%D9%88%D9%84%D8%A9%20%D9%85%D8%B2%D8%B9%D9%88%D9%85%D8%A9%20%D8%AA%D8%B5%D8%A7%D8%AF%D9%82%20%D8%A7%D9%84%D8%AD%D9%83%D9%88%D9%85%D8%A9.', folder_path='C:\\Users\\omaima\\Desktop\\Data_BI\\colonie')

