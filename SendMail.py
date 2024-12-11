from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Konfigurationsvariablen für die E-Mail
SMTP_SERVER = 'smtp.example.com'  # Ersetzen mit SMTP-Server
SMTP_PORT = 587  # Üblicherweise 587 für TLS oder 465 für SSL
EMAIL_ADDRESS = 'your-email@example.com'  # Ersetzen mit E-Mail-Adresse
EMAIL_PASSWORD = 'your-email-password'  # Ersetzen mit E-Mail-Passwort
RECIPIENT_EMAIL = 'recipient@example.com'  # E-Mail-Adresse, an die das Feedback gesendet werden soll

@app.route('/feedback', methods=['POST'])
def feedback():
    try:
        # Feedback-Daten aus der Anfrage abrufen
        data = request.json
        name = data.get('name', 'Anonym')
        email = data.get('email', 'Keine E-Mail angegeben')
        message = data.get('message', '')

        # E-Mail erstellen
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = 'Neues Feedback erhalten'

        body = f"Name: {name}\nE-Mail: {email}\n\nNachricht:\n{message}"
        msg.attach(MIMEText(body, 'plain'))

        # E-Mail senden
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # TLS-Verschlüsselung starten
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        return jsonify({'message': 'Feedback erfolgreich gesendet'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
