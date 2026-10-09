import smtplib
from email.message import EmailMessage

# Dados da sua conta
EMAIL_REMETENTE = email
# tomar cuidado com isso
SENHA_APP = "mtls ntmg kxxn aquu" 
DESTINATARIO = "pablo.moralez@aluno.senai.br"

# Criando o e-mail
email = EmailMessage()
email["Subject"] = "Código de Recuperação de senha"
email["From"] = EMAIL_REMETENTE
email["To"] = DESTINATARIO

email.set_content("seu Código é 123")

# Conectando ao Gmail e enviando
with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
    servidor.starttls()
    servidor.login(EMAIL_REMETENTE, SENHA_APP)
    servidor.send_message(email)

print("E-mail enviado com sucesso!")