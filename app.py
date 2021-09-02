from typing import ValuesView
import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import requests

image_header = Image.open('Author_style.png')

st.markdown(
    f"<h1 style='text-align: center; color: black;'>Identification d'un auteur</h1>",
    unsafe_allow_html=True)


st.image(image_header, width=700, use_column_width='always')

st.markdown(
    f"<h1 style='text-align: center; color: black;'>Qui est l'auteur qui aurait pu écrire ce paragraphe ?</h1>",
    unsafe_allow_html=True)
st.markdown(
    f"<h2 style='text-align: center; color: black;'>Découvrons-le grâce à notre modèle !</h2>",
    unsafe_allow_html=True)

text_input = st.text_input("""Copiez un paragraphe d'auteur ici""")

prediction = st.button('Prédire')

if prediction == True:

    text_input = '%20'.join(text_input.split(" "))
    response = requests.get(
        f'https://apiamd64-ywkwoqtfqq-ew.a.run.app/predict?paragraph={text_input}',
    ).json()
    auteurs = response['prediction']
    auteurs = dict(sorted(auteurs.items(), key=lambda item: item[1]))
    keys = list(auteurs.keys())
    values = list(auteurs.values())

    index_max = values.index(max(values))
    max_auteur = keys[index_max]

    root_path = os.path.dirname(__file__)
    path_folder = os.path.join(root_path, 'Auteurs_photos')

    auteur_nom = max_auteur.split(" ")
    auteur_nom = auteur_nom[1] + ' ' + auteur_nom[0]

    st.markdown(
        f"<h1 style='text-align: center; color: black;'>L'auteur le plus probable est {auteur_nom}</h1>",
        unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.text(' ')
        imag1 = Image.open(
            os.path.join(path_folder, ''.join([max_auteur, '.png'])))
        st.image(imag1, width=600)

    with col2:
        fig = plt.figure(figsize=(5, 5))
        plt.barh(keys, values, color='skyblue')
        plt.xlabel("Probabilité que le texte saisi appartienne à cet auteur")
        plt.ylabel("Nom des auteurs")
        plt.title("Prédiction du style de l'auteur")
        st.pyplot(fig)

#st.header("""C'est Simone de Beauvoire""")
#image = Image.open('Simone_de_Beauvoir.png')
#st.image(image, caption='Simone de Beauvoir', width=200)
