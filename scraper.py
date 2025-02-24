import requests
from bs4 import BeautifulSoup

# -------------------------
# 🕵 Fonction de Scraping
# -------------------------
def scrape_coinafrica(category, num_pages=1):
    base_url = f"https://sn.coinafrique.com/categorie/{category}"
    data = []

    for page in range(1, num_pages + 1):
        url = f"{base_url}?page={page}"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

        if response.status_code != 200:
            return None  # Si la requête échoue

        soup = BeautifulSoup(response.text, 'html.parser')
        listings = soup.find_all('div', class_='ad-card')

        if not listings:
            return None  # Si aucune annonce trouvée

        for listing in listings:
            try:
                title = listing.find('h2').text.strip()
                price = listing.find('span', class_='price').text.strip()
                address = listing.find('span', class_='location').text.strip()
                image = listing.find('img')['src']

                data.append({
                    "Détails": title,
                    "Prix": price,
                    "Adresse": address,
                    "Image": image
                })
            except:
                continue

    return data
