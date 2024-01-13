import streamlit as st

st.set_page_config(menu_items=[])

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


col1, col2, col3 = st.columns(3)


produit  = col1.selectbox('Produit', ['','Steak','Viande hachée','Buftek','Tond de tranche'])
quantite = col2.selectbox('Quantité', ['',1,2,3])
with col3:
    st.button('Valider')

st.write(f'Vous avez commandé : {quantite} Kg de {produit}' )


st.button('Commander')