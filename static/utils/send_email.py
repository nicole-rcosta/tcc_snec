import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

# Carrega o .env para o sistema
load_dotenv()

# Recupera os valores usando os.getenv()
email_envia = os.getenv("EMAIL")
app_senha = os.getenv("APP_PASSWORD")

# Dados da conta

def enviar_email(email, codigo):

    EMAIL_REMETENTE = email_envia
    # tomar cuidado com isso
    SENHA_APP = app_senha
    DESTINATARIO = email

    email = EmailMessage()
    email["Subject"] = "Código de Recuperação de senha"
    email["From"] = EMAIL_REMETENTE
    email["To"] = DESTINATARIO

    email.set_content(f'''
    Confirme seu e-mail

    Use este código no snec pra confirmar que este e-mail é seu:

    {codigo}

    ''')

    # Conectando ao Gmail e enviando

    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=3) as servidor:
            servidor.starttls()
            servidor.login(EMAIL_REMETENTE, SENHA_APP)

            print("Enviando e-mail...", flush=True)
            servidor.send_message(email)

            print("E-mail enviado com sucesso!", flush=True)

    except (smtplib.SMTPException, TimeoutError, OSError) as erro:
        print(f"Envio não confirmado: {erro}", flush=True)

    finally:
        print("Programa encerrado.", flush=True)
        return  True