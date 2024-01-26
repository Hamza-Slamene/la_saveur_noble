import streamlit as st
import pandas as pd
import sqlite3
from streamlit_option_menu import option_menu
import datetime
import pickle
from pathlib import Path
import streamlit_authenticator as stauth
import smtplib 
import ssl
import email
from database import Database
import smtplib
from email.mime.text import MIMEText

database = Database()


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

st.set_page_config(page_title="La Saveur Noble Tremblaysienne", layout="centered")
hide_st_style = """
                    <style>
                        footer {visibility: hidden;}
                        header {visibility: hidden;}
                    </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.markdown("""
        <style>
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)


with st.sidebar:
    selected = option_menu(
        menu_title = None,
        options = ['Home', 'Admin'],
        default_index = 0,
        orientation = 'vertical'
    )

database.create_tables()


if selected == 'Home':

    st.markdown("<h1 style='text-align: center; color: red;'>La Saveur Noble Tremblaysienne</h1>", unsafe_allow_html=True)

    #col1, col2, col3 = st.columns(3)
    #with col2:
    #    st.image("./assets/logo.PNG")

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



    def send_mail(destinataire, corps_message):
        # Paramètres du serveur SMTP
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587

        # Informations d'authentification
        email_address = 'lasaveurnoble@gmail.com'
        email_password = 'qsdd wams qrkz hwja'

        # Destinataire et contenu du message
   
        sujet = 'Facture de commande'
        
        # Créer le message MIME
        message = MIMEText(corps_message)
        message['Subject'] = sujet
        message['From'] = email_address
        message['To'] = destinataire

        # Établir la connexion SMTP
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            # Démarrer la connexion sécurisée
            server.starttls()
            # S'authentifier
            server.login(email_address, email_password)
            # Envoyer le message
            server.sendmail(email_address, destinataire, message.as_string())
            server.close()


    st.title("Information du client")
    with st.form("form1", clear_on_submit=True):
            nom     = st.text_input('Nom', placeholder="Saisissez votre nom").upper()
            prenom  = st.text_input('Prénom', placeholder="Saisissez votre prénom").upper()
            tel     = st.text_input('Téléphone', placeholder="Saisissez votre numéro de téléphone")
            mail    = st.text_input('Email', placeholder="Saisissez votre adresse mail")
            adresse = st.text_input('Adresse', placeholder="Saisissez votre adresse postale")
            produit = st.selectbox('Produit', ['','Steak','Viande hachée','Biftek','Tend de tranche'])
            kg      = st.selectbox('Kg', ['',1,2,3,4,5,6,7,8,9,10])
            grammes = st.selectbox('Grammes', ['',0,100,200,300,400,500,600,700,800,900])

            corps_message = f"""
                            Bonjour {nom} {prenom},

                            Vous avez commandé
                            un/des {produit}(s), quantité : {kg}.{grammes} Kg.
                            ça vous fait 43.50 € 
                            à régler à la livraison.

                            Merci de nous faire confiance pour vos achats. Nous vous remercions d’avance pour votre confiance.
                            Cordialemennt

                            """



            submitted = st.form_submit_button("Commander")
            if submitted:
                st.write(f"Vous avez commandé : {kg}.{grammes} kg de {produit}")
                database.commander(nom, prenom, tel, mail, adresse, produit, kg, grammes, date_actuelle)
                st.write('Votre commande a été enrgistrée')
                send_mail(mail, corps_message)
                st.write('mail envoyé au ', mail)


# ------- PARTIE ADMINISTRATION -------

if selected == 'Admin':
    file_path = Path(__file__).parent / "hashed_pwd.pkl"
    with file_path.open("rb") as file:
        hash_passwords = pickle.load(file)

    authenticator = stauth.Authenticate(names, usernames, hash_passwords, "sales", "abcdef")
    name, authentication_status, username = authenticator.login("Se Connecter", "main")

    if authentication_status == False:
        st.error("Incorrect username or password")
    if authentication_status == None:
        st.warning("No user has been logged in yet")
    if authentication_status : 
        st.title("Administration")
        st.write('Pour se déconnecter, cliquez sur Logout')
        authenticator.logout("Se déconnecter", "main")

        st.title("Ajouter un nouveau produit")
        with st.form("form2", clear_on_submit=True):
                produit = st.text_input('Produit', placeholder="Saisissez le nouveau produit").lower()
                prix    = st.text_input('Prix', placeholder="Saisissez le prix du produit")

                submitted = st.form_submit_button("AJOUTER")
                if submitted:
                    database.modifier_prix(produit, prix)
                    st.write("Le nouveau prix de ", produit, " est : ", prix, " €")
                    st.success('Le nouveau prix a été enregistré dans la base des données')


        st.title("Modifier les prix des produits")
        if st.button("Modifier"):
            with st.form("form3", clear_on_submit=True):
                    database.cursor.execute("SELECT produit FROM produits")
                    rows = database.cursor.fetchall()
                    resultats_liste = [element[0] for element in rows]
                    mon_ensemble = set(resultats_liste)
                    resultats_liste = list(mon_ensemble)
                    st.write(resultats_liste)
                  
                    produit = st.selectbox('Produit', resultats_liste)
                    prix    = st.text_input('Prix', placeholder="Saisissez le nouveau prix du produit")

                    submitted = st.form_submit_button("MODIFIER")
                    if submitted:
                        database.modifier_prix(produit, prix)
                        st.write("Le nouveau prix de ", produit, " est : ", prix, " €")
                        st.success('Le nouveau prix a été enregistré dans la base des données')

                        prix = pd.read_sql_query("SELECT * FROM produits", database.connection)
                        st.dataframe(prix)

        st.title('Tableau des commandes')
        prix = pd.read_sql_query("SELECT * FROM produits", database.connection)
        st.dataframe(prix)
        commandes = pd.read_sql_query("SELECT * FROM commandes", database.connection)
        result = pd.merge(commandes, prix, on='PRODUIT', how='left')
        result['QUANTITE'] = (result['KG'] * 1000 + result['GRAMMES']) / 1000
        result['MONTANT'] = result['QUANTITE'] * result['PRIX'].astype(float)
        st.dataframe(result)

        
        
        



        