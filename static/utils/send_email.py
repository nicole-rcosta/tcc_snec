import smtplib
from email.message import EmailMessage
from flask import render_template

# Dados da conta

def enviar_email(email, codigo):

    EMAIL_REMETENTE = "pablolorenzomoralez@gmail.com"
    # tomar cuidado com isso
    SENHA_APP = "mtls ntmg kxxn aquu" 
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

    # 2. Renderiza o template HTML do Flask passando a variável 'codigo'
    html_conteudo = render_template("email/email_codigo.html", codigo=codigo)

    # 3. Adiciona a versão HTML personalizada
    email.add_alternative(html_conteudo, subtype="html")

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