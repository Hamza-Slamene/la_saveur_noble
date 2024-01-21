import streamlit as st
import pandas as pd
import sqlite3
from streamlit_option_menu import option_menu
import datetime
import pickle
from pathlib import Path
import streamlit_authenticator as stauth


names = ["Brahim AMEUR-ZAIMECHE", "Hamza SLAMENE"]
usernames = ["baz", "hsl"]
#passwords = ["xxxxxxxx", "xxxxxxxxxxxx"]
#hash_passwords = stauth.Hasher(passwords).generate()
#
#file_path = Path(__file__).parent / "hashed_pwd.pkl"
#with file_path.open("wb") as file:
#    pickle.dump(hash_passwords, file)


date_actuelle = datetime.datetime.now()
date_actuelle = date_actuelle.strftime("%Y-%m-%d")

with st.sidebar:
    selected = option_menu(
        menu_title = None,
        options = ['Home', 'Admin'],
        default_index = 0,
        #orientation = 'horizontal'
    )
conn = sqlite3.connect('clients.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS commandes (
                        NOM TEXT,
                        PRENOM TEXT,
                        PRODUIT TEXT,
                        KG INTEGER,
                        GRAMMES INTEGER,
                        DATE TEXT);
                ''')

cursor.execute('''CREATE TABLE IF NOT EXISTS produits (PRODUIT TEXT, PRIX FLOAT); ''')

#cursor.execute(f''' INSERT INTO produits VALUES ('Steak', 20) ''') 
#conn.commit()

if selected == 'Home':

    st.markdown("<h1 style='text-align: center; color: red;'>LA SAVEUR NOBLE</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col2:
        st.image("./assets/logo.PNG")

    st.write("""
                Bienvenue chez La Saveur Noble, l'adresse incontournable pour les amateurs de viande exquise et de qualité exceptionnelle. Nous sommes fiers de vous proposer une sélection de viandes de prestige, soigneusement choisies pour satisfaire les palais les plus exigeants.

            """)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("./assets/steak.jpg", width=200, caption='Steak')
    with col2:
        st.image("./assets/viande-hachee.jpeg", width=200, caption='viande-hachee')
    with col3:
        st.image("./assets/tranche-grasse.jpg", width=200, caption='tranche-grasse')


    col1, col2, col3, col4, col5 = st.columns(5)

    nom = col1.text_input('Nom').upper()
    prenom = col2.text_input('Prénom').upper()
    produit  = col3.selectbox('Produit', ['','Steak','Viande hachée','Buftek','Tend de tranche'])
    kg = col4.selectbox('Kg', ['',1,2,3,4,5,6,7,8,9,10])
    grammes = col5.selectbox('Grammes', ['',100,200,300,400,500,600,700,800,900])

    def commander():
        cursor.execute(f''' INSERT INTO commandes VALUES ('{nom}', '{prenom}', '{produit}', {kg}, {grammes}, '{date_actuelle}') ''') 
        conn.commit() 
        #conn.close()

    if st.button('commander'):
        st.write(f"Vous avez commandé : {kg}.{grammes} kg de {produit}")
        commander()
        st.write('Votre commande a été enrgistrée')
        
if selected == 'Admin':
    file_path = Path(__file__).parent / "hashed_pwd.pkl"
    with file_path.open("rb") as file:
        hash_passwords = pickle.load(file)

    authenticator = stauth.Authenticate(names, usernames, hash_passwords, "sales", "abcdef")
    name, authentication_status, username = authenticator.login("Login", "main")

    if authentication_status == False:
        st.error("Incorrect username or password")
    if authentication_status == None:
        st.warning("No user has been logged in yet")
    if authentication_status : 
        st.title("Administration")
        st.write('Pour se déconnecter, cliquez sur Logout')
        authenticator.logout("Logout", "main")

        st.title('Tableau des commandes')

        prix = pd.read_sql_query("SELECT * FROM produits", conn)
        commandes = pd.read_sql_query("SELECT * FROM commandes", conn)

        result = pd.merge(commandes, prix, on='PRODUIT', how='left')
        result['QUANTITE'] = (result['KG'] * 1000 + result['GRAMMES']) / 1000
        result['MONTANT'] = result['QUANTITE'] * result['PRIX'].astype(float)
        st.dataframe(result)
        #conn.close()
        

        