import streamlit as st  # type: ignore
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs  # type: ignore

# Fonction pour scraper plusieurs pages
def scraper_pages(base_url, max_pages=5):
    data = []
    for page in range(1, max_pages + 1):
        url = f"{base_url}?page={page}"
        try:
            res = requests.get(url)
            res.raise_for_status()
            soup = bs(res.text, 'html.parser')
            containers = soup.find_all('div', class_="col s6 m4 l3")
            
            for container in containers:
                try:
                    nom = container.find('p', class_="ad__card-description").text.strip()
                    prix = container.find('p', class_="ad__card-price").text.replace('CFA', '').strip()
                    adresse = container.find('p', class_="ad__card-location").text.replace('location_on', '').strip()
                    image_lien = container.find('img', class_="ad__card-img")['src']
                    data.append({
                        'Nom': nom,
                        'Prix': prix,
                        'Adresse': adresse,
                        'Image_lien': image_lien
                    })
                except Exception:
                    continue
        except requests.exceptions.RequestException as e:
            st.error(f"Erreur de connexion : {e}")
            break
    return pd.DataFrame(data)

# Configuration de l'interface Streamlit
st.title("Application de Scraping et Évaluation")

# URLs des catégories
categories = {
    "Poules, lapins et pigeons": "https://sn.coinafrique.com/categorie/poules-lapins-et-pigeons",
    "Autres animaux": "https://sn.coinafrique.com/categorie/autres-animaux"
}

# Choix de la catégorie et nombre de pages
categorie = st.selectbox("Choisissez une catégorie", list(categories.keys()))
nombre_pages = st.slider("Nombre de pages à scraper", 1, 10, 5)

if st.button(f"Scraper les annonces de {categorie}"):
    df = scraper_pages(categories[categorie], max_pages=nombre_pages)
    st.write(df)
    
    if not df.empty:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Télécharger les données en CSV",
            data=csv,
            file_name="donnees_scrapees.csv",
            mime="text/csv"
        )

# Télécharger des données via Web Scraper
st.header("Télécharger les données non nettoyées")
uploaded_file = st.file_uploader("Télécharger un fichier de données", type=['csv', 'json'])
if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        data = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.json'):
        data = pd.read_json(uploaded_file)
    st.write(data)

# Formulaires d'évaluation
st.header("Formulaire d'évaluation via Kobo")
kobo_form_url = "https://ee.kobotoolbox.org/x/Ezm7tHcb"
st.write(f"Veuillez remplir le formulaire d'évaluation sur [Kobo]({kobo_form_url})")

st.header("Formulaire d'évaluation via Google Forms")
google_form_url = "https://forms.gle/aDaWA1VX5AXy9KAaA"
st.write(f"Veuillez remplir le formulaire d'évaluation du **Projet 11** sur [Google Forms]({google_form_url})")
