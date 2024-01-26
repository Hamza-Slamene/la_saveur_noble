import smtplib
from email.mime.text import MIMEText

class MailSender:
    def __init__(self, server='smtp.gmail.com', port=587):
        self.server = server
        self.port = port
        self.email_address = 'votre_adresse_email'
        self.email_password = 'votre_mot_de_passe'
        self.corps_message = ""
        self.message = MIMEText(self.corps_message)
        self.subject = self.message['Subject'] = ""
        self.frommail = self.message['From'] = self.email_address
        self.message['To'] = ""

    def send_mail(self, subject, message, from_addr, to_addrs, cc_addrs=[], bcc_addrs=[]):
        with smtplib.SMTP(self.server, self.port) as server:
            # Démarrer la connexion sécurisée
            server.starttls()
            # S'authentifier
            server.login(self.email_address, self.email_password)

            # Envoyer le message
            server.sendmail(self.email_address, destinataire, self.message.as_string())

        print("E-mail envoyé avec succès!")

        # Paramètres du serveur SMTP
        smtp_server = 'votre_serveur_smtp'
        smtp_port = 587  # Port SMTP standard

        # Informations d'authentification
        email_address = 'votre_adresse_email'
        email_password = 'votre_mot_de_passe'

        # Destinataire et contenu du message
        destinataire = 'adresse_destinataire@example.com'
        sujet = 'Objet du message'
        corps_message = 'Contenu du message.'

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

        print("E-mail envoyé avec succès!")
