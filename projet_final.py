# streamlit run projet_final.py
# streamlit run streamlit_app\Pages\app.py

import streamlit as st
import pandas as pd
import numpy as np
import requests
import zipfile
from io import BytesIO
import matplotlib.pyplot as plt

st.title('Etude sur les besoins en main d oeuvre en France')


##Bandeau
st.sidebar.title('Le projet')
text = st.sidebar.markdown('Dans le cadre de mon cursus scolaire nous devions réaliser un projet, qui a pour but de créer une application streamlit avec des données de data.gouv. ')

st.sidebar.title('Qui suis-je ?')
text = st.sidebar.markdown('Je m appelle Pauline Savatte, je suis actuellement en première année de Msc Data Management à Paris School of Business en partenariat avec l EFREI et également en alternance à la Banque Populaire Grand Ouest. Ci-dessous le lien vers mes réseaux. ')

#linkedin
image1 = 'image/lin.png'
link = 'https://www.linkedin.com/in/pauline-savatte-7083aa199/'
st.sidebar.image(image1)
st.sidebar.markdown(f'[LinkedIn]({link})')

#Github
image2 = 'image/git.jpg'
link2 = 'https://github.com/Pauline35500'
st.sidebar.image(image2)
st.sidebar.markdown(f'[Github]({link2})')

## Page principale
st.markdown('<h1 style="font-size: 36px;">I - Introduction</h1>', unsafe_allow_html=True)
st.write('Pour réaliser l étude ci-dessous nous avons tout d abord choisi le jeu de données sur les BMO (besoins en main d oeuvre) en France. Après avoir importé les données à l aide du lien stable disponible sur data.gouv. Nous avons nettoyé les données et créé des nouvelles colonnes comme la colonne percent_season ou percent_hard qui permettent de mieux visualiser le pourcentage de poste difficile à pourvoir ainsi que le pourcentage de recrutement saisonnier.')

image = 'image/intro.jpg'
st.image(image)

## Présentation du jeu de données
st.markdown('<h1 style="font-size: 36px;">II - Mon jeu de données</h1>', unsafe_allow_html=True)
url = 'https://www.data.gouv.fr/fr/datasets/r/cf654bbd-aa1e-458c-9d08-24252f66f16b'
response = requests.get(url)

zip_file = zipfile.ZipFile(BytesIO(response.content))
file_name = zip_file.namelist()[0]
data = zip_file.open(file_name)

df1 = pd.read_excel(data, sheet_name=1, dtype= str )
df = pd.read_excel(data, sheet_name=1, dtype= str )

st.write('Le fichier avant le nettoyage et la création de variables : ')
st.dataframe(df1.head())

st.write('Le fichier après le nettoyage et la création de variables : ')

## Traitement sur le jeu de données
df.rename(columns = {'annee':'annee', 'Code métier BMO':'code_metier_bmo', 'Nom métier BMO':'nom_metier_bmo','Famille_met':'famille_metier','Lbl_fam_met':'libelle_famille_metier','BE23':'code_bassin_emploi', 'NOMBE23':'nom_bassin_emploi','Dept' : 'departement','NomDept' : 'nom_departement', 'REG':'region','NOM_REG':'nom_region', 'met':'nb_proj_recrut','xmet':'nb_proj_recrut_hard', 'smet':'nb_proj_recrut_saison'}, inplace = True)
df = df[df['nb_proj_recrut_saison'] != '*']
df = df[df['nb_proj_recrut_hard'] != '*']
df = df[df['nb_proj_recrut'] != '*']
df['nb_proj_recrut'] = df['nb_proj_recrut'].astype('int64')
df['nb_proj_recrut_hard'] = df['nb_proj_recrut_hard'].astype('int64')
df['nb_proj_recrut_saison'] = df['nb_proj_recrut_saison'].astype('int64')

st.dataframe(df.head())

metier_unique = df['nom_metier_bmo'].nunique()
region_unique = df['region'].nunique()
departement_unique = df['departement'].nunique()
annee_en_cours = df.annee[1]

st.write('')
st.markdown('<h1 style="font-size: 36px;">III - Quelque chiffres clés</h1>', unsafe_allow_html=True)
## Création de texte intéractif avec le fichier csv c'est à dire texte qui se modifie si la source est modifié

st.markdown(f'<div style="text-align: center;"><span style="color:blue; font-size: 24px;">Ce sont des données de {annee_en_cours}</span></div>', unsafe_allow_html=True)
st.markdown(f'<div style="text-align: center;"><span style="color:blue; font-size: 24px;">{metier_unique} métiers différents</span></div>', unsafe_allow_html=True)
st.markdown(f'<div style="text-align: center;"><span style="color:blue; font-size: 24px;">{region_unique} régions représentées</span></div>', unsafe_allow_html=True)
st.markdown(f'<div style="text-align: center;"><span style="color:blue; font-size: 24px;">{departement_unique} départements représentés</span></div>', unsafe_allow_html=True)


st.markdown('<h1 style="font-size: 36px;">IV - Etudes sur les besoins en mains d oeuvres</h1>', unsafe_allow_html=True)
st.markdown('<h2 style="font-size: 24px;">a) Présentation des familles de métiers présent dans notre jeu de données puis zoom sur les métiers</h2>', unsafe_allow_html=True)

color = st.select_slider(
     'Choisissez une couleur pour les prochains graphiques :',
     options=['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet'])

df3 = df.groupby('libelle_famille_metier').count()
df_sorted = df3.sort_values(by='annee', ascending=False).head(10)
chart = df_sorted['annee'].plot.pie(autopct='%1.1f%%')

st.pyplot(chart.figure)

plt.clf()

nb = st.text_input('Combien de métier voulez-vous afficher ? ', '10')
nb = int(nb)

df4 = df.groupby('nom_metier_bmo').count()
sorted_df2 = df4.sort_values(by='annee', ascending=False).head(nb)
chart2 = sorted_df2['annee'].plot.barh(color=color)

st.pyplot(chart2.figure)

plt.clf()

st.markdown('<h2 style="font-size: 24px;">b) Classements des régions/départements en fonction du pourcentage de recrutements diffciles et saisonniers </h2>', unsafe_allow_html=True)


df2 = df.copy()
df_reg = df2.drop(['annee','code_metier_bmo', 'nom_metier_bmo','famille_metier','libelle_famille_metier','code_bassin_emploi', 'nom_bassin_emploi', 'departement', 'nom_departement','region'], axis=1)

df_reg = df_reg.groupby('nom_region').sum()
df_reg['percent_hard'] = (df_reg.nb_proj_recrut_hard*100/df_reg.nb_proj_recrut).round(2)
df_reg['percent_season'] = (df_reg.nb_proj_recrut_saison*100/df_reg.nb_proj_recrut).round(2)

df_dept = df2.drop(['annee','code_metier_bmo', 'nom_metier_bmo','famille_metier','libelle_famille_metier','code_bassin_emploi', 'nom_bassin_emploi','nom_region','region'], axis=1)

df_dept = df_dept.groupby('nom_departement').sum()
df_dept['percent_hard'] = (df_dept.nb_proj_recrut_hard*100/df_dept.nb_proj_recrut).round(2)
df_dept['percent_season'] = (df_dept.nb_proj_recrut_saison*100/df_dept.nb_proj_recrut).round(2)

option1 = st.radio(
    "Voir les données par :",
    ( 'Département', 'Région')
)

option2 = st.radio(
    "Voir les données par :",
    ('Top', 'Flop')
)


if option1 == 'Région' and option2 == 'Top' :
    sorted_df1 = df_reg.sort_values(by='percent_hard', ascending=False).head(10)
    sorted_df1['percent_hard'].plot.bar(color=color)
    # plt.xlabel('Index')
    # plt.ylabel('Percent Hard')
    plt.title('Top 10 des régions ayant le plus de difficultés à recruter')

    st.pyplot(plt)

    sorted_df1 = df_reg.sort_values(by='percent_season', ascending=False).head(10)
    sorted_df1['percent_season'].plot.bar(color=color)
    plt.xlabel('  ')
    plt.ylabel('  ')
    plt.title('Top 10 des régions ayant le plus de recrutements saisonnier')
    
    # plt.clf()
    st.pyplot(plt)

elif option1 == 'Région' and option2 == 'Flop' :
    sorted_df1 = df_reg.sort_values(by='percent_hard', ascending=True).head(10)
    sorted_df1['percent_hard'].plot.bar(color=color)
    plt.xlabel('  ')
    plt.ylabel('  ')
    plt.title('Flop 10 des régions ayant le plus de difficultés à recruter')

    # plt.clf()
    st.pyplot(plt)

    sorted_df1 = df_reg.sort_values(by='percent_season', ascending=True).head(10)
    sorted_df1['percent_season'].plot.bar(color=color)
    plt.xlabel('  ')
    plt.ylabel('  ')
    plt.title('Flop 10 des régions ayant le plus de recrutements saisonnier')
    
    # plt.clf()
    st.pyplot(plt)

elif option1 == 'Département' and option2 == 'Top' :
    sorted_df1 = df_dept.sort_values(by='percent_hard', ascending=False).head(10)
    sorted_df1['percent_hard'].plot.bar(color=color)
    plt.xlabel('  ')
    plt.ylabel('  ')
    plt.title('Top 10 des départements ayant le plus de difficultés à recruter')

    # plt.clf()
    st.pyplot(plt)

    sorted_df1 = df_dept.sort_values(by='percent_season', ascending=False).head(10)
    sorted_df1['percent_season'].plot.bar(color=color)
    plt.xlabel('  ')
    plt.ylabel('  ')
    plt.title('Top 10 des départements ayant le plus de recrutements saisonnier')

    # plt.clf()
    st.pyplot(plt)
else:
    sorted_df1 = df_dept.sort_values(by='percent_hard', ascending=True).head(10)
    sorted_df1['percent_hard'].plot.bar(color=color)
    plt.xlabel('  ')
    plt.ylabel('  ')
    plt.title('Flop 10 des départements ayant le plus de difficultés à recruter')

    # plt.clf()
    st.pyplot(plt)

    sorted_df1 = df_dept.sort_values(by='percent_season', ascending=True).head(10)
    sorted_df1['percent_season'].plot.bar(color=color)
    plt.xlabel('  ')
    plt.ylabel('  ')
    plt.title('Flop 10 des départements ayant le plus de recrutements saisonnier')
    
    # plt.clf()
    st.pyplot(plt)


## Détails par département, par région 

st.markdown('<h2 style="font-size: 24px;">c) Zoom sur une région, un département qui vous intéresse </h2>', unsafe_allow_html=True)

vertical_concat = pd.concat([df_dept, df_reg], axis=0)

options5 = vertical_concat.index.tolist()
options6 = st.selectbox("Sélectionnez le département ou la région qui vous intéresse", options5)
st.write(f"You chose: {options6}")


df_test = vertical_concat.loc[vertical_concat.index == options6]
hard= df_test['percent_hard'].values
season= df_test['percent_season'].values 


st.markdown(f'<div style="text-align: center;"><span style="color:red; font-size: 24px;">Ce sont des données sur {options6}</span></div>', unsafe_allow_html=True)
st.markdown(f'<div style="text-align: center;"><span style="color:red; font-size: 24px;">{hard}%   de recrutements difficil</span></div>', unsafe_allow_html=True)
st.markdown(f'<div style="text-align: center;"><span style="color:red; font-size: 24px;">{season}% de recrutements saisonnier</span></div>', unsafe_allow_html=True)



import geopandas as gpd
import folium
from streamlit_folium import folium_static


df2 = df_dept.copy()
df2['code_departement'] = df2['departement']
departements = gpd.read_file('data/departements.geojson')

data = departements.to_crs(epsg=4326)
m = folium.Map(location=[46.2276, 2.2137], zoom_start=5)

folium.Choropleth(
    geo_data=data,
    name='choropleth',
    data=df2,
    columns=['code_departement', 'percent_hard'],
    key_on='feature.properties.code',
    # fill_color='YlGn',
    # fill_opacity=0.7,
    # line_opacity=0.2,
    # legend_name='Data Column'
).add_to(m)

folium.LayerControl().add_to(m)
folium_static(m)
