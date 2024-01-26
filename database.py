import sqlite3

class Database:
    def __init__(self) -> None:
        self.connection = sqlite3.connect('clients.db')
        self.cursor = self.connection.cursor()

    def create_tables(self):
        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS commandes (
                            NOM TEXT,
                            PRENOM TEXT,
                            TEL TEXT,
                            EMAIL TEXT,
                            ADRESSE TEXT,
                            PRODUIT TEXT,
                            KG INTEGER,
                            GRAMMES INTEGER,
                            DATE TEXT);
                        ''')

        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS produits (
                            PRODUIT TEXT, 
                            PRIX FLOAT); 
                    ''')
        
    def commander(self, nom, prenom, tel, mail, adresse, produit, kg, grammes, date_actuelle):
        self.cursor.execute(f''' INSERT INTO commandes VALUES ('{nom}', '{prenom}', '{tel}', '{mail}', '{adresse}','{produit}', {kg}, {grammes}, '{date_actuelle}') ''') 
        self.connection.commit() 


    def modifier_prix(self, produit, prix):
        #self.cursor.execute(f''' INSERT INTO produits VALUES ('{produit}', {prix}) ''')
        self.cursor.execute(f''' UPDATE produits SET prix = {prix} WHERE produit = '{produit}' ''')
        self.connection.commit() 

    def modifier_prix(self, produit, prix):
        self.cursor.execute(f''' INSERT INTO produits VALUES ('{produit}', {prix}) ''')
        self.connection.commit() 
  