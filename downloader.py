import streamlit as st

# -------------------------
# 📥 Fonction pour télécharger les fichiers bruts
# -------------------------
def telecharger_fichier(nom_fichier):
    try:
        with open(nom_fichier, "r", encoding="utf-8") as fichier:
            return fichier.read()
    except FileNotFoundError:
        st.error(f"❌ Fichier {nom_fichier} introuvable.")
        return None
