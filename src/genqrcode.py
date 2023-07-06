import os
import pyotp
import qrcode
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def generate_qrcode(username, jwt_token):
    # Generate a secret key for the token
    secret_key = pyotp.random_base32()

    # Generate a TOTP based on the secret key
    totp = pyotp.TOTP(secret_key)

    # Generate the authentication URL for the TOTP
    #auth_url = totp.provisioning_uri(name=username, issuer_name='PayTonKawa')

    # Générer le QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(jwt_token)
    qr.make(fit=True)

    # Convertir le QR code en image
    qr_image = qr.make_image(fill_color="black", back_color="white")

    # Enregistrer l'image du QR code
    qr_image_path = "api_auth_qrcode.png"
    qr_image.save(qr_image_path)

    # Paramètres SMTP du serveur d'envoi
    smtp_host = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "fidelrmonteiro@gmail.com"
    smtp_password = os.environ.get("GMAIL_PASSWORD")
    #export GMAIL_PASSWORD="rwuciucxjuebqnvf"

    # Informations de l'expéditeur et du destinataire
    sender_email = "fidelrmonteiro@gmail.com"
    receiver_email = username

    # Créer le message multipart
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "QR Code pour se connecter à l'API PayTonKawa"

    # Ajouter le corps du message
    body = "Veuillez trouver ci-joint le QR code pour vous connecter à l'API PayTonKawa."
    message.attach(MIMEText(body, "plain"))

    # Ajouter l'image du QR code en pièce jointe
    with open(qr_image_path, "rb") as attachment:
        qr_image_mime = MIMEImage(attachment.read())
    qr_image_mime.add_header("Content-Disposition", "attachment", filename=qr_image_path)
    message.attach(qr_image_mime)

    # Se connecter au serveur SMTP et envoyer l'e-mail
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

    # Supprimer le fichier du QR code
    os.remove(qr_image_path)

    return { "data": f"Un mail avec le QR code vous a été envoyé à : {username}" }


if __name__ == "__main__":
    #secret_key = generate_qrcode()
    pass